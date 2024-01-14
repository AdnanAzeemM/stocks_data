# stock management project

## overview 
This Djangp project implement User, Stocks and transactions module.


## Data Models

### Users Table
- user_id: Unique identifier for users.
- username: User's username.
- balance: User's account balance.

### StockData Table
- ticker: Unique identifier for stocks.
- open_price: Opening price of the stock.
- close_price: Closing price of the stock.
- high: Highest price during the period.
- low: Lowest price during the period.
- volume: Stock trading volume.
- timestamp: Timestamp of the data.

### Transactions Table
- transaction_id: Unique identifier for transactions.
- user_id: Foreign key referencing Users table.
- ticker: ticker for transaction.
- transaction_type: Type of transaction (buy/sell).
- transaction_volume: Volume of the transaction.
- transaction_price: Price of the transaction.
- timestamp: Timestamp of the transaction.

## Endpoints

### POST /users/
- Register a new user with a username and initial balance.

### GET /users/{username}/
- Retrieve user data from Redis cache.

### POST /stocks/
- stock data and store it in the Postgres database.

### GET /stocks/
- Retrieve all stock data from Redis cache.

### GET /stocks/{ticker}/
- Retrieve specific stock data from Redis cache.

### POST /transactions/
- Post a new transaction, updating user's balance based on the current stock price.

### GET /transactions/{user_id}/
- Retrieve all transactions of a specific user.

### GET /transactions/{user_id}/{start_timestamp}/{end_timestamp}/
- Retrieve transactions of a specific user between two timestamps.

## Additional Features

- Add Swagger Documentation:

- Add Celery Integration: New transactions trigger tasks for processing via Celery and Redis.

- Add Flower Monitoring: Monitor Celery tasks using Flower.

- Unit Tests: Write unit tests for all APIs using pytest.

- Docker Setup: Docker Compose file provided for easy project deployment.
- Add Postgres DB:

## Getting Started

### Prerequisites
- Ensure you have Docker installed.

### Steps
1. Clone the repository.
2. Set up virtual environment and install dependencies: pip install -r requirements.txt
3. Run migrations: python manage.py migrate
4. Start Celery: celery -A stock_data worker --loglevel=info
5. Start Flower: celery -A stock_data flower --port=5555
7. test cases: pytest  
8. Run the Django development server: python manage.py runserver
9. Access the Swagger documentation at http://localhost:8000/docs/.

## Unit Tests
# Run unit tests using the following command:
   in terminal: pytest
# if postgres DB use for run pytest ensure have permission " ALTER USER myprojectuser CREATEDB; "

##Docker
Run command: docker-compose up  --build
