# E-Commerce RESTful API

## Overview
This is a production-grade RESTful API for an e-commerce platform that allows users to manage products and place orders. The API is designed with exception handling, comprehensive test cases, and is fully containerized for easy deployment using Docker.

## Features
- Retrieve a list of all available products
- Add new products with ID, name, description, price, and stock quantity
- Place orders while ensuring sufficient stock availability
- Automatic stock deduction upon successful order placement
- Exception handling and error responses for invalid data or insufficient stock
- Comprehensive unit and integration testing
- Fully dockerized setup for seamless deployment

## API Collection
The API endpoints and their details can be found in the following collection:
[Click here](https://drive.google.com/file/d/1MHLFKhSunK4OrXTCSgzNMOi6KWNjMGa9/view?usp=sharing)

## Business Logic & Constraints
- **Stock Management:** Orders will only be processed if sufficient stock is available.
- **Order Validation:** If stock is insufficient, an error response will be returned.
- **Error Handling:** Proper exception handling with meaningful error messages.

## Dockerization
The application is fully containerized with Docker. The `Dockerfile` ensures an optimized production-ready build. The `docker-compose.yml` file manages container networking and dependencies.

## Technologies Used
- **Python, Django, Django REST Framework** for API development
- **PostgreSQL** for database management
- **Docker, Docker Compose** for containerization
- **NGINX, Gunicorn** for production-grade deployment


## Installation & Setup
### **Prerequisites**
- Docker & Docker Compose installed

### **Build & Run the Application**
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Do the necessary changes in .env file
3. Build and run the application using Docker:
   ```sh
   docker-compose up --build -d
   ```
4. The API will be available at:
   ```
   http://localhost:8000
   ```

## **Installation & Setup on local system without docker (ubuntu)**

1. Clone git repo
    - git clone repository-url
2. Create virtual environment(python=3.11)
    - python3 -m venv venv
3. Activate the environment
    - . venv/bin/activate
4. Go to project path
    - cd EcomProject/
5. Install required packages
    - pip install -r requirements.txt
6. Setup postgres and create database
    - open postgres shell and paste below cmds
        - CREATE DATABASE db_name; 
        - CREATE USER db_user WITH PASSWORD 'secure_password';
        - ALTER ROLE db_user SET client_encoding TO 'utf8'; 
        - ALTER ROLE db_user SET default_transaction_isolation TO 'read committed'; 
        - ALTER ROLE db_user SET timezone TO 'UTC'; 
        - GRANT ALL PRIVILEGES ON DATABASE db_name TO db_user; 
7. Open .env file and do the necessary changes like DB configuration etc.
8. Export the environment variables
    - source .env
9. Run migrations
    - python manage.py makemigrations
    - python manage.py migrate
10. Run the django server
    - python manage.py runserver
    - Check the api's with the help of postman collection providedd above
11. That's it.

---

## Testing
TestingTest cases are written to ensure the correctness of the application. Run the tests using:

```sh
python manage.py test EcomApp.tests
```
This runs both unit and integration tests, ensuring endpoint behavior is correct.

---

## Thank you! 😊




