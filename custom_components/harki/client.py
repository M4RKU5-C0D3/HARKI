from __future__ import annotations

import csv
import logging
from typing import Any

try:
    from aiohttp import ClientSession
except ImportError:  # pragma: no cover
    ClientSession = None  # type: ignore[assignment,misc]

_LOGGER = logging.getLogger(__name__)

from .const import DATA_URL, DEFAULT_AGE_GROUP, DEFAULT_REGION


class HarkiError(Exception):
    pass


class HarkiClient:
    def __init__(self, session: ClientSession):
        self._session = session
        self._cache: dict[str, Any] | None = None

    async def get_data(
        self,
        age_group: str = DEFAULT_AGE_GROUP,
        region: str = DEFAULT_REGION,
    ) -> dict[str, Any]:
        if self._cache is None:
            self._cache = await self._fetch()

        data = self._cache
        result = {}

        for disease in ("ARE", "ILI"):
            key = (disease, age_group, region)
            row = data.get(key)
            if not row:
                raise HarkiError(f"No data for {disease} {age_group} {region}")
            result[disease.lower()] = {
                "value": float(row["Inzidenz"]),
                "meldungen": int(row["Meldungen"]) if row["Meldungen"] else None,
                "saison": row["Saison"],
                "erkrankung": row["Erkrankung"],
                "altersgruppe": row["Altersgruppe"],
                "region": row["Region"],
                "kalenderwoche": row["Kalenderwoche"],
            }

        return result

    async def _fetch(self) -> dict[tuple[str, str, str], dict[str, str]]:
        headers = {"User-Agent": "HomeAssistant-HARKI/1.0"}
        resp = await self._session.get(DATA_URL, headers=headers)
        if resp.status != 200:
            raise HarkiError(f"HTTP {resp.status}")

        text = await resp.text()
        reader = csv.DictReader(text.splitlines(), delimiter="\t")
        data: dict[tuple[str, str, str], dict[str, str]] = {}

        for row in reader:
            disease = row["Erkrankung"].strip()
            age_group = row["Altersgruppe"].strip()
            region = row["Region"].strip()
            cw = row["Kalenderwoche"].strip()
            # keep latest entry per (disease, age_group, region) - file goes forward in time
            key = (disease, age_group, region)
            data[key] = row
            data[f"{disease}_{age_group}_{region}_latest"] = row  # ensure we can get latest

        if not data:
            raise HarkiError("Empty dataset")

        # return all rows indexed by key - we'll pick latest by parsing CW
        # build index of latest per key
        latest: dict[tuple[str, str, str], dict[str, str]] = {}
        for row in reader if False else []:  # dummy
            pass

        # re-parse to find latest
        # easier: parse again
        latest = {}
        for row in csv.DictReader(text.splitlines(), delimiter="\t"):
            disease = row["Erkrankung"].strip()
            age_group = row["Altersgruppe"].strip()
            region = row["Region"].strip()
            key = (disease, age_group, region)
            if key not in latest:
                latest[key] = row
            else:
                # compare calendar week like 2025-W10
                cur = row["Kalenderwoche"].strip()
                prev = latest[key]["Kalenderwoche"].strip()
                if cur > prev:
                    latest[key] = row

        return latest
