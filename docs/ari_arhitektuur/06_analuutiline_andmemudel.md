# Analüütiline Andmemudel

## Eesmärk

Dokumendi eesmärk on kirjeldada, millised mart kihi tabelid ja vaated toetavad dashboardi, trendianalüüsi ja tulevast ML laiendust.

## Ulatus

Ulatus hõlmab päevaseid võlgnevuste snapshot'e, KPI arvutusi, kvaliteedivigade koondamist, filtreid ning ML sisendtunnuste võimalikku lisamist.

## Põhikirjeldus

Analüütiline mudel tugineb tabelile `mart.fact_debt_snapshot`, mille granulaarsus on üks rida ühe lepingu ühe raportikuupäeva kohta. Dashboard loeb otse `mart.kpi_daily_debt` tabelist või selle aluseks olevatest vaadetest. Täiendavad vaated võivad koondada kvaliteedivigu failiti ja kuvada viimase faili laadimise staatust.

## Analüütilised Väljundid

| Väljund | Allikas | Kasutus |
|---|---|---|
| Päevane võlasumma | `mart.fact_debt_snapshot` | Võlasumma trend dashboardil. |
| Päevane kaalutud keskmine võlapäevade arv | `mart.fact_debt_snapshot` | Võlapäevade trendi hindamine. |
| Maksimaalne võlapäevade arv | `mart.fact_debt_snapshot` | Kriitilise viivituse leidmine. |
| Võlas olevate lepingute arv | `mart.fact_debt_snapshot` | Portfelli ulatuse hindamine. |
| Ettevõtete arv võlas | `mart.fact_debt_snapshot`, `mart.dim_company` | Mõjutatud klientide arv. |
| Kvaliteedivigade arv failiti | `quality.quality_results` | Laadimiskvaliteedi jälgimine. |
| Viimase faili laadimise staatus | `staging.ingested_files`, `logs.pipeline_runs` | Operatiivne kontroll dashboardil. |

## Näidis SQL

```sql
SELECT
    snapshot_date,
    SUM(debt_amount) AS total_debt_amount,
    -- weighted average only over rows with debt_days > 0
    SUM(CASE WHEN debt_days > 0 THEN debt_days * debt_amount ELSE 0 END)
        / NULLIF(SUM(CASE WHEN debt_days > 0 THEN debt_amount ELSE 0 END), 0)
        AS weighted_avg_debt_days,
    MAX(debt_days) AS max_debt_days,
    COUNT(DISTINCT CASE WHEN debt_days > 0 THEN contract_key END) AS debt_contract_count
FROM mart.fact_debt_snapshot
GROUP BY snapshot_date;
```

## Trendide Arvutus

Trendide arvutamiseks võrreldakse sama KPI väärtust järjestikustel raportikuupäevadel. Näiteks saab arvutada võlasumma muutuse eelmise päevaga, võlapäevade keskmise muutuse ja mitme päeva järjest halvenenud maksekäitumise.

```sql
SELECT
    snapshot_date,
    total_debt_amount,
    total_debt_amount
        - LAG(total_debt_amount) OVER (ORDER BY snapshot_date) AS debt_amount_change
FROM mart.kpi_daily_debt;
```

## Filtreerimine

Dashboard peab toetama filtreerimist perioodi, ettevõtte, lepingu ja faili järgi. Vajadusel lisatakse hiljem riskitaseme või ettevõtte segmendi filter.

## ML Sisendtunnused

Tulevase ML komponendi jaoks saab lisada tunnuseid nagu viimase 7 või 30 päeva võlasumma muutus, maksimaalne võlapäevade arv viimase 90 päeva jooksul, korduvate viivituste arv ja kvaliteedivigade arv kliendi andmetes.

## Tehnilised Märkused

KPI-de arvutus võib toimuda transform teenuses SQL-i abil. Dashboard API peaks lugema eelarvutatud KPI tabelit, et veebivaade oleks kiire ja stabiilne.


