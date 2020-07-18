import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

db_type=os.environ.get('db_type')
db_username=os.environ.get('db_username')
db_password=os.environ.get('db_password')
db_host=os.environ.get('db_host')
db_port=os.environ.get('db_port')
db_test_name=os.environ.get('db_test_name')
db_name=os.environ.get('db_name')