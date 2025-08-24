# Animal Feed Store CLI Application

A terminal-based system for managing animal feed purchases and inventory using Python, SQLAlchemy, and SQLite.

## Features

- **User Interface**: Browse feeds, make purchases, view transaction history
- **Admin Interface**: Manage inventory (CRUD operations), view all transactions and users
- **Database**: SQLite with SQLAlchemy ORM for data persistence
- **Role-based Access**: Different interfaces for users and administrators

## Installation

1. Install dependencies:
   ```bash
   pipenv install
   ```

2. Activate virtual environment:
   ```bash
   pipenv shell
   ```

3. Seed the database (optional):
   ```bash
   python seed_data.py
   ```

## Usage

Run the application:
```bash
python main.py
```

### User Operations
- View available feeds with prices and stock
- Purchase feeds by specifying ID and quantity
- View personal transaction history

### Admin Operations
- All user operations plus:
- Add new feeds to inventory
- Update feed details (name, price, stock)
- Delete feeds from system
- View all user transactions
- View all registered users

## Database Schema

- **Users**: id, name, role
- **Feeds**: id, name, price, stock_quantity
- **Transactions**: id, user_id, feed_id, quantity, total_price, date

## Project Structure

```
├── main.py          # Application entry point
├── models.py        # SQLAlchemy database models
├── database.py      # Database operations manager
├── cli.py           # Command-line interface
├── seed_data.py     # Database seeding script
├── Pipfile          # Dependencies
└── README.md        # Documentation
```