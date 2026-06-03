# Kreator zestawu komputerowego 💻

Aplikacja w **Streamlit**, która na podstawie kilku pytań proponuje kompletny,
kompatybilny zestaw komputerowy dopasowany do budżetu i przeznaczenia.

## Pomysł

Użytkownik w panelu bocznym podaje:

- **przeznaczenie** komputera (gry, biuro i dom, grafika/montaż wideo, programowanie),
- **budżet** (zł),
- preferowanego **producenta procesora** (dowolny / AMD / Intel),
- minimalną ilość **RAM**,
- minimalną **pojemność dysku SSD**.

Aplikacja dobiera procesor, płytę główną, RAM, kartę graficzną, dysk, zasilacz,
obudowę i chłodzenie tak, aby:

- zmieścić się w budżecie,
- zachować **kompatybilność** (gniazdo procesora = gniazdo płyty głównej),
- dobrać **zasilacz** o mocy pokrywającej pobór prądu (z zapasem 30%),
- maksymalnie wykorzystać budżet, podbijając wydajność tam, gdzie to się najbardziej opłaca.

Na koniec pokazuje listę podzespołów, koszt, ocenę wydajności, szacowany pobór mocy
oraz wykresy podziału kosztów.

## Skąd dane?

Nie trzeba pobierać żadnej bazy z internetu — podzespoły i ceny (przykładowe,
edukacyjne) znajdują się w pliku [`data/components.csv`](data/components.csv).
Możesz go swobodnie edytować: dopisać własne podzespoły, zmienić ceny czy parametry.

Kolumny w pliku CSV:

| kolumna | opis |
|---|---|
| `category` | kategoria: CPU, Motherboard, RAM, GPU, SSD, HDD, PSU, Case, Cooler |
| `name`, `brand`, `price` | nazwa, marka, cena w zł |
| `perf_gaming` / `perf_office` / `perf_content` | wydajność (0–100) w grach / biurze / pracy graficznej |
| `socket` | gniazdo (dla CPU i płyt głównych) |
| `capacity_gb` | pojemność (RAM, dyski) |
| `wattage` | moc zasilacza |
| `power_draw` | pobór mocy podzespołu |
| `notes` | krótki opis |

## Uruchomienie

```bash
pip install -r requirements.txt
streamlit run app.py
```

Aplikacja otworzy się w przeglądarce (domyślnie `http://localhost:8501`).
