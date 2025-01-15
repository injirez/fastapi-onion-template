# fastapi-onion-template
A FastAPI template to use Onion architecture with a simple example of JWT authentication.

## Overview
This template provides a structured approach to building FastAPI applications using the Onion architecture. Onion architecture promotes a clean separation of concerns, making your application more modular, testable, and maintainable. The template includes a simple example of JWT (JSON Web Token) authentication to demonstrate how to secure your API endpoints.

## Features
- Onion Architecture: Organizes your application into layers, promoting a clear separation of concerns.
- JWT Authentication: Secures your API endpoints using JSON Web Tokens.
- Docker Support: Includes Docker configuration for easy deployment.
- Configuration Management: Uses a configuration file (app.conf) to manage application settings.

## Clone project
```
git clone https://github.com/injirez/fastapi-onion-template && cd fastapi-onion-template
```

## Edit ```app.conf```
The ```app.conf``` file contains the base configuration for the application. You can edit this file to customize the settings.
```editorconfig
# app.conf
[BASE]
port_backend = 8989
port_frontend = 3000
secret_key = ***** # Key for JWT encoding (generates automatically, to use your own, create an environment variable $SECRET_KEY)
jwt_access_expiration_seconds = 3600
jwt_refresh_expiration_seconds = 7200
```

## Start pre-run commands
Before running the project, you need to execute some pre-run commands to set up the environment.
- Sets secret key from env
- Sets ports to docker config files
- ...
```commandline
make pre-run
```

## Run project
Use Docker Compose to build and run the project.
```commandline
docker-compose up --build -d
```

## Check Logs
To check the logs of the running application, you can use the following commands:
```commandline
docker exec -it docker exec -it fastapi-onion-template_image_id bash
tail -f /var/log/fastapi-onion-template.log
```

## Project structure
```commandline
fastapi-onion-template/
├── backend/
│   ├── alembic/
│   │   └── ...
│   ├── app/
│   │   ├── api/
│   │   │   └── ...
│   │   ├── core/
│   │   │   └── ...
│   │   ├── domain/
│   │   │   └── ...
│   │   ├── infrastructure/
│   │   │   └── ...
│   │   ├── services/
│   │   │   └── ...
│   │   ├── main.py
│   │   └── ...
│   ├── alembic.ini
│   ├── database.db
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
├── app.conf
├── docker-compose.yml
└── README.md
```
- backend 
  - alembic/: Directory for Alembic migrations. 
  - app/: Main application directory.
      - api/: Contains API-related code.
      - core/: Contains core application settings and configurations.
      - domain/: Contains domain models and business logic.
      - infrastructure/: Contains infrastructure-related code.
      - services/: Contains service layer code.
      - main.py: Main entry point of the application.
  - alembic.ini: Alembic configuration file.
  - Dockerfile: Docker configuration for the application.
  - requirements.txt: List of Python dependencies.
  - app.conf: Application configuration file.
  - docker-compose.yml: Docker Compose configuration file. 
  - README.md: Project documentation.