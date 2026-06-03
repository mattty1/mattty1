import os

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Ile procent budzetu przeznaczamy na kazda kategorie w zaleznosci od zastosowania.
# Sumy moga sie nieznacznie roznic - sluza tylko jako wskazowka przy doborze.
PROFILE_BUDZETU = {
    "Gry": {
        "gpu": True,
        "wagi": {"cpu": 0.20, "motherboard": 0.08, "ram": 0.08, "gpu": 0.38,
                 "storage": 0.10, "psu": 0.07, "case": 0.06, "cooler": 0.03},
    },
    "Praca biurowa / nauka": {
        "gpu": False,
        "wagi": {"cpu": 0.32, "motherboard": 0.15, "ram": 0.15, "gpu": 0.00,
                 "storage": 0.20, "psu": 0.08, "case": 0.06, "cooler": 0.04},
    },
    "Programowanie": {
        "gpu": True,
        "wagi": {"cpu": 0.28, "motherboard": 0.10, "ram": 0.20, "gpu": 0.16,
                 "storage": 0.14, "psu": 0.06, "case": 0.04, "cooler": 0.02},
    },
    "Grafika / montaż wideo": {
        "gpu": True,
        "wagi": {"cpu": 0.25, "motherboard": 0.08, "ram": 0.18, "gpu": 0.28,
                 "storage": 0.12, "psu": 0.05, "case": 0.02, "cooler": 0.02},
    },
    "Streaming": {
        "gpu": True,
        "wagi": {"cpu": 0.26, "motherboard": 0.08, "ram": 0.12, "gpu": 0.30,
                 "storage": 0.10, "psu": 0.06, "case": 0.05, "cooler": 0.03},
    },
}


@st.cache_data
def wczytaj_dane():
    """Wczytuje caly katalog podzespolow z plikow CSV (nasza 'baza danych')."""
    pliki = ["cpu", "motherboard", "ram", "gpu", "storage", "psu", "cooler", "case"]
    return {p: pd.read_csv(os.path.join(DATA_DIR, f"{p}.csv")) for p in pliki}


def wybierz(df, sub_budzet, kolumna_ceny="price", kolumna_oceny="score"):
    """Wybiera najlepszy (najwyzsza ocena) podzespol miesczacy sie w pod-budzecie.

    Jesli nic sie nie miesci, bierze najtanszy dostepny - zeby zestaw zawsze byl kompletny.
    """
    if df.empty:
        return None
    stac_nas = df[df[kolumna_ceny] <= sub_budzet]
    if not stac_nas.empty:
        return stac_nas.sort_values(kolumna_oceny, ascending=False).iloc[0]
    return df.sort_values(kolumna_ceny, ascending=True).iloc[0]


def zloz_komputer(dane, budzet, zastosowanie, marka_cpu, min_ram, dysk_min, dysk_max,
                  typ_dysku, wymus_gpu):
    profil = PROFILE_BUDZETU[zastosowanie]
    wagi = profil["wagi"]
    potrzebny_gpu = profil["gpu"] or wymus_gpu

    zestaw = {}
    powody = []

    # --- Procesor ---
    cpu_df = dane["cpu"]
    if marka_cpu != "Obojętne":
        cpu_df = cpu_df[cpu_df["brand"] == marka_cpu]
    cpu = wybierz(cpu_df, budzet * wagi["cpu"])
    zestaw["Procesor"] = cpu

    # --- Plyta glowna (musi pasowac do gniazda procesora) ---
    mobo_df = dane["motherboard"][dane["motherboard"]["socket"] == cpu["socket"]]
    mobo = wybierz(mobo_df, budzet * wagi["motherboard"])
    zestaw["Płyta główna"] = mobo

    # --- Pamiec RAM (musi pasowac do typu pamieci plyty + min. pojemnosc) ---
    ram_df = dane["ram"][
        (dane["ram"]["ram_type"] == mobo["ram_type"])
        & (dane["ram"]["capacity_gb"] >= min_ram)
    ]
    if ram_df.empty:  # fallback gdy zadana pojemnosc niedostepna dla typu pamieci
        ram_df = dane["ram"][dane["ram"]["ram_type"] == mobo["ram_type"]]
        powody.append(f"Brak RAM ≥ {min_ram} GB w standardzie {mobo['ram_type']} - dobrano najwieksza dostepna.")
    ram = wybierz(ram_df, budzet * wagi["ram"])
    zestaw["Pamięć RAM"] = ram

    # --- Karta graficzna ---
    gpu_df = dane["gpu"]
    if potrzebny_gpu:
        gpu_df = gpu_df[gpu_df["price"] > 0]
        gpu = wybierz(gpu_df, budzet * wagi["gpu"])
    else:
        gpu = gpu_df[gpu_df["price"] == 0].iloc[0]  # karta zintegrowana
    zestaw["Karta graficzna"] = gpu

    # --- Dysk (zakres pojemnosci + ewentualnie typ) ---
    storage_df = dane["storage"][
        (dane["storage"]["capacity_gb"] >= dysk_min)
        & (dane["storage"]["capacity_gb"] <= dysk_max)
    ]
    if typ_dysku != "Obojętne":
        storage_df = storage_df[storage_df["type"] == typ_dysku]
    if storage_df.empty:
        storage_df = dane["storage"]
        powody.append("Brak dysku w zadanym zakresie pojemnosci/typie - dobrano alternatywe.")
    storage = wybierz(storage_df, budzet * wagi["storage"])
    zestaw["Dysk"] = storage

    # --- Zasilacz (musi miec moc >= zalecanej dla karty graficznej) ---
    min_w = int(gpu["min_psu_w"]) if gpu["min_psu_w"] > 0 else 450
    psu_df = dane["psu"][dane["psu"]["watt"] >= min_w]
    if psu_df.empty:
        psu_df = dane["psu"]
    psu = wybierz(psu_df, budzet * wagi["psu"])
    if psu["watt"] < min_w:
        powody.append(f"Uwaga: zalecany zasilacz ≥ {min_w} W dla wybranej karty graficznej.")
    zestaw["Zasilacz"] = psu

    # --- Chlodzenie ---
    cooler = wybierz(dane["cooler"], budzet * wagi["cooler"])
    zestaw["Chłodzenie"] = cooler

    # --- Obudowa ---
    obudowa = wybierz(dane["case"], budzet * wagi["case"])
    zestaw["Obudowa"] = obudowa

    return zestaw, powody


def zestaw_do_tabeli(zestaw):
    wiersze = []
    for kategoria, czesc in zestaw.items():
        wiersze.append({
            "Kategoria": kategoria,
            "Model": czesc["model"],
            "Cena (PLN)": int(czesc["price"]),
        })
    return pd.DataFrame(wiersze)


# ----------------------------- INTERFEJS -----------------------------
st.set_page_config(page_title="Kreator zestawu komputerowego", page_icon="🖥️", layout="wide")
st.title("🖥️ Kreator zestawu komputerowego")
st.write("Powiedz, do czego ma służyć komputer i ile chcesz wydać — aplikacja dobierze "
         "kompatybilny zestaw podzespołów z katalogu.")

dane = wczytaj_dane()

st.sidebar.title("Twoje wymagania")
budzet = st.sidebar.slider("Budżet (PLN)", min_value=2000, max_value=15000,
                           value=5000, step=250)
zastosowanie = st.sidebar.selectbox("Do czego ma służyć komputer?",
                                    list(PROFILE_BUDZETU.keys()))
marka_cpu = st.sidebar.radio("Preferowany procesor", ["Obojętne", "AMD", "Intel"],
                             horizontal=True)
min_ram = st.sidebar.select_slider("Minimalna ilość RAM (GB)",
                                   options=[8, 16, 32, 64], value=16)
dysk_min, dysk_max = st.sidebar.select_slider(
    "Zakres pojemności dysku (GB)",
    options=[480, 500, 1000, 2000, 4000],
    value=(500, 2000),
)
typ_dysku = st.sidebar.selectbox("Typ dysku",
                                 ["Obojętne", "SSD NVMe", "SSD SATA", "HDD"])
wymus_gpu = st.sidebar.checkbox("Wymuś dedykowaną kartę graficzną", value=False)

st.sidebar.caption(f"Katalog: {sum(len(v) for v in dane.values())} podzespołów w bazie.")

if st.sidebar.button("🔧 Złóż komputer", type="primary"):
    zestaw, powody = zloz_komputer(dane, budzet, zastosowanie, marka_cpu, min_ram,
                                   dysk_min, dysk_max, typ_dysku, wymus_gpu)
    tabela = zestaw_do_tabeli(zestaw)
    suma = int(tabela["Cena (PLN)"].sum())

    kol1, kol2 = st.columns([3, 2])

    with kol1:
        st.subheader(f"Proponowany zestaw — {zastosowanie}")
        st.dataframe(tabela, hide_index=True, use_container_width=True)

        st.metric("Łączny koszt", f"{suma} PLN", delta=f"{suma - budzet} PLN do budżetu",
                  delta_color="inverse")
        if suma <= budzet:
            st.success(f"Zmieściliśmy się w budżecie! Zostało Ci {budzet - suma} PLN.")
        else:
            st.warning(f"Zestaw przekracza budżet o {suma - budzet} PLN. "
                       "Zmniejsz wymagania (np. RAM, dysk) lub zwiększ budżet.")

        for p in powody:
            st.info(p)

        st.download_button("⬇️ Pobierz zestaw (CSV)",
                           tabela.to_csv(index=False).encode("utf-8"),
                           file_name="moj_zestaw.csv", mime="text/csv")

    with kol2:
        st.subheader("Podział kosztów")
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.barh(tabela["Kategoria"], tabela["Cena (PLN)"], color="#4c8bf5")
        ax.set_xlabel("Cena (PLN)")
        ax.invert_yaxis()
        for i, v in enumerate(tabela["Cena (PLN)"]):
            ax.text(v, i, f" {int(v)}", va="center")
        st.pyplot(fig)
else:
    st.info("Ustaw parametry po lewej i kliknij **Złóż komputer**.")

with st.expander("📚 Zobacz pełny katalog podzespołów (baza danych)"):
    nazwy = {"cpu": "Procesory", "motherboard": "Płyty główne", "ram": "Pamięć RAM",
             "gpu": "Karty graficzne", "storage": "Dyski", "psu": "Zasilacze",
             "cooler": "Chłodzenie", "case": "Obudowy"}
    for klucz, df in dane.items():
        st.markdown(f"**{nazwy[klucz]}**")
        st.dataframe(df, hide_index=True, use_container_width=True)
