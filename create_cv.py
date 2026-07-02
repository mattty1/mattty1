from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def register_fonts() -> tuple[str, str]:
    regular_font = "Helvetica"
    bold_font = "Helvetica-Bold"

    regular_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    bold_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

    if regular_path.exists() and bold_path.exists():
        pdfmetrics.registerFont(TTFont("DejaVuSans", str(regular_path)))
        pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", str(bold_path)))
        regular_font = "DejaVuSans"
        bold_font = "DejaVuSans-Bold"

    return regular_font, bold_font


def wrap_text(text: str, font_name: str, font_size: int, max_width: float) -> list[str]:
    words = text.split()
    if not words:
        return [""]

    lines: list[str] = []
    current = words[0]

    for word in words[1:]:
        trial = f"{current} {word}"
        width = pdfmetrics.stringWidth(trial, font_name, font_size)
        if width <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def draw_section_title(
    c: canvas.Canvas, x: float, y: float, title: str, heading_font: str
) -> float:
    c.setFillColor(HexColor("#153E75"))
    c.setFont(heading_font, 13)
    c.drawString(x, y, title)
    c.setStrokeColor(HexColor("#BDD4F6"))
    c.setLineWidth(1)
    c.line(x, y - 4, x + 520, y - 4)
    return y - 18


def draw_bullet_list(
    c: canvas.Canvas,
    x: float,
    y: float,
    items: list[str],
    width: float,
    regular_font: str,
    font_size: int = 10,
    leading: int = 13,
) -> float:
    bullet_offset = 13
    for item in items:
        wrapped = wrap_text(item, regular_font, font_size, width - bullet_offset)
        c.setFont(regular_font, font_size)
        c.setFillColor(HexColor("#1A202C"))
        c.drawString(x, y, "•")
        c.drawString(x + bullet_offset, y, wrapped[0])
        y -= leading

        for line in wrapped[1:]:
            c.drawString(x + bullet_offset, y, line)
            y -= leading
        y -= 2
    return y


def create_cv(output_path: Path) -> None:
    regular_font, bold_font = register_fonts()

    c = canvas.Canvas(str(output_path), pagesize=A4)
    page_width, page_height = A4

    margin = 32
    card_x = margin
    card_y = margin
    card_w = page_width - 2 * margin
    card_h = page_height - 2 * margin

    c.setFillColor(HexColor("#EEF3FB"))
    c.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    c.setFillColor(Color(0, 0, 0, alpha=0.08))
    c.rect(card_x + 5, card_y - 5, card_w, card_h, fill=1, stroke=0)

    c.setFillColor(white)
    c.roundRect(card_x, card_y, card_w, card_h, 12, fill=1, stroke=0)

    header_h = 110
    c.setFillColor(HexColor("#153E75"))
    c.roundRect(card_x, page_height - margin - header_h, card_w, header_h, 12, fill=1, stroke=0)
    c.rect(card_x, page_height - margin - header_h, card_w, 12, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont(bold_font, 28)
    c.drawString(card_x + 24, page_height - margin - 48, "Mateusz Pluta")
    c.setFont(regular_font, 12)
    c.drawString(card_x + 24, page_height - margin - 70, "Curriculum Vitae")

    current_y = page_height - margin - header_h - 24
    text_x = card_x + 24
    text_w = card_w - 48

    current_y = draw_section_title(c, text_x, current_y, "Dane personalne", bold_font)
    current_y = draw_bullet_list(
        c,
        text_x,
        current_y,
        [
            "Telefon: 783 156 382",
            "E-mail: mateuszpluta29@gmail.com",
            "Data urodzenia: 28.06.2004r.",
        ],
        text_w,
        regular_font,
    )

    current_y = draw_section_title(c, text_x, current_y, "Wykształcenie", bold_font)
    current_y = draw_bullet_list(
        c,
        text_x,
        current_y,
        [
            "Technikum Ekonomiczno-Handlowe w Lublinie – Technik informatyk(INF 02 i INF 03), 09.2019 – 04.2024",
            "Politechnika Lubelska, Sztuczna inteligencja w biznesie 2024 - obecnie",
        ],
        text_w,
        regular_font,
    )

    current_y = draw_section_title(c, text_x, current_y, "Doświadczenie zawodowe", bold_font)
    current_y = draw_bullet_list(
        c,
        text_x,
        current_y,
        [
            "Staż w zawodzie technik informatyk - X-COM Jarosław Krawczyk - 06.2022-07.2022",
            "Pomocnik biurowy w gminie – staż – 05.2023",
            "Operator produkcji - praca sezonowa - Nestle Waters Nałęczowianka 07.2024-08.2024",
            "Realizacja i pakowanie zamówień oraz przyjmowanie i wydawanie towarów - praca sezonowa – VMV Studio 08.2025 – 09.2025",
            "Prace magazynowe – DHL Parcel Lublin 05.2025 – obecnie",
        ],
        text_w,
        regular_font,
    )

    current_y = draw_section_title(c, text_x, current_y, "Umiejętności", bold_font)
    current_y = draw_bullet_list(
        c,
        text_x,
        current_y,
        [
            "Sprawna obsługa komputera w tym pakietu MS Office(Word, Excel, Access)",
            "Angielski – komunikatywny",
            "Diagnoza, naprawa i wymiana podstawowych części komputerowych",
            "Podstawowa znajomość: PHP, CSS, HTML, JS i MSSQL",
        ],
        text_w,
        regular_font,
    )

    current_y = draw_section_title(c, text_x, current_y, "Dodatkowe informacje", bold_font)
    current_y = draw_bullet_list(
        c,
        text_x,
        current_y,
        [
            "Prawo jazdy kat. B",
            "Status studenta",
            "Książeczka sanepidowska",
        ],
        text_w,
        regular_font,
    )

    current_y = draw_section_title(c, text_x, current_y, "Klauzula RODO", bold_font)
    current_y = draw_bullet_list(
        c,
        text_x,
        current_y,
        [
            "Wyrażam zgodę na przetwarzanie moich danych osobowych dla potrzeb niezbędnych do realizacji procesu rekrutacji (zgodnie z ustawą z dnia 10 maja 2018 roku o ochronie danych osobowych (Dz. Ustaw z 2018, poz. 1000) oraz zgodnie z Rozporządzeniem Parlamentu Europejskiego i Rady (UE) 2016/679 z dnia 27 kwietnia 2016 r.",
        ],
        text_w,
        regular_font,
        font_size=8,
        leading=11,
    )

    c.save()


if __name__ == "__main__":
    create_cv(Path("CV_Mateusz_Pluta_odswiezone.pdf"))
