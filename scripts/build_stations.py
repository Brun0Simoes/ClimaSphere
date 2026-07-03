"""Gera data/stations.json a partir do catálogo público da NOAA (ISD history).

Fonte real e gratuita: https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv
Mantém o mesmo formato do endpoint /api/stations do ClimWeb, para o painel
consumir o snapshot de forma transparente quando o servidor não está acessível.
Executado diariamente pelo GitHub Actions (ver .github/workflows/refresh-stations.yml).
"""
import csv
import io
import json
import urllib.request
from datetime import datetime, timezone

URL = "https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv"
OUT = "data/stations.json"
LIMIT = 800
MIN_END_YEAR = datetime.now(timezone.utc).year - 1  # ativa recentemente


def main():
    raw = urllib.request.urlopen(URL, timeout=120).read().decode("utf-8", "replace")
    rows = list(csv.DictReader(io.StringIO(raw)))
    stations = []
    for d in rows:
        try:
            lat = float(d.get("LAT") or "nan")
            lon = float(d.get("LON") or "nan")
        except ValueError:
            continue
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            continue
        if abs(lat) < 0.02 and abs(lon) < 0.02:
            continue
        end = (d.get("END") or "")[:4]
        if not (end.isdigit() and int(end) >= MIN_END_YEAR):
            continue  # somente estações reportando recentemente (operacionais)
        name = (d.get("STATION NAME") or "").strip() or (d.get("ICAO") or "").strip()
        if not name:
            continue
        sid = (d.get("ICAO") or "").strip() or f"{d.get('USAF','')}-{d.get('WBAN','')}"
        try:
            elev = float(d.get("ELEV(M)") or 0)
        except ValueError:
            elev = 0.0
        stations.append({
            "id": sid,
            "name": name.title()[:120],
            "wigos_id": sid,
            "operating_status": "Operational",
            "station_type": "Land (fixed)",
            "elevation": elev,
            "lon": round(lon, 4),
            "lat": round(lat, 4),
        })
        if len(stations) >= LIMIT:
            break

    payload = {
        "stations": stations,
        "count": len(stations),
        "source": "NOAA ISD (snapshot diário via GitHub Actions)",
        "updated": datetime.now(timezone.utc).isoformat(),
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False)
    print(f"ok: {len(stations)} estações -> {OUT}")


if __name__ == "__main__":
    main()
