<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deal or No Deal</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Hero Section -->
        <div class="hero">
            <h1 class="game-title">DEAL OR NO DEAL</h1>
            <p class="tagline">Risk it all... or take the offer?</p>
        </div>

        <!-- Introduction Section -->
        <div class="intro-box">
            <h2>How to Play</h2>
            <div class="rules">
                <div class="rule-item">
                    <span class="step-number">1.</span>
                    <p><strong>Choose your briefcase</strong> - Pick one to keep as yours. You won't know what's inside!</p>
                </div>
                <div class="rule-item">
                    <span class="step-number">2.</span>
                    <p><strong>Open other cases</strong> - Each round, reveal what's inside other briefcases.</p>
                </div>
                <div class="rule-item">
                    <span class="step-number">3.</span>
                    <p><strong>Get an offer</strong> - After each round, the Banker makes you an offer based on what's left.</p>
                </div>
                <div class="rule-item">
                    <span class="step-number">4.</span>
                    <p><strong>Decide</strong> - Take the deal and walk away, or keep going for what's in YOUR case?</p>
                </div>
            </div>
            <!-- Prize Information Section -->
            <div class="prize-info">
                <h3>Prize Range</h3>
                <p>From <strong>$1</strong> to <strong>$500,000</strong></p>
                <p class="small-text">15 briefcases. Only one is yours. Make the right choice!</p>
            </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-box">
            <form action="game.php" method="POST">
                <button type="submit" name="start_game" class="btn-start">
                    Start Game
                </button>
            </form>
            <a href="about.php" class="btn-link">Learn More</a>
        </div>

        <!-- Footer -->
        <footer>
            <p>Good luck!</p>
        </footer>
    </div>
</body>
</html>
