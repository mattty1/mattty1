"""
Konfigurator PC – aplikacja Streamlit.

Źródło danych (do wyboru):
  1. Wbudowana baza danych (domyślna).
  2. Własny plik CSV wgrany przez użytkownika (np. ceny z Morele / Ceneo).

Format CSV:
  kategoria, nazwa, cena, wydajnosc, tdp, zastosowania
  procesor, AMD Ryzen 5 7600X, 880, 74, 105, gaming,programowanie
  gpu, NVIDIA RTX 3060, 1040, 65, 0, gaming,grafika
  ram, 16 GB DDR4 3200, 210, 16, 0, dowolne
  dysk, 1 TB NVMe M.2, 325, 0, 0, dowolne
"""

import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

# ─────────────────────────────────────────────────────────────────────────────
# WBUDOWANA BAZA DANYCH
# ─────────────────────────────────────────────────────────────────────────────

PROCESORY_DOMYSLNE = pd.DataFrame([
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

GPU_DOMYSLNE = pd.DataFrame([
    {"nazwa": "Zintegrowana (brak karty)",  "cena": 0,    "wydajnosc": 5,   "zastosowania": "biuro,ogolne"},
    {"nazwa": "NVIDIA GeForce GTX 1650",    "cena": 540,  "wydajnosc": 34,  "zastosowania": "ogolne,gaming"},
    {"nazwa": "AMD Radeon RX 6600",         "cena": 840,  "wydajnosc": 58,  "zastosowania": "gaming"},
    {"nazwa": "NVIDIA GeForce RTX 3060",    "cena": 1040, "wydajnosc": 65,  "zastosowania": "gaming,grafika"},
    {"nazwa": "NVIDIA GeForce RTX 3070 Ti", "cena": 1700, "wydajnosc": 80,  "zastosowania": "gaming,grafika,wideo"},
    {"nazwa": "AMD Radeon RX 7900 XT",      "cena": 2450, "wydajnosc": 90,  "zastosowania": "gaming,grafika,wideo"},
    {"nazwa": "NVIDIA GeForce RTX 4080",    "cena": 3400, "wydajnosc": 95,  "zastosowania": "gaming,grafika,wideo"},
    {"nazwa": "NVIDIA GeForce RTX 4090",    "cena": 5400, "wydajnosc": 100, "zastosowania": "gaming,grafika,wideo"},
])

RAM_DOMYSLNE = pd.DataFrame([
    {"opis": "8 GB DDR4 3200 MHz",  "rozmiar": 8,  "typ": "DDR4", "cena": 120},
    {"opis": "16 GB DDR4 3200 MHz", "rozmiar": 16, "typ": "DDR4", "cena": 210},
    {"opis": "16 GB DDR5 5200 MHz", "rozmiar": 16, "typ": "DDR5", "cena": 340},
    {"opis": "32 GB DDR4 3600 MHz", "rozmiar": 32, "typ": "DDR4", "cena": 375},
    {"opis": "32 GB DDR5 5200 MHz", "rozmiar": 32, "typ": "DDR5", "cena": 610},
    {"opis": "64 GB DDR5 5600 MHz", "rozmiar": 64, "typ": "DDR5", "cena": 1100},
])

DYSKI_DOMYSLNE = pd.DataFrame([
    {"opis": "256 GB SSD SATA",  "pojemnosc_gb": 256,  "typ": "SSD SATA", "cena": 110},
    {"opis": "500 GB SSD SATA",  "pojemnosc_gb": 500,  "typ": "SSD SATA", "cena": 165},
    {"opis": "500 GB NVMe M.2",  "pojemnosc_gb": 500,  "typ": "NVMe M.2", "cena": 195},
    {"opis": "1 TB SSD SATA",    "pojemnosc_gb": 1000, "typ": "SSD SATA", "cena": 255},
    {"opis": "1 TB NVMe M.2",    "pojemnosc_gb": 1000, "typ": "NVMe M.2", "cena": 325},
    {"opis": "2 TB SSD SATA",    "pojemnosc_gb": 2000, "typ": "SSD SATA", "cena": 475},
    {"opis": "2 TB NVMe M.2",    "pojemnosc_gb": 2000, "typ": "NVMe M.2", "cena": 610},
    {"opis": "4 TB HDD",         "pojemnosc_gb": 4000, "typ": "HDD",      "cena": 285},
])

PLYTY_GLOWNE = {
    ("Intel", "DDR4"): {"nazwa": "MSI PRO B660M-A DDR4",        "cena": 440},
    ("Intel", "DDR5"): {"nazwa": "ASUS PRIME Z790-P DDR5",       "cena": 690},
    ("AMD",   "DDR4"): {"nazwa": "MSI MAG B550 TOMAHAWK DDR4",   "cena": 490},
    ("AMD",   "DDR5"): {"nazwa": "ASUS ROG STRIX X670E-F DDR5",  "cena": 890},
}

ZASILACZE = pd.DataFrame([
    {"opis": "450W 80+ Bronze", "moc": 450, "cena": 190},
    {"opis": "550W 80+ Bronze", "moc": 550, "cena": 250},
    {"opis": "650W 80+ Gold",   "moc": 650, "cena": 340},
    {"opis": "750W 80+ Gold",   "moc": 750, "cena": 410},
    {"opis": "850W 80+ Gold",   "moc": 850, "cena": 490},
    {"opis": "1000W 80+ Plat.", "moc": 1000,"cena": 690},
])

OBUDOWY = pd.DataFrame([
    {"nazwa": "Fractal Design Core 1000", "cena": 200},
    {"nazwa": "be quiet! Pure Base 500",  "cena": 340},
    {"nazwa": "NZXT H7 Flow",             "cena": 490},
    {"nazwa": "Lian Li PC-O11 Dynamic",   "cena": 580},
])

# ─────────────────────────────────────────────────────────────────────────────
# OBSŁUGA WŁASNEGO CSV
# Format: kategoria, nazwa, cena, wydajnosc, tdp, zastosowania
#         (kolumna "marka" i "rozmiar" / "pojemnosc_gb" są opcjonalne)
# ─────────────────────────────────────────────────────────────────────────────

CSV_SZABLON = """\
kategoria,nazwa,cena,wydajnosc,tdp,marka,rozmiar_gb,pojemnosc_gb,typ_ram,typ_dysku,zastosowania
procesor,AMD Ryzen 5 7600X,880,74,105,AMD,,,,,gaming|programowanie
procesor,Intel Core i5-13600K,1100,80,125,Intel,,,,,gaming|programowanie|grafika
gpu,NVIDIA GeForce RTX 3060,1040,65,0,,,,,,gaming|grafika
gpu,Zintegrowana (brak karty),0,5,0,,,,,,biuro|ogolne
ram,16 GB DDR4 3200 MHz,210,16,0,,16,,DDR4,,dowolne
ram,32 GB DDR5 5200 MHz,600,32,0,,32,,DDR5,,dowolne
dysk,1 TB NVMe M.2,325,0,0,,,,1000,NVMe M.2,dowolne
dysk,500 GB SSD SATA,165,0,0,,,,500,SSD SATA,dowolne
"""
# Zastosowania używają '|' jako separatora wewnętrznego (nie koliduje z CSV).


def wczytaj_csv(uploaded_file):
    """Wczytuje wgrany CSV i zwraca słownik DataFramów zastępujących wbudowane dane."""
    df = pd.read_csv(uploaded_file, dtype=str)
    df.columns = [c.strip().lower() for c in df.columns]

    required = {"kategoria", "nazwa", "cena"}
    if not required.issubset(df.columns):
        return None, f"CSV musi zawierać kolumny: {required}. Znaleziono: {set(df.columns)}"

    df["cena"] = pd.to_numeric(df["cena"], errors="coerce").fillna(0).astype(int)
    df["wydajnosc"] = pd.to_numeric(df.get("wydajnosc", 0), errors="coerce").fillna(0).astype(int)
    df["tdp"]       = pd.to_numeric(df.get("tdp",       0), errors="coerce").fillna(0).astype(int)
    if "zastosowania" not in df.columns:
        df["zastosowania"] = "biuro,ogolne,gaming,programowanie,grafika,wideo"
    # Normalizacja separatora: '|' → ',' żeby pasowało do logiki scoringu
    df["zastosowania"] = df["zastosowania"].str.replace("|", ",", regex=False)

    procesory = df[df["kategoria"].str.strip().str.lower() == "procesor"].copy()
    gpu       = df[df["kategoria"].str.strip().str.lower() == "gpu"].copy()
    ram       = df[df["kategoria"].str.strip().str.lower() == "ram"].copy()
    dyski     = df[df["kategoria"].str.strip().str.lower() == "dysk"].copy()

    # Mapuj kolumny na schemat wbudowanej bazy
    if not procesory.empty:
        procesory = procesory.rename(columns={"nazwa": "nazwa"})
        if "marka" not in procesory.columns:
            procesory["marka"] = procesory["nazwa"].apply(
                lambda n: "AMD" if "AMD" in str(n) or "Ryzen" in str(n) else "Intel"
            )

    if not ram.empty:
        if "rozmiar_gb" in ram.columns:
            ram["rozmiar"] = pd.to_numeric(ram["rozmiar_gb"], errors="coerce").fillna(8).astype(int)
        else:
            ram["rozmiar"] = ram["nazwa"].str.extract(r'(\d+)\s*GB').astype(float).fillna(16).astype(int)
        ram = ram.rename(columns={"nazwa": "opis"})
        if "typ_ram" not in ram.columns:
            ram["typ"] = ram["opis"].str.extract(r'(DDR[45])')[0].fillna("DDR4")
        else:
            ram = ram.rename(columns={"typ_ram": "typ"})

    if not dyski.empty:
        if "pojemnosc_gb" in dyski.columns:
            dyski["pojemnosc_gb"] = pd.to_numeric(dyski["pojemnosc_gb"], errors="coerce").fillna(500).astype(int)
        else:
            dyski["pojemnosc_gb"] = dyski["nazwa"].str.extract(r'(\d+)\s*(TB|GB)').apply(
                lambda r: int(r[0]) * 1000 if r[1] == "TB" else int(r[0]), axis=1
            ).fillna(500).astype(int)
        dyski = dyski.rename(columns={"nazwa": "opis"})
        if "typ_dysku" not in dyski.columns:
            dyski["typ"] = dyski["opis"].str.extract(r'(NVMe|SSD SATA|HDD)')[0].fillna("SSD SATA")
        else:
            dyski = dyski.rename(columns={"typ_dysku": "typ"})

    if not gpu.empty:
        gpu = gpu.rename(columns={"nazwa": "nazwa"})

    return {
        "procesory": procesory if not procesory.empty else None,
        "gpu":       gpu       if not gpu.empty       else None,
        "ram":       ram       if not ram.empty        else None,
        "dyski":     dyski     if not dyski.empty      else None,
    }, None


# ─────────────────────────────────────────────────────────────────────────────
# LOGIKA REKOMENDACJI
# ─────────────────────────────────────────────────────────────────────────────

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


def score_component(row, zastosowanie):
    zast_lista = str(row.get("zastosowania", "")).split(",")
    bonus = 1.4 if zastosowanie in zast_lista else 0.8
    return float(row.get("wydajnosc", 0)) * bonus


def wybierz_najlepszy(df, budzet, zastosowanie, col_cena="cena"):
    kandydaci = df[df[col_cena] <= budzet].copy()
    if kandydaci.empty:
        kandydaci = df.nsmallest(1, col_cena)
    if "wydajnosc" in df.columns:
        kandydaci["_score"] = kandydaci.apply(lambda r: score_component(r, zastosowanie), axis=1)
        return kandydaci.loc[kandydaci["_score"].idxmax()]
    return kandydaci.loc[kandydaci[col_cena].idxmax()]


def dobierz_zasilacz(tdp_cpu, tdp_gpu):
    wymagana_moc = (tdp_cpu + tdp_gpu) * 1.30 + 100
    pasujace = ZASILACZE[ZASILACZE["moc"] >= wymagana_moc]
    return pasujace.iloc[0] if not pasujace.empty else ZASILACZE.iloc[-1]


def rekomenduj(budzet, zastosowanie, marka_cpu, min_ram_gb, min_dysk_gb, typ_dysku,
               procesory_df, gpu_df, ram_df, dyski_df):
    przydzial = PRZYDZIAL_BUDZETU[zastosowanie]

    # CPU
    cpu_df = procesory_df.copy()
    if marka_cpu != "Bez preferencji" and "marka" in cpu_df.columns:
        filtered = cpu_df[cpu_df["marka"] == marka_cpu]
        cpu_df = filtered if not filtered.empty else cpu_df
    cpu = wybierz_najlepszy(cpu_df, budzet * przydzial["cpu"], zastosowanie)

    # RAM
    r_df = ram_df[ram_df["rozmiar"] >= min_ram_gb].copy() if not ram_df.empty else ram_df.copy()
    if r_df.empty:
        r_df = ram_df.copy()
    r_df["wydajnosc"] = r_df["rozmiar"]
    r_df["zastosowania"] = "biuro,ogolne,gaming,programowanie,grafika,wideo"
    ram = wybierz_najlepszy(r_df, budzet * przydzial["ram"], zastosowanie)

    # Płyta główna
    typ_ram = ram.get("typ", "DDR4")
    klucz = (cpu.get("marka", "Intel"), typ_ram)
    plyta = PLYTY_GLOWNE.get(klucz, PLYTY_GLOWNE.get((cpu.get("marka","Intel"), "DDR4"),
            {"nazwa": "Płyta główna standardowa", "cena": 450}))

    # Dysk
    d_df = dyski_df[dyski_df["pojemnosc_gb"] >= min_dysk_gb].copy() if not dyski_df.empty else dyski_df.copy()
    if typ_dysku != "Dowolny" and "typ" in d_df.columns:
        tmp = d_df[d_df["typ"] == typ_dysku]
        if not tmp.empty:
            d_df = tmp
    if d_df.empty:
        d_df = dyski_df.copy()
    d_df["wydajnosc"] = d_df["pojemnosc_gb"] / 40
    d_df["zastosowania"] = "biuro,ogolne,gaming,programowanie,grafika,wideo"
    dysk = wybierz_najlepszy(d_df, budzet * przydzial["dysk"], zastosowanie)

    # GPU
    if przydzial["gpu"] == 0:
        gpu = gpu_df.iloc[0]
    else:
        gpu = wybierz_najlepszy(gpu_df, budzet * przydzial["gpu"], zastosowanie)

    # Zasilacz i obudowa
    tdp_gpu = 0 if "Zintegrowana" in str(gpu.get("nazwa", "")) else 150
    zasilacz = dobierz_zasilacz(int(cpu.get("tdp", 65)), tdp_gpu)

    bud_obudowa = budzet * przydzial["obudowa"]
    pasujace_o = OBUDOWY[OBUDOWY["cena"] <= bud_obudowa]
    obudowa = pasujace_o.iloc[-1] if not pasujace_o.empty else OBUDOWY.iloc[0]

    return {
        "Procesor":        {"opis": cpu.get("nazwa","?"),        "cena": int(cpu.get("cena",0)),      "wydajnosc": int(cpu.get("wydajnosc",0))},
        "Karta graficzna": {"opis": gpu.get("nazwa","?"),        "cena": int(gpu.get("cena",0)),      "wydajnosc": int(gpu.get("wydajnosc",0))},
        "RAM":             {"opis": ram.get("opis","?"),          "cena": int(ram.get("cena",0)),      "wydajnosc": int(ram.get("rozmiar",0))},
        "Dysk":            {"opis": dysk.get("opis","?"),         "cena": int(dysk.get("cena",0)),     "wydajnosc": None},
        "Płyta główna":    {"opis": plyta["nazwa"],               "cena": int(plyta["cena"]),          "wydajnosc": None},
        "Zasilacz":        {"opis": zasilacz["opis"],             "cena": int(zasilacz["cena"]),       "wydajnosc": None},
        "Obudowa":         {"opis": obudowa["nazwa"],             "cena": int(obudowa["cena"]),        "wydajnosc": None},
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
    min_value=1500, max_value=15000, value=4000, step=500,
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
    options=[8, 16, 32, 64], value=16,
    format_func=lambda x: f"{x} GB",
)

st.sidebar.markdown("---")

min_dysk_gb = st.sidebar.select_slider(
    "Minimalna pojemność dysku",
    options=[256, 500, 1000, 2000, 4000], value=500,
    format_func=lambda v: f"{v} GB" if v < 1000 else f"{v // 1000} TB",
)

typ_dysku = st.sidebar.radio(
    "Typ dysku",
    ["NVMe M.2", "SSD SATA", "HDD", "Dowolny"], index=3,
)

st.sidebar.markdown("---")

# ── Wgrywanie własnego CSV ────────────────────────────────────────────────────
with st.sidebar.expander("📂 Własna baza danych (CSV)"):
    st.markdown(
        "Możesz wgrać własny CSV z cenami z **Morele / Ceneo** lub innego sklepu. "
        "Pobierz szablon, uzupełnij ceny i wgraj plik."
    )
    st.download_button(
        label="⬇️ Pobierz szablon CSV",
        data=CSV_SZABLON,
        file_name="podzespoly_szablon.csv",
        mime="text/csv",
    )
    uploaded_file = st.file_uploader(
        "Wgraj plik CSV z cenami",
        type=["csv"],
        help="Format: kategoria, nazwa, cena, wydajnosc, tdp, zastosowania",
    )

st.sidebar.markdown("---")
generuj = st.sidebar.button("🔍 Generuj rekomendację", use_container_width=True)

# ── Wczytanie danych ──────────────────────────────────────────────────────────
use_custom = False
procesory_df = PROCESORY_DOMYSLNE.copy()
gpu_df       = GPU_DOMYSLNE.copy()
ram_df       = RAM_DOMYSLNE.copy()
dyski_df     = DYSKI_DOMYSLNE.copy()

if uploaded_file is not None:
    dane, blad = wczytaj_csv(uploaded_file)
    if blad:
        st.sidebar.error(f"Błąd CSV: {blad}")
    else:
        use_custom = True
        if dane["procesory"] is not None:
            procesory_df = dane["procesory"]
        if dane["gpu"] is not None:
            gpu_df = dane["gpu"]
        if dane["ram"] is not None:
            ram_df = dane["ram"]
        if dane["dyski"] is not None:
            dyski_df = dane["dyski"]
        st.sidebar.success(
            f"✅ Wgrano CSV: {len(procesory_df)} CPU | {len(gpu_df)} GPU | "
            f"{len(ram_df)} RAM | {len(dyski_df)} dysków"
        )

# ── GŁÓWNY OBSZAR ─────────────────────────────────────────────────────────────

# Info o zastosowaniu
st.info(f"**{zastosowanie_label}** – {ZASTOSOWANIE_OPISY[zastosowanie]}")

if use_custom:
    st.success("Używasz własnej bazy danych z wgranego CSV.")
else:
    st.caption("Używasz wbudowanej bazy danych. Możesz wgrać własny CSV z aktualnymi cenami ze sklepu.")

if generuj or "rekomendacja" in st.session_state:
    if generuj:
        st.session_state["rekomendacja"] = rekomenduj(
            budzet, zastosowanie, marka_cpu, min_ram_gb, min_dysk_gb, typ_dysku,
            procesory_df, gpu_df, ram_df, dyski_df,
        )
        st.session_state["budzet_snapshot"] = budzet
        st.session_state["zrodlo"] = "CSV (własna baza)" if use_custom else "Wbudowana baza danych"

    rec         = st.session_state["rekomendacja"]
    budzet_snap = st.session_state.get("budzet_snapshot", budzet)
    zrodlo      = st.session_state.get("zrodlo", "?")

    # ── Tabela wynikowa ───────────────────────────────────────────────────────
    st.subheader("📋 Rekomendowany zestaw")
    st.caption(f"Źródło danych: {zrodlo}")

    wiersze = []
    suma = 0
    for kategoria, dane in rec.items():
        wiersze.append({"Podzespół": kategoria, "Model": dane["opis"], "Cena (PLN)": dane["cena"]})
        suma += dane["cena"]

    df_wynik = pd.DataFrame(wiersze)
    df_wynik.index = df_wynik.index + 1
    st.dataframe(df_wynik, use_container_width=True)

    # ── Metryki ───────────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Łączny koszt", f"{suma} PLN")
    col2.metric("📊 Budżet", f"{budzet_snap} PLN")
    oszcz = budzet_snap - suma
    col3.metric("💵 Pozostało", f"{oszcz} PLN",
                delta=f"{oszcz:+} PLN",
                delta_color="normal" if oszcz >= 0 else "inverse")

    if suma > budzet_snap:
        st.warning(f"⚠️ Zestaw przekracza budżet o **{suma - budzet_snap} PLN**.")
    else:
        st.success("✅ Zestaw mieści się w podanym budżecie.")

    st.markdown("---")

    # ── Wykresy ───────────────────────────────────────────────────────────────
    nazwy = [w["Podzespół"] for w in wiersze]
    ceny  = [w["Cena (PLN)"] for w in wiersze]

    col_w1, col_w2 = st.columns(2)

    with col_w1:
        st.subheader("💸 Koszt podzespołów")
        fig1, ax1 = plt.subplots(figsize=(7, 4))
        kolory = plt.cm.Blues(np.linspace(0.4, 0.9, len(nazwy)))
        bars = ax1.barh(nazwy, ceny, color=kolory)
        ax1.set_xlabel("Cena (PLN)")
        for bar, cena in zip(bars, ceny):
            ax1.text(bar.get_width() + 10, bar.get_y() + bar.get_height() / 2,
                     f"{cena} PLN", va="center", fontsize=9)
        ax1.set_xlim(0, max(ceny) * 1.3 if max(ceny) > 0 else 100)
        plt.tight_layout()
        st.pyplot(fig1)

    with col_w2:
        st.subheader("📊 Udział w budżecie")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.pie(ceny, labels=nazwy, autopct="%1.1f%%", startangle=90,
                wedgeprops={"linewidth": 1, "edgecolor": "white"},
                colors=plt.cm.Set3.colors[:len(nazwy)])
        ax2.set_title("Struktura kosztów")
        plt.tight_layout()
        st.pyplot(fig2)

    # ── Wydajność ─────────────────────────────────────────────────────────────
    wydajnosci = {k: v["wydajnosc"] for k, v in rec.items() if v["wydajnosc"] is not None}
    if wydajnosci:
        st.subheader("⚡ Ocena wydajności kluczowych podzespołów")
        fig3, ax3 = plt.subplots(figsize=(8, 3))
        vals = np.array(list(wydajnosci.values()), dtype=float)
        kolory2 = plt.cm.RdYlGn(vals / max(vals.max(), 1))
        ax3.barh(list(wydajnosci.keys()), vals, color=kolory2)
        ax3.set_xlim(0, 110)
        ax3.set_xlabel("Ocena (0–100)")
        for i, (k, v) in enumerate(wydajnosci.items()):
            ax3.text(v + 1, i, str(v), va="center", fontsize=10)
        plt.tight_layout()
        st.pyplot(fig3)

    st.markdown("---")

    # ── Podgląd bazy ──────────────────────────────────────────────────────────
    with st.expander("📄 Pełna lista procesorów w bieżącej bazie"):
        cols = [c for c in ["nazwa", "marka", "cena", "wydajnosc", "tdp"] if c in procesory_df.columns]
        rename = {"nazwa": "Model", "marka": "Marka", "cena": "Cena (PLN)",
                  "wydajnosc": "Ocena", "tdp": "TDP (W)"}
        st.dataframe(procesory_df[cols].rename(columns=rename), use_container_width=True)

    with st.expander("📄 Pełna lista kart graficznych w bieżącej bazie"):
        cols = [c for c in ["nazwa", "cena", "wydajnosc"] if c in gpu_df.columns]
        rename = {"nazwa": "Model", "cena": "Cena (PLN)", "wydajnosc": "Ocena"}
        st.dataframe(gpu_df[cols].rename(columns=rename), use_container_width=True)

    with st.expander("📄 Pełna lista opcji RAM"):
        cols = [c for c in ["opis", "rozmiar", "typ", "cena"] if c in ram_df.columns]
        rename = {"opis": "Opis", "rozmiar": "Rozmiar (GB)", "typ": "Typ", "cena": "Cena (PLN)"}
        st.dataframe(ram_df[cols].rename(columns=rename), use_container_width=True)

    with st.expander("📄 Pełna lista dysków"):
        cols = [c for c in ["opis", "pojemnosc_gb", "typ", "cena"] if c in dyski_df.columns]
        rename = {"opis": "Opis", "pojemnosc_gb": "Pojemność (GB)", "typ": "Typ", "cena": "Cena (PLN)"}
        st.dataframe(dyski_df[cols].rename(columns=rename), use_container_width=True)

    # ── JSON ──────────────────────────────────────────────────────────────────
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

        > **Chcesz aktualnych cen z Morele lub Ceneo?**
        > Pobierz szablon CSV z paska bocznego, uzupełnij ceny ręcznie i wgraj plik.
        > Wszystkie obliczenia zostaną przeliczone na nowo.

        Wbudowane ceny są orientacyjne (stan ~2024).
        """
    )

    st.subheader("🗺️ Sklepy komputerowe w Polsce (przykładowe lokalizacje)")
    sklepy = pd.DataFrame({
        "lat": [52.2297, 50.0647, 54.3520, 51.1079, 53.4285],
        "lon": [21.0122, 19.9450, 18.6466, 17.0385, 14.5528],
    })
    st.map(sklepy)
