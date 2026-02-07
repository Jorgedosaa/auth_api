# Auth API — Enterprise Grade Authentication Service

A robust, scalable authentication microservice built with Django 6, Django REST Framework, and SimpleJWT. This project provides a secure foundation for modern applications requiring role-based access control (RBAC), JWT authentication with token blacklisting, and comprehensive test coverage.

## 🚀 Features

- **JWT Authentication**: Secure stateless authentication using SimpleJWT (Access & Refresh tokens).
- **Token Blacklisting**: Implements a blacklist mechanism to invalidate refresh tokens upon logout.
- **Role-Based Access Control (RBAC)**: Distinct access levels for `admin` and `user` roles.
- **Protected Endpoints**: Custom permissions ensuring only authorized users access specific resources.
- **User Management**: Registration and profile retrieval endpoints.
- **Enterprise Testing**: Full test suite using `pytest` covering success and failure scenarios.

## 🛠 Tech Stack

- **Framework**: Django 6 (Latest)
- **API Toolkit**: Django REST Framework (DRF)
- **Authentication**: SimpleJWT
- **Testing**: Pytest + pytest-django
- **Database**: SQLite (Default, easily swappable for PostgreSQL)

## 📦 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/auth_api.git
   cd auth_api
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

## ⚡ Usage

### Running the Server

Start the development server:

```bash
python manage.py runserver
```

The API will be available at http://127.0.0.1:8000/.

### Running Tests

Execute the full test suite to ensure system integrity:

```bash
pytest -v
```

## 🔐 API Endpoints

| Method | Endpoint                | Description                    | Auth Required |
| :----- | :---------------------- | :----------------------------- | :------------ |
| POST   | `/api/auth/register/`   | Register a new user            | ❌            |
| POST   | `/api/auth/login/`      | Obtain Access & Refresh tokens | ❌            |
| POST   | `/api/auth/refresh/`    | Get a new Access token         | ❌            |
| POST   | `/api/auth/logout/`     | Blacklist the Refresh token    | ✅            |
| GET    | `/api/auth/profile/`    | Get current user details       | ✅            |
| GET    | `/api/auth/admin-only/` | Admin-only restricted area     | ✅ (Admin)    |

## 📂 Project Structure

```text
auth_api/
├── config/               # Project configuration
├── users/                # Users application
│   ├── models.py         # Custom User model
│   ├── views.py          # API Controllers
│   ├── urls.py           # Route definitions
│   ├── serializers.py    # Data validation & transformation
│   ├── permissions.py    # Custom RBAC permissions
│   └── test_auth.py      # Pytest suite
├── requirements.txt      # Project dependencies
├── pytest.ini            # Test configuration
└── manage.py             # Django CLI utility
```

## 📝 Authentication Notes

This project uses JSON Web Tokens (JWT).

- **Access Token**: Short-lived (e.g., 5-15 minutes). Used to authenticate requests in the Authorization header: `Bearer <token>`.
- **Refresh Token**: Long-lived (e.g., 24 hours). Used to obtain new access tokens.
- **Logout**: When a user logs out, their refresh token is added to a blacklist, preventing it from being used to generate new access tokens. This enhances security by ensuring logged-out sessions are truly terminated.
