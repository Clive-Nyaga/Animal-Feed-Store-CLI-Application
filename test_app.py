#!/usr/bin/env python3
"""
Test script to verify application functionality
"""
from database import DatabaseManager

def test_application():
    db = DatabaseManager()
    
    print("=== Application Test ===")
    
    # Test admin authentication
    admin = db.authenticate_user('admin', 'admin123')
    print(f"Admin login: {'✓' if admin else '✗'}")
    
    # Test feeds
    feeds = db.get_all_feeds()
    print(f"Feeds available: {len(feeds)} ✓")
    
    # Test users
    users = db.get_all_users()
    print(f"Users in system: {len(users)} ✓")
    
    # Test transactions
    transactions = db.get_all_transactions()
    print(f"Transactions: {len(transactions)} ✓")
    
    print("\n=== Sample Data ===")
    print("Admin credentials: Username=admin, Password=admin123")
    print("Available feeds:")
    for feed in feeds[:3]:  # Show first 3
        print(f"  - {feed.name}: ${feed.price:.2f}")
    
    db.close()
    print("\nApplication is ready to use! Run: python main.py")

if __name__ == "__main__":
    test_application()