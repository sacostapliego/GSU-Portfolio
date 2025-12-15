<?php
// result.php - Game result and summary
session_start();
$title = "Results - Santa's Adaptive Christmas Fifteen Puzzle";
include 'includes/header.php';
?>
<main class="results-wrapper">
    <div class="celebration">🎉 🎊 🎉</div>
    <h2>🏆 Game Results 🏆</h2>
    <p>🎄 Great job! Here's how you did: 🎄</p>
    <ul class="stats-list">
        <li>⏱️ Time: <span id="result-time">00:00</span></li>
        <li>📊 Moves: <span id="result-moves">0</span></li>
        <li>⭐ Difficulty: <span id="result-difficulty">Normal</span></li>
    </ul>
    <div id="story-mode" class="story-card">
        <h3>📖 Santa's Workshop Story 📖</h3>
        <h4 id="story-title"></h4>
        <div id="story-segment">Loading story...</div>
    </div>
    <div id="solved-image"></div>
    <button id="next-stage-btn" class="start-btn" style="margin-top: 1.5em;">➡️ Next Stage</button>
    <button id="play-again-btn" class="start-btn" style="margin-top: 1.5em;">🎮 Play Again 🎮</button>
    <div class="decoration">🎁 🎅 🦌 🎅 🎁</div>
</main>
<script>
// Stage story content (1..5)
const STAGES = {
    1: {
        title: "Stage 1: Welcome to Santa's Workshop",
        segments: [
            "Santa's workshop is unusually quiet. The elves are gathered around a long worktable, staring at a half-finished display of magical tiles. Santa explains that these tiles power the workshop's systems, but something has gone wrong. The pieces are scattered, and without restoring order, production cannot begin. This first task is simple, meant to test your understanding of how the workshop works. Once the tiles are restored, the workshop lights flicker back on, signaling that the preparations for Christmas can finally begin."
        ]
    },
    2: {
        title: "Stage 2: The Toy Assembly Line Breakdown",
        segments: [
            "With the workshop running again, the elves rush to the toy assembly line. Suddenly, the conveyor system freezes. The control tiles that guide toy construction have shifted out of place. Santa asks you to fix the layout before valuable time is lost. The elves warn that the tiles are trickier this time, and careless moves could slow everything down. As you restore the correct order, the machines hum back to life and toys begin moving down the line once more."
        ]
    },
    3: {
        title: "Stage 3: Sorting the Enchanted Gift Tiles",
        segments: [
            "As Christmas Eve draws closer, the gifts themselves begin to glow with enchantment. These magical tiles determine which gifts go to which destinations around the world. Unfortunately, the enchantments interfere with each other, scrambling the tile order. Santa needs precision now. The tiles resist being moved, and only careful planning will restore harmony. When the puzzle is solved, the glow stabilizes, and the gifts align perfectly, ready for delivery."
        ]
    },
    4: {
        title: "Stage 4: Training the Elves Under Pressure",
        segments: [
            "The elves must now be trained to handle last-minute changes. Santa rearranges the workshop layout to simulate chaos, intentionally making the puzzle more complex. Time is short, and mistakes matter. The elves watch closely as you restore order, learning from every move. Solving this puzzle proves that you can think clearly under pressure. When the tiles click into place, the elves cheer, confident they can handle whatever Christmas throws at them."
        ]
    },
    5: {
        title: "Stage 5: Final Preparations for Christmas Eve",
        segments: [
            "It is the final night before Christmas. Snow falls outside as Santa prepares the sleigh. The most important control tiles of all are scattered across the table. This puzzle represents the entire workshop working together. Every move must be deliberate. When the final tile slides into place, the workshop glows brighter than ever. Santa smiles, knowing everything is ready. Thanks to your help, Christmas can begin."
        ]
    }
};

let storyIndex = 0;
const lastResult = JSON.parse(localStorage.getItem('lastResult') || '{}');
const stageForStory = Math.max(1, Math.min(5, parseInt(lastResult.stage || localStorage.getItem('unlockedStage') || '1', 10)));
const story = STAGES[stageForStory];
document.getElementById('story-title').textContent = story.title;

document.getElementById('result-time').textContent = lastResult.time !== undefined ? formatTime(lastResult.time) : '00:00';
document.getElementById('result-moves').textContent = lastResult.moves !== undefined ? lastResult.moves : '0';
document.getElementById('result-difficulty').textContent = lastResult.difficulty || 'Normal';
if (lastResult.image) {
    const solvedImage = document.getElementById('solved-image');
    // Ensure proper image loading with error handling
    const img = new Image();
    img.onload = function() {
        solvedImage.style.backgroundImage = `url('${lastResult.image}')`;
        solvedImage.style.backgroundSize = 'cover';
        solvedImage.style.backgroundPosition = 'center';
    };
    img.onerror = function() {
        console.warn('Image failed to load:', lastResult.image);
        solvedImage.style.background = '#333';
        solvedImage.style.display = 'flex';
        solvedImage.style.alignItems = 'center';
        solvedImage.style.justifyContent = 'center';
        solvedImage.style.color = '#fff';
        solvedImage.textContent = '🖼️ Image not found';
    };
    img.src = lastResult.image;
}

// Display all story segments at once
document.getElementById('story-segment').textContent = story.segments.join('\n\n');

function formatTime(t) {
    const m = String(Math.floor(t / 60)).padStart(2, '0');
    const s = String(t % 60).padStart(2, '0');
    return `${m}:${s}`;
}

document.getElementById('next-stage-btn').onclick = function() {
    const next = Math.min(5, (stageForStory || 1) + 1);
    localStorage.setItem('unlockedStage', String(next));
    localStorage.setItem('currentStage', String(next));
    location.href = 'game.php';
};

document.getElementById('play-again-btn').onclick = function() {
    localStorage.setItem('currentStage', String(stageForStory));
    location.href = 'game.php';
};
</script>
<?php include 'includes/footer.php'; ?>
