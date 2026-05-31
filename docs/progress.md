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
