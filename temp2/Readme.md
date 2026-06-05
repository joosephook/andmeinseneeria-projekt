
/* fail char11.html muutus kuna tegin sinna menüü juurde. Sinna andmeid toov api_weighted_avg_debtdays.php ei muutunud.
Kõikidele html failidele kuvatakse dünaamiline menüü failist menu.php.
Näidis pilt esimsese lahe kohta: Sample1.png. AI-ga tehtud logo on logo2.png.
 */



/* chart2.html ja api_overdues_counts.php näitavad seda alltoodud viewd. Ühel lehel kaks graafikut. 
Näidis pilt teise lehe kohta Sample2.png. */

CREATE OR REPLACE VIEW reports.v_overdues_counts
AS SELECT report_date,
    count(DISTINCT company_code) AS company_count,
    count(DISTINCT ROW(company_code, sap_contract)) AS contract_count
   FROM reports.overdues o
  WHERE debtdays IS NOT NULL
  GROUP BY report_date;
  

  
/* overdues_report.html ja overdues_data.php näitavad kahte allpool toodud viewd. Php fail paneb need 2 viewd kokku.
Näidis pilt kolmanda lehe kohta Sample3.png */

  CREATE OR REPLACE VIEW reports.v_overdues_last5_dates
AS SELECT row_number() OVER (ORDER BY report_date) AS col_nr,
    report_date,
    to_char(report_date::timestamp with time zone, 'DD.MM.YYYY'::text) AS report_date_label
   FROM ( SELECT DISTINCT overdues.report_date
           FROM reports.overdues
          WHERE overdues.debtdays IS NOT NULL
          ORDER BY overdues.report_date DESC
         LIMIT 5) d;
  
  
  
  CREATE OR REPLACE VIEW reports.v_overdues_company_pivot_last5
AS WITH last_dates AS (
         SELECT d.report_date,
            row_number() OVER (ORDER BY d.report_date) AS rn
           FROM ( SELECT DISTINCT overdues.report_date
                   FROM reports.overdues
                  WHERE overdues.debtdays IS NOT NULL
                  ORDER BY overdues.report_date DESC
                 LIMIT 5) d
        ), pivot_dates AS (
         SELECT max(last_dates.report_date) FILTER (WHERE last_dates.rn = 1) AS d1,
            max(last_dates.report_date) FILTER (WHERE last_dates.rn = 2) AS d2,
            max(last_dates.report_date) FILTER (WHERE last_dates.rn = 3) AS d3,
            max(last_dates.report_date) FILTER (WHERE last_dates.rn = 4) AS d4,
            max(last_dates.report_date) FILTER (WHERE last_dates.rn = 5) AS d5
           FROM last_dates
        )
 SELECT o.company_code,
    round(sum(o.debtsum * o.debtdays::numeric) FILTER (WHERE o.report_date = p.d1) / NULLIF(sum(o.debtsum) FILTER (WHERE o.report_date = p.d1), 0::numeric))::integer AS value_1,
    round(sum(o.debtsum * o.debtdays::numeric) FILTER (WHERE o.report_date = p.d2) / NULLIF(sum(o.debtsum) FILTER (WHERE o.report_date = p.d2), 0::numeric))::integer AS value_2,
    round(sum(o.debtsum * o.debtdays::numeric) FILTER (WHERE o.report_date = p.d3) / NULLIF(sum(o.debtsum) FILTER (WHERE o.report_date = p.d3), 0::numeric))::integer AS value_3,
    round(sum(o.debtsum * o.debtdays::numeric) FILTER (WHERE o.report_date = p.d4) / NULLIF(sum(o.debtsum) FILTER (WHERE o.report_date = p.d4), 0::numeric))::integer AS value_4,
    round(sum(o.debtsum * o.debtdays::numeric) FILTER (WHERE o.report_date = p.d5) / NULLIF(sum(o.debtsum) FILTER (WHERE o.report_date = p.d5), 0::numeric))::integer AS value_5
   FROM reports.overdues o
     CROSS JOIN pivot_dates p
  WHERE o.debtdays IS NOT NULL
  GROUP BY o.company_code, p.d1, p.d2, p.d3, p.d4, p.d5;