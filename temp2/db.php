<?php
// Ühised andmebaasi ühenduse seaded.
// Muuda need väärtused vastavalt oma serverile.
$dbHost = '';
$dbPort = '5432';
$dbName = 'postgres';
$dbUser = '';
$dbPass = '';

$dsn = "pgsql:host={$dbHost};port={$dbPort};dbname={$dbName}";

$pdo = new PDO($dsn, $dbUser, $dbPass, [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
]);
