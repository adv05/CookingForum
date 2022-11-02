# CookingForum

This small project is for managing a basic user database. Its backend is based on FastAPI and it uses a Postgres database.

## Installation

To build and run, simply run `docker compose up` from the main directory. Tests will be performed automatically.

To access the Swagger UI go to: http://localhost:8000/docs

## How it works

The **User Signup** API route lets you register a new user through JSON.
The **User Login** route lets you login through username and password, assuming you don't have 2FA enabled. If you do, it will then generate a one-time password that you can use to complete your login process through the **Complete 2FA** route.
