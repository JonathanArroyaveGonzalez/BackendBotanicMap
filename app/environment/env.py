import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from google.cloud import storage as gcs

# Cargar variables de entorno
load_dotenv()

service_account_key = {
    "type": "service_account",
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN")
}

# Inicializar las credenciales de Firebase
cred = credentials.Certificate(service_account_key)
#client = gcs.Client.from_service_account_json(service_account_key)
#client = storage.Client.from_service_account_info(service_account_key)
#firebase_admin.initialize_app(cred)