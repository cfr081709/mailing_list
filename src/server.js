

const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const csvPath = path.join(__dirname, '..', 'data', 'emails.csv');

app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/subscribe', (req, res) => {
  const email = (req.body.email || '').trim().toLowerCase();

  if (!email) {
    return res.status(400).send('Please provide an email address.');
  }

  const timestamp = new Date().toISOString();
  const entry = `"${email}","${timestamp}"\n`;

  fs.appendFileSync(csvPath, entry, 'utf8');

  res.redirect('/?success=1');
});

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});