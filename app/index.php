<?php
$env = [];
$env_file = __DIR__ . '/../.env';

if (is_readable($env_file)) {
    foreach (file($env_file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        $line = trim($line);
        if ($line === '' || str_starts_with($line, '#') || !str_contains($line, '=')) {
            continue;
        }

        [$key, $value] = explode('=', $line, 2);
        $env[trim($key)] = trim($value);
    }
}

$db_host = $env['DB_HOST'] ?? 'localhost';
$db_user = $env['DB_USER'] ?? '';
$db_password = $env['DB_PASSWORD'] ?? '';
$db_name = $env['DB_NAME'] ?? '';

$conn = new mysqli($db_host, $db_user, $db_password, $db_name);
if ($conn->connect_error) {
    die("DB connection failed: " . $conn->connect_error);
}

$result = $conn->query("SELECT name, description, price, stock FROM products ORDER BY id");
?>
<!DOCTYPE html>
<html>
<head>
    <title>Riverbend Boutique</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #fafafa; }
        h1 { color: #2c3e50; }
        table { border-collapse: collapse; width: 100%; max-width: 800px; background: #fff; }
        th, td { padding: 10px 15px; border: 1px solid #ddd; text-align: left; }
        th { background: #2c3e50; color: #fff; }
        tr:nth-child(even) { background: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Riverbend Boutique</h1>
    <p>Handmade accessories — shop is live.</p>
    <h2>Products</h2>
    <table>
        <tr><th>Name</th><th>Description</th><th>Price</th><th>Stock</th></tr>
        <?php while ($row = $result->fetch_assoc()): ?>
        <tr>
            <td><?= htmlspecialchars($row['name']) ?></td>
            <td><?= htmlspecialchars($row['description']) ?></td>
            <td>$<?= number_format($row['price'], 2) ?></td>
            <td><?= (int)$row['stock'] ?></td>
        </tr>
        <?php endwhile; ?>
    </table>
</body>
</html>
