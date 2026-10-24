# Home Assistant RKI Integration (HARKI)

[![HACS Custom Repository](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/M4RKU5-C0D3/HARKI)
[![GitHub release](https://img.shields.io/github/v/release/M4RKU5-C0D3/HARKI?style=for-the-badge)](https://github.com/M4RKU5-C0D3/HARKI/releases)

Home Assistant custom component that exposes weekly GrippeWeb influenza-like illness (ILI) and acute respiratory infection (ARE) incidence data from the Robert Koch-Institut (RKI).

## Installation

### Via HACS (recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=M4RKU5-C0D3&repository=HARKI&category=integration)

1. In HACS go to **HACS → ⋮ → Custom repositories**
2. Add the repository URL `https://github.com/M4RKU5-C0D3/HARKI` with category **Integration**
3. Click **Download** on "Home Assistant RKI"
4. Restart Home Assistant
5. Go to **Settings → Devices & Services → Add Integration** → search **"Home Assistant RKI"** and choose name, age group and region/grossregion

### Manually

1. Copy the `custom_components/harki/` directory into your HA `config/custom_components/harki/`
2. Restart Home Assistant
3. Go to **Settings → Devices & Services → Add Integration** → search **"Home Assistant RKI"**

## Provided entities

All entities belong to one device and update daily (polling, `iot_class: cloud_polling`).

| Entity | Type | State | Purpose |
|---|---|---|---|
| `sensor.<name>_are` | Sensor | Incidence per 100.000 | Acute respiratory infections (ARE) |
| `sensor.<name>_ili` | Sensor | Incidence per 100.000 | Influenza-like illness (ILI) |

### Sensor attributes

| Key | Description |
|---|---|
| `calendar_week` | RKI calendar week (YYYY-WXX) |
| `season` | Influenza season (e.g. `2025/26`) |
| `age_group` | Age group (default: `00+` all ages) |
| `region` | Selected region/grossregion (`Bundesweit`, `Sueden`, `Mitte (West)`, `Norden (West)`, `Osten`) |
| `meldungen` | Number of reports used for calculation |
| `source` | Data source URL |
| `last_updated` | Timestamp of last data fetch (via coordinator) |

## Available regions

The GrippeWeb weekly report provides data for:

- `Bundesweit` (Germany overall)
- `Sueden`
- `Mitte (West)`
- `Norden (West)`
- `Osten`

Individual German federal states are **not** included in the published TSV.

## Examples

See [`examples/`](examples/) for ready-to-use Lovelace YAML cards.

## Data source

- [GrippeWeb_Daten_des_Wochenberichts](https://github.com/robert-koch-institut/GrippeWeb_Daten_des_Wochenberichts) (raw TSV via GitHub raw content)

Data is published weekly (Fridays) by the RKI. The integration polls daily and caches results.

**Data license:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (see LICENSE/LIZENZ in upstream repo). Robert Koch-Institut (RKI), [GrippeWeb - Daten des Wochenberichts](https://doi.org/10.5281/zenodo.23555842).

## Vibe coding

This project was built with AI assistance via [opencode](https://opencode.ai) using the model `big-pickle`. All code was reviewed and released by a human maintainer.
