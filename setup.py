from setuptools import setup, find_packages

setup(
    name="hexlet-code",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask==3.0.2",
        "gunicorn==21.2.0",
        "python-dotenv==1.0.1",
        "psycopg2-binary==2.9.9",
        "requests==2.31.0",
        "validators==0.22.0",
    ]
)