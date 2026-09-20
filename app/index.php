<?php
$conn = new mysqli("localhost", "shopuser", "StrongPass123!", "riverbend_shop");
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
