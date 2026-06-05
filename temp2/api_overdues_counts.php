<?php
// api_overdues_counts.php
// Loeb ettevõtete arvu ja lepingute arvu view-st reports.v_overdues_counts

require_once __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');

try {
    $sql = "
        SELECT
            report_date,
            company_count,
            contract_count
        FROM reports.v_overdues_counts
        ORDER BY report_date;
    ";

    $stmt = $pdo->query($sql);

    $data = [];

    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        $data[] = [
            'report_date' => $row['report_date'],
            'company_count' => $row['company_count'] !== null ? (int)$row['company_count'] : null,
            'contract_count' => $row['contract_count'] !== null ? (int)$row['contract_count'] : null,
        ];
    }

    echo json_encode($data, JSON_UNESCAPED_UNICODE);

} catch (Throwable $e) {
    http_response_code(500);

    echo json_encode([
        'error' => 'Andmete lugemine view-st reports.v_overdues_counts ebaõnnestus',
        'message' => $e->getMessage()
    ], JSON_UNESCAPED_UNICODE);
}
