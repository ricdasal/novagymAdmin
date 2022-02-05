# novagym
Administrador/BackEnd NovaGym

# Requirements
Python 3.8.12 64 bits

Usage:

- Copy .env.example and rename it to .env
- Change the configuration inside the file as needed. 
  it's recommend to set USE_SQLITE to True for development stage. 
  But if you want to use a different db, set USE_SQLITE to False and
  set DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT to the your correspoding
  db settings


If new libs are required, add them to the requirements file as follow:

    - Generate: pip freeze > requirements.txt

    - Install: pip install -r requirements.txt
