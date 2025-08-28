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

3. Run database migrations:
   ```bash
   alembic upgrade head
   ```

4. Seed the database (optional):
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

- **Users**: id, username, name, password, role
- **Feeds**: id, name, price, stock_quantity
- **Transactions**: id, user_id, feed_id, quantity, total_price, date

## Authentication

- Users register with username and password
- Login using username instead of ID
- Admin credentials: Username=admin, Password=admin123

## Project Structure

```
├── main.py          # Application entry point
├── models.py        # SQLAlchemy database models
├── database.py      # Database operations manager
├── cli.py           # Command-line interface
├── seed_data.py     # Database seeding script

├── Pipfile          # Dependencies
├── alembic/         # Database migrations
└── README.md        # Documentation
```

## Function Workflow

### Main Application Flow (`main.py`)
- Entry point that initializes CLI and starts the application
- Imports CLI class and runs the main loop

### CLI Functions (`cli.py`)

**Authentication Functions:**
- `login()`: Handles user authentication and registration
- `start()`: Main application loop with role-based menu routing

**User Functions:**
- `user_menu()`: Displays user options and handles input
- `view_feeds()`: Shows available feeds with stock status using tuples and lists
- `purchase_feed()`: Processes feed purchases with input validation
- `view_my_transactions()`: Displays user's transaction history

**Admin Functions:**
- `admin_menu()`: Displays admin options with comprehensive error handling
- `add_feed()`: Creates new feed entries with validation
- `update_feed()`: Modifies existing feed details
- `delete_feed()`: Removes feeds with confirmation prompts
- `view_all_transactions()`: Shows all transactions with statistics using dictionaries and tuples
- `view_all_users()`: Displays user information with spending statistics using dictionaries

### Database Functions (`database.py`)

**User Operations:**
- `create_user()`: Creates new user accounts
- `authenticate_user()`: Validates login credentials
- `get_user_by_username()`: Retrieves user by username
- `get_user_by_id()`: Retrieves user by ID
- `get_all_users()`: Returns all registered users

**Feed Operations:**
- `create_feed()`: Adds new feed to inventory
- `get_all_feeds()`: Returns all available feeds
- `get_feed_by_id()`: Retrieves specific feed
- `update_feed()`: Modifies feed details
- `delete_feed()`: Removes feed from system

**Transaction Operations:**
- `create_transaction()`: Processes purchases and updates stock
- `get_user_transactions()`: Returns user's transaction history
- `get_all_transactions()`: Returns all system transactions

### Database Models (`models.py`)
- `User`: Stores user credentials and role information
- `Feed`: Manages feed inventory with precise decimal pricing
- `Transaction`: Records all purchases with relationships

### Data Structures Used
- **Lists**: Feed data processing, transaction sorting
- **Tuples**: Feed display data, summary statistics
- **Dictionaries**: User statistics, transaction organization
- **List Comprehensions**: Data transformation and filtering

## Migration Management

The project uses Alembic for database schema management:

1. **Initial Migration**: Creates all tables (users, feeds, transactions)
2. **Performance Migration**: Adds database indexes for optimization

```bash
# View migration history
alembic history

# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## Error Handling

The application includes comprehensive error handling:
- Input validation for all user inputs
- Database operation error catching
- Graceful handling of keyboard interrupts
- User-friendly error messages with guidance
- Confirmation prompts for destructive operations