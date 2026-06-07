# Sprint 3 Video — Täpne plaan

## Video struktuur (kuni 10 min)

Video salvestab AK. Teised osapooled on oma tööosad projekti käigus valmis teinud; videos näidatakse valmis rakendust, dokumentatsiooni ja demo tulemusi.

### 1. Probleem ja äriküsimus (1 min)
- Milline äriprobleem lahendatakse?
- Miks on see oluline?
- Mis on äriküsimus(ed)?

### 2. Arhitektuur ja tööriistade valik (2 min)
- Milline andmearhitektuur valiti ja miks?
- Milliseid tööriistasid kasutati?
- Kuidas on struktureeritud andmevoog (staging → mart)?
- Näita relatsioonilise mudeli ERD joonist ja DDL vastavust `sql/init_schema.sql` failile

### 3. Demo: Töövoog ja näidikulaud (3–4 min)
- Kuidas käivitada pipeline (`docker compose up --build`)?
- Mis andmete-lähteid kasutatakse (`docs/aruanne.zip`, 5 näidisfaili)?
- Näita andmekvaliteedi kontrollide tulemusi
- Näita valminud näidikulauda ja selle funktsionaalsust
- Vastused äriküsimustele visualiseeritud andmete kaudu

### 4. Andmekvaliteet ja turve (1–2 min)
- Millised andmekvaliteedi kontrollid on rakendatud?
- Kuidas käsitletakse vigaseid andmeid?
- Kuidas on tagatud andmete turvalisus?

### 5. Õppetunnid ja refleksioon (1 min)
- Mis läks hästi?
- Mida oleks saanud teha paremini?
- Millised on tulevikus parandamise võimalused?

---

## Video salvestamise vihjed

### Tarkvara
- Teams, Zoom, Google Meet vms ekraanijagamine
- Võite kasutada ka OBS Studio, ScreenFlow (Mac) või muid ekraanijagamise tööriistu

### Montaaz
- Minimaline montaaz, sisu on tähtsam kui vorm
- Põhjalikku video monteerimist pole kindlasti tarvis teha

### Privaatsus
- **Ärge näidake:** saladusi, isikuandmeid, tööandja konfidentsiaalseid andmeid
- **Näidake:** koodi struktuuri, peamisi transformatsioone, andmekvaliteedi teste
- **Kasutage:** näidiandmeid, mitte pärisandmeid

### Failiformaat
- MP4 või muud levinud video formaadid (WebM, MOV jne)
- Soovitav bitrate: 1000–2500 kbps

---

## Video üleslaadimine

### Veebikeskkond
- YouTube (unlisted link)
- Google Drive
- Vimeo
- Dropbox
- Muu avalik video jagamise teenus

### Tähtis
- **Video peab avanema ilma sisselogimiseta**
- **Testige link enne esitamist**
- Veenduge, et link töötab ja video laeb

---

## Video Salvestamine

| Vastutus | Täitja | Märkus |
|---|---|---|
| Demo video salvestamine | AK / Anti | AK salvestab kogu video ja näitab valmis rakendust. |
| Valmis tööde näitamine | AK / Anti | Videos viidatakse andmetele, dashboardile, pipeline'ile, testidele ja arhitektuurile kui valminud tööosadele. |

---

## Head Praktikad

### Enne salvestamist
- [ ] Testida, et kõik näidised/näited töötavad
- [ ] Harjutada, mis saab ütluseks
- [ ] Reguleerida helikvaliteeti
- [ ] Kontrollida valgustust ja ekraani nähtavust

### Salvestamise ajal
- [ ] Rääkida selgelt ja aeg-ajalt teha lühike paus
- [ ] Kuvada relevantseid vaateid (dashboard, terminali väljund jne)
- [ ] Parandada ilmsed vead ümbersalvestamisega
- [ ] Säilitada loogiline järjekord

### Pärast salvestamist
- [ ] Kontrollida salvestatud videot
- [ ] Üleslaadimine veebikeskkonda
- [ ] Linki jagamine grupikaustale
- [ ] Finaalse lingi kontrollimine

---

## Näited, mida näidata demos

```bash
# 1. Pipeline käivitamine
docker compose up --build

# 1a. Pipeline käsitsi uuesti käivitamine
docker compose run --rm trigger_pipeline

# 2. Andmete kontrollimine
docker compose exec postgres psql -U debtuser -d debtdb -c \
  "SELECT COUNT(*) as total_rows FROM staging.raw_debt_rows;"

# 3. Andmekvaliteedi kontrollid
docker compose exec postgres psql -U debtuser -d debtdb -c \
  "SELECT status, rule_code, COUNT(*) as count 
   FROM quality.quality_results 
   GROUP BY status, rule_code 
   ORDER BY rule_code, status;"

# 4. Mart-kihi andmed
docker compose exec postgres psql -U debtuser -d debtdb -c \
  "SELECT * FROM mart.kpi_daily_debt LIMIT 10;"

# 5. Dashboard käivitamine
# Näita http://localhost:5000/dashboard
```

---

## Valmistuse ajaskala

- **04.06 (E):** Video plaan ja AK salvestusvastutus määratud
- **05.06 (K):** Esimene harjutus/proovisalvestus
- **06.06 (N):** Video finaliseerimine pärast kontrolle
- **07.06 (P) kuni 23:59:** Video link esitatud Moodles
