import os

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Kreator zestawu komputerowego", page_icon="💻", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "components.csv")

# Kategorie tworzące kompletny zestaw (kolejność = kolejność doboru)
CATEGORIES = ["CPU", "Motherboard", "RAM", "GPU", "SSD", "PSU", "Case", "Cooler"]

CATEGORY_LABELS = {
    "CPU": "Procesor",
    "Motherboard": "Płyta główna",
    "RAM": "Pamięć RAM",
    "GPU": "Karta graficzna",
    "SSD": "Dysk SSD",
    "PSU": "Zasilacz",
    "Case": "Obudowa",
    "Cooler": "Chłodzenie",
}

# Dla każdego przeznaczenia: która kolumna wydajności jest ważna oraz jak dzielimy budżet
PURPOSES = {
    "Gry": {
        "perf": "perf_gaming",
        "budget": {"CPU": 0.18, "Motherboard": 0.10, "RAM": 0.08, "GPU": 0.40,
                   "SSD": 0.08, "PSU": 0.07, "Case": 0.05, "Cooler": 0.04},
    },
    "Biuro i dom": {
        "perf": "perf_office",
        "budget": {"CPU": 0.25, "Motherboard": 0.15, "RAM": 0.12, "GPU": 0.10,
                   "SSD": 0.18, "PSU": 0.10, "Case": 0.06, "Cooler": 0.04},
    },
    "Grafika i montaż wideo": {
        "perf": "perf_content",
        "budget": {"CPU": 0.28, "Motherboard": 0.12, "RAM": 0.15, "GPU": 0.25,
                   "SSD": 0.10, "PSU": 0.05, "Case": 0.03, "Cooler": 0.02},
    },
    "Programowanie": {
        "perf": "perf_mix",
        "budget": {"CPU": 0.27, "Motherboard": 0.13, "RAM": 0.18, "GPU": 0.12,
                   "SSD": 0.18, "PSU": 0.06, "Case": 0.04, "Cooler": 0.02},
    },
}

POWER_MARGIN = 1.3  # zapas mocy zasilacza


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # Kolumna pomocnicza dla "Programowanie" - średnia z biura i grafiki
    df["perf_mix"] = (df["perf_office"] + df["perf_content"]) / 2
    return df


def pick_best(candidates, perf_col, max_price):
    """Wybiera najlepszy (najwyższa wydajność) podzespół mieszczący się w budżecie.
    Jeśli nic się nie mieści, zwraca najtańszy dostępny."""
    if candidates.empty:
        return None
    affordable = candidates[candidates["price"] <= max_price]
    pool = affordable if not affordable.empty else candidates
    if not affordable.empty:
        return pool.sort_values(perf_col, ascending=False).iloc[0]
    return pool.sort_values("price", ascending=True).iloc[0]


def recommend_build(df, purpose, total_budget, cpu_brand, min_ram, min_storage):
    cfg = PURPOSES[purpose]
    perf_col = cfg["perf"]
    alloc = cfg["budget"]
    chosen = {}

    # 1. Procesor (z uwzględnieniem preferowanej marki)
    cpus = df[df["category"] == "CPU"]
    if cpu_brand != "Dowolny":
        cpus = cpus[cpus["brand"] == cpu_brand]
    chosen["CPU"] = pick_best(cpus, perf_col, total_budget * alloc["CPU"])
    cpu_socket = chosen["CPU"]["socket"]

    # 2. Płyta główna - musi pasować do gniazda procesora
    boards = df[(df["category"] == "Motherboard") & (df["socket"] == cpu_socket)]
    chosen["Motherboard"] = pick_best(boards, perf_col, total_budget * alloc["Motherboard"])

    # 3. RAM - co najmniej tyle, ile wybrał użytkownik, w typie zgodnym z płytą (DDR4/DDR5)
    board_mem = chosen["Motherboard"]["mem_type"]
    rams = df[(df["category"] == "RAM") & (df["capacity_gb"] >= min_ram) & (df["mem_type"] == board_mem)]
    chosen["RAM"] = pick_best(rams, perf_col, total_budget * alloc["RAM"])

    # 4. Karta graficzna
    gpus = df[df["category"] == "GPU"]
    chosen["GPU"] = pick_best(gpus, perf_col, total_budget * alloc["GPU"])

    # 5. Dysk SSD - co najmniej wybrana pojemność
    ssds = df[(df["category"] == "SSD") & (df["capacity_gb"] >= min_storage)]
    chosen["SSD"] = pick_best(ssds, perf_col, total_budget * alloc["SSD"])

    # 6. Obudowa i chłodzenie
    chosen["Case"] = pick_best(df[df["category"] == "Case"], perf_col, total_budget * alloc["Case"])
    chosen["Cooler"] = pick_best(df[df["category"] == "Cooler"], perf_col, total_budget * alloc["Cooler"])

    # 7. Zasilacz - dobierany tak, aby pokryć pobór mocy z zapasem
    required_w = sum(c["power_draw"] for c in chosen.values() if c is not None) * POWER_MARGIN
    psus = df[df["category"] == "PSU"]
    fitting = psus[psus["wattage"] >= required_w].sort_values("price")
    chosen["PSU"] = fitting.iloc[0] if not fitting.empty else psus.sort_values("wattage").iloc[-1]

    chosen = upgrade_with_leftover(df, chosen, perf_col, total_budget, cpu_brand, min_ram, min_storage)
    return chosen, required_w


def upgrade_with_leftover(df, chosen, perf_col, total_budget, cpu_brand, min_ram, min_storage):
    """Jeśli zostało jeszcze pieniądze w budżecie, próbujemy podnieść wydajność
    podmieniając podzespoły na lepsze (zachowując kompatybilność i limity)."""
    for _ in range(12):  # ograniczona liczba prób, żeby pętla się zawsze kończyła
        spent = sum(c["price"] for c in chosen.values() if c is not None)
        leftover = total_budget - spent
        best_upgrade = None  # (zysk_wydajnosci, kategoria, nowy_podzespol)

        for cat in ["GPU", "CPU", "RAM", "SSD", "Motherboard", "Cooler", "Case"]:
            current = chosen[cat]
            if current is None:
                continue
            options = df[df["category"] == cat]
            if cat == "CPU":
                # Procesor możemy podmienić tylko na pasujący do obecnej płyty (to samo gniazdo)
                options = options[options["socket"] == chosen["Motherboard"]["socket"]]
                if cpu_brand != "Dowolny":
                    options = options[options["brand"] == cpu_brand]
            if cat == "Motherboard":
                # Płytę podmieniamy tylko na pasującą do procesora (gniazdo) i pamięci (typ)
                options = options[(options["socket"] == chosen["CPU"]["socket"]) &
                                  (options["mem_type"] == chosen["RAM"]["mem_type"])]
            if cat == "RAM":
                options = options[(options["capacity_gb"] >= min_ram) &
                                  (options["mem_type"] == chosen["Motherboard"]["mem_type"])]
            if cat == "SSD":
                options = options[options["capacity_gb"] >= min_storage]

            for _, opt in options.iterrows():
                extra = opt["price"] - current["price"]
                gain = opt[perf_col] - current[perf_col]
                if extra <= 0 or gain <= 0 or extra > leftover:
                    continue
                score = gain / extra
                if best_upgrade is None or score > best_upgrade[0]:
                    best_upgrade = (score, cat, opt)

        if best_upgrade is None:
            break
        chosen[best_upgrade[1]] = best_upgrade[2]

    return chosen


def build_to_frame(chosen):
    rows = []
    for cat in CATEGORIES:
        c = chosen[cat]
        if c is None:
            continue
        rows.append({
            "Kategoria": CATEGORY_LABELS[cat],
            "Podzespół": c["name"],
            "Marka": c["brand"],
            "Cena (zł)": int(c["price"]),
        })
    return pd.DataFrame(rows)


# ----------------------------- INTERFEJS ---------------------------------

def main():
    st.title("💻 Kreator zestawu komputerowego")
    st.write("Odpowiedz na kilka pytań w panelu po lewej, a aplikacja zaproponuje "
             "kompletny, kompatybilny zestaw komputerowy dopasowany do budżetu.")

    df = load_data(DATA_PATH)

    st.sidebar.title("Twoje wymagania")
    purpose = st.sidebar.radio("Do czego ma służyć komputer?", list(PURPOSES.keys()))
    budget = st.sidebar.slider("Budżet (zł)", min_value=1500, max_value=12000, value=5000, step=250)
    cpu_brand = st.sidebar.radio("Preferowany producent procesora", ["Dowolny", "AMD", "Intel"])
    min_ram = st.sidebar.select_slider("Minimalna ilość RAM (GB)", options=[8, 16, 32, 64], value=16)
    min_storage = st.sidebar.select_slider(
        "Minimalna pojemność dysku SSD (GB)",
        options=[480, 1000, 2000, 4000],
        value=1000,
    )

    st.sidebar.markdown("---")
    generate = st.sidebar.button("🔧 Złóż zestaw", type="primary", use_container_width=True)

    if not generate:
        st.info("Ustaw parametry po lewej i kliknij **Złóż zestaw**, aby zobaczyć propozycję.")
        with st.expander("Podgląd bazy podzespołów"):
            st.dataframe(df.drop(columns=["perf_mix"]), use_container_width=True)
        st.stop()

    chosen, required_w = recommend_build(df, purpose, budget, cpu_brand, min_ram, min_storage)
    table = build_to_frame(chosen)
    total = table["Cena (zł)"].sum()

    # Średnia wydajność dla wybranego przeznaczenia
    perf_col = PURPOSES[purpose]["perf"]
    avg_perf = sum(chosen[c][perf_col] for c in CATEGORIES if chosen[c] is not None) / len(CATEGORIES)

    st.header(f"Propozycja zestawu: {purpose}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Koszt zestawu", f"{total} zł", delta=f"{total - budget:+d} zł względem budżetu")
    col2.metric("Ocena wydajności", f"{avg_perf:.0f}/100")
    col3.metric("Szac. pobór mocy", f"{int(required_w / POWER_MARGIN)} W")

    if total <= budget:
        st.success(f"Zestaw mieści się w budżecie. Pozostało {budget - total} zł.")
    else:
        st.warning("Zestaw nieznacznie przekracza budżet — przy tych wymaganiach trudno zejść niżej. "
                   "Spróbuj zmniejszyć wymagania (RAM/dysk) lub zwiększyć budżet.")

    # Sprawdzenie zasilacza
    psu_w = chosen["PSU"]["wattage"]
    if psu_w >= required_w:
        st.caption(f"✅ Zasilacz {int(psu_w)} W pokrywa zapotrzebowanie (~{int(required_w)} W z zapasem).")
    else:
        st.caption(f"⚠️ Uwaga: zasilacz {int(psu_w)} W może być zbyt słaby (potrzeba ~{int(required_w)} W).")

    st.subheader("Lista podzespołów")
    st.dataframe(table, use_container_width=True, hide_index=True)

    # Wykres podziału kosztów (matplotlib)
    st.subheader("Na co idą pieniądze?")
    left, right = st.columns(2)
    with left:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(table["Kategoria"], table["Cena (zł)"], color="#4C72B0")
        ax.set_xlabel("Cena (zł)")
        ax.invert_yaxis()
        for i, v in enumerate(table["Cena (zł)"]):
            ax.text(v + max(table["Cena (zł)"]) * 0.01, i, f"{v} zł", va="center", fontsize=8)
        st.pyplot(fig)
    with right:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.pie(table["Cena (zł)"], labels=table["Kategoria"], autopct="%1.0f%%", startangle=90)
        ax2.axis("equal")
        st.pyplot(fig2)

    st.caption("Dane podzespołów i ceny są przykładowe (plik data/components.csv) i służą celom edukacyjnym.")


if __name__ == "__main__":
    main()
