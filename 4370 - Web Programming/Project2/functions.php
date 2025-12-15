<?php
// Core game functions

require_once 'config.php';

// Start a brand new game
function startNewGame() {
    // Shuffle the money values randomly
    $values = MONEY_VALUES;
    shuffle($values);
    
    // Assign each value to a briefcase number (1, 2, 3, etc.)
    $caseValues = [];
    foreach ($values as $index => $value) {
        $caseValues[$index + 1] = $value; // Cases numbered from 1
    }
    
    // Store everything in the session
    $_SESSION['case_values'] = $caseValues;
    $_SESSION['opened_cases'] = [];
    $_SESSION['player_case'] = null;
    $_SESSION['round'] = 1;
    $_SESSION['cases_opened_this_round'] = 0;
    $_SESSION['game_state'] = 'choose_player_case';
    $_SESSION['current_offer'] = 0;
    $_SESSION['accepted_offer'] = null;
    $_SESSION['last_opened_case'] = null;
    
    // Enhanced features
    $_SESSION['offer_history'] = []; // Track all banker offers
    $_SESSION['revealed_values'] = []; // Progressive value revelation
    $_SESSION['offer_expiration'] = null; // Strategic offer expiration
    $_SESSION['banker_strategy'] = 'neutral'; // neutral, bluff, pressure
}

// Get remaining (unopened) case numbers
function getRemainingCases() {
    $allCases = array_keys($_SESSION['case_values']);
    $openedCases = $_SESSION['opened_cases'];
    $playerCase = $_SESSION['player_case'];
    
    // Filter out opened cases and player's case
    $remaining = array_filter($allCases, function($case) use ($openedCases, $playerCase) {
        return !in_array($case, $openedCases) && $case !== $playerCase;
    });
    
    return array_values($remaining);
}

// Get the values still in play (unopened cases)
function getRemainingValues() {
    $remainingCases = getRemainingCases();
    $playerCase = $_SESSION['player_case'];
    
    // Add player's case to the remaining
    if ($playerCase !== null) {
        $remainingCases[] = $playerCase;
    }
    
    //Used to get Banker value by putting case values in list
    $values = [];
    foreach ($remainingCases as $caseNum) {
        $values[] = $_SESSION['case_values'][$caseNum];
    }
    
    return $values;
}

// Calculate the Banker's offer with strategic elements
function calculateBankerOffer() {
    $remainingValues = getRemainingValues();
    
    // Average of remaining values
    $average = array_sum($remainingValues) / count($remainingValues);
    
    // Get multiplier based on round
    $round = $_SESSION['round'];
    $multipliers = BANKER_MULTIPLIERS;
    
    // If round is beyond our list, use the last multiplier
    $multiplier = $multipliers[$round] ?? end($multipliers);
    
    // Banker's Strategic Offers - bluff or pressure tactics
    $strategy = ['neutral', 'bluff', 'pressure'][rand(0, 2)];
    $_SESSION['banker_strategy'] = $strategy;
    
    $strategyModifier = 1.0;
    if ($strategy === 'bluff') {
        // Banker bluffs with higher offer to pressure acceptance
        $strategyModifier = 1.20;
    } elseif ($strategy === 'pressure') {
        // Banker pressures with lower offer
        $strategyModifier = 0.80;
    }
    
    // Calculate base offer
    $offer = $average * $multiplier * $strategyModifier;
    
    // Add volatility randomness (±5%)
    $randomFactor = (rand(95, 105) / 100);
    $offer = $offer * $randomFactor;
    
    // Strategic offer expiration - offer expires after 1 round
    $_SESSION['offer_expiration'] = $_SESSION['round'] + 1;
    
    return round($offer);
}

// Open a briefcase
function openCase($caseNumber) {
    // Validate the case can be opened
    if (in_array($caseNumber, $_SESSION['opened_cases'])) {
        return false; // Already opened
    }
    
    if ($caseNumber == $_SESSION['player_case']) {
        return false; // Can't open player's own case
    }
    
    // Open it
    $_SESSION['opened_cases'][] = $caseNumber;
    $_SESSION['cases_opened_this_round']++;
    $_SESSION['last_opened_case'] = $caseNumber;
    
    return true;
}

// Check if round is complete
function isRoundComplete() {
    $round = $_SESSION['round'];
    $casesPerRound = CASES_PER_ROUND;
    
    // How many cases should be opened this round?
    $required = $casesPerRound[$round] ?? 1;
    
    return $_SESSION['cases_opened_this_round'] >= $required;
}

// Progressive Value Revelation - reveal value ranges as game progresses
function getRevealedValueRange() {
    $round = $_SESSION['round'];
    
    // Gradually reveal more information about remaining values
    if ($round >= 3) {
        $remaining = getRemainingValues();
        sort($remaining);
        return [
            'min' => min($remaining),
            'max' => max($remaining),
            'count' => count($remaining)
        ];
    }
    
    return null;
}

// Move to banker offer phase
function moveToOfferPhase() {
    $_SESSION['game_state'] = 'banker_offer';
    $offer = calculateBankerOffer();
    $_SESSION['current_offer'] = $offer;
    
    // Add to offer history for tracking
    $_SESSION['offer_history'][] = [
        'round' => $_SESSION['round'],
        'offer' => $offer,
        'strategy' => $_SESSION['banker_strategy'],
        'remaining_cases' => count(getRemainingValues())
    ];
}

// Accept the deal
function acceptDeal() {
    $_SESSION['accepted_offer'] = $_SESSION['current_offer'];
    $_SESSION['game_state'] = 'deal_accepted';
}

// Reject the deal and continue
function rejectDeal() {
    $_SESSION['round']++;
    $_SESSION['cases_opened_this_round'] = 0;
    
    // Check if only 2 cases left (player's + 1 other)
    $remaining = getRemainingCases();
    if (count($remaining) <= 1) {
        $_SESSION['game_state'] = 'final_choice';
    } else {
        $_SESSION['game_state'] = 'open_round_cases';
    }
}

// Format money with commas and dollar sign
function formatMoney($amount) {
    return '$' . number_format($amount);
}

// Get how many cases left to open this round
function getCasesLeftThisRound() {
    $round = $_SESSION['round'];
    $casesPerRound = CASES_PER_ROUND;
    $required = $casesPerRound[$round] ?? 1;
    
    return max(0, $required - $_SESSION['cases_opened_this_round']);
}

?>
