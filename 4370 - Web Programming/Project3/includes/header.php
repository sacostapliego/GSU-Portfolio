<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= isset($title) ? htmlspecialchars($title) : "Math Game - Project 3" ?></title>
    <link rel="stylesheet" href="<?= isset($base_path) ? $base_path : '' ?>css/style.css">
</head>
<body>

<!-- Background Music (Optional - can be removed if not needed) -->
<audio id="bg-music" loop>
    <source src="<?= isset($base_path) ? $base_path : '' ?>assets/christmas.mp3" type="audio/mpeg">
</audio>

<!-- Music Control Button -->
<div class="music-controls" style="position:fixed;top:10px;right:10px;z-index:1000;">
    <button id="music-toggle" class="music-btn" title="Toggle Music">🔊</button>
    <input type="range" id="volume-slider" class="volume-slider" min="0" max="100" value="15" title="Volume Control">
</div>

<header>
        <h1>🎅 Santa's Adaptive Christmas Fifteen Puzzle 🎄</h1>    <nav>
        <div class="nav-container">
            <a href="<?= isset($base_path) ? $base_path : '' ?>index.php" class="logo">🏠 Home</a>
            <?php if (isset($_SESSION['logged_in']) && $_SESSION['logged_in']): ?>
                <span style="margin-left:20px;">Welcome, <strong><?= htmlspecialchars($_SESSION['username']) ?></strong>!</span>
                <a href="<?= isset($base_path) ? $base_path : '' ?>game.php">🎮 Play Game</a>
                <a href="<?= isset($base_path) ? $base_path : '' ?>achievements.php">🏆 Achievements</a>
                <a href="<?= isset($base_path) ? $base_path : '' ?>api/logout.php">🚪 Logout</a>
            <?php else: ?>
                <a href="<?= isset($base_path) ? $base_path : '' ?>api/login.php">🔑 Login</a>
                <a href="<?= isset($base_path) ? $base_path : '' ?>api/register.php">📝 Register</a>
            <?php endif; ?>
            <button id="theme-toggle" style="float:right;margin-left:2em;">🌙 Dark Mode</button>
        </div>
    </nav>
</header>

<main>

<script>
// Theme toggle and Background Music Control
document.addEventListener('DOMContentLoaded', function() {
    const themeBtn = document.getElementById('theme-toggle');
    const bgMusic = document.getElementById('bg-music');
    const musicToggle = document.getElementById('music-toggle');
    const volumeSlider = document.getElementById('volume-slider');
    
    // Theme toggle
    function setTheme(theme) {
        document.body.classList.toggle('theme-dark', theme === 'dark');
        localStorage.setItem('theme', theme);
        if (themeBtn) {
            themeBtn.textContent = theme === 'dark' ? '☀️ Light Mode' : '🌙 Dark Mode';
        }
    }
    
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    
    if (themeBtn) {
        themeBtn.onclick = function() {
            const newTheme = document.body.classList.contains('theme-dark') ? 'light' : 'dark';
            setTheme(newTheme);
        };
    }
    
    // Background Music Control
    if (bgMusic) {
        bgMusic.volume = 0.15;
        
        // Try to autoplay (may be blocked by browser)
        bgMusic.play().catch(() => {
            console.log('Autoplay prevented. Click to enable music.');
        });
        
        // Toggle music on/off
        if (musicToggle) {
            musicToggle.onclick = function() {
                if (bgMusic.paused) {
                    bgMusic.play();
                    musicToggle.textContent = '🔊';
                    localStorage.setItem('musicEnabled', 'true');
                } else {
                    bgMusic.pause();
                    musicToggle.textContent = '🔇';
                    localStorage.setItem('musicEnabled', 'false');
                }
            };
        }
        
        // Volume slider control
        if (volumeSlider) {
            volumeSlider.oninput = function() {
                bgMusic.volume = this.value / 100;
                localStorage.setItem('musicVolume', this.value);
            };
            
            // Load saved volume
            const savedVolume = localStorage.getItem('musicVolume');
            if (savedVolume) {
                volumeSlider.value = savedVolume;
                bgMusic.volume = savedVolume / 100;
            }
        }
        
        // Load music state
        if (localStorage.getItem('musicEnabled') === 'false') {
            bgMusic.pause();
            if (musicToggle) {
                musicToggle.textContent = '🔇';
            }
        }
    }
});
</script>
