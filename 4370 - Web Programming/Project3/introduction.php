<?php
session_start();
$title = "Introduction - Santa's Adaptive Christmas Fifteen Puzzle";
$base_path = '';
include 'includes/header.php';
?>

<link rel="stylesheet" href="css/introduction.css">

<div class="about-container">
    
    <!-- Introduction Section -->
    <div class="hero">
        <h1 class="game-title">Santa's Adaptive Christmas Fifteen Puzzle — Introduction</h1>
        <p class="tagline">An overview of the team and the project.</p>
    </div>
    
    <!-- Project overview grid -->
    <div class="about-section">
        <div class="team-grid">
            
            <div class="team-member">
                <h3>Project Leader</h3>
                <p><strong>Saquib S. Ahmed</strong></p>
            </div>
            
            <div class="team-member">
                <h3>Project Title</h3>
                <p><strong>Santa's Adaptive Christmas Fifteen Puzzle</strong></p>
            </div>
            
            <div class="team-member">
                <h3>Project Description</h3>
                <p>An adaptive festive sliding puzzle game featuring 5 progressive stages, dynamic difficulty levels, and a comprehensive achievement system. Built with PHP, MySQL, and vanilla JavaScript.</p>
            </div>
            
            <!-- Team members + roles -->
            <div class="team-member">
                <h3>Team Members & Roles</h3>
                <ul style="text-align: left; margin: 10px 0; padding-left: 20px;">
                    <li><strong>Saquib S. Ahmed</strong> — Team Leader & PHP Logic Developer</li>
                    <li><strong>Steven Acosta-Pliego</strong> — UI/UX Designer & CSS Specialist</li>
                    <li><strong>Vincent Shoulars</strong> — Tester & Documentation Specialist</li>
                </ul>
            </div>
            
        </div>
    </div>
    
    <!-- Index Button -->
    <div class="action-box">
        <a href="index.php" class="btn-start" aria-label="Go to Santa's Adaptive Christmas Fifteen Puzzle home page">Start Game</a>
    </div>
</div>

<?php include 'includes/footer.php'; ?>