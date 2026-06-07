# Andmestik

## Asukoht

Andmestik asub failis:

```text
docs/aruanne.zip
```

## Failide Paiknemine

Reaalses elus tuleb ühe ja sama nimetusega andmefail iga päev ühte kindlasse kausta ehk kirjutatakse üle.

Sellise olukorra simuleerimiseks tekitasin kataloogi `aruanne` sisse alamkataloogid, näiteks `2025-12-31` jne. Alamkataloogi nimi võib olla ka suvaline.

Kood peab toimima nii, et võtab kataloogist `aruanne` kõik olemasolevad alamkataloogid ja loeb sama nimetusega failide sisu baasi.

Faili nimi on alati:

```text
LN002 Laenude võlgnevus.xlsx
```

## Aruande Kuupäev

Aruande kuupäev saadakse faili metadatast: `date modified`.

Sellest lahutatakse üks päev, sest andmeladu toimetab päevase hilinemisega.

## Näidisfailid

Projektitöös on kokku 5 algfaili.

| Aruande kuupäev |
|---|
| 31.12.2025 |
| 31.01.2026 |
| 28.02.2026 |
| 31.03.2026 |
| 30.04.2026 |

Nendes näidisfailides on väli `date modified` käsitsi üle kirjutatud nende kuupäevade järgi pluss üks lisapäev ehk siis järgmise kuu esimene kuupäev, simuleerimaks tegelikku olukorda.

## Võlapäevad

Osadel summadel ei ole algfailis märgitud võlapäevi.

Nende summade tähtaeg on aruande kuupäev ehk võlga veel tekkinud ei ole ja need võib kõrvale jätta.
