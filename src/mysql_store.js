const pool = require('./config/database');

async function saveSubscriber(email) {
  const normalizedEmail = (email || '').trim().toLowerCase();

  if (!normalizedEmail) {
    throw new Error('Email is required.');
  }

  const connection = await pool.getConnection();
  try {
    await connection.execute(
      'CREATE TABLE IF NOT EXISTS emails (id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255) NOT NULL UNIQUE)'
    );

    await connection.execute(
      'INSERT IGNORE INTO emails (email) VALUES (?)',
      [normalizedEmail]
    );
  } finally {
    connection.release();
  }
}

module.exports = { saveSubscriber };
