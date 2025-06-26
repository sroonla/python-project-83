import os
import sys
from setuptools import setup, find_packages

if os.environ.get('GITHUB_ACTIONS') and 'hexlet' in os.environ.get('RUNNER_WORKSPACE', ''):
    print("\n\n!!! Hexlet CI workaround - installing system dependencies !!!\n")
    os.system("sudo apt-get update && sudo apt-get install -y libpq-dev > /dev/null 2>&1")
    print("System dependencies installed\n\n")
    psycopg_package = "psycopg2==2.9.9"
else:
    psycopg_package = "psycopg2-binary==2.9.9"

setup(
    name="hexlet-code",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask==3.0.2",
        "gunicorn==21.2.0",
        "python-dotenv==1.0.1",
        psycopg_package,
        "requests==2.31.0",
        "validators==0.22.0",
    ]
)