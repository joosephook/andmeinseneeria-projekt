<?php
// menu.php
// See fail väljastab lehe ülaosa: logo, saidi pealkiri ja menüü.

header('Content-Type: text/html; charset=utf-8');

$siteTitle = 'Projektitöö: "Võlapäevade trendid"';
$logoPath = 'logo2.png';

$menuItems = [
    [
        'title' => 'Keskmiste võlapäevade graafik',
        'url' => 'chart1.html',
    ],
	[
        'title' => 'Võlas lepingud ja firmad',
        'url' => 'chart2.html',
    ],
    [
        'title' => 'Keskmiste võlapäevade aruanne',
        'url' => 'overdues_report.html',
    ],
];

$currentPage = $_GET['page'] ?? '';

function h($value) {
    return htmlspecialchars((string)$value, ENT_QUOTES, 'UTF-8');
}
?>

<header class="site-header">
    <div class="top-bar">
        <a href="chart1.html" class="logo-link">
            <img src="<?php echo h($logoPath); ?>" alt="Logo" class="site-logo">
        </a>

        <div class="site-title">
            <?php echo h($siteTitle); ?>
        </div>
    </div>

    <nav class="main-menu">
        <?php foreach ($menuItems as $item): ?>
            <?php
                $isActive = basename($item['url']) === basename($currentPage);
                $class = $isActive ? 'active' : '';
            ?>
            <a class="<?php echo h($class); ?>" href="<?php echo h($item['url']); ?>">
                <?php echo h($item['title']); ?>
            </a>
        <?php endforeach; ?>
    </nav>
</header>