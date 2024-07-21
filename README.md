
# My AI Assistant Bot

This project is a Telegram bot developed using the Pyrogram library. The bot provides AI-assisted responses and interacts through various commands.

## Requirements
Before running this project, you need to meet the following requirements:

- Python 3.8 or newer
- Required Python libraries (refer to `requirements.txt` file)

### Required Libraries
To install the libraries listed in `requirements.txt`, use the following command:

```sh
pip install -r requirements.txt
```

## Installation
### Step 1: Clone the Repository
```sh
git clone https://github.com/Suphiozturk8/ChatGPT-TgBot
cd ChatGPT-TgBot
```

### Step 2: Set Up Environment Variables
Create a `.env` file in the root directory of the project and copy the variables from `sample.env` to this file using the following command:

```sh
cp sample.env .env
```

Edit the values in the `.env` file with your API information:

```env
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN
API_BASE_URL=YOUR_API_BASE_URL
```

## Running
To start the bot, use the following command:

```sh
python main.py
```

## Usage
Once the bot is running, you can interact with it using the following commands:

- `/start`: Sends a welcome message.
- `/help`: Sends a help message.
- `/createchat`: Create a new chat session to save your messages.
- `/deletechat`: Delete an existing chat session.

The bot also responds to direct messages and provides AI-assisted replies.

## License
This project is licensed under the terms of the [GNU General Public License v3.0](LICENSE).
