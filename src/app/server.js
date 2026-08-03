

const express = require('express');
const path = require('path');
const { saveSubscriber } = require('../mysql_store');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/subscribe', async (req, res) => {
  const email = (req.body.email || '').trim().toLowerCase();

  if (!email) {
    return res.status(400).send('Please provide an email address.');
  }

  try {
    await saveSubscriber(email);
    res.redirect('/?success=1');
  } catch (error) {
    console.error(error);
    res.status(500).send(`Unable to save subscription: ${error.message}`);
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});