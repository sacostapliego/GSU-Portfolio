<?php
// game.php - Main game page
session_start();

// Require login to play
if (!isset($_SESSION['logged_in']) || !$_SESSION['logged_in']) {
    $_SESSION['error_message'] = "Please login to play the game.";
    header("Location: api/login.php");
    exit;
}

$title = "Play - Santa's Adaptive Christmas Fifteen Puzzle";
include 'includes/header.php';
?>
<main>
    <div class="decoration">🎄 ⛄ 🎄</div>
    <h2 style="text-align:center;margin-bottom:1em;">Welcome, <?= htmlspecialchars($_SESSION['username']) ?>! 🎮</h2>
    <div id="game-board"></div>
    <div id="game-ui">
        <span id="timer">⏱️ 00:00</span>
        <span id="move-counter">📊 Moves: 0</span>
        <span id="stage-indicator" style="margin-left:1em;">🎯 Stage: 1 | Difficulty: Easy</span>
        <div style="margin-top: 1.5em;">
            <button id="reset-btn">🔄 Reset</button>
            <button id="newgame-btn">✨ New Game</button>
            <span style="display:inline-block; white-space:nowrap;">
                <button id="miracle-btn">🎄 Christmas Miracle</button>
                <span id="miracle-lives" style="margin-left:0.5em;">❤️ 2</span>
            </span>
            <button id="freeze-btn">❄️ Freeze Timer</button>
            <button id="shuffle-btn">🔀 Mini Shuffle</button>
            <button id="solve-btn">✅ Solve Automatically</button>
        </div>
    </div>
    <div class="decoration">🎁 🎅 🦌 🎅 🎁</div>

    <div id="results-overlay" class="results-overlay hidden">
        <div class="results-card">
            <h2>🎉 Puzzle Solved!</h2>
            <div class="results-stats">
                <span id="res-time">Time: --</span>
                <span id="res-moves">Moves: --</span>
                <span id="res-difficulty">Difficulty: --</span>
            </div>
            <div class="results-story">
                <h3 id="res-story-title"></h3>
                <p id="res-story-text"></p>
            </div>
            <div id="res-image" class="results-image"></div>
            <div style="margin-top:1.2em;">
                <button id="close-results" class="start-btn">Play Again</button>
            </div>
        </div>
    </div>
</main>
<script src="js/game.js"></script>
<script>
// Stage indicator binding for main project
document.addEventListener('DOMContentLoaded', function() {
    const stageIndicator = document.getElementById('stage-indicator');
    const STAGE_TEXT = { 1: 'Easy', 2: 'Normal', 3: 'Hard', 4: 'Hard', 5: 'Hard' };
    const unlocked = parseInt(localStorage.getItem('unlockedStage') || '1', 10);
    stageIndicator.textContent = `🎯 Stage: ${unlocked} | Difficulty: ${STAGE_TEXT[unlocked]}`;
    
    // New Game button - start from Stage 1
    document.getElementById('newgame-btn').onclick = function() {
        localStorage.setItem('unlockedStage', '1');
        localStorage.removeItem('currentStage');
        if (typeof startGame === 'function') startGame();
    };
});
</script>
<?php include 'includes/footer.php'; ?>
