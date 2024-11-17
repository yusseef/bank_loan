# Loan Management System Backend

This repository contains the backend implementation of the Loan Management System, built using Django and Django Rest Framework (DRF). The system supports user roles like Loan Provider, Loan Customer, and Bank Personnel. It also provides APIs for managing loans, applications, and payments.

---

## Features

- JWT-based authentication using Django Rest Framework SimpleJWT.
- Role-based access control for Loan Providers, Loan Customers, and Bank Personnel.
- APIs for:
  - Managing loans and payments.
  - Viewing loan applications.
  - Managing loan fund limits.
- Dockerized deployment for ease of setup and scalability.
- ERD attached for beeter DB schema.
- Flow chart attached for better viewing the flow.
- All APIS are swaggerised and you can find it in ```/swagger```


---

## Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.10+
- PostgreSQL (if running without Docker)

---

### Local Setup

1. **Clone the Repository**:
   ```bash
    https://github.com/yusseef/bank_loan.git
    cd bank_loan
    ```

2. **Runs with Docker**:
  ```bash
    docker-compose up --build
  ```
  Migration is running with ```entry_point.sh``` file

3. **Create a Superuser**:
   ```bash
   docker-compose exec django_web python manage.py createsuperuser
   ```

## API Endpoints
You will find all endpoints in ```/swagger```

## Testing
Run tests with
```bash
docker-compose exec django_web python manage.py test
```
