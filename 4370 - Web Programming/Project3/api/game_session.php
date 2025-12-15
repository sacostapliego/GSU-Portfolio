<?php
// API endpoint for starting/ending a game session
require_once '../includes/session.php';
require_once '../includes/db.php';

$action = $_POST['action'] ?? '';
$user_id = $_SESSION['user_id'] ?? null;
$session_id = $_SESSION['session_id'];

if ($action === 'start') {
    $stmt = $pdo->prepare('INSERT INTO game_sessions (session_id, user_id, start_time) VALUES (?, ?, NOW())');
    $stmt->execute([$session_id, $user_id,]);
    echo json_encode(['status' => 'started', 'session_id' => $session_id]);
    exit;
}
if ($action === 'end') {
    $moves = intval($_POST['moves'] ?? 0);
    $time = intval($_POST['time'] ?? 0);
    $difficulty = $_POST['difficulty'] ?? 'normal';
    $completed = intval($_POST['completed'] ?? 0);
    $stmt = $pdo->prepare('UPDATE game_sessions SET end_time = NOW(), moves = ?, time = ?, difficulty = ?, completed = ? WHERE session_id = ?');
    $stmt->execute([$moves, $time, $difficulty, $completed, $session_id]);
    echo json_encode(['status' => 'ended']);
    exit;
}
echo json_encode(['status' => 'error', 'message' => 'Invalid action']);
