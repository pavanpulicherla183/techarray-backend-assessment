# TechArray Backend Assessment

Containerized **Django REST API** for asynchronous batch transaction processing using **Celery, Redis, PostgreSQL, and Docker**.

This project demonstrates how to process financial transactions in batches asynchronously using background workers.

---

# Tech Stack

* Python
* Django
* Django REST Framework
* Celery
* Redis
* PostgreSQL
* Docker
* Docker Compose

---

# Features

* Client management
* Batch transaction processing
* Asynchronous task execution using Celery
* Redis message broker
* PostgreSQL database
* Dockerized environment for easy setup
* RESTful APIs for managing transactions

---

# Project Structure

```
backend-assessment
│
├── apps
│   ├── batches
│   ├── clients
│   └── transactions
│
├── config
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── wait_for_db.py
├── .env.example
└── README.md
```

---

# Setup Instructions

## 1. Clone the Repository

```
git clone https://github.com/pavanpulicherla183/techarray-backend-assessment.git
cd techarray-backend-assessment
```

---

## 2. Create Environment File

Create a `.env` file based on `.env.example`.

Example:

```
DEBUG=True
SECRET_KEY=your_secret_key
POSTGRES_DB=transactions_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_URL=redis://redis:6379/0
```

---

## 3. Build and Run Containers

```
docker-compose up --build
```

This will start:

* Django API server
* PostgreSQL database
* Redis
* Celery worker

---

## 4. Apply Database Migrations

Open another terminal and run:

```
docker-compose exec web python manage.py migrate
```

---

## 5. Create Superuser (Optional)

```
docker-compose exec web python manage.py createsuperuser
```

Access admin panel:

```
http://localhost:8000/admin
```

---

# API Workflow Example

Below is a typical workflow to test the system.

---

# 1. Create a Client

Endpoint:

```
POST /api/clients/
```

Example Request:

```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

---

# 2. Create a Batch

Endpoint:

```
POST /api/batches/
```

Example Request:

```json
{
  "client": 1,
  "total_amount": 1000
}
```

---

# 3. Add Transactions

Endpoint:

```
POST /api/transactions/
```

Example Request:

```json
{
  "batch": 1,
  "amount": 200,
  "status": "pending"
}
```

---

# 4. Process Batch (Celery Task)

Trigger asynchronous processing:

```
POST /api/batches/1/process/
```

This will trigger a **Celery background task** that processes the transactions.

---

# 5. Check Transactions

Endpoint:

```
GET /api/transactions/
```

Example Response:

```json
[
  {
    "id": 1,
    "batch": 1,
    "amount": 200,
    "status": "completed"
  }
]
```

---

# Running Celery Worker (if needed)

If the Celery worker is not running automatically:

```
docker-compose exec web celery -A config worker -l info
```

---

# API Endpoints

| Endpoint                     | Method | Description        |
| ---------------------------- | ------ | ------------------ |
| `/api/clients/`              | POST   | Create client      |
| `/api/clients/`              | GET    | List clients       |
| `/api/batches/`              | POST   | Create batch       |
| `/api/batches/`              | GET    | List batches       |
| `/api/batches/{id}/process/` | POST   | Process batch      |
| `/api/transactions/`         | POST   | Create transaction |
| `/api/transactions/`         | GET    | List transactions  |

---

# How Asynchronous Processing Works

1. A batch is created.
2. Transactions are added to the batch.
3. The batch processing endpoint triggers a **Celery task**.
4. Celery sends the task to **Redis message broker**.
5. The Celery worker processes transactions in the background.

This allows the API to remain fast while heavy processing happens asynchronously.

---

# Future Improvements

* Add authentication (JWT)
* Add unit tests
* Add API rate limiting
* Add transaction validation
* Add API documentation using Swagger

---

# Author

Pavan Kumar Reddy Pulicherla
