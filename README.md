# Feiertage API

Gesetzliche Feiertage in Deutschland und Österreich als öffentliche REST API — komplett in Python mit FastAPI, OpenAPI/Swagger und Docker.

Basierend auf dem Go-Projekt [wlbr/feiertage](https://github.com/wlbr/feiertage) mit identischem Verhalten.

## Features

- Alle gesetzlichen Feiertage aller 16 deutschen und 9 österreichischen Bundesländer
- Bewegliche Feiertage per Gauß-Osterformel (Ostern, Karfreitag, Pfingsten, etc.)
- Spezielle Tage (Advent, Thanksgiving, Sommer-/Winterzeit, etc.)
- **Public API** — keine Authentifizierung, kein API-Key, keine Limits
- **Multi-Format Support**: JSON, XML, CSV, TSV, TXT
- **Swagger UI** (`/docs`) und **ReDoc** (`/redoc`)
- **Web-Frontend** mit Live-API-Testing
- **100% Test Coverage** — 763 Tests, verifiziert gegen Go-Referenz

## Quickstart (Docker)

```bash
# Port in .env konfigurieren (default: 8000)
echo "FEIERTAGE_WEB_PORT=8000" > .env

# Starten
docker compose up -d

# API testen
curl http://localhost:8000/api/region/Bayern?year=2026
curl http://localhost:8000/api/easter?year=2026
```

## Quickstart (Lokal)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API Endpunkte

Alle Endpunkte unterstützen den `?format=` Parameter: `json` (default), `xml`, `csv`, `tsv`, `txt`.

| Methode | Pfad | Beschreibung |
|---------|------|-------------|
| `GET` | `/` | Web-Frontend mit API-Dokumentation |
| `GET` | `/docs` | Swagger UI (interaktiv) |
| `GET` | `/redoc` | ReDoc |
| `GET` | `/openapi.json` | OpenAPI Schema |
| `GET` | `/api/regions?year=2026` | Alle Regionen mit Feiertagen |
| `GET` | `/api/regions?year=2026&country=de` | Nur DE-Regionen |
| `GET` | `/api/regions?year=2026&includeSundays=true` | Inklusive Sonntage |
| `GET` | `/api/region/Bayern?year=2026` | Feiertage einer Region |
| `GET` | `/api/feiertage?year=2026` | Alle Feiertage eines Jahres |
| `GET` | `/api/feiertage?year=2026&region=Berlin` | Nach Region gefiltert |
| `GET` | `/api/feiertage/2026-12-25` | Feiertage an einem Datum |
| `GET` | `/api/isFeiertag?date=2026-11-15&region=Niederösterreich` | Feiertagsstatus mit Geltungsbereich |
| `GET` | `/api/easter?year=2026` | Osterdatum (Gauß) |

> `year` ist optional und fällt auf das aktuelle Jahr zurück. Die JSON-Response-Schemas
> aller Endpunkte sind in Swagger UI und ReDoc dokumentiert.

### Allgemeine und eingeschränkte Feiertage

`GET /api/isFeiertag` unterscheidet zwischen allgemein geltenden gesetzlichen
Feiertagen (`isPublicHoliday`) und Feiertagen, die nur eingeschränkte
Personengruppen betreffen (`isLimitedHoliday`). Bei eingeschränkten Feiertagen
beschreibt `scope` den typischen Geltungsbereich. Die konkrete Anwendbarkeit kann
je nach Schulart oder Dienstrecht abweichen.

```json
{
  "date": "2026-11-15",
  "isPublicHoliday": false,
  "isLimitedHoliday": true,
  "holidays": [
    {
      "name": "Leopolditag",
      "region": "Niederösterreich",
      "regionShort": "NÖ",
      "isPublicHoliday": false,
      "isLimitedHoliday": true,
      "scope": "Primarily pupils and teaching staff at schools in Niederösterreich; applicability may vary by school type. It is not a general work-free day."
    }
  ]
}
```

Als eingeschränkt werden derzeit die in der API enthaltenen österreichischen
Landespatronstage sowie der Kärntner Tag der Volksabstimmung geführt:

- Josefitag: Kärnten, Steiermark, Tirol und Vorarlberg
- Florianitag: Oberösterreich
- Rupertitag: Salzburg
- Tag der Volksabstimmung: Kärnten
- Martinstag: Burgenland
- Leopolditag: Niederösterreich und Wien

Grundlage der Abgrenzung sind insbesondere die abschließende Feiertagsliste in
[§ 7 Arbeitsruhegesetz](https://www.ris.bka.gv.at/NormDokument.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10008541&Paragraf=7)
und die Regelungen zu schulfreien Landespatronstagen im
[Schulzeitgesetz 1985](https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer=10009575).

### Format-Beispiele

```bash
# JSON (default)
curl "http://localhost:8000/api/region/Bayern?year=2026"

# XML
curl "http://localhost:8000/api/region/Bayern?year=2026&format=xml"

# CSV
curl "http://localhost:8000/api/feiertage?year=2026&format=csv"

# TSV
curl "http://localhost:8000/api/feiertage?year=2026&format=tsv"

# Plain Text
curl "http://localhost:8000/api/easter?year=2026&format=txt"
``` |

## Regionen

### Deutschland (16 Bundesländer + Deutschland)
Baden-Württemberg, Bayern, Berlin, Brandenburg, Bremen, Hamburg, Hessen, Mecklenburg-Vorpommern, Niedersachsen, Nordrhein-Westfalen, Rheinland-Pfalz, Saarland, Sachsen, Sachsen-Anhalt, Schleswig-Holstein, Thüringen, Deutschland

### Österreich (9 Bundesländer + Österreich)
Burgenland, Kärnten, Niederösterreich, Oberösterreich, Salzburg, Steiermark, Tirol, Vorarlberg, Wien, Österreich

### Alle
Der Spezialwert `Alle` enthält alle bekannten Feiertage inklusive spezieller Tage.

## Tests

```bash
# Lokal
pytest tests/ -v --cov=app --cov-report=term-missing

# Im Docker Container
docker compose exec feiertage python -m pytest tests/ -v --cov=app
```

**Ergebnis:** 763 Tests, 100% Coverage — alle Werte gegen die Go-Referenzimplementierung verifiziert.

## Konfiguration

Die `.env`-Datei im Projekt-Root wird von Docker Compose gelesen:

```env
FEIERTAGE_WEB_PORT=8000
```

## Projektstruktur

```
feiertage/
├── Dockerfile
├── docker-compose.yml
├── .env
├── requirements.txt
├── pyproject.toml
├── .gitlab-ci.yml
├── app/
│   ├── feiertage.py          # 60+ Feiertagsfunktionen
│   ├── region.py             # Region-Logik (DE + AT)
│   ├── formatter.py          # JSON / XML / CSV / TSV / TXT
│   ├── main.py               # FastAPI App
│   └── static/
│       └── index.html        # Web-Frontend
└── tests/
    ├── test_feiertage.py     # Feiertags-Berechnungen
    ├── test_region.py        # Region-Logik
    ├── test_formatter.py     # Format-Konverter Tests
    ├── test_api.py           # API-Endpunkte
    └── test_go_comparison.py # Go vs. Python Vergleich
```

## Vergleich mit Go-Implementierung

Alle Berechnungen wurden gegen die Go-Referenzimplementierung `wlbr/feiertage` verifiziert:

- **Ostern**: Gauß-Osterformel (erweiterter Algorithmus), getestet für 1954, 1981, 2015, 2016
- **Buß- und Bettag**, **Thanksgiving**, **Advent**, **Muttertag**: Daten identisch zu Go-Tests
- **Feiertagszahlen pro Bundesland**: Alle 37 parametrisierten Testfälle aus `region_test.go` reproduziert
- **Spezialfälle**: Reformationstag 2017, Frauentag Berlin ab 2019, Tag der Befreiung Berlin 2020 etc.

## Lizenz

MIT — siehe Go-Originalprojekt [wlbr/feiertage](https://github.com/wlbr/feiertage)
