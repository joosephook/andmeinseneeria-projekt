<?php
// /mes/api_weighted_avg_debtdays.php

require_once __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');

try {
    $sql = "
        SELECT
            report_date,
            weighted_avg_debtdays
        FROM reports.v_overdues_summary
        ORDER BY report_date
    ";

    $stmt = $pdo->query($sql);

    $data = [];

    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        $data[] = [
            'report_date' => $row['report_date'],
            'weighted_avg_debtdays' => $row['weighted_avg_debtdays'] !== null
                ? (float)$row['weighted_avg_debtdays']
                : null
        ];
    }

    echo json_encode($data, JSON_UNESCAPED_UNICODE);

} catch (Throwable $e) {
    http_response_code(500);

    echo json_encode([
        'error' => 'Andmete lugemine view-st ebaõnnestus'
    ], JSON_UNESCAPED_UNICODE);
}