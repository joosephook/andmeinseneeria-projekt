CREATE SCHEMA IF NOT EXISTS reports;
 
CREATE TABLE IF NOT EXISTS reports.overdues_stg (
 id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 company_code text,
 sap_contract text,
 debtsum text,
 debtdays text,
 report_date date
);
 
 
CREATE TABLE IF NOT EXISTS reports.overdues (
	id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	company_code integer NOT NULL,
	sap_contract integer NOT NULL,
	debtsum numeric(12,2),
	debtdays integer,
	report_date date NOT NULL
);
 
 
 
CREATE OR REPLACE VIEW reports.v_overdues_summary AS
SELECT
o.report_date,
SUM(o.debtsum) AS company_debtsum_total,
ROUND(
SUM(o.debtsum * o.debtdays) / NULLIF(SUM(o.debtsum), 0)
) AS weighted_avg_debtdays,
COUNT(DISTINCT o.company_code) AS company_count,
COUNT(DISTINCT (o.company_code, o.sap_contract)) AS contract_count
FROM reports.overdues o
WHERE o.debtdays IS NOT NULL
GROUP BY
o.report_date;
