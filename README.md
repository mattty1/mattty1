# 🖥️ Kreator zestawu komputerowego (Streamlit)

Praktyczna aplikacja w Streamlit, która na podstawie **budżetu** i **przeznaczenia**
komputera proponuje kompatybilny zestaw podzespołów (procesor, płyta główna, RAM,
karta graficzna, dysk, zasilacz, chłodzenie, obudowa).

## Pomysł

Użytkownik w panelu bocznym ustawia:

- **budżet** (suwak, PLN),
- **do czego ma służyć** komputer (gry, biuro/nauka, programowanie, grafika/montaż, streaming),
- **preferowaną markę procesora** (AMD / Intel / obojętne),
- **minimalną ilość RAM**,
- **zakres pojemności dysku** i jego typ (NVMe / SATA / HDD),
- czy **wymusić dedykowaną kartę graficzną**.

Aplikacja:

- dzieli budżet pomiędzy kategorie wg profilu zastosowania,
- dla każdej kategorii wybiera najlepszy podzespół mieszczący się w pod-budżecie,
- pilnuje **kompatybilności**: gniazdo CPU ↔ płyta główna, typ pamięci płyta ↔ RAM,
  minimalna moc zasilacza ↔ karta graficzna,
- pokazuje tabelę zestawu, łączny koszt, informację o zmieszczeniu się w budżecie
  oraz wykres podziału kosztów (matplotlib),
- pozwala pobrać zestaw jako CSV.

## Baza danych

To **nie** wymaga żadnego zewnętrznego API. Katalog podzespołów to zwykłe pliki CSV
w folderze [`data/`](data/) — łatwo je edytować, dopisywać nowe modele lub aktualizować ceny.

## Uruchomienie

```bash
pip install -r requirements.txt
streamlit run app.py
```

Następnie otwórz adres pokazany w terminalu (domyślnie http://localhost:8501).

## Struktura

```
app.py              # aplikacja Streamlit
data/               # katalog podzespołów (CSV = "baza danych")
  cpu.csv
  motherboard.csv
  ram.csv
  gpu.csv
  storage.csv
  psu.csv
  cooler.csv
  case.csv
requirements.txt
```
