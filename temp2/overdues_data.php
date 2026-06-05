<?php
require_once __DIR__ . "/db.php";

header("Content-Type: application/json; charset=utf-8");

try {
    $dateSql = "
        SELECT
            col_nr,
            report_date,
            report_date_label
        FROM reports.v_overdues_last5_dates
        ORDER BY col_nr;
    ";

    $dateStmt = $pdo->query($dateSql);
    $dates = $dateStmt->fetchAll();

    $dataSql = "
        SELECT
            company_code,
            value_1,
            value_2,
            value_3,
            value_4,
            value_5
        FROM reports.v_overdues_company_pivot_last5
        ORDER BY company_code;
    ";

    $dataStmt = $pdo->query($dataSql);
    $rows = $dataStmt->fetchAll();

    echo json_encode([
        "dates" => $dates,
        "rows" => $rows
    ], JSON_UNESCAPED_UNICODE);

} catch (PDOException $e) {
    http_response_code(500);

    echo json_encode([
        "error" => "Päringu käivitamine ebaõnnestus",
        "message" => $e->getMessage()
    ], JSON_UNESCAPED_UNICODE);
}