<?php
// Ühised andmebaasi ühenduse seaded.
// Muuda need väärtused vastavalt oma serverile.
$dbHost = '127.0.0.1';
$dbPort = '5432';
$dbName = 'postgres';
$dbUser = 'jaan';
$dbPass = 'JaaniPASS';

$dsn = "pgsql:host={$dbHost};port={$dbPort};dbname={$dbName}";

$pdo = new PDO($dsn, $dbUser, $dbPass, [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
]);
