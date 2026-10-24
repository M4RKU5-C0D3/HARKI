# Beispielkarten für HARKI

Hier ein paar Vorschläge, um die ARE/ILI-Inzidenzen aus der HARKI-Integration darzustellen.

Ersetze `<name>` durch den Namen, den du bei der Integration gewählt hast (z. B. aus `sensor.<name>_are`).

## Benötigte Custom Cards (optional)

- [ApexCharts Card](https://github.com/RomRider/apexcharts-card) – für Verlauf/Trend
- [Mushroom](https://github.com/piitaya/lovelace-mushroom) – kompakt & modern
- [mini-graph-card](https://github.com/kalkih/mini-graph-card) – schlanker Verlauf

## Dateien

| Datei | Beschreibung |
|---|---|
| `entities-card.yaml` | Einfache Entities-Karte mit aktuellen Werten und Attributen |
| `apexcharts-card.yaml` | ApexCharts mit ARE und ILI für den aktuellen Stand (basiert auf Attributen) |
| `mushroom-cards.yaml` | Kompakte Mushroom-Chips/Entities für Dashboard |
| `markdown-card.yaml` | Kurzübersicht für Header/Info-Karten |
