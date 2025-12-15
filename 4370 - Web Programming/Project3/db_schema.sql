-- Database schema for Santa's Adaptive Christmas Fifteen Puzzle

-- User management table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    theme_pref VARCHAR(20) DEFAULT 'light',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Game sessions table
CREATE TABLE game_sessions (
    session_id VARCHAR(50) PRIMARY KEY,
    user_id INT,
    start_time DATETIME,
    end_time DATETIME,
    moves INT,
    time INT,
    difficulty VARCHAR(20),
    completed TINYINT(1),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Puzzle storage table
CREATE TABLE puzzles (
    puzzle_id INT AUTO_INCREMENT PRIMARY KEY,
    layout TEXT NOT NULL,
    difficulty VARCHAR(20) NOT NULL
);

-- Analytics table
CREATE TABLE analytics (
    user_id INT PRIMARY KEY,
    total_sessions INT DEFAULT 0,
    avg_time FLOAT DEFAULT 0,
    avg_moves FLOAT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Indexes for performance
CREATE INDEX idx_sessions_user_id ON game_sessions(user_id);
CREATE INDEX idx_sessions_difficulty ON game_sessions(difficulty);
