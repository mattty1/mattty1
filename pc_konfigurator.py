import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

# ─────────────────────────────────────────────────────────────────────────────
# BAZA DANYCH PODZESPOŁÓW
# Wszystkie ceny w PLN (przybliżone ceny rynkowe).
# Pole "zastosowania" to lista słów kluczowych oddzielonych przecinkiem.
# Pole "wydajnosc" to subiektywna ocena 0-100.
# ─────────────────────────────────────────────────────────────────────────────

PROCESORY = pd.DataFrame([
    {"nazwa": "Intel Core i3-12100",   "marka": "Intel", "cena": 480,  "wydajnosc": 40, "tdp": 60,  "zastosowania": "biuro,ogolne"},
    {"nazwa": "Intel Core i5-12400F",  "marka": "Intel", "cena": 720,  "wydajnosc": 63, "tdp": 65,  "zastosowania": "biuro,ogolne,gaming,programowanie"},
    {"nazwa": "Intel Core i5-13600K",  "marka": "Intel", "cena": 1100, "wydajnosc": 80, "tdp": 125, "zastosowania": "gaming,programowanie,grafika"},
    {"nazwa": "Intel Core i7-13700K",  "marka": "Intel", "cena": 1650, "wydajnosc": 90, "tdp": 125, "zastosowania": "gaming,programowanie,grafika,wideo"},
    {"nazwa": "Intel Core i9-14900K",  "marka": "Intel", "cena": 2600, "wydajnosc": 97, "tdp": 125, "zastosowania": "gaming,programowanie,grafika,wideo"},
    {"nazwa": "AMD Ryzen 5 5600",      "marka": "AMD",   "cena": 530,  "wydajnosc": 60, "tdp": 65,  "zastosowania": "biuro,ogolne,gaming"},
    {"nazwa": "AMD Ryzen 5 7600X",     "marka": "AMD",   "cena": 880,  "wydajnosc": 74, "tdp": 105, "zastosowania": "gaming,programowanie"},
    {"nazwa": "AMD Ryzen 7 5800X3D",   "marka": "AMD",   "cena": 1350, "wydajnosc": 87, "tdp": 105, "zastosowania": "gaming"},
    {"nazwa": "AMD Ryzen 7 7700X",     "marka": "AMD",   "cena": 1440, "wydajnosc": 86, "tdp": 105, "zastosowania": "gaming,programowanie,grafika"},
    {"nazwa": "AMD Ryzen 9 7950X",     "marka": "AMD",   "cena": 2850, "wydajnosc": 99, "tdp": 170, "zastosowania": "wideo,grafika,programowanie"},
])

RAM_DF = pd.DataFrame([
    {"opis": "8 GB DDR4 3200 MHz",  "rozmiar": 8,  "typ": "DDR4", "cena": 120},
    {"opis": "16 GB DDR4 3200 MHz", "rozmiar": 16, "typ": "DDR4", "cena": 210},
    {"opis": "16 GB DDR5 5200 MHz", "rozmiar": 16, "typ": "DDR5", "cena": 340},
    {"opis": "32 GB DDR4 3600 MHz", "rozmiar": 32, "typ": "DDR4", "cena": 375},
    {"opis": "32 GB DDR5 5200 MHz", "rozmiar": 32, "typ": "DDR5", "cena": 610},
    {"opis": "64 GB DDR5 5600 MHz", "rozmiar": 64, "typ": "DDR5", "cena": 1100},
])

DYSKI_DF = pd.DataFrame([
    {"opis": "256 GB SSD SATA",  "pojemnosc_gb": 256,  "typ": "SSD SATA", "cena": 110},
    {"opis": "500 GB SSD SATA",  "pojemnosc_gb": 500,  "typ": "SSD SATA", "cena": 165},
    {"opis": "500 GB NVMe M.2",  "pojemnosc_gb": 500,  "typ": "NVMe M.2", "cena": 195},
    {"opis": "1 TB SSD SATA",    "pojemnosc_gb": 1000, "typ": "SSD SATA", "cena": 255},
    {"opis": "1 TB NVMe M.2",    "pojemnosc_gb": 1000, "typ": "NVMe M.2", "cena": 325},
    {"opis": "2 TB SSD SATA",    "pojemnosc_gb": 2000, "typ": "SSD SATA", "cena": 475},
    {"opis": "2 TB NVMe M.2",    "pojemnosc_gb": 2000, "typ": "NVMe M.2", "cena": 610},
    {"opis": "4 TB HDD",         "pojemnosc_gb": 4000, "typ": "HDD",      "cena": 285},
])

GPU_DF = pd.DataFrame([
    {"nazwa": "Zintegrowana (brak karty)",  "cena": 0,    "wydajnosc": 5,   "zastosowania": "biuro,ogolne"},
    {"nazwa": "NVIDIA GeForce GTX 1650",    "cena": 540,  "wydajnosc": 34,  "zastosowania": "ogolne,gaming"},
    {"nazwa": "AMD Radeon RX 6600",         "cena": 840,  "wydajnosc": 58,  "zastosowania": "gaming"},
    {"nazwa": "NVIDIA GeForce RTX 3060",    "cena": 1040, "wydajnosc": 65,  "zastosowania": "gaming,grafika"},
    {"nazwa": "NVIDIA GeForce RTX 3070 Ti", "cena": 1700, "wydajnosc": 80,  "zastosowania": "gaming,grafika,wideo"},
    {"nazwa": "AMD Radeon RX 7900 XT",      "cena": 2450, "wydajnosc": 90,  "zastosowania": "gaming,grafika,wideo"},
    {"nazwa": "NVIDIA GeForce RTX 4080",    "cena": 3400, "wydajnosc": 95,  "zastosowania": "gaming,grafika,wideo"},
    {"nazwa": "NVIDIA GeForce RTX 4090",    "cena": 5400, "wydajnosc": 100, "zastosowania": "gaming,grafika,wideo"},
])

PLYTY_GLOWNE = {
    ("Intel", "DDR4"): {"nazwa": "MSI PRO B660M-A DDR4",        "cena": 440},
    ("Intel", "DDR5"): {"nazwa": "ASUS PRIME Z790-P DDR5",       "cena": 690},
    ("AMD",   "DDR4"): {"nazwa": "MSI MAG B550 TOMAHAWK DDR4",   "cena": 490},
    ("AMD",   "DDR5"): {"nazwa": "ASUS ROG STRIX X670E-F DDR5",  "cena": 890},
}

ZASILACZE = pd.DataFrame([
    {"opis": "450W 80+ Bronze", "moc": 450, "cena": 190},
    {"opis": "550W 80+ Bronze", "moc": 550, "cena": "250"},
    {"opis": "650W 80+ Gold",   "moc": 650, "cena": 340},
    {"opis": "750W 80+ Gold",   "moc": 750, "cena": 410},
    {"opis": "850W 80+ Gold",   "moc": 850, "cena": 490},
    {"opis": "1000W 80+ Plat.", "moc": 1000,"cena": 690},
])
ZASILACZE["cena"] = pd.to_numeric(ZASILACZE["cena"])

OBUDOWY = pd.DataFrame([
    {"nazwa": "Fractal Design Core 1000", "cena": 200},
    {"nazwa": "be quiet! Pure Base 500",  "cena": 340},
    {"nazwa": "NZXT H7 Flow",             "cena": 490},
    {"nazwa": "Lian Li PC-O11 Dynamic",   "cena": 580},
])

# Przydział budżetu na poszczególne podzespoły w zależności od zastosowania
PRZYDZIAL_BUDZETU = {
    "gaming":        {"cpu": 0.20, "gpu": 0.38, "ram": 0.08, "dysk": 0.08, "plyta": 0.10, "zasilacz": 0.08, "obudowa": 0.08},
    "biuro":         {"cpu": 0.28, "gpu": 0.00, "ram": 0.14, "dysk": 0.20, "plyta": 0.18, "zasilacz": 0.10, "obudowa": 0.10},
    "programowanie": {"cpu": 0.28, "gpu": 0.05, "ram": 0.22, "dysk": 0.17, "plyta": 0.14, "zasilacz": 0.08, "obudowa": 0.06},
    "grafika":       {"cpu": 0.18, "gpu": 0.38, "ram": 0.15, "dysk": 0.12, "plyta": 0.08, "zasilacz": 0.06, "obudowa": 0.03},
    "wideo":         {"cpu": 0.20, "gpu": 0.35, "ram": 0.18, "dysk": 0.12, "plyta": 0.07, "zasilacz": 0.05, "obudowa": 0.03},
    "ogolne":        {"cpu": 0.24, "gpu": 0.12, "ram": 0.13, "dysk": 0.18, "plyta": 0.16, "zasilacz": 0.10, "obudowa": 0.07},
}

ZASTOSOWANIE_ETYKIETY = {
    "gaming":        "🎮 Gaming",
    "biuro":         "💼 Praca biurowa",
    "programowanie": "💻 Programowanie",
    "grafika":       "🎨 Grafika / projektowanie",
    "wideo":         "🎬 Edycja wideo",
    "ogolne":        "🖥️ Użytek ogólny",
}

ZASTOSOWANIE_OPISY = {
    "gaming":        "Wysokie klatki na sekundę, mocna karta graficzna, szybka pamięć.",
    "biuro":         "Wydajność na co dzień, zintegrowana grafika często wystarczy.",
    "programowanie": "Dużo RAM-u, mocny procesor wielowątkowy, szybki dysk NVMe.",
    "grafika":       "Mocna karta graficzna, sprawny procesor, duży dysk.",
    "wideo":         "Maksymalny procesor i GPU, dużo RAM-u i miejsca na dysku.",
    "ogolne":        "Zbalansowany zestaw do codziennych zadań.",
}

# ─────────────────────────────────────────────────────────────────────────────
# LOGIKA REKOMENDACJI
# ─────────────────────────────────────────────────────────────────────────────

def score_component(row, zastosowanie, col_zast="zastosowania", col_wyd="wydajnosc"):
    """Oblicza wynik podzespołu: wydajnosc * bonus_za_zastosowanie."""
    zast_lista = str(row[col_zast]).split(",")
    bonus = 1.4 if zastosowanie in zast_lista else 0.8
    return row[col_wyd] * bonus


def wybierz_najlepszy(df, budzet, zastosowanie, col_cena="cena"):
    """Zwraca wiersz DataFrame z najlepszym podzespołem mieszczącym się w budżecie."""
    kandydaci = df[df[col_cena] <= budzet].copy()
    if kandydaci.empty:
        # Jeśli żaden się nie mieści – bierz najtańszy
        kandydaci = df.nsmallest(1, col_cena)
    if "wydajnosc" in df.columns and "zastosowania" in df.columns:
        kandydaci["_score"] = kandydaci.apply(
            lambda r: score_component(r, zastosowanie), axis=1
        )
        return kandydaci.loc[kandydaci["_score"].idxmax()]
    # Dla podzespołów bez punktacji – wybierz najtańszy mieszczący się w budżecie
    return kandydaci.loc[kandydaci[col_cena].idxmax()]


def dobierz_zasilacz(tdp_cpu, tdp_gpu):
    """Wybiera zasilacz z 30% zapasem mocy nad sumą TDP."""
    wymagana_moc = (tdp_cpu + tdp_gpu) * 1.30 + 100  # +100W na resztę
    pasujace = ZASILACZE[ZASILACZE["moc"] >= wymagana_moc]
    if pasujace.empty:
        return ZASILACZE.iloc[-1]
    return pasujace.iloc[0]


def rekomenduj(budzet, zastosowanie, marka_cpu, min_ram_gb, min_dysk_gb, typ_dysku):
    """Główna funkcja rekomendacji – zwraca słownik z wybranymi podzespołami."""
    przydzial = PRZYDZIAL_BUDZETU[zastosowanie]

    # 1. PROCESOR
    cpu_df = PROCESORY.copy()
    if marka_cpu != "Bez preferencji":
        cpu_df = cpu_df[cpu_df["marka"] == marka_cpu]
        if cpu_df.empty:
            cpu_df = PROCESORY.copy()
    cpu = wybierz_najlepszy(cpu_df, budzet * przydzial["cpu"], zastosowanie)

    # 2. RAM – filtruj po minimalnym rozmiarze
    ram_df = RAM_DF[RAM_DF["rozmiar"] >= min_ram_gb].copy()
    if ram_df.empty:
        ram_df = RAM_DF.copy()
    ram_df["wydajnosc"] = ram_df["rozmiar"]          # im więcej GB, tym lepiej
    ram_df["zastosowania"] = "biuro,ogolne,gaming,programowanie,grafika,wideo"
    ram = wybierz_najlepszy(ram_df, budzet * przydzial["ram"], zastosowanie)

    # 3. PŁYTA GŁÓWNA – dobierana do marki CPU i typu RAM
    typ_ram = ram["typ"]
    klucz_plyty = (cpu["marka"], typ_ram)
    if klucz_plyty not in PLYTY_GLOWNE:
        klucz_plyty = (cpu["marka"], "DDR4")
    plyta = PLYTY_GLOWNE[klucz_plyty]

    # 4. DYSK – filtruj po pojemności i typie
    dysk_df = DYSKI_DF[DYSKI_DF["pojemnosc_gb"] >= min_dysk_gb].copy()
    if typ_dysku != "Dowolny":
        tmp = dysk_df[dysk_df["typ"] == typ_dysku]
        if not tmp.empty:
            dysk_df = tmp
    if dysk_df.empty:
        dysk_df = DYSKI_DF.copy()
    dysk_df["wydajnosc"] = dysk_df["pojemnosc_gb"] / 40     # więcej GB = lepiej
    dysk_df["zastosowania"] = "biuro,ogolne,gaming,programowanie,grafika,wideo"
    dysk = wybierz_najlepszy(dysk_df, budzet * przydzial["dysk"], zastosowanie)

    # 5. KARTA GRAFICZNA
    if przydzial["gpu"] == 0:
        gpu = GPU_DF.iloc[0]   # zintegrowana
    else:
        gpu = wybierz_najlepszy(GPU_DF, budzet * przydzial["gpu"], zastosowanie)

    # 6. ZASILACZ
    tdp_gpu = 0 if "Zintegrowana" in str(gpu["nazwa"]) else 150
    zasilacz = dobierz_zasilacz(cpu["tdp"], tdp_gpu)

    # 7. OBUDOWA – najtańsza mieszcząca się w budżecie na obudowę
    bud_obudowa = budzet * przydzial["obudowa"]
    pasujace_obudowy = OBUDOWY[OBUDOWY["cena"] <= bud_obudowa]
    obudowa = pasujace_obudowy.iloc[-1] if not pasujace_obudowy.empty else OBUDOWY.iloc[0]

    return {
        "Procesor":        {"opis": cpu["nazwa"],    "cena": int(cpu["cena"]),       "wydajnosc": int(cpu["wydajnosc"])},
        "Karta graficzna": {"opis": gpu["nazwa"],    "cena": int(gpu["cena"]),       "wydajnosc": int(gpu["wydajnosc"])},
        "RAM":             {"opis": ram["opis"],      "cena": int(ram["cena"]),       "wydajnosc": int(ram["rozmiar"])},
        "Dysk":            {"opis": dysk["opis"],     "cena": int(dysk["cena"]),      "wydajnosc": None},
        "Płyta główna":    {"opis": plyta["nazwa"],  "cena": int(plyta["cena"]),     "wydajnosc": None},
        "Zasilacz":        {"opis": zasilacz["opis"], "cena": int(zasilacz["cena"]), "wydajnosc": None},
        "Obudowa":         {"opis": obudowa["nazwa"], "cena": int(obudowa["cena"]),  "wydajnosc": None},
    }


# ─────────────────────────────────────────────────────────────────────────────
# INTERFEJS STREAMLIT
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Konfigurator PC", page_icon="💻", layout="wide")

st.title("🖥️ Konfigurator PC – dobierz podzespoły")
st.markdown(
    "Odpowiedz na kilka pytań, a aplikacja zaproponuje optymalny zestaw komputerowy "
    "dopasowany do Twoich potrzeb i budżetu."
)

# ── PASEK BOCZNY ─────────────────────────────────────────────────────────────
st.sidebar.title("⚙️ Twoje preferencje")

zastosowanie_label = st.sidebar.radio(
    "Do czego ma służyć komputer?",
    list(ZASTOSOWANIE_ETYKIETY.values()),
)
zastosowanie = {v: k for k, v in ZASTOSOWANIE_ETYKIETY.items()}[zastosowanie_label]

st.sidebar.markdown("---")

budzet = st.sidebar.slider(
    "Budżet (PLN)",
    min_value=1500,
    max_value=15000,
    value=4000,
    step=500,
)
st.sidebar.write(f"Wybrany budżet: **{budzet} PLN**")

st.sidebar.markdown("---")

marka_cpu = st.sidebar.radio(
    "Preferowana marka procesora",
    ["AMD", "Intel", "Bez preferencji"],
)

st.sidebar.markdown("---")

min_ram_gb = st.sidebar.select_slider(
    "Minimalna ilość RAM",
    options=[8, 16, 32, 64],
    value=16,
    format_func=lambda x: f"{x} GB",
)

st.sidebar.markdown("---")

min_dysk_gb = st.sidebar.select_slider(
    "Minimalna pojemność dysku",
    options=[256, 500, 1000, 2000, 4000],
    value=500,
    format_func=lambda v: f"{v} GB" if v < 1000 else f"{v // 1000} TB",
)

typ_dysku = st.sidebar.radio(
    "Typ dysku",
    ["NVMe M.2", "SSD SATA", "HDD", "Dowolny"],
    index=3,
)

st.sidebar.markdown("---")
generuj = st.sidebar.button("🔍 Generuj rekomendację", use_container_width=True)

# ── GŁÓWNY OBSZAR ─────────────────────────────────────────────────────────────

# Informacja o wybranym zastosowaniu
st.info(f"**{zastosowanie_label}** – {ZASTOSOWANIE_OPISY[zastosowanie]}")

if generuj or "rekomendacja" in st.session_state:
    if generuj:
        st.session_state["rekomendacja"] = rekomenduj(
            budzet, zastosowanie, marka_cpu, min_ram_gb, min_dysk_gb, typ_dysku
        )
        st.session_state["budzet_snapshot"] = budzet

    rec = st.session_state["rekomendacja"]
    budzet_snap = st.session_state.get("budzet_snapshot", budzet)

    # ── Tabela z podzespołami ─────────────────────────────────────────────────
    st.subheader("📋 Rekomendowany zestaw")

    wiersze = []
    suma = 0
    for kategoria, dane in rec.items():
        wiersze.append({"Podzespół": kategoria, "Model": dane["opis"], "Cena (PLN)": dane["cena"]})
        suma += dane["cena"]

    df_wynik = pd.DataFrame(wiersze)
    df_wynik.index = df_wynik.index + 1   # numeracja od 1

    st.dataframe(df_wynik, use_container_width=True)

    # ── Metryki ──────────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Łączny koszt", f"{suma} PLN")
    col2.metric("📊 Budżet", f"{budzet_snap} PLN")
    oszczednosci = budzet_snap - suma
    col3.metric(
        "💵 Pozostało w budżecie",
        f"{oszczednosci} PLN",
        delta=f"{oszczednosci:+} PLN",
        delta_color="normal" if oszczednosci >= 0 else "inverse",
    )

    if suma > budzet_snap:
        st.warning(
            f"⚠️ Zestaw przekracza budżet o **{suma - budzet_snap} PLN**. "
            "Rozważ zwiększenie budżetu lub mniej rygorystyczne wymagania."
        )
    else:
        st.success("✅ Zestaw mieści się w podanym budżecie.")

    st.markdown("---")

    # ── Wykresy ──────────────────────────────────────────────────────────────
    col_wykres1, col_wykres2 = st.columns(2)

    nazwy = [w["Podzespół"] for w in wiersze]
    ceny = [w["Cena (PLN)"] for w in wiersze]

    # Wykres słupkowy – ceny podzespołów
    with col_wykres1:
        st.subheader("💸 Koszt poszczególnych podzespołów")
        fig1, ax1 = plt.subplots(figsize=(7, 4))
        kolory = plt.cm.Blues(np.linspace(0.4, 0.9, len(nazwy)))
        bars = ax1.barh(nazwy, ceny, color=kolory)
        ax1.set_xlabel("Cena (PLN)")
        ax1.set_title("Podział kosztów")
        for bar, cena in zip(bars, ceny):
            ax1.text(
                bar.get_width() + 10,
                bar.get_y() + bar.get_height() / 2,
                f"{cena} PLN",
                va="center",
                fontsize=9,
            )
        ax1.set_xlim(0, max(ceny) * 1.25)
        plt.tight_layout()
        st.pyplot(fig1)

    # Wykres kołowy – udział procentowy
    with col_wykres2:
        st.subheader("📊 Udział w budżecie (%)")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        wedge_props = {"linewidth": 1, "edgecolor": "white"}
        ax2.pie(
            ceny,
            labels=nazwy,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops=wedge_props,
            colors=plt.cm.Set3.colors[: len(nazwy)],
        )
        ax2.set_title("Struktura kosztów zestawu")
        plt.tight_layout()
        st.pyplot(fig2)

    st.markdown("---")

    # ── Wykres wydajności podzespołów z oceną ────────────────────────────────
    st.subheader("⚡ Ocena wydajności kluczowych podzespołów")

    wydajnosci = {k: v["wydajnosc"] for k, v in rec.items() if v["wydajnosc"] is not None}
    if wydajnosci:
        fig3, ax3 = plt.subplots(figsize=(8, 3))
        kolory2 = plt.cm.RdYlGn(np.array(list(wydajnosci.values())) / 100)
        ax3.barh(list(wydajnosci.keys()), list(wydajnosci.values()), color=kolory2)
        ax3.set_xlim(0, 110)
        ax3.set_xlabel("Ocena (0–100)")
        ax3.set_title("Subiektywna ocena wydajności podzespołu")
        for i, (k, v) in enumerate(wydajnosci.items()):
            ax3.text(v + 1, i, str(v), va="center", fontsize=10)
        plt.tight_layout()
        st.pyplot(fig3)

    st.markdown("---")

    # ── Przegląd wszystkich procesorów w tabeli ───────────────────────────────
    with st.expander("📄 Pełna lista procesorów w bazie danych"):
        st.dataframe(
            PROCESORY[["nazwa", "marka", "cena", "wydajnosc", "tdp"]].rename(
                columns={"nazwa": "Model", "marka": "Marka", "cena": "Cena (PLN)",
                         "wydajnosc": "Ocena", "tdp": "TDP (W)"}
            ),
            use_container_width=True,
        )

    with st.expander("📄 Pełna lista kart graficznych w bazie danych"):
        st.dataframe(
            GPU_DF[["nazwa", "cena", "wydajnosc"]].rename(
                columns={"nazwa": "Model", "cena": "Cena (PLN)", "wydajnosc": "Ocena"}
            ),
            use_container_width=True,
        )

    with st.expander("📄 Pełna lista opcji RAM"):
        st.dataframe(
            RAM_DF.rename(columns={"opis": "Opis", "rozmiar": "Rozmiar (GB)",
                                   "typ": "Typ", "cena": "Cena (PLN)"}),
            use_container_width=True,
        )

    with st.expander("📄 Pełna lista dysków"):
        st.dataframe(
            DYSKI_DF.rename(columns={"opis": "Opis", "pojemnosc_gb": "Pojemność (GB)",
                                     "typ": "Typ", "cena": "Cena (PLN)"}),
            use_container_width=True,
        )

    # ── JSON z konfiguracją (jak na zajęciach) ────────────────────────────────
    st.subheader("🗂️ Konfiguracja w formacie JSON")
    json_config = {k: {"model": v["opis"], "cena_pln": v["cena"]} for k, v in rec.items()}
    json_config["SUMA"] = suma
    st.json(json_config)

else:
    st.markdown(
        """
        ### 👈 Ustaw preferencje i kliknij **Generuj rekomendację**

        Aplikacja dobierze dla Ciebie:
        - **Procesor** (CPU) – Intel lub AMD
        - **Kartę graficzną** (GPU)
        - **Pamięć RAM**
        - **Dysk** (SSD / NVMe / HDD)
        - **Płytę główną**
        - **Zasilacz** (dobrany do poboru mocy)
        - **Obudowę**

        Wszystkie ceny są orientacyjne i oparte na polskim rynku.
        """
    )

    # Mapa przykładowych lokalizacji sklepów komputerowych w Polsce (dla zabawy)
    st.subheader("🗺️ Sklepy komputerowe w Polsce (przykładowe lokalizacje)")
    sklepy = pd.DataFrame(
        {
            "lat": [52.2297, 50.0647, 54.3520, 51.1079, 53.4285],
            "lon": [21.0122, 19.9450, 18.6466, 17.0385, 14.5528],
        }
    )
    st.map(sklepy)
