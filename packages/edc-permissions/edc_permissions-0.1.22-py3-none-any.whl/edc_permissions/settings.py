import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_NAME = "edc_permissions"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "fyb^npvycj&*z(+5u*r-bvwce)cd&ych!1&k#4d9-bkba!$!*c"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 40

ETC_DIR = BASE_DIR

EMAIL_CONTACTS = {"data_manager": "user@example.com"}
EMAIL_ENABLED = False

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_crypto_fields.apps.AppConfig",
    "edc_action_item.apps.AppConfig",
    "edc_appointment.apps.AppConfig",
    "edc_auth.apps.AppConfig",
    "edc_dashboard.apps.AppConfig",
    "edc_export.apps.AppConfig",
    "edc_lab.apps.AppConfig",
    "edc_lab_dashboard.apps.AppConfig",
    "edc_locator.apps.AppConfig",
    "edc_metadata.apps.AppConfig",
    "edc_metadata_rules.apps.AppConfig",
    "edc_navbar.apps.AppConfig",
    "edc_notification.apps.AppConfig",
    "edc_offstudy.apps.AppConfig",
    "edc_pharmacy.apps.AppConfig",
    "edc_registration.apps.AppConfig",
    "edc_reference.apps.AppConfig",
    # 'edc_pharmacy_dashboard.apps.AppConfig',
    "edc_permissions.apps.AppConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "edc_dashboard.middleware.DashboardMiddleware",
    "edc_subject_dashboard.middleware.DashboardMiddleware",
    "edc_lab_dashboard.middleware.DashboardMiddleware",
]

ROOT_URLCONF = "edc_permissions.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "edc_permissions.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"

DASHBOARD_URL_NAMES = {
    "subject_listboard_url": "edc_subject_dashboard:subject_listboard_url",
    "subject_dashboard_url": "edc_subject_dashboard:subject_dashboard_url",
}

LAB_DASHBOARD_REQUISITION_MODEL = "edc_lab.subjectrequisition"
LAB_DASHBOARD_URL_NAMES = {}
LAB_DASHBOARD_BASE_TEMPLATES = {}

EDC_BOOTSTRAP = 3

if "test" in sys.argv:

    class DisableMigrations:
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()
    PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
    DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"
