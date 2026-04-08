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
git clone https://github.com/bemndy/weather-space-app.git
cd weather-space-app 
```


### 2. Create a Virtual Environment

Create a virtual environment to isolate project dependencies.

Mac/Linux:

```bash
python3 -m venv venv
```

Windows:

```bash
python -m venv venv
```



### 3. Activate the Virtual Environment

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```


### 4. Install Dependencies

Install all required Python packages.

```bash
pip install -r requirements.txt
```


### 5. Apply Database Migrations

```bash
python manage.py migrate
```


### 6. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```


### 7. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and go to:

```
http://127.0.0.1:8000/
```


# Project Structure

Describe here how you organized your repo. For example:

```
weather-space-app/
│
├── manage.py
├── requirements.txt
├── db.sqlite3
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
│
└── /login
    ├── models.py
    ├── views.py
    ├── urls.py
    └── templates/

```
