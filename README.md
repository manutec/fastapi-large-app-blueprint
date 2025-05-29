# 🚀 FastAPI Scalable API Template

A scalable and modular FastAPI project template designed to build large-scale APIs with a clean and organized architecture. This starter project includes everything needed to start developing right away, including versioning, authentication, logging, database integration, and a sample setup.

---

## 📁 Project Structure

```
.
├── app/                    # Core application logic
│   ├── api/                # API versions (v1, v2, etc.)
│   │   ├── v1/
│   │   │   ├── routes/     # Route definitions for v1
│   │   │   │   └── __init__.py  # Groups v1 routes
│   │   │   └── services/   # Business logic for v1
│   ├── core/               # Core configuration and setup
│   │   ├── auth.py         # Authentication logic
│   │   ├── database.py     # DB configuration (SQLite/MySQL)
│   │   └── logger.py       # Logging setup
│   ├── middleware/         # Custom middleware
│   │   ├── cors_middleware.py
│   │   └── logger_middleware.py
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── helpers/            # Helper utilities per model
│   │   └── user_helper.py  # Example: password generation
│   └── utils/              # Generic utility functions
├── scripts/                # CLI tasks, cron jobs, etc.
├── tests/                  # Unit and integration tests
├── .env                    # Environment configuration
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Python dependencies
└── README.md               # Project overview
```

---

## 💠 Features

* ✅ Modular architecture with versioned APIs
* 🔒 Built-in authentication system
* 📂 Support for both SQLite and MySQL databases
* 📊 Custom logger configuration (console and file)
* 🧩 Middleware support (CORS, logging)
* 🔃 Dependency injection-ready services
* 🧪 Example routes and services for quick start
* 👤 Initial super admin with full permissions
* ⚙️ Easy environment setup with `.env`
* 📆 Scriptable utilities (cron jobs, CLI commands)

---

## ⚙️ Environment Setup

1. **Clone the repository:**

```bash
git clone https://github.com/manutec/fastapi-large-api-blueprint.git
cd fastapi-api-template
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**

Update `.env` with your desired settings:

```dotenv
APP_ENV=development
LOG_LEVEL_CONSOLE=debug
LOG_LEVEL_FILE=info

DB_ENGINE=sqlite
DB_NAME=app.db
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=supersecurepassword
```

4. **Run the API:**

```bash
uvicorn app.api.v1.routes:app --reload
```

---

## 🚧 API Versioning

Each major version of the API resides in its own directory under `app/api/`. This keeps route logic and services modular and maintainable.

Example structure for v1:

```
app/api/v1/
├── routes/
│   ├── __init__.py        # Includes and registers all v1 routes
│   └── user.py            # Sample route
└── services/
    └── user_service.py    # Logic for user-related operations
```

---

## 🧪 Sample Routes & Admin Setup

* On first launch, an **admin user** is created with full permissions.
* A couple of example routes and services are provided for reference (`users`, `health check`, etc.)

---

## 📂 Database Configuration

Two default database options:

* **SQLite** (default)
* **MySQL** (you can switch by changing `.env` and updating `core/database.py`)

---

## 📓 Scripts

Place any CLI utilities, cron jobs, or maintenance scripts in the `scripts/` folder. These are designed to run outside of the main API process.

---

## 📓 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 Contributions

Feel free to fork, adapt, and contribute to this template. PRs are welcome!
