<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About - Deal or No Deal</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="about-container">
        
        <div class="hero">
            <h1 class="game-title">About the Game</h1>
        </div>
        
        <!-- What is Deal or No Deal -->
        <div class="about-section">
            <h2>What is Deal or No Deal?</h2>
            <p>
                Deal or No Deal is a high-stakes game of risk and strategy based on the popular TV game show.
                You'll be faced with tough decisions as you try to win as much money as possible!
            </p>
            <br>
            <p>
                The game tests your nerves, instincts, and ability to calculate risk. Will you play it safe
                and take the Banker's offer, or will you trust your gut and go all the way?
            </p>
        </div>
        
        <!-- How It Works -->
        <div class="about-section">
            <h2>How It Works</h2>
            <ol style="text-align: left; max-width: 600px; margin: 0 auto; line-height: 1.8;">
                <li><strong>Pick Your Case:</strong> Choose one briefcase from 15 available. This is YOUR case - you keep it until the end.</li>
                <li><strong>Reveal Other Cases:</strong> Each round, you'll open several other briefcases to reveal their values. These get eliminated from the game.</li>
                <li><strong>Banker Makes an Offer:</strong> After each round, the mysterious Banker calculates an offer based on the remaining values. This is real money you could walk away with!</li>
                <li><strong>Deal or No Deal?:</strong> Accept the offer (Deal) and end the game, or reject it (No Deal) and continue playing.</li>
                <li><strong>Final Showdown:</strong> If you make it to the end, only two cases remain - yours and one other. You can keep yours or swap!</li>
                <li><strong>Big Reveal:</strong> Find out what was in your case all along. Did you make the right choice?</li>
            </ol>
        </div>
        
        <!-- The Strategy -->
        <div class="about-section">
            <h2>The Strategy</h2>
            <p>
                Success in Deal or No Deal is all about understanding probabilities and managing risk:
            </p>
            <ul style="text-align: left; max-width: 600px; margin: 20px auto; line-height: 1.8;">
                <li><strong>Early Rounds:</strong> The Banker's offers are usually low. Keep playing if big amounts are still in play.</li>
                <li><strong>Watch the Board:</strong> If high values get eliminated, your chances of winning big decrease - consider taking the deal.</li>
                <li><strong>Trust Your Gut:</strong> Sometimes the numbers say one thing, but your instinct says another. This is your game!</li>
                <li><strong>Risk vs Reward:</strong> Every "No Deal" is a gamble. Are you a risk-taker or do you play it safe?</li>
            </ul>
        </div>
        
        <!-- Prize Values -->
        <div class="about-section">
            <h2>Prize Values</h2>
            <p>There are 15 briefcases with these amounts inside:</p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 20px; max-width: 500px; margin-left: auto; margin-right: auto;">
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$1</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$5</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$10</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$50</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$100</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$500</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$1,000</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$5,000</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$10,000</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$25,000</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$50,000</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$75,000</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$100,000</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">$200,000</div>
                <div style="padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px; color: #ffd700; font-weight: bold;">$500,000</div>
            </div>
        </div>
        
        <!-- Project Info -->
        <div class="about-section">
            <h2>Project Information</h2>
            <p>
                This game was created as a web programming project to demonstrate:
            </p>
            <ul style="text-align: left; max-width: 600px; margin: 20px auto; line-height: 1.8;">
                <li>PHP session management for game state</li>
                <li>Dynamic content generation and form handling</li>
                <li>CSS animations and transitions</li>
                <li>Responsive web design</li>
                <li>Game logic and probability calculations</li>
                <li>User experience design</li>
            </ul>
        </div>
        
        <!-- Team Section (customize this) -->
        <div class="about-section">
            <h2>Development Team</h2>
            <div class="team-grid">
                <div class="team-member">
                    <h3>Saquib S. Ahmed</h3>
                    <p>Team Leader & PHP Logic Developer</p>
                </div>
                <div class="team-member">
                    <h3>Steven Acosta-Pliego</h3>
                    <p>UI/UX Designer & CSS Specialist</p>
                </div>
                <div class="team-member">
                    <h3>Vincent Shoulars</h3>
                    <p>Tester & Documentation Specialist</p>
                </div>
            </div>
        </div>
        
        <!-- Back to Game -->
        <div class="action-box">
            <a href="index.php" class="btn-start">Back to Home</a>
        </div>
        
    </div>
</body>
</html>
