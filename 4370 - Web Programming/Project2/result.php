<?php
session_start();
require_once 'functions.php';

// Make sure there's a game to show results for
if (!isset($_SESSION['game_state']) || $_SESSION['game_state'] !== 'deal_accepted') {
    header('Location: index.php');
    exit;
}

$playerCase = $_SESSION['player_case'];
$playerCaseValue = $_SESSION['case_values'][$playerCase];
$acceptedOffer = $_SESSION['accepted_offer'];

// Did they do better or worse?
$difference = $playerCaseValue - $acceptedOffer;
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deal or No Deal - Results</title>
    <link rel="stylesheet" href="style.css">
</head>
<body class="result-body">
    
    <div class="result-container">
        
        <h1 class="result-title">The Results Are In!</h1>
        
        <!-- What they won -->
        <div class="result-box won-box">
            <h2>You Won</h2>
            <div class="result-amount big">
                <?php echo formatMoney($acceptedOffer); ?>
            </div>
        </div>
        
        <!-- What was in their case -->
        <div class="result-box case-box">
            <h2>Your Case (#<?php echo $playerCase; ?>) Contained</h2>
            <div class="result-amount">
                <?php echo formatMoney($playerCaseValue); ?>
            </div>
        </div>
        
        <!-- The verdict -->
        <div class="verdict-box">
            <?php if ($difference > 0): ?>
                <!-- They left money on the table -->
                <div class="verdict bad">
                    <h3>Ouch!</h3>
                    <p>You left <strong><?php echo formatMoney($difference); ?></strong> on the table!</p>
                    <p>But hey, you still won <?php echo formatMoney($acceptedOffer); ?>!</p>
                </div>
            <?php elseif ($difference < 0): ?>
                <!-- They made a smart deal -->
                <div class="verdict good">
                    <h3>Smart Move!</h3>
                    <p>You got <strong><?php echo formatMoney(abs($difference)); ?></strong> more than what was in your case!</p>
                    <p>Great instincts!</p>
                </div>
            <?php else: ?>
                <!-- Exactly the same -->
                <div class="verdict neutral">
                    <h3>Unbelievable!</h3>
                    <p>The offer matched your case EXACTLY!</p>
                    <p>What are the odds?!</p>
                </div>
            <?php endif; ?>
        </div>
        
        <!-- Other case info (if they made it to final round) -->
        <?php
        $remaining = getRemainingCases();
        if (count($remaining) === 1):
            $otherCase = $remaining[0];
            $otherValue = $_SESSION['case_values'][$otherCase];
        ?>
        <div class="other-case-box">
            <p>The other case (#<?php echo $otherCase; ?>) had: <strong><?php echo formatMoney($otherValue); ?></strong></p>
        </div>
        <?php endif; ?>
        
        <!-- Stats -->
        <div class="stats-box">
            <h3>Game Stats</h3>
            <ul>
                <li>Rounds played: <strong><?php echo $_SESSION['round']; ?></strong></li>
                <li>Cases opened: <strong><?php echo count($_SESSION['opened_cases']); ?></strong></li>
                <li>Your case number: <strong><?php echo $playerCase; ?></strong></li>
            </ul>
        </div>
        
        <!-- Play again -->
        <div class="action-buttons">
            <form method="POST" action="game.php">
                <button type="submit" name="start_game" class="btn-play-again">
                    Play Again
                </button>
            </form>
            <a href="index.php" class="btn-home">Home</a>
        </div>
        
    </div>
    
</body>
</html>
