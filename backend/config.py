from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

VAULT_URL = "https://flask-calc-secret.vault.azure.net/"
CLIENT = SecretClient(vault_url=VAULT_URL, credential=DefaultAzureCredential())

DB_USERNAME = CLIENT.get_secret("ptt-db-username")
DB_PASSWORD = CLIENT.get_secret("ptt-db-password")
INSTRUMENTATION_KEY = CLIENT.get_secret("ptt-instrumentation-key")