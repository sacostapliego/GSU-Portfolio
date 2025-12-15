# Santa's Adaptive Christmas Fifteen Puzzle

Welcome to Santa's Adaptive Christmas Fifteen Puzzle! This is a festive, web-based sliding puzzle game where you can challenge yourself, unlock achievements, and enjoy a bit of holiday magic—all while helping Santa in his workshop.

## 🎄 What Makes This Game Special?
- **Classic 4x4 Puzzle:** Slide image tiles (not just numbers!) to complete a cheerful Christmas scene.
- **Festive Themes:** Switch between a cozy light Christmas look and a magical dark winter night.
- **Smooth Animations:** Tiles glide and UI elements transition for a polished, modern feel.
- **Adaptive Difficulty:** The game gets easier or harder based on how you play because Santa is always watching!
- **Power-Ups:** Use hints, freeze the timer, or shuffle a few tiles if you get stuck.
- **Achievements:** Earn fun titles like "Fast Solver" and "Holiday Hero" as you play.
- **Story Mode:** Unlock a heartwarming Santa’s Workshop story, one chapter at a time.
- **User Profiles:** Register and log in to save your progress, theme, and rewards.
- **Secure Backend:** All data is handled safely with PHP and MySQL (using prepared statements).

## 📁 Project Structure (What’s in the Box)
```
Santa's_Adaptive_Christmas/
├── api/         # All the PHP endpoints (game sessions, login, achievements, etc.)
├── assets/      # Images and other fun stuff
├── css/         # Stylesheets for the festive look
├── includes/    # Reusable PHP bits (header, footer, db connection)
├── js/          # JavaScript for the puzzle and UI
├── index.php    # Home page
├── game.php     # Where the magic happens (the puzzle)
├── result.php   # Results and story mode
├── db_schema.sql# Database schema (manual setup)
├── setup_db.sql # One-step database setup script
└── README.md    # This file
```


## 🚀 How to Get Started (Run Locally)

**Important:** MySQL is not set up by default! You must create the database and tables before the app will work.

1. **Set up the database:**
   - Open MySQL and run:
     ```
     SOURCE path/to/setup_db.sql;
     ```
   - This will create the required database and tables. If you skip this step, the app will not run!
2. **Copy the project folder** to your web server root (for XAMPP, use `C:/xampp/htdocs/`).
3. **Edit `includes/db.php`** if your MySQL username/password is not `root`/no password.
4. **Start Apache and MySQL** in your XAMPP/WAMP control panel.
5. **Open your browser:**
   - Go to [http://localhost/Santa's_Adaptive_Christmas/index.php](http://localhost/Santa's_Adaptive_Christmas/index.php)
6. **Register, log in, and enjoy the game!**

## ✅ What’s Working So Far
- All the backend logic (PHP, MySQL, sessions, API endpoints)
- The core puzzle engine and adaptive difficulty
- Theme system, power-ups, achievements, and story mode
- Basic UI and navigation

## ✨ What’s Coming Next (UI/UX Polish)
- Finalize the style guide and color palette
- Make it look great on phones and tablets
- Add more holiday animations (like snowfall and win celebrations)
- Create wireframes and docs for the team

