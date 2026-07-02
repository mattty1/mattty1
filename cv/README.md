# CV — Mateusz Pluta

Odświeżona, kolorowa wersja CV. Treść jest identyczna jak w oryginalnym pliku
`CV_-_Mateusz_Pluta.pdf` — zmieniona została jedynie oprawa graficzna.

## Pliki

- `cv.html` — źródło CV (HTML + CSS, jedna strona A4).
- `CV_-_Mateusz_Pluta.pdf` — gotowy PDF wygenerowany z `cv.html`.

## Jak wygenerować PDF ponownie

Wymagany jest [WeasyPrint](https://weasyprint.org/):

```bash
pip install weasyprint
weasyprint cv.html CV_-_Mateusz_Pluta.pdf
```
