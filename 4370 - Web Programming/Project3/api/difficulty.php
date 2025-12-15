<?php
// Adaptive difficulty endpoint
require_once '../includes/db.php';
require_once '../includes/session.php';

$user_id = $_SESSION['user_id'] ?? null;
if (!$user_id) {
    echo json_encode(['difficulty' => 'normal']);
    exit;
}

// Get recent performance
$stmt = $pdo->prepare('SELECT AVG(moves) as avg_moves, AVG(time) as avg_time FROM game_sessions WHERE user_id = ? AND completed = 1 ORDER BY end_time DESC LIMIT 10');
$stmt->execute([$user_id]);
$row = $stmt->fetch();
$avg_moves = $row['avg_moves'] ?? 50;
$avg_time = $row['avg_time'] ?? 300;

// Adaptive logic: faster and fewer moves = harder
if ($avg_time < 90 && $avg_moves < 40) {
    $difficulty = 'hard';
} elseif ($avg_time < 180 && $avg_moves < 50) {
    $difficulty = 'normal';
} else {
    $difficulty = 'easy';
}

echo json_encode(['difficulty' => $difficulty]);
