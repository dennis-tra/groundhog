# Groundhog

Groundhog day - A telegram bot that sends you day in day out the same questions 
about your mood and saves it to a Google Spreadsheet.

## Setup
The following environment variables need to be set:
```
TELEGRAM_API_TOKEN=
TELEGRAM_CHAT_ID=
SPREADSHEET_KEY=
MOOD_WORKSHEET_NAME=
NOTE_WORKSHEET_NAME=
SERVICE_ACCOUNT_CREDENTIALS=
```

The `SERVICE_ACCOUNT_CREDENTIALS` json has the following format:
```json
{  
   "type":"service_account",
   "project_id":"groundhog-232422",
   "private_key_id":"",
   "private_key":"-----BEGIN PRIVATE KEY-----\nGIBBERISH\n-----END PRIVATE KEY-----\n",
   "client_email":"xxx@xxx.iam.gserviceaccount.com",
   "client_id":"123456789",
   "auth_uri":"https://accounts.google.com/o/oauth2/auth",
   "token_uri":"https://oauth2.googleapis.com/token",
   "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
   "client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/xxxxx"
}
```
In order to pass the JSON to the environment variable you need to remove the new-lines and have
the JSON in one long line.

## Licence
MIT