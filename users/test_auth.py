import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

# -----------------------------------------------------------------------------
# Fixtures (Configuración reutilizable)
# -----------------------------------------------------------------------------

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "user@example.com",
        "password": "UserPass123!",
        "role": "user"
    }

@pytest.fixture
def admin_data():
    return {
        "username": "adminuser",
        "email": "admin@example.com",
        "password": "AdminPass123!",
        "role": "admin"
    }

@pytest.fixture
def normal_user(user_data):
    return User.objects.create_user(**user_data)

@pytest.fixture
def admin_user(admin_data):
    return User.objects.create_user(**admin_data)

@pytest.fixture
def user_tokens(api_client, normal_user, user_data):
    """Obtiene tokens (access y refresh) para el usuario normal"""
    response = api_client.post(reverse('login'), {
        "username": user_data["username"],
        "password": user_data["password"]
    })
    return response.data

@pytest.fixture
def admin_tokens(api_client, admin_user, admin_data):
    """Obtiene tokens (access y refresh) para el usuario admin"""
    response = api_client.post(reverse('login'), {
        "username": admin_data["username"],
        "password": admin_data["password"]
    })
    return response.data

# -----------------------------------------------------------------------------
# Suite de Tests de Autenticación
# -----------------------------------------------------------------------------

@pytest.mark.django_db
class TestAuthAPI:

    def test_register_success(self, api_client):
        """Verifica que un usuario se pueda registrar correctamente."""
        url = reverse('register')
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "NewPass123!",
            "role": "user"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="newuser").exists()

    def test_register_invalid_data(self, api_client):
        """Verifica que falle el registro con datos incompletos."""
        url = reverse('register')
        data = {"username": "", "password": "123"}  # Datos inválidos
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_success(self, api_client, normal_user, user_data):
        """Verifica login exitoso y recepción de tokens."""
        url = reverse('login')
        data = {"username": user_data["username"], "password": user_data["password"]}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_invalid_credentials(self, api_client, normal_user, user_data):
        """Verifica fallo de login con contraseña incorrecta."""
        url = reverse('login')
        data = {"username": user_data["username"], "password": "WrongPassword"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_refresh_success(self, api_client, user_tokens):
        """Verifica que se pueda obtener un nuevo access token con el refresh token."""
        url = reverse('token_refresh')
        data = {"refresh": user_tokens["refresh"]}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_profile_access_success(self, api_client, normal_user, user_tokens):
        """Verifica acceso al perfil con token válido."""
        url = reverse('user_profile')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_tokens["access"]}')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == normal_user.username

    def test_profile_access_no_token(self, api_client):
        """Verifica rechazo (401) al intentar acceder sin token."""
        url = reverse('user_profile')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_only_access_as_admin(self, api_client, admin_user, admin_tokens):
        """Verifica que un admin pueda acceder a la ruta protegida."""
        url = reverse('admin_only')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_tokens["access"]}')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_admin_only_access_as_user(self, api_client, normal_user, user_tokens):
        """Verifica que un usuario normal NO pueda acceder a la ruta de admin (403)."""
        url = reverse('admin_only')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_tokens["access"]}')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_logout_success(self, api_client, user_tokens):
        """Verifica logout exitoso (blacklist del refresh token)."""
        url = reverse('logout')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_tokens["access"]}')
        data = {"refresh": user_tokens["refresh"]}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_205_RESET_CONTENT

    def test_use_blacklisted_token(self, api_client, user_tokens):
        """Verifica que un token en blacklist no sirva para refrescar."""
        # 1. Logout para enviar el token a la blacklist
        logout_url = reverse('logout')
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_tokens["access"]}')
        api_client.post(logout_url, {"refresh": user_tokens["refresh"]})

        # 2. Intentar usar el mismo refresh token
        refresh_url = reverse('token_refresh')
        api_client.credentials() # Limpiamos credenciales por seguridad
        response = api_client.post(refresh_url, {"refresh": user_tokens["refresh"]})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
