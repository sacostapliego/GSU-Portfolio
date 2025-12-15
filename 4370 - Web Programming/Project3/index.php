<?php
// index.php - Landing page for Santa's Adaptive Christmas Fifteen Puzzle
session_start();
$title = "Santa's Adaptive Christmas Fifteen Puzzle";
include 'includes/header.php';
?>
<main>
    <?php if (isset($_SESSION['logged_in']) && $_SESSION['logged_in']): ?>
        <h1>❄️ Welcome back, <?= htmlspecialchars($_SESSION['username']) ?>! ❄️</h1>
        <p>🎁 Ready for another festive puzzle challenge? Let's make some Christmas magic! 🎁</p>
    <?php else: ?>
        <h1>❄️ Welcome to Santa's Workshop! ❄️</h1>
        <p>🎁 Challenge yourself with this festive sliding puzzle game. Register, log in, or jump straight into play mode! 🎁</p>
    <?php endif; ?>
    <div class="decoration">🎄 ⛄ 🎄 ⛄ 🎄</div>
    <a href="game.php" class="start-btn">🚀 Start Game 🚀</a>
    <div class="decoration">🔔 🎅 🦌 🎅 🔔</div>
</main>
<?php include 'includes/footer.php'; ?>
