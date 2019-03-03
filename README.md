# <img style="padding-right: 12px;" align="left" src="./logo.png" width="31"> Groundhog 

> Groundhog Day is a 1993 American comedy fantasy film [...]. It stars Bill Murray [...] who, during an assignment covering the annual Groundhog Day event, is caught in a time loop, repeatedly reliving the same day. - *[Wikipedia (Groundhog day)](https://en.wikipedia.org/wiki/Groundhog_Day_(film))*

**Groundhog** is a telegram bot that will send three daily reminders to track your current mood. 

* One in the morning
* One around noon
* One before going to bed

The mood rating will be a number between 0 and 5 and synced to a Google Spreadsheet. The bot makes use of a preconfigured keyboard in telegram that allows to handily enter your current mood. 

You can enter your mood any time you like. Same goes for arbitrary notes concerning your mood. Theses are synced to separate worksheet in the same Google Spreadsheet.

## Demo
![Animated Demo](showcase.gif)

## Credits

This project is heavily influenced by [krausefx/mood](https://github.com/KrauseFx/mood). Major differences lie in the programming language used (Python vs. Ruby) and the database backend. 

While it's not completely clear what exactly [krausefx/mood](https://github.com/KrauseFx/mood) is using as a database it'll certainly be some kind of relational database. Groundhog on the other hand uses Google Sheets.

## Setup
You can pull the latest docker image via
```
docker pull dennistra/groundhog:latest
```
To run a container make the following environment variables accessible inside the container:
```
TELEGRAM_API_TOKEN=
TELEGRAM_CHAT_ID=
SPREADSHEET_KEY=
MOOD_WORKSHEET_NAME=
NOTE_WORKSHEET_NAME=
SERVICE_ACCOUNT_CREDENTIALS=
```
Rename the `.env.example` file to `.env` and fill in the environment variables. Now run the container with the following command:
```
docker run --env-file .env dennistra/groundhog:latest
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