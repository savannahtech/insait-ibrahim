# Insight-Backend-Test

Backend Test for Insait

# Flask App Documentation

This README provides an overview of the Flask app, including how to build, run, and manage the application using Docker, as well as database migrations. Additionally, it provides details on how to use the associated `Makefile` for ease of development.

## Requirements

Before running the Flask app in Docker, make sure you have the following installed on your machine:

- Docker
- Docker Compose

If you don't have `make` installed, you can still execute the individual Docker commands as described below.

## How to setup and run the project locally.

To set up and run the Flask app in your local environment, follow the steps below.

### Clone the Repository

```bash
git clone git@github.com:savannahtech/insait-ibrahim.git Insight-Backend-Test
cd Insight-Backend-Test
```

### Environment Configuration

Create a .env file in the root directory of the project. A sample is provided in the `.env.example` with the required keys

### Build and run the docker image

The following command are to be executed one after the order.
The original command are being abstracted by using `make`. This makes the commands simple and easy to remember

The Makefile simplifies the process of interacting with Docker Compose and Alembic for managing your Flask app. Below are the available commands you can run with make.

> Note: If you do not have make installed, you can always copy the Docker commands from the `Makefile` and run them directly.

#### 1. Build Docker Image

The first step after cloning the repo and creating `.env` file is to build the docker image. Run the command below in the terminal to start the building process.

```bash
make build
```

> If you do not have `make` installed, run the command below instead

```bash
docker compose -f docker-compose.yml build
```

#### 2. Run Docker Image

Once the docker image has been built with the command above, you can run it with the command below

```bash
make run
```

> If you do not have `make` installed, run the command below instead

```bash
docker compose -f docker-compose.yml up --no-build --abort-on-container-exit --remove-orphans
```

#### Build and run the image with a single command (Alternative approach)

Instead of running two command to build and run the image, it can be done with a single command instead.
This command will build the image and run it automatically after building

```bash
make build-run
```

> If you do not have `make` installed, run the command below instead

```bash
docker compose -f docker-compose.yml up --build
```

### Making requests

Once the docker image is running, you can access the `/ask` endpoint by making a POST request to `http://localhost:8000/ask`
A sample payload is show below

```json
{
  "question": "In 250 characters, what is Django in Python?"
}
```

A sample response is shown below

```json
{
  "answer": "Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It promotes the use of the Model-View-Template (MVT) architecture, providing built-in features like an admin panel, ORM, and security tools for developers.",
  "created_at": "Fri, 20 Dec 2024 16:00:45 GMT",
  "id": 4,
  "question": "In 250 characters, what is Django?"
}
```

### Making migrations

If any changes were make to the `Question` class inside the `insait/models.py` file, and the changes are to reflect in the database, then the command below is what is needed.

> Before running the command, a migration message should be added to the `Makefile` (if using the `mak` approach). The migration message will replace `"Initial migration"` that is inside the `Makefile`. The migration message should be de detailed

```bash
make migrate
```

> If you do not have `make` installed, run the command below instead, while replacing `"Initial migration"` with the intended migration message

```bash
docker-compose exec flask-app alembic revision --autogenerate -m "Initial migration"
```

### Running Tests

The repo has 3 test cases included. To run these tests ore any other test added to the `insait/tes_app.py`, the command below can be used

```bash
make test
```

> If you do not have `make` installed, run the command below instead

```bash
docker-compose exec flask-app pytest
```

### Shutting down the docker container

To stop the container when it's no longer needed, run the command below

```bash
make down
```

> If you do not have `make` installed, run the command below instead

```bash
docker compose -f docker-compose.yml down --remove-orphans
```
