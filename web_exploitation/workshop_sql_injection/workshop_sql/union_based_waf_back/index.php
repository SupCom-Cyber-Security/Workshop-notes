<?php
require_once 'waf.php';
require_once 'config.php';

$error = '';
$results = [];

if (isset($_GET['id'])) {
    $id = $_GET['id'];

    // --- WAF check happens BEFORE the query touches the DB ---
    $block_reason = waf_inspect($id);
    if ($block_reason !== null) {
        http_response_code(403);
        die("<h2>🛑 Blocked by WAF</h2><p>Reason: " . htmlspecialchars($block_reason) . "</p>");
    }

    // PHP 8.1+ makes mysqli throw exceptions on SQL errors by default.
    // We want the classic false-return + ->error behavior instead, since
    // the app's "oracle" (echoing raw SQL errors) depends on it.
    mysqli_report(MYSQLI_REPORT_OFF);

    $mysqli = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    if ($mysqli->connect_errno) {
        die("DB connection failed");
    }

    // VULNERABLE: raw string concatenation, no prepared statement
    $query = "SELECT id, name, description FROM products WHERE id = '$id'";

    $res = $mysqli->query($query);

    if ($res === false) {
        // Deliberately leak the SQL error to make UNION-based injection feasible
        $error = "SQL Error: " . $mysqli->error;
    } else {
        while ($row = $res->fetch_assoc()) {
            $results[] = $row;
        }
    }
    $mysqli->close();
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>CTF Shop - Product Lookup</title>
    <style>
        body { font-family: monospace; background:#0d1117; color:#c9d1d9; padding:40px; }
        input { padding:6px; width:300px; }
        button { padding:6px 12px; }
        .err { color:#ff6b6b; }
        table { border-collapse: collapse; margin-top:20px; }
        td, th { border:1px solid #30363d; padding:6px 12px; }
    </style>
</head>
<body>
    <h1>🛒 Product Lookup</h1>
    <p>Search a product by ID.</p>
    <form method="GET">
        <input type="text" name="id" placeholder="e.g. 1" value="<?= htmlspecialchars($_GET['id'] ?? '') ?>">
        <button type="submit">Search</button>
    </form>

    <?php if ($error): ?>
        <p class="err"><?= htmlspecialchars($error) ?></p>
    <?php endif; ?>

    <?php if ($results): ?>
        <table>
            <tr><th>ID</th><th>Name</th><th>Description</th></tr>
            <?php foreach ($results as $row): ?>
                <tr>
                    <td><?= htmlspecialchars($row['id']) ?></td>
                    <td><?= htmlspecialchars($row['name']) ?></td>
                    <td><?= htmlspecialchars($row['description']) ?></td>
                </tr>
            <?php endforeach; ?>
        </table>
    <?php endif; ?>
</body>
</html>