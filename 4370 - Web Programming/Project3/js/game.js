// Santa's Adaptive Christmas Fifteen Puzzle - Core Puzzle Engine
// Step 2: Board logic, rendering, movement, win check

let BOARD_SIZE = 3; // Dynamic board size
let board = [];
let emptyTile = { row: 2, col: 2 }; // Will be adjusted based on BOARD_SIZE
let moveCount = 0;
let timer = 0;
let timerInterval = null;
let currentStage = 1; // 1..5
let currentDifficulty = 'normal';
let miracleLives = 2; // Christmas Miracle power-up uses
// Images are placed directly under assets/ per user setup
let puzzleImagePath = "assets/stage1.png"; // default; supports .png or .jpg
let imageLoaded = false;

// Stage configuration: difficulty + power-up availability + grid size
const STAGE_CONFIG = {
    1: { difficulty: 'easy', gridSize: 3, hints: 'full', freeze: true, shuffleDepth: 20 },
    2: { difficulty: 'normal', gridSize: 4, hints: 'reduced', freeze: true, shuffleDepth: 80 },
    3: { difficulty: 'hard', gridSize: 4, hints: 'few', freeze: true, shuffleDepth: 150 },
    4: { difficulty: 'hard', gridSize: 5, hints: 'minimal', freeze: true, shuffleDepth: 220 },
    5: { difficulty: 'hard', gridSize: 5, hints: 'none', freeze: false, shuffleDepth: 300 }
};

// Stage story content for inline results
const STAGE_STORY = {
    1: {
        title: "Stage 1: Welcome to Santa's Workshop",
        text: "Santa's workshop is unusually quiet. The elves gather around a half-finished display of magical tiles that power the workshop's systems. The pieces are scattered and must be restored before production can begin. This first task tests how the workshop works; once the tiles are restored, the lights flicker back on. Gameplay meaning: intro puzzle with lowest difficulty and full hints available."
    },
    2: {
        title: "Stage 2: The Toy Assembly Line Breakdown",
        text: "With the workshop running, the elves rush to the toy assembly line when the conveyor freezes. Control tiles have shifted, and you need to fix the layout fast. The tiles are trickier now, and careless moves slow things down; restoring order brings the machines back to life. Gameplay meaning: moderate shuffle depth with slightly reduced hints."
    },
    3: {
        title: "Stage 3: Sorting the Enchanted Gift Tiles",
        text: "As Christmas Eve nears, gifts glow with enchantment. These tiles decide destinations, but the magic scrambles the order. Precision is needed; the tiles resist being moved, and only careful planning restores harmony. Solving stabilizes the glow and aligns gifts for delivery. Gameplay meaning: harder shuffle, fewer power-ups, higher difficulty."
    },
    4: {
        title: "Stage 4: Training the Elves Under Pressure",
        text: "Santa trains the elves for last-minute changes by rearranging the workshop into controlled chaos. Time is short and mistakes matter. Restoring order teaches the elves, and when the tiles click into place they cheer, confident they can handle anything. Gameplay meaning: high difficulty, minimal hints, faster pace or tighter limits."
    },
    5: {
        title: "Stage 5: Final Preparations for Christmas Eve",
        text: "On the final night before Christmas, snow falls as Santa prepares the sleigh. The most important control tiles lie scattered, representing the whole workshop working together. Every move must be deliberate; when the last tile slides in, the workshop glows and Christmas can begin. Gameplay meaning: maximum difficulty with no or minimal hints—the final challenge."
    }
};

// Initialize board with image tiles (0 to BOARD_SIZE²-2), empty is last, then shuffle to solvable state
function initBoard() {
    let tiles = [];
    const totalTiles = BOARD_SIZE * BOARD_SIZE;
    for (let i = 0; i < totalTiles - 1; i++) {
        tiles.push(i);
    }
    tiles.push(null); // empty tile
    do {
        shuffleArray(tiles);
    } while (!isSolvable(tiles));
    board = [];
    for (let r = 0; r < BOARD_SIZE; r++) {
        let row = [];
        for (let c = 0; c < BOARD_SIZE; c++) {
            let idx = r * BOARD_SIZE + c;
            row.push(tiles[idx]);
            if (tiles[idx] === null) emptyTile = { row: r, col: c };
        }
        board.push(row);
    }
}

// Fisher-Yates shuffle
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// Check if a board is solvable
function isSolvable(tiles) {
    let invCount = 0;
    for (let i = 0; i < tiles.length - 1; i++) {
        for (let j = i + 1; j < tiles.length; j++) {
            if (tiles[i] !== null && tiles[j] !== null && tiles[i] > tiles[j]) invCount++;
        }
    }
    // Find row of empty tile counting from bottom (1-based)
    const emptyIndex = tiles.indexOf(null);
    const emptyRow = Math.floor(emptyIndex / BOARD_SIZE);
    const emptyRowFromBottom = BOARD_SIZE - emptyRow; // 1..BOARD_SIZE
    // Solvability rules:
    // - If grid width is odd: puzzle is solvable when inversion count is even
    // - If grid width is even: puzzle is solvable when
    //     * the blank is on an even row counting from the bottom and number of inversions is odd
    //     * the blank is on an odd row counting from the bottom and number of inversions is even
    if (BOARD_SIZE % 2 === 1) {
        return invCount % 2 === 0;
    } else {
        const blankEvenFromBottom = (emptyRowFromBottom % 2 === 0);
        return (blankEvenFromBottom && invCount % 2 === 1) || (!blankEvenFromBottom && invCount % 2 === 0);
    }
}

// Render board as image tiles with dynamic sizing
function renderBoard() {
    const boardDiv = document.getElementById('game-board');
    boardDiv.innerHTML = '';
    boardDiv.className = 'board';
    
    // Calculate tile and board size based on BOARD_SIZE
    const tileSize = Math.max(40, Math.min(80, 240 / BOARD_SIZE)); // Responsive tile sizing
    const boardSize = tileSize * BOARD_SIZE + (BOARD_SIZE - 1) * 4; // Include 2px margins
    
    boardDiv.style.width = `${boardSize}px`;
    boardDiv.style.height = `${boardSize}px`;
    
    for (let r = 0; r < BOARD_SIZE; r++) {
        for (let c = 0; c < BOARD_SIZE; c++) {
            const tile = board[r][c];
            const tileDiv = document.createElement('div');
            tileDiv.className = tile === null ? 'tile empty' : 'tile';
            tileDiv.style.left = `${c * (tileSize + 4)}px`;
            tileDiv.style.top = `${r * (tileSize + 4)}px`;
            tileDiv.style.width = `${tileSize}px`;
            tileDiv.style.height = `${tileSize}px`;
            if (tile !== null) {
                if (imageLoaded) {
                    // Single image slicing: use puzzleImagePath and set background position
                    tileDiv.style.backgroundImage = `url('${puzzleImagePath}')`;
                    tileDiv.style.backgroundSize = `${boardSize}px ${boardSize}px`;
                    const sr = Math.floor(tile / BOARD_SIZE);
                    const sc = tile % BOARD_SIZE;
                    tileDiv.style.backgroundPosition = `${-sc * (tileSize + 4)}px ${-sr * (tileSize + 4)}px`;
                } else {
                    // Fallback: show tile number with a festive background
                    tileDiv.style.background = '#1f2a44';
                    tileDiv.style.color = '#ffd54f';
                    tileDiv.style.display = 'flex';
                    tileDiv.style.alignItems = 'center';
                    tileDiv.style.justifyContent = 'center';
                    tileDiv.style.fontWeight = 'bold';
                    tileDiv.textContent = tile + 1; // human-friendly 1..15
                }
                tileDiv.dataset.row = r;
                tileDiv.dataset.col = c;
                tileDiv.addEventListener('click', onTileClick);
            }
            boardDiv.appendChild(tileDiv);
        }
    }
}

// Preload the puzzle image to decide whether to slice or use fallback
// Try loading .png first, then .jpg if .png missing
function resolvePuzzleImagePath(stageNum) {
    // Look directly under assets/ (no images/puzzles folder)
    const base = `assets/stage${stageNum}`;
    return new Promise(resolve => {
        const tryPng = new Image();
        tryPng.onload = () => resolve(`${base}.png`);
        tryPng.onerror = () => {
            const tryJpg = new Image();
            tryJpg.onload = () => resolve(`${base}.jpg`);
            tryJpg.onerror = () => resolve(`${base}.png`); // default back to .png
            tryJpg.src = `${base}.jpg`;
        };
        tryPng.src = `${base}.png`;
    });
}

function preloadPuzzleImage(path) {
    return new Promise(resolve => {
        const img = new Image();
        img.onload = function() { imageLoaded = true; resolve(true); };
        img.onerror = function() { imageLoaded = false; resolve(false); };
        img.src = path;
    });
}

// Check if move is valid (adjacent to empty)
function isValidMove(row, col) {
    const dr = Math.abs(row - emptyTile.row);
    const dc = Math.abs(col - emptyTile.col);
    return (dr + dc === 1);
}

// Swap tile with empty
function moveTile(row, col) {
    if (!isValidMove(row, col)) return;
    board[emptyTile.row][emptyTile.col] = board[row][col];
    board[row][col] = null;
    emptyTile = { row, col };
    moveCount++;
    updateMoveCounter();
    renderBoard();
    if (checkWin()) {
        onWin();
    }
}

function onTileClick(e) {
    const row = parseInt(e.target.dataset.row);
    const col = parseInt(e.target.dataset.col);
    moveTile(row, col);
}

// Check for win
function checkWin() {
    let count = 0;
    const lastRow = BOARD_SIZE - 1;
    const lastCol = BOARD_SIZE - 1;
    for (let r = 0; r < BOARD_SIZE; r++) {
        for (let c = 0; c < BOARD_SIZE; c++) {
            if (r === lastRow && c === lastCol) return board[r][c] === null;
            if (board[r][c] !== count) return false;
            count++;
        }
    }
    return true;
}

function onWin() {
    clearInterval(timerInterval);
    timerInterval = null;
    // Prevent further moves
    const tiles = document.querySelectorAll('.tile');
    tiles.forEach(t => t.replaceWith(t.cloneNode(true))); // remove listeners by cloning
    // Unlock next stage (client-side); server-side persistence can be added
    const unlocked = parseInt(localStorage.getItem('unlockedStage') || '1', 10);
    if (unlocked < 5) localStorage.setItem('unlockedStage', String(unlocked + 1));
    // Unlock achievements based on performance
    if (timer < 90) unlockAchievement('Fast Solver');
    if (moveCount < 40) unlockAchievement('Holiday Hero');
    if (currentDifficulty === 'hard') unlockAchievement("Santa's Apprentice");
    alert('Congratulations! You solved the puzzle!');
    // Persist last result locally for results page
    // Convert relative path to absolute URL for server compatibility
    let imagePath = puzzleImagePath;
    if (!imagePath.startsWith('http') && !imagePath.startsWith('/')) {
        // Get the directory of the current page and construct absolute path
        const currentDir = window.location.pathname.substring(0, window.location.pathname.lastIndexOf('/'));
        imagePath = currentDir + '/' + imagePath;
    }
    localStorage.setItem('lastResult', JSON.stringify({
        time: timer,
        moves: moveCount,
        difficulty: currentDifficulty,
        stage: currentStage,
        image: imagePath
    }));
    const redirectToResults = () => {
        if (location.pathname.endsWith('game_demo.html')) {
            location.href = 'result_demo.html';
        } else {
            location.href = 'result.php';
        }
    };
    // Send result to backend (fail-safe redirect if offline/file://)
    fetch('api/game_session.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `action=end&moves=${moveCount}&time=${timer}&difficulty=${currentDifficulty}&completed=1`
    })
    .then(res => res.json())
    .then(() => redirectToResults())
    .catch(() => redirectToResults());
}

function unlockAchievement(name) {
    fetch('api/achievements.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `name=${encodeURIComponent(name)}`
    });
}

function updateMoveCounter() {
    document.getElementById('move-counter').textContent = `Moves: ${moveCount}`;
}

function startTimer() {
    startTimerWithReset(true);
}

function stopTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
}

function startTimerWithReset(reset = false) {
    if (timerInterval) return; // already running
    if (reset) {
        timer = 0;
        document.getElementById('timer').textContent = '00:00';
    }
    timerInterval = setInterval(() => {
        timer++;
        const min = String(Math.floor(timer / 60)).padStart(2, '0');
        const sec = String(timer % 60).padStart(2, '0');
        document.getElementById('timer').textContent = `${min}:${sec}`;
    }, 1000);
}

// Initialize game

function startGame() {
    stopTimer();
    // Load stage and image path - check currentStage first (set by results page), then fall back to unlockedStage
    const stageToLoad = localStorage.getItem('currentStage');
    if (stageToLoad) {
        currentStage = Math.max(1, Math.min(5, parseInt(stageToLoad, 10)));
        localStorage.removeItem('currentStage'); // Clear after reading so next time it uses unlockedStage
    } else {
        const unlocked = parseInt(localStorage.getItem('unlockedStage') || '1', 10);
        currentStage = Math.max(1, Math.min(5, unlocked));
    }
    // Resolve actual existing image extension
    resolvePuzzleImagePath(currentStage).then((resolvedPath) => {
        puzzleImagePath = resolvedPath;
        const cfg = STAGE_CONFIG[currentStage];
        currentDifficulty = cfg.difficulty;
        // Set board size based on stage configuration
        BOARD_SIZE = cfg.gridSize;
        // Reset Christmas Miracle lives at start of each game
        miracleLives = 2;
        updateMiracleLives();
        // Power-up availability
        const freezeBtn = document.getElementById('freeze-btn');
        const miracleBtn = document.getElementById('miracle-btn');
        if (freezeBtn) freezeBtn.disabled = !cfg.freeze;
        if (miracleBtn) miracleBtn.disabled = false;
        initBoard();
        moveCount = 0;
        updateMoveCounter();
        preloadPuzzleImage(puzzleImagePath).then(() => {
            renderBoard();
        });
        startTimerWithReset(true);
        // Reset freeze toggle text
        const freezeBtnLive = document.getElementById('freeze-btn');
        if (freezeBtnLive) freezeBtnLive.textContent = '❄️ Freeze Timer';
        isFrozen = false;
    });
    // Notify backend to start a new session
    fetch('api/game_session.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'action=start'
    })
    .then(res => res.json())
    .then(data => {
        // Optionally handle session_id or errors
    });
}

document.addEventListener('DOMContentLoaded', () => {
    startGame();
    document.getElementById('reset-btn').addEventListener('click', startGame);
    document.getElementById('newgame-btn').addEventListener('click', startGame);
    document.getElementById('miracle-btn').addEventListener('click', useChristmasMiracle);
    document.getElementById('freeze-btn').addEventListener('click', toggleFreeze);
    document.getElementById('shuffle-btn').addEventListener('click', useMiniShuffle);
    const solveBtn = document.getElementById('solve-btn');
    if (solveBtn) solveBtn.addEventListener('click', solveAutomatically);
});

function updateMiracleLives() {
    const livesSpan = document.getElementById('miracle-lives');
    const miracleBtn = document.getElementById('miracle-btn');
    if (livesSpan) {
        livesSpan.textContent = `❤️ ${miracleLives}`;
    }
    if (miracleBtn) {
        miracleBtn.disabled = (miracleLives <= 0);
    }
}

function useChristmasMiracle() {
    if (miracleLives <= 0) return;
    
    // Solve 4-6 random tiles by placing them in correct positions
    const tilesToSolve = 4 + Math.floor(Math.random() * 3); // 4-6 tiles
    let solved = 0;
    const solveable = [];
    
    // Find all tiles that aren't in correct position
    for (let r = 0; r < BOARD_SIZE; r++) {
        for (let c = 0; c < BOARD_SIZE; c++) {
            if (board[r][c] !== null && board[r][c] !== r * BOARD_SIZE + c) {
                solveable.push({ row: r, col: c, value: board[r][c] });
            }
        }
    }
    
    // Shuffle solveable tiles and place first tilesToSolve in their correct positions
    for (let i = 0; i < Math.min(tilesToSolve, solveable.length) && solved < tilesToSolve; i++) {
        const randomIdx = Math.floor(Math.random() * solveable.length);
        const { value } = solveable[randomIdx];
        const correctRow = Math.floor(value / BOARD_SIZE);
        const correctCol = value % BOARD_SIZE;
        
        // Swap current position with correct position
        const temp = board[correctRow][correctCol];
        board[correctRow][correctCol] = board[solveable[randomIdx].row][solveable[randomIdx].col];
        board[solveable[randomIdx].row][solveable[randomIdx].col] = temp;
        
        // Update empty tile if we swapped it
        if (temp === null) {
            emptyTile = { row: solveable[randomIdx].row, col: solveable[randomIdx].col };
        }
        
        solveable.splice(randomIdx, 1);
        solved++;
    }
    
    // Decrement lives and update display
    miracleLives--;
    updateMiracleLives();
    moveCount++;
    updateMoveCounter();
    renderBoard();
    
    // Check if puzzle is solved
    if (isSolved()) {
        onWin();
    }
}

function useHint() {
    // Highlight a tile that is not in the correct position but can move
    for (let r = 0; r < BOARD_SIZE; r++) {
        for (let c = 0; c < BOARD_SIZE; c++) {
            if (board[r][c] !== null && board[r][c] !== r * BOARD_SIZE + c && isValidMove(r, c)) {
                // Highlight this tile
                const tiles = document.querySelectorAll('.tile');
                tiles.forEach(tile => {
                    if (parseInt(tile.dataset.row) === r && parseInt(tile.dataset.col) === c) {
                        tile.style.boxShadow = '0 0 16px 6px #ffd700';
                        setTimeout(() => { tile.style.boxShadow = ''; }, 1200);
                    }
                });
                return;
            }
        }
    }
}

let isFrozen = false;
function toggleFreeze() {
    const btn = document.getElementById('freeze-btn');
    if (!isFrozen) {
        // Pause until clicked again
        stopTimer();
        isFrozen = true;
        if (btn) btn.textContent = '▶️ Resume Timer';
    } else {
        startTimerWithReset(false);
        isFrozen = false;
        if (btn) btn.textContent = '❄️ Freeze Timer';
    }
}

function solveAutomatically() {
    // Set board to solved state (0..14, null at bottom-right)
    board = [];
    for (let r = 0; r < BOARD_SIZE; r++) {
        const row = [];
        for (let c = 0; c < BOARD_SIZE; c++) {
            if (r === BOARD_SIZE - 1 && c === BOARD_SIZE - 1) {
                row.push(null);
            } else {
                row.push(r * BOARD_SIZE + c);
            }
        }
        board.push(row);
    }
    emptyTile = { row: BOARD_SIZE - 1, col: BOARD_SIZE - 1 };
    renderBoard();
    // Trigger win flow to show story/results
    onWin();
}

function showResultsOverlay() {
    const overlay = document.getElementById('results-overlay');
    if (!overlay) return;
    const resTime = document.getElementById('res-time');
    const resMoves = document.getElementById('res-moves');
    const resDiff = document.getElementById('res-difficulty');
    const resTitle = document.getElementById('res-story-title');
    const resText = document.getElementById('res-story-text');
    const resImg = document.getElementById('res-image');

    const min = String(Math.floor(timer / 60)).padStart(2, '0');
    const sec = String(timer % 60).padStart(2, '0');
    if (resTime) resTime.textContent = `Time: ${min}:${sec}`;
    if (resMoves) resMoves.textContent = `Moves: ${moveCount}`;
    if (resDiff) resDiff.textContent = `Difficulty: ${currentDifficulty}`;

    const story = STAGE_STORY[currentStage];
    if (story) {
        if (resTitle) resTitle.textContent = story.title;
        if (resText) resText.textContent = story.text;
    }
    if (resImg) {
        resImg.style.backgroundImage = `url('${puzzleImagePath}')`;
    }

    overlay.classList.remove('hidden');

    const closeBtn = document.getElementById('close-results');
    if (closeBtn) {
        closeBtn.onclick = () => {
            overlay.classList.add('hidden');
            startGame();
        };
    }
}

function useMiniShuffle() {
    // Shuffle 3 random movable tiles
    let movable = [];
    for (let r = 0; r < BOARD_SIZE; r++) {
        for (let c = 0; c < BOARD_SIZE; c++) {
            if (isValidMove(r, c)) movable.push({ r, c });
        }
    }
    for (let i = 0; i < 3 && movable.length > 0; i++) {
        const idx = Math.floor(Math.random() * movable.length);
        const { r, c } = movable[idx];
        moveTile(r, c);
        movable.splice(idx, 1);
    }
}
