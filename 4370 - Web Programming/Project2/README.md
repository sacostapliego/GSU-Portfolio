# Deal or No Deal Web Game

A fully functional web-based implementation of the popular TV game show Deal or No Deal built with PHP, HTML, and CSS.

# Game Overview

Players choose a briefcase and progressively open other cases while the Banker makes offers. The tension builds as you decide whether to take the deal or risk it all for what's in your case!

# Project Structure


Deal_Or_NoDeal/
 -index.php          # Homepage with game intro and start button.
 -game.php           # Main game board (handles all gameplay).
 -result.php         # Final results screen.
 -about.php          # Rules, info, and team details.
 -config.php         # Game configuration (money values, rounds).
 -introduction.php   # A seperate introduction page.
 -functions.php      # All game logic functions.
 -style.css          # Complete styling with animations.
 -README.md          # This file


# How It Works

Game Flow

1. Start Game - Shuffles money values and assigns to cases
2. Choose Your Case - Player picks one case to keep
3. Open Cases - Each round, open a set number of cases
4. Banker Offer - Get an offer based on remaining values
5. Deal or No Deal - Accept offer or continue playing
6. Final Result - See what you won vs what was in your case

Key Features

Session Management: All game state stored in $_SESSION.
Random Shuffling: Each game has different case values.
Smart Banker AI: Offers calculated based on average of remaining values, round number, and random factor.
Progressive Rounds: Round 1 opens 5 cases, Round 2 opens 4 cases, Round 3 opens 3 cases, Round 4 opens 2 cases, Round 5+ opens 1 case each round.

Enhanced Features (Added)

1. Banker Strategic Offers
   Three strategies: neutral, bluff (20% higher), pressure (20% lower)
   Offer history tracking in session
   Offer expiration system (expires next round)

2. Progressive Value Revelation
   Starting Round 3, shows minimum and maximum value range
   Intelligence Report displayed on offer screen
   Helps player make informed decisions

3. Dynamic Round Structure
   Non-linear progression (5, 4, 3, 2, 1 cases per round)
   Bonus round system with 20% trigger chance
   Configurable in config.php

# Design Features

Responsive Design: Works on desktop and mobile.
Smooth Animations: Flip animation when cases open, pulsing glow on player's case, slide-up effect for offers, hover effects on clickable elements.
Visual Feedback: Green/crossed out remaining values, different colors for different game states, clear indicators for which case is yours.

# Technical Concepts Used

PHP Features.
Session management ($_SESSION).
Form handling (POST requests).
Functions and code organization.
Array manipulation (shuffle, array_filter).
Conditional logic and game state machine.
Include/require statements.

Frontend Features

Semantic HTML5.
CSS Grid and Flexbox.
CSS Animations and Transitions.
Responsive design with media queries.
Modern gradient backgrounds.
Backdrop filters for glassmorphism effect.


# Project Requirements Covered

This project demonstrates:

PHP session management.
Form processing (POST/GET).
Dynamic content generation.
Game logic implementation.
CSS styling and animations.
Responsive web design.
User experience design.
Code organization (separate config, functions, pages).
Banker strategic offers with history tracking.
Progressive value revelation.
Dynamic round structure.

# Game Configuration

You can customize the game in config.php:

Money values: Change the prize amounts.
Cases per round: Adjust difficulty.
Banker multipliers: Make offers more/less generous.

Example:
```php
// Make the game easier with fewer cases
define('MONEY_VALUES', [
    10, 50, 100, 500, 1000, 5000, 10000
]);

// Make Banker more generous
define('BANKER_MULTIPLIERS', [
    1 => 0.50,  // 50% instead of 35%
    2 => 0.65,
    // etc...
]);
```

# Testing Checklist

Test these scenarios:

Start a new game multiple times (values shuffle correctly).
Choose different cases as yours.
Open cases in each round.
Cannot click on opened cases.
Cannot click on your own case.
Accept a Deal (see results).
Reject all offers until final 2 cases.
Final choice: Keep vs Swap.
Play Again button works.
Mobile responsiveness.
Banker strategy hints display.
Value revelation appears after Round 3.
Offer expiration warnings show.

