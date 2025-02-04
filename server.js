const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());  // Middleware to parse JSON requests

// Initialize the SQLite database
const db = new sqlite3.Database('mood_tracker.db', (err) => {
  if (err) {
    console.error("Error opening database:", err);
  } else {
    console.log('Database connected.');
  }
});

// Create the mood_logs table (if it doesn't exist)
db.run(`
  CREATE TABLE IF NOT EXISTS mood_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    mood TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

// Route to log mood
app.post('/log_mood', (req, res) => {
  const { user_id, mood } = req.body;
  if (!user_id || !mood) {
    return res.status(400).send("User ID and mood are required.");
  }

  // Insert the mood data into the database
  db.run('INSERT INTO mood_logs (user_id, mood) VALUES (?, ?)', [user_id, mood], function (err) {
    if (err) {
      return res.status(500).send("Error logging mood.");
    }
    res.status(200).send({ message: "Mood logged successfully!", id: this.lastID });
  });
});

// Route to get mood history
app.get('/get_mood_history/:user_id', (req, res) => {
  const { user_id } = req.params;

  db.all('SELECT * FROM mood_logs WHERE user_id = ? ORDER BY timestamp DESC', [user_id], (err, rows) => {
    if (err) {
      return res.status(500).send("Error fetching mood history.");
    }
    res.status(200).json(rows);
  });
});

// Start the server
const port = 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
