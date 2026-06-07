# Docker: käskude ja kontrollide juhend

See dokument kogub kokku levinumad Docker/Compose käsud ja kirjeldab, kuidas kontrollida, et hosti pordid ei konfliktiks kohaliku "live" keskkonnaga enne teenuste ülesvõtmist.

## Kopeeri näidiskonfiguratsioon

```powershell
cp .env.example .env
# muuda .env vastavalt oma keskkonnale
```

## Ehita ja käivita

```powershell
docker compose up --build
```

## Logid ja haldus

Vaata logisid (kõik teenused):

```powershell
docker compose logs -f
```

Peata ja eemalda konteinerid ning võrgud:

```powershell
docker compose down
```

Peata ja eemalda konteinerid koos püsimahtudega:

```powershell
docker compose down -v --remove-orphans
```

Ehitamine ja taaskäivitamine ühele teenusele:

```powershell
docker compose build api
docker compose up api
```

## Pipeline käsitsi käivitamine

Automaatselt käivitub pipeline `pipeline` teenuses scheduleriga. Ühekordseks käsitsi käivitamiseks kasuta `trigger_pipeline` teenust:

```powershell

```

## Portide konflikti kontroll — oluline enne `up`

Praegune `compose.yml` kasutab `network_mode: host`, seega konteinerid kasutavad otse hosti porte. Enne `docker compose up` käivitamist tasub kontrollida, et vajalikud pordid ei oleks juba lokaalse PostgreSQL-i, Flaski või mõne muu teenuse poolt kasutuses.

Projektis ei ole enam eraldi portide kontrolli skripte. Need skriptid olid varasemas versioonis olemas, kuid eemaldati kasutuseta failidena. Kontroll tuleb teha käsitsi või operatsioonisüsteemi enda tööriistadega.

Selle projekti puhul on olulised pordid:

| Port | Kasutus |
|---|---|
| `5432` | PostgreSQL |
| `5000` | Flask dashboard API ja veebiliides |

Windows PowerShell:

```powershell
Get-NetTCPConnection -LocalPort 5432,5000 -ErrorAction SilentlyContinue
```

Kui käsk tagastab ridu, on vähemalt üks port juba kasutuses. Sel juhul peata vastav lokaalne teenus või muuda Compose/API konfiguratsiooni.

Alternatiivne kontroll Windowsis:

```powershell
netstat -ano | findstr ":5432"
netstat -ano | findstr ":5000"
```

Linux/macOS:

```bash
lsof -i :5432
lsof -i :5000
```

Kui port on vaba, ei väljasta need käsud tavaliselt midagi.

### Pre-start wrapperid

Projektis ei ole praegu `scripts/prestart.sh` ega `scripts/prestart.ps1` faile. Käivitus toimub otse Compose käsuga:

```powershell
docker compose up --build
```

Pipeline'i saab käsitsi uuesti käivitada:

```powershell
docker compose run --rm trigger_pipeline
```

Kui portide konflikt tekib, on tüüpilised sümptomid:

- PostgreSQL konteiner ei saa käivituda või healthcheck ebaõnnestub.
- Flask API ei avane aadressil `http://localhost:5000/dashboard`.
- Logides on teade stiilis `address already in use`.

Sellisel juhul kontrolli pordid üle, peata konflikti põhjustav protsess ning käivita Compose uuesti.

## Korduma kippuvad juhud

- Kui `.env` muutmise järel on vaja uuesti ehitada: `docker compose build --no-cache`.
- Kui püsimahtud (volumes) segavad testimist, tee need eemaldamiseks:

```powershell
docker volume ls
docker volume rm <name>
```

---
