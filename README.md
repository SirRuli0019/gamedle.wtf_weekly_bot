# Gamedle Bot

An automated bot for completing Gamedle weekly challenges.

## ⚠️ Disclaimer

This project is created for **educational purposes only**. It is not intended to "break" or exploit the game, but rather as a learning exercise in web automation and browser interaction with Selenium.

## 📋 Requirements

- **Python 3.7+**
- **Selenium** library
- **Chrome** or **Brave** browser installed

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/Anghios/gamedle.wtf_weekly_bot.git
cd gamedle.wtf_weekly_bot
```

2. Install required dependencies:
```bash
pip install selenium
```

## 🎮 Usage

Run the bot:
```bash
python gamedle_bot.py
```

The bot will prompt you to:
1. Select your browser (Chrome or Brave)
2. Enter the week number you want to complete

The bot will automatically:
- Navigate to the weekly challenge
- Extract game information from network requests
- Complete all games in the weekly challenge
- Ask if you want to play another week

## 🌐 Browser Support

- ✅ Google Chrome
- ✅ Brave Browser

## 📝 Notes

- This bot is **only tested with weekly mode** (`/weekly/`)
- Other game modes have not been tested and may not work
- The bot automatically handles consent dialogs
- Each new week opens a fresh browser instance
- ⚠️ **Important**: Do not minimize the browser window while the bot is running. Minimizing will cause an exception and the bot will close

## ❓ FAQ

**Q: Is this bot detectable by Gamedle?**
A: I believe it's not detectable since it simulates legitimate browser navigation, but I'm not 100% sure. Use at your own risk.

**Q: Can I save/export my progress with a token?**
A: Not at the moment. This feature is not currently implemented.

## 🙏 Acknowledgments

Special thanks to:
- **[Ruli](https://x.com/RuliHamakuka)** for the idea and curiosity
- **Markitos** :)

## 📜 License

This project is provided as-is for educational purposes.
