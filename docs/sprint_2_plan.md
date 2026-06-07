# Sprint 2 — Plaan ja ülesanded (25.05–31.05)

Eesmärk: 31.05 lõpuks toimiv minimaalne andmevoog — üks allikas → ingest → transform → üks visuaal.

Lühikokkuvõte projekti seisust (mis on juba tehtud)

- SQL initskript ja skeemid olemas: `sql/init_schema.sql` (skeemid `staging`, `quality`, `mart`, `logs`).
- Ingest ja transform teenuste alged olemas `services/ingest` ja `services/transform` (pandas, openpyxl, psycopg2).
- Scheduler ja cron wrapper on lisatud `services/scheduler` ning `docker-compose.example.yml` sisaldab `scheduler` teenust.
- Pre-start ja portikontrolli skriptid lisatud: `scripts/check_free_ports.py`, `scripts/check_ports.ps1`, `scripts/prestart.sh`, `scripts/prestart.ps1`.
- Dokumentatsioon: `docs/docker.md` ja arhitektuurifail `docs/ari_arhitektuur/05_relatsiooniline_postgresql_andmemudel.md` ajakohastatud (viimane skripti käivituse timestamp).

Peamised riskid / puudujäägid (mida tuleb lõpetada)

- Idempotentsus: ingest peab vältima topelt-laadimist (kontroll checksum/unique constraint + käsitletud tõrked).
- Quality tracking: puudub täielik reeglistik ja salvestus `quality.quality_results` kasutamiseks.
- Transform: upsert dimensiionid, fact snapshot ja KPI arvutused vajavad lõplikku testimist ja koodikõlbmakst.
- Visualiseerimine: lihtne KPI/graafik pole reposse lõplikult lisatud (notebook või lihtne HTML/dashboard).
- E2E testimine: käsud + CI / käivituswrapperid tuleb reaalsetel andmetel proovida.

Osalejate põhijagunemine (uuendatud)

- JS / Jaan — Andmed, äriprobleem, dashboard ja KPI-de äriline selgitus
  - Toob ja kinnitab näidisandmed, kirjeldab KPI ärireeglid ning valideerib dashboardi ärilise õigsuse.

- JH / Joosep — Git, Docker/Compose, pipeline/API käivitus ja tehniline demo
  - Hoolitseb Compose käivituse, pipeline/API töökindluse, lokaalse E2E testi ja tehnilise demo eest.

- ST / Sorell — Testid, andmekvaliteedi kontrollid ja testiraport
  - Koostab ja viib läbi testid andmete kvaliteedi, transformatsiooni ja KPI õiguse kontrolliks.
  - Vastutab `quality.quality_results` reeglite, testiraporti ja testimise juhendi eest.

- AK / Anti — Arhitektuur, dokumentatsioon ja demo video salvestamine
  - Vastutab arhitektuuridokumentide, dokumentatsiooni terviklikkuse ja valmis rakenduse demo video salvestamise eest.

Konkreetne ülesannete jaotus (prioriteetsus koos eeldatava töömahu ja omanikuga)


- Kõrge prioriteet:
  - [JH] Käivita pre-start ja `docker compose up` lokaalselt; fikseeri kõik mount/permission probleemid (2–4h).
  - [JS] Pane repo `TMP/aruanne` näidisfailidega (1h). Lisa README reeglid failinime ja modtime→report_date määramiseks (0.5h).
  - [JH] Testi ingest skripti ühe näidisfailiga, kinnita et read sisestatakse `staging.raw_debt_rows` (2–4h).


- Keskmine prioriteet (nv):
  - [JH] Implement idempotent insert: enne uue faili importi kontroll checksum; lükka tagasi või märgi `ingested_files.status` (2–4h).
  - [JH] Koosta lihtne `start.sh` wrapper, mis kutsub `prestart` sobival platvormil (1h).
  - [ST] Koosta prototüüpvisual (notebook) kasutades testandmeid (2–4h).


- Madalam prioriteet (viimane päev/steal-time):
  - [ST] Lisa `quality.quality_results` reeglid ja insert, kui rida ei vasta formaadile (2–6h).
  - [Kõik] Kirjuta `docs/progress.md` koos valmis/osaline/takistab kirjetega ja linkidega (1h).

Kontrollpunktid & verifitseerimine (kuidas juhendaja kontrollib sprinti edukust)

- E2E kontroll (väike checklist):
  1. Pre-start portikontroll: `./scripts/prestart.sh -f docker-compose.example.yml` (või Windowsi ekvivalent).
  2. Käivita scheduler või käsitsi: `docker compose exec scheduler /app/scripts/run_pipeline.sh`.
  3. Kontrolli, et `staging.ingested_files` on rida failiga ja `staging.raw_debt_rows` sisaldab read.
     - Näide psql päringust (Postgres konteineris):

```powershell
docker compose -f docker-compose.example.yml exec postgres bash -lc "psql -U $POSTGRES_USER -d $POSTGRES_DB -c 'select count(*) from staging.raw_debt_rows;'"
```

  4. Kontrolli, et `mart.fact_debt_snapshot` sisaldab snapshot ridu ja `mart.kpi_daily_debt` on arvutatud.
  5. Avage visuaal (notebook HTML/visual) ja näidake KPI-d või graafikut.

Tähtaegade jaotus (kiire ajakava — 31.05 eesmärk)

- 27.05 (täna): andmete kogumine (`JS`), käivitus- ja portikontroll (`AK`), esimene ingest test (`JH`).
- 28.05: idempotentsuse ja ingest parandused (`JH` + `AK`), näidisvisuali prototüüp algus (`ST`).
- 29.05: transform ja mart täiendamine (`JH`), KPI arvutused valmis, smoke tests (`Kõik`).
- 30.05: visual valmis ja integreeritud (`ST`), docs/progress.md ja esitluse märkmik (`Kõik`).
- 31.05: lõplik test, vea korrektsioonid, push ja Moodle esitus (kell 23:59) (`Kõik`).

Deliverables (mis commitida ja esitada Moodle'ile)

- `docs/progress.md` — lühike ja aus seis (mis valmis, järgmised sammud, takistused) + link repo kohta (1 para).
- Töökorras pipeline repo rootis: `docker-compose.example.yml`, `sql/init_schema.sql`, `services/ingest`, `services/transform`, `services/scheduler`, `scripts/prestart.*`.
- Visual/output faili link või notebook (`notebooks/` või `services/visualize/`), et juhendaja saaks KPI näha.

Kiired käsud kontrolliks ja arenduseks

```powershell
# Kopeeri .env näidis
cp .env.example .env

# Kontrolli porte (Windows PowerShell)
.\scripts\check_ports.ps1 -ComposeFile docker-compose.example.yml

# või Linux/macOS
python scripts/check_free_ports.py --compose-file docker-compose.example.yml

# Käivita pre-start (ehitamise ja käivitamise wrapper)
./scripts/prestart.sh -f docker-compose.example.yml

# Käivita pipeline käsitsi scheduler konteineris (test)
docker compose -f docker-compose.example.yml exec scheduler /app/scripts/run_pipeline.sh

# Kontrolli ridade arvu staging'is
docker compose -f docker-compose.example.yml exec postgres bash -lc "psql -U $POSTGRES_USER -d $POSTGRES_DB -c 'select count(*) from staging.raw_debt_rows;'"
```

Riskid & lihtsad leevendusmeetmed

- Kui Docker mount või permissions vigane → testida `prestart` ja parandab compose volüümi parameetrid.
- Kui transform ei toimi andmetega → lülita sisse mitmed failivariandid ja logi iga samm (ingest → transform → mart) ning dokumenteeri vead `docs/progress.md`.


