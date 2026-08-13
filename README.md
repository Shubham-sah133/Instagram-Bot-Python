# 📸 Instagram Follow & Unfollow Automation

A Python-based Instagram automation project built with **Instagrapi**. The application manages selected follow and unfollow activities, keeps track of followed users using a JSON file, and schedules daily automation sessions.

This project was created as a learning project to practice Python automation, API/client libraries, file handling, JSON data management, environment variables, session management, date/time operations, and task scheduling.

> ⚠️ **Important:** Automated activity on social media platforms may be restricted by their terms, policies, or technical limits. Use this project only with accounts you own or are authorized to automate, and review Instagram's current policies before using it.

---

## 🚀 Features

* 🔐 Instagram login using environment variables
* 💾 Persistent login session using `session.json`
* 👥 Load existing Instagram followings
* 🔎 Check potential users before following
* 📊 Filter users based on follower count
* 🚫 Option to exclude business accounts
* #️⃣ Find potential users through hashtag media
* ➕ Follow selected users
* 📝 Record followed users in a JSON log
* ⏳ Assign randomized future unfollow dates
* 🔄 Automatically unfollow users whose scheduled date has arrived
* ⏰ Schedule daily automation sessions
* 🎲 Randomize session times and delays

---

## 🛠️ Technologies Used

* **Python 3**
* **Instagrapi** — Instagram client library
* **python-dotenv** — Environment variable management
* **Schedule** — Task scheduling
* **JSON** — Follow tracking and local data storage
* **Datetime** — Date/time calculations
* **Random** — Randomized scheduling and delays
* **OS** — File and environment handling
* **Time** — Execution delays

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
```

### File Description

| File              | Description                                         |
| ----------------- | --------------------------------------------------- |
| `main.py`         | Main automation script                              |
| `.env`            | Stores Instagram credentials                        |
| `session.json`    | Stores the Instagrapi client session                |
| `follow_log.json` | Stores followed-user information and unfollow dates |
| `.gitignore`      | Prevents sensitive/local files from being committed |
| `README.md`       | Project documentation                               |

---

## ⚙️ Configuration

The application uses several configuration variables:

```python
follower_threshold = 800
follow_businesses = False
maximum_follows_per_session = 5
min_unfollow_days = 3
max_unfollow_days = 7
follow_log_file = "follow_log.json"
```

### Follower Threshold

```python
follower_threshold = 800
```

Potential accounts with a follower count greater than or equal to this value are skipped.

### Business Accounts

```python
follow_businesses = False
```

When set to `False`, business accounts are excluded.

### Follow Limit

```python
maximum_follows_per_session = 5
```

This variable represents the intended maximum number of follows per session.

### Unfollow Period

```python
min_unfollow_days = 3
max_unfollow_days = 7
```

When a user is followed, the program calculates a future unfollow date within this range.

---

## 🔐 Environment Variables

Instagram credentials are loaded using `python-dotenv`.

Create a `.env` file:

```env
EMAIL=your_instagram_username
PASSWORD=your_instagram_password
```

The application loads these values using:

```python
load_dotenv()

USERNAME = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
```

### ⚠️ Never commit `.env`

Add the following to `.gitignore`:

```gitignore
.env
session.json
follow_log.json
__pycache__/
*.pyc
```

This helps prevent credentials, session information, and local follow records from being uploaded to GitHub.

---

## 🔑 Login & Session Management

The `login_user()` function manages the Instagram client session.

The application:

1. Checks whether `session.json` exists.
2. Loads the saved session settings.
3. Attempts to log in.
4. Tests the session using the timeline feed.
5. If the existing session fails, the client settings are reset.
6. A new login is performed.
7. The new session settings are saved.

This allows the application to reuse an existing session instead of creating a new session every time it starts.

---

## 👥 Following System

The `follow_users()` function is responsible for following users discovered through recent hashtag media.

The process is:

```text
Hashtag
   ↓
Recent hashtag media
   ↓
Potential users
   ↓
Check user
   ↓
Apply filters
   ↓
Follow eligible user
   ↓
Record follow information
```

Before following an account, the application checks:

* Whether the user's information can be retrieved.
* Whether the account is a business account.
* Whether the follower count is below the configured threshold.
* Whether the account is already being followed.

---

## 🔎 User Filtering

The `check_user()` function determines whether an account is eligible.

The account is skipped when:

* User information cannot be retrieved.
* The account is a business account while business accounts are disabled.
* The account has reached the follower threshold.
* The account is already being followed.

---

## 📝 Follow Log

After successfully following an account, the application stores its information in:

```text
follow_log.json
```

Example:

```json
{
  "123456789": {
    "username": "example_user",
    "followed_at": "2026-08-13T10:30:00",
    "unfollow_after": "2026-08-17T18:45:00"
  }
}
```

The log stores:

* User ID
* Username
* Follow timestamp
* Scheduled unfollow timestamp

---

## 🔄 Unfollow System

The `unfollow_due_users()` function checks the follow log for users whose scheduled unfollow time has arrived.

The process is:

```text
Load follow log
      ↓
Check unfollow dates
      ↓
Find due users
      ↓
Attempt unfollow
      ↓
Remove successful records
```

If an unfollow operation fails, the user's record remains in the log so that it can be retried during a later run.

---

## ⏰ Session Scheduling

The project uses the `schedule` library to create daily automation sessions.

The application:

* Creates between 1 and 2 daily session slots.
* Selects times between 08:00 and 22:59.
* Avoids placing sessions too close together.
* Recreates the day's schedule.
* Checks for pending scheduled tasks every 30 seconds.

The scheduler runs continuously:

```python
while True:
    schedule.run_pending()
    time.sleep(30)
```

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repository.git
```

### 2. Navigate to the project

```bash
cd your-repository
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install instagrapi python-dotenv schedule
```

### 6. Configure `.env`

Create:

```env
EMAIL=your_instagram_username
PASSWORD=your_instagram_password
```

### 7. Run the application

```bash
python main.py
```

---

## 🧠 Concepts Practiced

This project demonstrates practical Python concepts including:

* Functions
* Dictionaries
* Sets
* Lists
* File handling
* JSON serialization/deserialization
* Environment variables
* Exception handling
* Date and time manipulation
* `datetime` and `timedelta`
* Random number generation
* Loops
* Conditional statements
* External libraries
* Session management
* Task scheduling
* Basic automation architecture

---

## 🔒 Security

Never upload sensitive information to GitHub.

Recommended `.gitignore`:

```gitignore
.env
session.json
follow_log.json
__pycache__/
*.pyc
```

The `.env` file may contain your Instagram credentials, while `session.json` may contain session information.

If credentials are accidentally committed to a repository, remove them from the repository and change the affected credentials immediately.

---

## ⚠️ Limitations & Considerations

This is a **learning project**, not a production-grade social media automation system.

Potential considerations include:

* Instagram may restrict or block automated activity.
* API/client behavior can change over time.
* Login/session behavior can vary.
* The script depends on third-party libraries.
* Credentials and session data must be protected.
* Automated social-media actions should comply with applicable platform policies.

Use the project only for accounts and activities you are authorized to automate.

---

## 🔮 Future Improvements

Possible improvements include:

* Add a command-line configuration system
* Add structured logging
* Improve exception handling
* Add configurable hashtags
* Add a dry-run/testing mode
* Add statistics and reports
* Separate configuration from application logic
* Add unit tests
* Use a database instead of JSON
* Add better scheduling controls
* Create a GUI for configuration and monitoring

---

## 👨‍💻 Author

**Shubham Kumar**

GitHub: https://github.com/Shubham-sah133

---

## ⭐ Support

If you found this project useful for learning Python automation, consider giving the repository a ⭐ on GitHub.
