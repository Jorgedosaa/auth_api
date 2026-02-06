📌 Auth API — Django REST Framework + JWT (Enterprise Grade)
Autenticación profesional con Django REST Framework y SimpleJWT, incluyendo:

Registro de usuarios

Login con JWT

Refresh de tokens

Perfil del usuario autenticado

Roles (admin, user)

Endpoint protegido solo para administradores

Logout con blacklist de refresh tokens

Suite completa de tests automáticos con pytest

Este proyecto está diseñado como una base sólida para aplicaciones modernas que requieren autenticación robusta y escalable.

🚀 Tecnologías utilizadas
Tecnología	Uso
Django 6	Framework principal
Django REST Framework	API REST
SimpleJWT	Autenticación con tokens
Pytest + pytest-django	Tests automáticos
SQLite	Base de datos por defecto
📦 Instalación
Clona el repositorio:

bash
git clone https://github.com/tuusuario/auth_api.git
cd auth_api
Crea un entorno virtual:

bash
python3 -m venv venv
source venv/bin/activate
Instala dependencias:

bash
pip install -r requirements.txt
⚙️ Migraciones
bash
python manage.py makemigrations
python manage.py migrate
🧪 Ejecutar tests
Asegúrate de tener este archivo en la raíz:

pytest.ini
ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = tests.py test_*.py *_tests.py
Ejecuta:

bash
pytest -v
🔐 Endpoints principales
Registro
POST /api/auth/register/

Login
POST /api/auth/login/

Devuelve:

json
{
  "refresh": "...",
  "access": "..."
}
Refresh
POST /api/auth/refresh/

Perfil
GET /api/auth/profile/  
Requiere token.

Admin-only
GET /api/auth/admin-only/  
Requiere rol admin.

Logout
POST /api/auth/logout/  
Requiere:

Header: Authorization: Bearer <access>

Body:

json
{
  "refresh": "<refresh_token>"
}
🧱 Arquitectura del proyecto
Código
auth_api/
│── config/
│── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── test_auth.py  ← tests automáticos
│── pytest.ini
│── requirements.txt
│── manage.py
🧪 Tests incluidos
Registro exitoso

Registro inválido

Login exitoso

Login inválido

Refresh token

Acceso a perfil con token

Acceso a perfil sin token

Admin-only como admin

Admin-only como usuario normal

Logout exitoso

Refresh token bloqueado

Permisos por rol