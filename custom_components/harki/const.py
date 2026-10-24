DOMAIN = "harki"

CONF_NAME = "name"
CONF_AGE_GROUP = "age_group"
CONF_REGION = "region"

DEFAULT_NAME = "RKI GrippeWeb"
DEFAULT_AGE_GROUP = "00+"
DEFAULT_REGION = "Bundesweit"

SCAN_INTERVAL_SECONDS = 86400  # daily

DATA_URL = "https://raw.githubusercontent.com/robert-koch-institut/GrippeWeb_Daten_des_Wochenberichts/main/GrippeWeb_Daten_des_Wochenberichts.tsv"

AGE_GROUPS = ["0-4", "5-14", "15-34", "35-59", "60+", "0-14", "15+", "00+"]

# GrippeWeb Wochenbericht: nur Großregionen + Bundesweit (keine einzelnen Bundesländer in den Rohdaten)
REGIONS = ["Bundesweit", "Sueden", "Mitte (West)", "Norden (West)", "Osten"]
REGION_LABELS = {
    "Bundesweit": "Bundesweit",
    "Sueden": "Süden",
    "Mitte (West)": "Mitte (West)",
    "Norden (West)": "Norden (West)",
    "Osten": "Osten",
}
