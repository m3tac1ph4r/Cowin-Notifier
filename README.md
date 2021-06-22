# Cowin Notifier
![visitors](https://visitor-badge.laobi.icu/badge?page\_id=m3tac1ph4r.Cowin-Notifier)
![Python](https://img.shields.io/badge/-Python-000000?style=flat&logo=python)
<img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99" alt="Star Badge"/>

## About
Cowin-Notifer is a simple telegram bot that automatically sends notification regarding the availability of vaccine in your district. This is also a real time tracker of vaccine , you can check availability of vaccine using command /vaxinfo . You can host this bot in on your device.

---
## Installation
1. Clone the repo  `git clone https://github.com/`
2. Install dependencies `pip install python-decouple pyTelegramBotAPI time datetime requests`  [Docs](https://pypi.org/project/pyTelegramBotAPI/)
4. [Create a telegram bot using BotFather](https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot)
5. Put the Bot's API Token in the .env file
6. Run  `python3 main.py`
7. Run  `python3 vaccine.py`
8. Enjoy
---
## Note
On 6th May 2021, CoWin API added caching and rate limits. The public API data would be cached upto 30 minutes, so the alerts wouldn't be so instant in busy areas, which reduced this bot's functionality to being a nice UI for public CoWin site in Telegram.

---
## Demo
[![asciicast](https://asciinema.org/a/419770.svg)](https://asciinema.org/a/419770)

1.Now open your bot in telegram and click start.

2.Then click notify-start and then give the required details.


---
## Made with Love <3 
* [Ashutosh Gupta](https://www.linkedin.com/in/ashutoshg547/)
* [Shubham Arya](https://github.com/ev1lm0rty)

