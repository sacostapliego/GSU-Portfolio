<?php
// Game configuration file
// This holds all the money values and round settings

// Define the money values for briefcases
// You can add or remove values to make the game easier/harder
define('MONEY_VALUES', [
    1,
    5,
    10,
    50,
    100,
    500,
    1000,
    5000,
    10000,
    25000,
    50000,
    75000,
    100000,
    200000,
    500000
]);

// Dynamic Round Structure - non-linear progression
// Can vary based on game state and player choices
define('CASES_PER_ROUND', [
    1 => 5,  // Round 1 - Start aggressive
    2 => 4,  // Round 2
    3 => 3,  // Round 3
    4 => 2,  // Round 4
    5 => 1,  // Round 5 and beyond
]);

// Bonus rounds can trigger mid-game (20% chance)
define('BONUS_ROUND_CHANCE', 20);

// Banker offer multipliers by round
// Early rounds = lower offers to keep tension
// Later rounds = higher offers as risk increases
define('BANKER_MULTIPLIERS', [
    1 => 0.35,  // 35% of average
    2 => 0.45,  // 45% of average
    3 => 0.60,  // 60% of average
    4 => 0.75,  // 75% of average
    5 => 0.85,  // 85% of average and up
]);

?>
