<?php
// Start session first!
session_start();

require_once 'functions.php';

// Always ensure game is initialized when page loads
// This must happen BEFORE any other checks
if (!isset($_SESSION['game_state']) || !isset($_SESSION['case_values'])) {
    startNewGame();
}

// Handle game actions FIRST before checking if game exists
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['start_game'])) {
        // Starting a fresh game
        startNewGame();
    } elseif (isset($_POST['choose_case'])) {
        // Player chose their briefcase
        $caseNum = intval($_POST['choose_case']);
        $_SESSION['player_case'] = $caseNum;
        $_SESSION['game_state'] = 'open_round_cases';
    } elseif (isset($_POST['open_case'])) {
        // Player opening a case during a round
        $caseNum = intval($_POST['open_case']);
        openCase($caseNum);
        
        // Check if round is done
        if (isRoundComplete()) {
            moveToOfferPhase();
        }
    } elseif (isset($_POST['decision'])) {
        // Player chose Deal or No Deal
        if ($_POST['decision'] === 'deal') {
            acceptDeal();
            header('Location: result.php');
            exit;
        } else {
            rejectDeal();
        }
    } elseif (isset($_POST['final_decision'])) {
        // Final choice: keep your case or swap
        if ($_POST['final_decision'] === 'keep') {
            $_SESSION['game_state'] = 'deal_accepted';
            $_SESSION['accepted_offer'] = $_SESSION['case_values'][$_SESSION['player_case']];
        } else {
            // Swap with last remaining case
            $remaining = getRemainingCases();
            $_SESSION['accepted_offer'] = $_SESSION['case_values'][$remaining[0]];
            $_SESSION['game_state'] = 'deal_accepted';
        }
        header('Location: result.php');
        exit;
    }
}

$gameState = $_SESSION['game_state'];
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deal or No Deal - Game Board</title>
    <link rel="stylesheet" href="style.css">
</head>
<body class="game-body">
    
    <div class="game-container">
        
        <!-- Header -->
        <div class="game-header">
            <h1>Deal or No Deal</h1>
            <?php if ($gameState !== 'choose_player_case'): ?>
                <p class="round-info">Round <?php echo $_SESSION['round']; ?></p>
            <?php endif; ?>
        </div>

        <!-- Main game area -->
        <div class="game-main">
            
            <!-- Left sidebar: Remaining values -->
            <?php if ($gameState !== 'choose_player_case'): ?>
            <div class="values-sidebar">
                <h3>Money Left</h3>
                <div class="values-grid">
                    <?php
                    $allValues = MONEY_VALUES;
                    $remainingValues = getRemainingValues();
                    
                    foreach ($allValues as $value) {
                        $isRemaining = in_array($value, $remainingValues);
                        $class = $isRemaining ? 'value-item' : 'value-item crossed';
                        echo "<div class='$class'>" . formatMoney($value) . "</div>";
                    }
                    ?>
                </div>
            </div>
            <?php endif; ?>
            
            <!-- Center: Game board -->
            <div class="game-board">
                
                <?php if ($gameState === 'choose_player_case'): ?>
                    <!-- Phase 1: Choose your case -->
                    <div class="instruction-box">
                        <h2>Choose Your Briefcase</h2>
                        <p>Pick one briefcase to keep. You won't see what's inside until the end!</p>
                    </div>
                    
                    <div class="cases-grid">
                        <?php foreach ($_SESSION['case_values'] as $caseNum => $value): ?>
                            <form method="POST" style="display: inline;">
                                <button type="submit" name="choose_case" value="<?php echo $caseNum; ?>" class="case-button">
                                    <span class="case-number"><?php echo $caseNum; ?></span>
                                </button>
                            </form>
                        <?php endforeach; ?>
                    </div>
                
                <?php elseif ($gameState === 'open_round_cases'): ?>
                    <!-- Phase 2: Open cases this round -->
                    <div class="instruction-box">
                        <h2>Open <?php echo getCasesLeftThisRound(); ?> More Case<?php echo getCasesLeftThisRound() !== 1 ? 's' : ''; ?></h2>
                        <p>Click on briefcases to reveal their values.</p>
                    </div>
                    
                    <div class="cases-grid">
                        <?php foreach ($_SESSION['case_values'] as $caseNum => $value): ?>
                            <?php if ($caseNum === $_SESSION['player_case']): ?>
                                <!-- Player's case -->
                                <div class="case-button player-case">
                                    <span class="case-number"><?php echo $caseNum; ?></span>
                                    <span class="case-label">YOUR CASE</span>
                                </div>
                            <?php elseif (in_array($caseNum, $_SESSION['opened_cases'])): ?>
                                <!-- Already opened case -->
                                <div class="case-button opened-case">
                                    <span class="case-number"><?php echo $caseNum; ?></span>
                                    <span class="case-value"><?php echo formatMoney($value); ?></span>
                                </div>
                            <?php else: ?>
                                <!-- Available to open -->
                                <form method="POST" style="display: inline;">
                                    <button type="submit" name="open_case" value="<?php echo $caseNum; ?>" class="case-button">
                                        <span class="case-number"><?php echo $caseNum; ?></span>
                                    </button>
                                </form>
                            <?php endif; ?>
                        <?php endforeach; ?>
                    </div>
                
                <?php elseif ($gameState === 'banker_offer'): ?>
                    <!-- Phase 3: Banker's offer with enhanced features -->
                    <div class="offer-panel">
                        <h2>The Banker's Offer</h2>
                        
                        <div class="offer-amount">
                            <?php echo formatMoney($_SESSION['current_offer']); ?>
                        </div>
                        
                        <?php
                        // Display banker strategy hint
                        $strategy = $_SESSION['banker_strategy'];
                        $strategyHints = [
                            'neutral' => 'The Banker seems calculating...',
                            'bluff' => 'The Banker seems unusually generous...',
                            'pressure' => 'The Banker seems impatient...'
                        ];
                        ?>
                        <p class="strategy-hint"><?php echo $strategyHints[$strategy]; ?></p>
                        
                        <p class="offer-question">Will you take it?</p>
                        
                        <div class="offer-buttons">
                            <form method="POST" style="display: inline;">
                                <button type="submit" name="decision" value="deal" class="btn-deal">
                                    DEAL
                                </button>
                            </form>
                            <form method="POST" style="display: inline;">
                                <button type="submit" name="decision" value="no-deal" class="btn-no-deal">
                                    NO DEAL
                                </button>
                            </form>
                        </div>
                        
                        <p class="offer-hint">
                            Cases left: <?php echo count(getRemainingValues()); ?>
                            <?php if ($_SESSION['offer_expiration']): ?>
                                <br><span class="expiration-warning">WARNING: Offer expires next round!</span>
                            <?php endif; ?>
                        </p>
                        
                        <?php
                        // Progressive Value Revelation (Round 3+)
                        $valueRange = getRevealedValueRange();
                        if ($valueRange !== null):
                        ?>
                            <div class="value-revelation">
                                <p><strong>Intelligence Report:</strong></p>
                                <p>Remaining values range from <?php echo formatMoney($valueRange['min']); ?> 
                                to <?php echo formatMoney($valueRange['max']); ?></p>
                            </div>
                        <?php endif; ?>
                        
                        <?php if (count($_SESSION['offer_history']) > 1): ?>
                            <div class="offer-history">
                                <p><small>Previous offer: <?php echo formatMoney($_SESSION['offer_history'][count($_SESSION['offer_history'])-2]['offer']); ?></small></p>
                            </div>
                        <?php endif; ?>
                    </div>
                
                <?php elseif ($gameState === 'final_choice'): ?>
                    <!-- Phase 5: Final two cases -->
                    <div class="offer-panel">
                        <h2>Final Decision</h2>
                        <p>Only two briefcases remain!</p>
                        
                        <?php
                        $remaining = getRemainingCases();
                        $otherCase = $remaining[0];
                        ?>
                        
                        <div class="final-cases">
                            <div class="final-case-box">
                                <div class="case-display player-case">
                                    <?php echo $_SESSION['player_case']; ?>
                                </div>
                                <p>Your Case</p>
                            </div>
                            <div class="vs">VS</div>
                            <div class="final-case-box">
                                <div class="case-display">
                                    <?php echo $otherCase; ?>
                                </div>
                                <p>Other Case</p>
                            </div>
                        </div>
                        
                        <p class="offer-question">Keep your case or swap?</p>
                        
                        <div class="offer-buttons">
                            <form method="POST" style="display: inline;">
                                <button type="submit" name="final_decision" value="keep" class="btn-deal">
                                    Keep Mine
                                </button>
                            </form>
                            <form method="POST" style="display: inline;">
                                <button type="submit" name="final_decision" value="swap" class="btn-no-deal">
                                    Swap
                                </button>
                            </form>
                        </div>
                    </div>
                    
                <?php endif; ?>
                
            </div>
            
        </div>
        
        <!-- Last opened case reveal if left -->
        <?php if ($gameState === 'open_round_cases' && $_SESSION['last_opened_case'] !== null): ?>
        <div class="last-reveal">
            <p>
                Case <?php echo $_SESSION['last_opened_case']; ?> contained: 
                <strong><?php echo formatMoney($_SESSION['case_values'][$_SESSION['last_opened_case']]); ?></strong>
            </p>
        </div>
        <?php endif; ?>
        
    </div>
    
</body>
</html>
