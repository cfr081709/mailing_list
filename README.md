# Mailing List

A simple local mailing list app with a Node.js server, a basic HTML signup form, and a Python email sender.

## Project structure

- `src/public/index.html` — signup page
- `src/server/server.js` — Express server for collecting subscriptions
- `data/emails.csv` — CSV storage for subscriber emails
- `src/email_sender.py` — Python sender script for emailing subscribers

## Run locally

### Web app

```bash
npm install
npm start
```

Then open http://localhost:3000.

### Email sender

Set your Gmail credentials as environment variables:

```bash
export EMAIL_SENDER="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
```

Then run:

```bash
python src/email_sender.py
```

## License

This project is licensed under the MIT License.
