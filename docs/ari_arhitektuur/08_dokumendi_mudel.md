# Dokumendi Mudel

## Eesmärk

Dokumendi eesmärk on kirjeldada SAP-ist saabuvat XLSX sisendfaili, selle välju ja metaandmeid.

## Ulatus

Ulatus hõlmab allikafaili veerge, faili metaandmeid, rea metaandmeid ja toorandmete JSON payloadi säilitamist.

## Põhikirjeldus

SAP salvestab jagatud kataloogi regulaarselt XLSX faili, mis sisaldab võlgnevuste ridu. Fail ei ole staatiline ja andmetoru peab tuvastama uued failid kontrollsumma alusel. Iga failirida loetakse staging kihti koos algse payloadiga, et hiljem oleks võimalik vigasid analüüsida ja vajadusel tagasi jälitada.

## XLSX Väljad

| Väli | Kirjeldus | Tüüp | Kohustuslik |
|---|---|---|---|
| REG kood | ettevõtte registrikood | text | jah |
| Lepingu nr | lepingu number | text | jah |
| Summa | võlasumma | numeric | jah |
| Võlapäevad | võlapäevade arv | integer | sõltub allikast |

## Faili ja aruande reeglid

| Reegel | Kirjeldus |
|---|---|
| Failinimi | Allikas kasutab alati sama faili nime: "LN002 Laenude võlgnevus.xlsx" — erinevad raportikuupäevad peidetakse alamkataloogide või faili metaandmetesse. |
| Raporti kuupäev | Raporti kuupäev leitakse faili metadata'st (`date modified`) ja kirjeldatakse kui metadata kuupäevist lahutatud üks päev (andmeladu töötab päevase hilinemisega). |
| Alamkataloogid | Sarnase nimega failid võivad asuda alamkataloogides (nt `aruanne/2026-01-31/LN002 Laenude võlgnevus.xlsx`). Ingest peab korjama kõik alamkataloogid ja lugema sama nimetusega failid. |

## Metaandmed

| Metaandme väli | Kirjeldus |
|---|---|
| failinimi | SAP ekspordi faili nimi. |
| faili asukoht | Jagatud kataloogi tee. |
| kontrollsumma | Faili sisu põhjal arvutatud kontrollsumma. |
| raportikuupäev | Kuupäev, mille kohta fail andmeseisu kirjeldab. |
| laadimise aeg | Aeg, millal ingest teenus faili töötles. |
| rea number | Rea asukoht algses XLSX failis. |
| algne JSON payload | Rea algne väärtuste komplekt JSON kujul. |

## JSON Näide

```json
{
  "file_name": "sap_debt_2026-05-21.xlsx",
  "file_checksum": "sha256:...",
  "report_date": "2026-05-21",
  "row_number": 42,
  "payload": {
    "registry_code": "12345678",
    "contract_number": "L-2026-0001",
    "debt_amount": 1250.75,
    "debt_days": 30
  }
}
```

## Tehnilised Märkused

Ingest teenus peab säilitama algse payloadi JSONB väljana, sest SAP faili veerunimed või formaat võivad aja jooksul muutuda. Tüübiteisendused ja kvaliteedikontrollid tuleb logida nii, et vigase rea põhjus oleks hiljem leitav.


