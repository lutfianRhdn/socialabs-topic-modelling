import os
from dotenv import load_dotenv
load_dotenv()

app_env = os.getenv('APP_ENV')
app_debug = os.getenv('APP_DEBUG')
app_port = os.getenv('APP_PORT')
db_url = os.getenv('DB_URL')
db_url2 = os.getenv('DB_URL_DATAGATHERING')
db_name = os.getenv('DB_NAME')
openai_key = os.getenv('AZURE_OPENAI_KEY')
openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
openai_deploy_name = os.getenv('AZURE_OPENAI_MODEL_NAME')