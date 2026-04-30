# About The Project

At its core, worNDly is meant to be a fun game where users get 6 chances to guess a 5-letter word. Each guess provides feedback in the form of color-coded clues, guiding players towards the correct answer. The game combines vocabulary skills with logical deduction, offering a daily challenge that has captured the interest of word enthusiasts around the world.

# Getting Started

## Prerequisites

Make sure you have the following installed:

* Python 3.x
  [https://www.python.org/downloads/](https://www.python.org/downloads/)

* Git
  [https://git-scm.com/](https://git-scm.com/)

Check installation:

```bash
python --version
git --version
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/bemndy/worNDly.git
cd worNDly
```

### 2. Create a Virtual Environment

Mac/Linux:

```bash
python3 -m venv .venv
```

Windows:

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

Mac/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 5. Apply Database Migrations

```bash
python3 manage.py migrate
```

### 6. Create a Superuser (Optional)

```bash
python3 manage.py createsuperuser
```

### 7. Get your access token

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "your username", "password": "your password"}' https://jcssantos.pythonanywhere.com/api/token/
```

The response will be in the format of

```bash
{"refresh":"a-refresh-token","access":"an-access-token"}
```

Copy the token with of the "access" attribute

### 8. Create a .env file with .env.template

```bash
cp .env.template .env
```

Inside the .env file, fill in the ACCESS_TOKEN variable

```bash
ACCESS_TOKEN={your access token}
```

### 9. Run the Development Server

```bash
python3 manage.py runserver
```

Open your browser and go to:

```
http://localhost:8000/
```

# Project Structure

```
worNDly/
│
├── manage.py
├── requirements.txt
├── db.sqlite3
├── .env.template
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   └── base.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│       └── worNDly_logo.png
│
├── accounts/
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   └── templates/
│       └── accounts/
│           ├── login.html
│           └── register.html
│
├── game/
│   ├── views.py
│   ├── models.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   └── templates/
│       └── game/
│           ├── game.html
│           └── language_select.html
│
├── tokens/
│   ├── views.py
│   ├── models.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   └── templates/
│       └── tokens/
│           └── token_balance.html
│
└── words/
    ├── en.txt
    ├── es.txt
    ├── fr.txt
    ├── de.txt
    └── pt.txt
```

# URL Structure

```
/                               Home (redirects based on auth)
│
├── login/                      Login page (logged out)
├── logout/                     Logout (not valid page *django class-based)
├── signup/                     Register page (logged out)
│
├── game/                       Game dashboard / history & stats (logged in)
├── game/select/                Language selection (logged in)
├── game/<language>/start/      Start a new game (logged in)
├── game/<game_id>/play/        Active game board (logged in)
├── game/<game_id>/guess/       Submit a guess (logged in)
│
├── tokens/                     Token store / buy plays (logged in)
├── tokens/buy-play/            Purchase a play (end point redirect)
│
└── admin/                      Django admin panel (superuser)
```

# Phase 2 Deliverables

| Deliverable | Location |
|-------------|----------|
| Phase 2 Report | `Phase_2_Report_Group22.pdf` (root of repo and Gradescope) |
| Source Code | Root of repo (`config/`, `accounts/`, `game/`, `tokens`) |
| README | `README.md` |
| CONTRIBUTIONS | `CONTRIBUTIONS.md` |

**Features implemented:** 

1.1 (Create User Profile),
1.2 (Log-in),
1.3 (Log-out),
2.1 (Play Game),
3.1 (View all prior plays),
3.2 (Viewing basic statistics),
4.1 (Buying more games)
