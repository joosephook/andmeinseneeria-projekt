# Sprint 2 — Progress template

Täida see lühike malle iga osaleja kohta enne sprinti lõpetamist.

## Projekt kokku
- Mis on valmis: 
  * töötav, idempotentne andmetoru
  * 1 transformatsioon, mis loob andmed dashboardi jaoks
  * 1 dashboard, mis kinnitab, et andmetoru töötab algusest lõpuni
- Järgmised sammud: 
  * äriküsimuste täpsustamine aitab aru saada, mis küsimustele vastuseid otsime
  * graafikute lisamine täiustab dashboardi ning aitab vastata äriküsimustele
  * vajadusel andmetorus rohkemate andmete sisselugemine, et vastata keerulisematele äriküsimustele
  * vajadusel andmete täiustamine välistest andmetest, kui äriküsimused seda nõuavad
- Mis takistab: 
  * äripoolne nägemus soovib veidi täpsustamist
- Kontrollpunkt (käsk või link, mille juhendaja saab käivitada): 
  * [Kliki mind](https://github.com/joosephook/andmeinseneeria-projekt/tree/docs-document#docker-quickstart)

---

## JH (Joosep Hook)
- Mis on valmis: 
  * andmetoru jookseb dockeris
  * http api apache echartide tegemiseks jookseb dockeris
  * dashboard jookseb dockeris ja on kohalikust masinast kättesaadav
  * pipeline ja api logimine ühte faili
- Järgmised sammud: 
  * andmete rikastamine? 
- Mis takistab: 
  * äripoolne nägemus soovib veidi täpsustamist
  * täpsed äriküsimused aitavad hinnata, kuhu ressurssi edaspidi suunata

- Kontrollpunkt: docker quickstarti läbimisel peaksid nägema oma masinas graafikut nagu `../images/sprint-02-dashboard.png`

---

## AK (Anti Kasuk)
- Mis on valmis: 
  * esialgne töötav andmetoru arhitektuur
  * andmetoru failide sisselugemisest transformatsioonini
  * projekti põhjalik dokumentatsioon
- Järgmised sammud: 
- Mis takistab: 
- Kontrollpunkt: link arhitektuurifailile `docs/ari_arhitektuur/05_relatsiooniline_postgresql_andmemudel.md`

---

## JS (Jaan Soots)
- Mis on valmis: üks graafik (Apache Echart: html, javascript, php)
- Järgmised sammud: teha juurde graafikuid ja aruandeid
- Mis takistab: otseseid takistusi ei ole
- Kontrollpunkt: näidisandmete asukoht `TMP/aruanne/` ja näidisfaili nimi

---

## ST (Sorell Tudelep)
- Mis on valmis: lisasin ingest-faasi andmekvaliteedi kontrollid. Iga sisendrea kohta kontrollitakse registrikoodi, lepingu numbri, võlasumma ja võlapäevade väärtuseid. Kontrollide tulemused salvestatakse tabelisse quality.quality_results staatustega PASSED või FAILED.
- Järgmised sammud: kvaliteedikontrollide laiendamine ja tulemuste sidumine täpsemalt konkreetsete andmeridadega. lisada mart-kihi järelkontrollid, mis kontrollivad `mart.fact_debt_snapshot` ja `mart.kpi_daily_debt` tabelite täitumist.
- Mis takistab: otseseid takistusi ei ole
- Kontrollpunkt: 
    Pipeline käivitamine:
    `docker compose up --build`
  Kontroll, et andmed laaditi stagingusse:
  `docker compose exec postgres psql -U debtuser -d debtdb -c "select count(*) from staging.raw_debt_rows;"`
  Kontroll, et kvaliteedikontrollid käivitusid:
  `docker compose exec postgres psql -U debtuser -d debtdb -c "select status, rule_code, count(*) from quality.quality_results group by status, rule_code order by rule_code, status;"`

---

# Sprint 3 — Projekti lõpetamine

## Periood
- **Alustus:** 01.06.2026
- **Lõpp:** 07.06.2026
- **Tähtaeg:** **Pühapäev 07.06 kell 23:59**

## Eesmärk
Projekt saab esitlusvalmis: kõik andmevood ja transformatsioonid on lõpuni tehtud, andmekvaliteedi testid kirjas, näidikulaud viimistletud, README täidetud ja video salvestatud.

---

## Tegevused

### 1. Andmevood lõpuni viia
- Lisada Sprint 2-st lahtiseks jäänud allikad ja transformatsioonid
- Testida täielikku andmetoru (algusest lõpuni)
- Tagada andmete ajalise muutumise nähtavus

### 2. Andmekvaliteedi testid (vähemalt 3)
- Unikaalsus (distinctness)
- Nullväärtuste kohustuslikkus (not null)
- Väärtuste vahemik (range validation)
- Äriloogika testid
- Tulemused dokumenteerida

### 3. Näidikulaud viimistleda
- Vähemalt 2 äriküsimusele vastavat KPI-d või visuaali
- Andmete ajaline muutumise kuvamine
- Kasutajasõbralik disain

### 4. README täitmine
- Kasutada ut-andmeinseneeria-2026 repos olevat malli
- Kõik sektsioonid peavad täidetud olema
- Eriti tähtis: äriküsimus, arhitektuur, käivitusjuhend, testid

### 5. Video salvestamine
- **Pikkus:** Kuni 10 minutit
- **Vaatajad:** Juhendajad ja teised kursusel osalejad
- **Täpne plaan:** Vt allpool video.md faili

---

## Video.md — Täpne plaan

Loo eraldi fail `docs/video.md` järgmise sisuga:

```markdown
# Sprint 3 Video - Täpne plaan

## Video struktuur (kuni 10 min)

### 1. Probleem ja äriküsimus (1 min)
- Milline äriprobleem lahendatakse?
- Miks on see oluline?
- Mis on äriküsimus(ed)?

### 2. Arhitektuur ja tööriistade valik (2 min)
- Milline andmearhitektuur valiti ja miks?
- Milliseid tööriistasid kasutati?
- Kuidas on struktureeritud andmevoog (staging → mart)?

### 3. Demo: Töövoog ja näidikulaud (3–4 min)
- Kuidas käivitada pipeline (`docker compose up --build`)?
- Mis andmete-lähteid kasutatakse?
- Näita andmekvaliteedi kontrollide tulemusi
- Näita valminud näidikulauda ja selle funktsionaalsust
- Vastused äriküsimustele visualiseeritud andmete kaudu

### 4. Andmekvaliteet ja turve (1–2 min)
- Milised andmekvaliteedi kontrollid on rakendatud?
- Kuidas käsitletakse vigaseid andmeid?
- Kuidas on tagatud andmete turvalisus?

### 5. Õppetunnid ja refleksioon (1 min)
- Mis läks hästi?
- Mida oleks saanud teha paremini?
- Millised on tulevikus parandamise võimalused?

## Video salvestamise vihjed

- **Tarkvara:** Teams, Zoom, Google Meet vms ekraanijagamine
- **Montaaz:** Minimaline montaaz, sisu on tähtsam kui vorm
- **Privaatsus:**
  - Ärge näidake saladusi, isikuandmeid, tööandja konfidentsiaalseid andmeid
  - Näidake koodi struktuuri ja peamisi transformatsioone
  - Kasutage näidiandmeid, mitte pärisandmeid
- **Failiformaat:** MP4 või muud levinud video formaadid

## Video üleslaadimine

- YouTube (unlisted), Google Drive, vms
- Video peab avanema **ilma sisselogimiseta**
- Testige link enne esitamist

## Esitajad video.md-s

- **AK / Anti:** salvestab kogu demo video valmis rakendusest
- **JS / Jaan:** andmed, äriprobleem, dashboard ja KPI-de äriline selgitus on sisendina valmis
- **JH / Joosep:** Git, Docker/Compose, pipeline/API käivitus ja tehniline demo on sisendina valmis
- **ST / Sorell:** testid, andmekvaliteedi kontrollid ja testiraport on sisendina valmis
```

---

## Projekt kokku — Sprint 3 tegevused

| Isik | Tegevus | Kirjeldus |
|------|---------|-----------|
| **JS / Jaan** | Andmed ja dashboard | Äriprobleem, KPI-de äriline selgitus, dashboardi ja aruande tööosa valmis |
| **JH / Joosep** | Git, Docker ja tehniline demo | Docker/Compose, pipeline/API käivitus ja käivitusjuhend valmis |
| **ST / Sorell** | Testid ja raport | Andmekvaliteedi kontrollid, testi raport ja testimise juhend valmis |
| **AK / Anti** | Arhitektuur ja demo video | Arhitektuur, dokumentatsioon ja kogu demo video salvestamine |

---

## Esitamise nõuded (Pühapäev 07.06 kell 23:59)

### Grupitöö — Moodle assignmentis "Projektitöö esitus"
1. **Video link** (YouTube unlisted, Google Drive vms — avaneb ilma sisselogimata)
2. **Repository link**
3. **README** (täies mahus, kõik sektsioonid)

### Individuaalne — Moodle assignmentis "Sprint 3 vahetagasiside (individuaalne)"
- Sama vorm kui igal nädalal
- 3 küsimust
- Umbes 5 minutit
- Nähtav ainult juhendajatele

---

## Hindamise kriteeriumid

Juhendajad hindavad video ja repo põhjal. Tagasiside teiste gruppidele (08.06–14.06) tohib teha samade kriteeriumide alusel:

### 1. **Äriküsimus ja väärtus**
- Kas küsimus on selge ja hästi defineeritud?
- Kas näidikulaud vastab äriküsimustele?
- Kas andmete kaudu saab äriülesandele vastuseid?

### 2. **Andmevoog**
- Kas andmetoru on terviklik (algusest lõpuni)?
- Kas ajas muutuvus on nähtav?
- Kas kõik andmeallikad on integreeritud?

### 3. **Andmekvaliteet**
- Kas testid katavad olulisi probleeme?
- Kas testide tulemused on dokumenteeritud?
- Kas vigased andmed käsitletakse õigesti?

### 4. **Tehniline lahendus**
- Kas tehniline valik on põhjendatud?
- Kas töövoog on korratav (käivitatav)?
- Kas kood on arusaadav ja hästi dokumenteeritud?

### 5. **Selgus ja esitlus**
- Kas video on arusaadav ka väljaspool gruppi olijale?
- Kas README on täielik ja selge?
- Kas demonstratsioon on mugav jälgida?

### 6. **Refleksioon**
- Kas grupp on analüüsinud, mis läks hästi?
- Kas tuvastatud on parandamise võimalused?
- Kas dokumenteeritud puudused on ausalt märgitud?

---

## Hindamiskriteerium: Arvestus
**Arvestus antakse arvestatud/mittearvestatud otsusega.**

Järgmise nädala jooksul (08.06–14.06) peab grupp andma **tagasisidet kahele teisele grupile**, kasutades ülaltoodud kriteeriumeid.

---

## Sprint 3 tegevuste checklist

- [ ] Andmevood lõpuni tehtud
- [ ] Andmekvaliteedi testid dokumenteeritud (vähemalt 3)
- [ ] Näidikulaud valminud (vähemalt 2 KPI/visuaali)
- [ ] README täidetud kõigi sektsioonidega
- [ ] video.md plaan tehtud ja AK salvestusvastutus määratud
- [ ] Video salvestatud ja üleslaaditav link teada
- [ ] Repository link testitud
- [ ] Individuaalne tagasiside Moodles valmis
- [ ] Kõik failid 07.06 kell 23:59 enne Moodles esitatud
