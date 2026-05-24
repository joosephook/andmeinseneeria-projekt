# Docker: käskude ja kontrollide juhend

See dokument kogub kokku levinumad Docker/Compose käsud ja kirjeldab, kuidas kontrollida, et hosti pordid ei konfliktiks kohaliku "live" keskkonnaga enne teenuste ülesvõtmist.

## Kopeeri näidiskonfiguratsioon

```powershell
cp .env.example .env
# muuda .env vastavalt oma keskkonnale
```

## Ehita ja käivita

```powershell
docker compose -f docker-compose.example.yml up --build -d
```

## Logid ja haldus

Vaata logisid (kõik teenused):

```powershell
docker compose -f docker-compose.example.yml logs -f
```

Peata ja eemalda konteinerid ning võrgud:

```powershell
docker compose -f docker-compose.example.yml down
```

Ehitamine ja taaskäivitamine ühele teenusele:

```powershell
docker compose -f docker-compose.example.yml build ingest
docker compose -f docker-compose.example.yml up -d ingest
```

## Pipeline käsitsi käivitamine (scheduler)

```powershell
docker compose -f docker-compose.example.yml exec scheduler /app/scripts/run_pipeline.sh
```

## Portide konflikti kontroll — oluline enne `up`

Et vältida olukorda, kus lokaalsete teenuste (nt PostgreSQL, HTTP/HTTPS) portid on juba kasutuses ja põhjustavad konflikte Dockeri käivitamisel, käivita kontroll enne `docker compose up`.

Projekt sisaldab skripti, mis kontrollib hosti pordikasutust ja tagastab mittetühise väljundi (exit code != 0) kui leidub hõivatud porte.


Näited:

```bash
# Parim praktika: kontrolli compose faili hosti porte (Linux/macOS)
python scripts/check_free_ports.py --compose-file docker-compose.example.yml

# või kontrolli konkreetseid porte
python scripts/check_free_ports.py --ports 5432,80,443
```

Windows PowerShell wrapper:

```powershell
.\scripts\check_ports.ps1 -ComposeFile docker-compose.example.yml
```

Kui skript leiab hõivatud pordi, annab see nimekirja kasutajatest portidest ja väljub koodiga `1`. See võimaldab enne `docker compose up` lisada lihtsa kontrolli skripti või CI-sammuna.

### Pre-start wrapperid

Projekt sisaldab mugavaid pre-start skripte, mis käivitavad portikontrolli ja ainult siis sooritavad `docker compose up`.

Linux / macOS (bash):

```bash
./scripts/prestart.sh -f docker-compose.example.yml
```

Windows PowerShell:

```powershell
.\scripts\prestart.ps1 -ComposeFile docker-compose.example.yml
```

Need skriptid tagavad, et hostis olevad teenused ei blokeeri Compose poolt määratud hosti porte. Kui port on hõivatud, siis skript abortib ja väljastab kasutatavad portid.

## Korduma kippuvad juhud

- Kui `.env` muutmise järel on vaja uuesti ehitada: `docker compose build --no-cache`.
- Kui püsimahtud (volumes) segavad testimist, tee need eemaldamiseks:

```powershell
docker volume ls
docker volume rm <name>
```

---

Kui soovid, lisan `pre-start` skripti, mis käivitab `check_free_ports.py` automaatselt enne `docker compose up` ja abortib, kui leidub konflikte.
