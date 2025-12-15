<?php
// Achievements API: unlock and fetch user achievements
require_once '../includes/db.php';
require_once '../includes/session.php';

$user_id = $_SESSION['user_id'] ?? null;
if (!$user_id) {
    echo json_encode(['status'=>'error','message'=>'Not logged in']);
    exit;
}

// Create achievements table if not exists (run once in DB):
// CREATE TABLE achievements (user_id INT, name VARCHAR(50), unlocked_at DATETIME, PRIMARY KEY(user_id, name), FOREIGN KEY(user_id) REFERENCES users(user_id));

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = $_POST['name'] ?? '';
    if ($name) {
        $stmt = $pdo->prepare('INSERT IGNORE INTO achievements (user_id, name, unlocked_at) VALUES (?, ?, NOW())');
        $stmt->execute([$user_id, $name]);
        echo json_encode(['status'=>'success']);
        exit;
    }
}
// GET: fetch all achievements
$stmt = $pdo->prepare('SELECT name, unlocked_at FROM achievements WHERE user_id = ?');
$stmt->execute([$user_id]);
$rows = $stmt->fetchAll();
$all = array_map(function($r){return $r['name'];}, $rows);
echo json_encode(['status'=>'ok','achievements'=>$all]);
