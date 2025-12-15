<?php
// achievements.php - Display user achievements
session_start();

// Require login to view achievements
if (!isset($_SESSION['logged_in']) || !$_SESSION['logged_in']) {
    $_SESSION['error_message'] = "Please login to view achievements.";
    header("Location: api/login.php");
    exit;
}

require_once 'includes/db.php';

$title = "Achievements - Santa's Adaptive Christmas Fifteen Puzzle";
include 'includes/header.php';

// Get user's game statistics
$user_id = $_SESSION['user_id'];
$stmt = $conn->prepare("SELECT COUNT(*) as total_games, 
                               MIN(time) as best_time, 
                               MIN(moves) as best_moves,
                               SUM(CASE WHEN difficulty = 'hard' THEN 1 ELSE 0 END) as hard_completed
                        FROM game_sessions 
                        WHERE user_id = ? AND completed = 1");
$stmt->bind_param("i", $user_id);
$stmt->execute();
$result = $stmt->get_result();
$stats = $result->fetch_assoc();
$stmt->close();

// Define achievements
$achievements = [
    [
        'id' => 'first_win',
        'title' => '🎉 First Victory',
        'description' => 'Complete your first puzzle',
        'earned' => $stats['total_games'] > 0
    ],
    [
        'id' => 'fast_solver',
        'title' => '⚡ Fast Solver',
        'description' => 'Complete a puzzle in under 90 seconds',
        'earned' => $stats['best_time'] !== null && $stats['best_time'] < 90
    ],
    [
        'id' => 'holiday_hero',
        'title' => '🏆 Holiday Hero',
        'description' => 'Complete a puzzle in under 40 moves',
        'earned' => $stats['best_moves'] !== null && $stats['best_moves'] < 40
    ],
    [
        'id' => 'santa_apprentice',
        'title' => '🎅 Santa\'s Apprentice',
        'description' => 'Complete a puzzle on Hard difficulty',
        'earned' => $stats['hard_completed'] > 0
    ],
    [
        'id' => 'puzzle_master',
        'title' => '⭐ Puzzle Master',
        'description' => 'Complete 10 puzzles',
        'earned' => $stats['total_games'] >= 10
    ],
    [
        'id' => 'christmas_champion',
        'title' => '🎄 Christmas Champion',
        'description' => 'Complete all 5 stages',
        'earned' => false // Will be unlocked when stage 5 is completed
    ]
];

$earned_count = count(array_filter($achievements, fn($a) => $a['earned']));
?>

<main>
    <div class="decoration">🏆 ⭐ 🏆</div>
    <h1>🎁 Your Achievements 🎁</h1>
    <h2 style="text-align:center;margin-bottom:2em;">Welcome, <?= htmlspecialchars($_SESSION['username']) ?>!</h2>
    
    <div style="text-align:center;margin-bottom:2em;">
        <p style="font-size:1.3em;"><strong>Achievements Earned: <?= $earned_count ?> / <?= count($achievements) ?></strong></p>
    </div>

    <div class="achievements-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.5em;max-width:1000px;margin:2em auto;padding:0 1em;">
        <?php foreach ($achievements as $achievement): ?>
            <div class="achievement-card" style="background:<?= $achievement['earned'] ? 'linear-gradient(135deg, #27ae60, #229954)' : 'rgba(100,100,100,0.3)' ?>;padding:1.5em;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.2);text-align:center;<?= $achievement['earned'] ? '' : 'opacity:0.6;' ?>">
                <h3 style="font-size:2em;margin-bottom:0.3em;"><?= $achievement['title'] ?></h3>
                <p style="font-size:1.1em;margin:0.5em 0;"><?= $achievement['description'] ?></p>
                <?php if ($achievement['earned']): ?>
                    <p style="color:#ffd700;font-weight:bold;margin-top:1em;">✓ UNLOCKED</p>
                <?php else: ?>
                    <p style="color:#ccc;margin-top:1em;">🔒 Locked</p>
                <?php endif; ?>
            </div>
        <?php endforeach; ?>
    </div>

    <div style="text-align:center;margin:3em 0;">
        <h2>📊 Your Statistics</h2>
        <div style="display:inline-block;text-align:left;background:rgba(255,255,255,0.1);padding:2em;border-radius:12px;margin-top:1em;">
            <p style="font-size:1.2em;margin:0.5em 0;"><strong>Total Games Completed:</strong> <?= $stats['total_games'] ?></p>
            <p style="font-size:1.2em;margin:0.5em 0;"><strong>Best Time:</strong> <?= $stats['best_time'] !== null ? gmdate("i:s", $stats['best_time']) : 'N/A' ?></p>
            <p style="font-size:1.2em;margin:0.5em 0;"><strong>Best Moves:</strong> <?= $stats['best_moves'] !== null ? $stats['best_moves'] : 'N/A' ?></p>
            <p style="font-size:1.2em;margin:0.5em 0;"><strong>Hard Puzzles Completed:</strong> <?= $stats['hard_completed'] ?></p>
        </div>
    </div>

    <div style="text-align:center;margin:2em 0;">
        <a href="game.php" class="start-btn">🎮 Play Again 🎮</a>
    </div>
    
    <div class="decoration">🎁 🎅 🦌 🎅 🎁</div>
</main>

<?php include 'includes/footer.php'; ?>
