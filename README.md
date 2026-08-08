# Instagram Follow & Unfollow Automation

A Python-based Instagram automation script built with `instagrapi`. The project automates selected follow and unfollow tasks based on configurable conditions and maintains a local record of followed accounts.

The project is intended as a learning project for practicing Python automation, API/client libraries, JSON file handling, environment variables, session management, and task scheduling.

> **Important:** Automated interactions with Instagram may be subject to Instagram's Terms of Use and platform restrictions. Use automation responsibly and only with accounts and actions you are authorized to automate.

---

## 🚀 Features

- Instagram login using environment variables
- Persistent Instagram session management
- Load existing following accounts
- Filter potential users based on follower count
- Option to exclude business accounts
- Follow users from recent hashtag media
- Track followed users in a JSON file
- Assign an individual unfollow date to each followed account
- Automatically unfollow accounts when their scheduled date is reached
- Daily session scheduling
- Randomized session count and execution times
- Configurable follow and unfollow settings

---

## 🛠️ Technologies Used

- **Python 3**
- **Instagrapi** — Instagram client library
- **python-dotenv** — Environment variable management
- **Schedule** — Task scheduling
- **JSON** — Follow tracking and local data storage
- **OS** — File and environment handling
- **Datetime** — Date and time calculations
- **Random** — Randomized intervals and scheduling
- **Time** — Execution delays

---

## 📂 Project Structure

```text
InstagramAutomation/
│
├── main.py
├── .env
├── session.json
├── follow_log.json
├── .gitignore
└── README.md