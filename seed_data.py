from database import DatabaseManager

def seed_database():
    db = DatabaseManager()
    
    # Create admin user
    admin = db.create_user("Admin", "admin")
    print(f"Admin created with ID: {admin.id}")
    
    # Create sample feeds
    feeds_data = [
        ("Chicken Feed Premium", 25.99, 100),
        ("Cattle Feed Pellets", 45.50, 50),
        ("Pig Starter Feed", 35.75, 75),
        ("Horse Oats", 28.00, 60),
        ("Sheep Grain Mix", 32.25, 40)
    ]
    
    for name, price, stock in feeds_data:
        feed = db.create_feed(name, price, stock)
        print(f"Feed '{feed.name}' created with ID: {feed.id}")
    
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()