from database import DatabaseManager

class CLI:
    def __init__(self):
        self.db = DatabaseManager()
        self.current_user = None
    
    def start(self):
        print("Welcome to Animal Feed Store!")
        self.login()
        
        while True:
            if self.current_user.role == 'admin':
                self.admin_menu()
            else:
                self.user_menu()
    
    def login(self):
        print("\n1. Login")
        print("2. Register")
        choice = input("Choose option: ")
        
        if choice == '1':
            user_id = int(input("Enter your user ID: "))
            user = self.db.get_user_by_id(user_id)
            if user:
                self.current_user = user
                print(f"Welcome back, {user.name}!")
            else:
                print("User not found!")
                self.login()
        elif choice == '2':
            name = input("Enter your name: ")
            role = input("Enter role (user/admin): ").lower()
            if role not in ['user', 'admin']:
                role = 'user'
            user = self.db.create_user(name, role)
            self.current_user = user
            print(f"Registration successful! Your ID is: {user.id}")
    
    def user_menu(self):
        print(f"\n--- User Menu ({self.current_user.name}) ---")
        print("1. View Available Feeds")
        print("2. Purchase Feed")
        print("3. View My Transactions")
        print("4. Logout")
        
        choice = input("Choose option: ")
        
        if choice == '1':
            self.view_feeds()
        elif choice == '2':
            self.purchase_feed()
        elif choice == '3':
            self.view_my_transactions()
        elif choice == '4':
            self.logout()
        else:
            print("Invalid option!")
    
    def admin_menu(self):
        print(f"\n--- Admin Menu ({self.current_user.name}) ---")
        print("1. View Available Feeds")
        print("2. Add New Feed")
        print("3. Update Feed")
        print("4. Delete Feed")
        print("5. View All Transactions")
        print("6. View All Users")
        print("7. Logout")
        
        choice = input("Choose option: ")
        
        if choice == '1':
            self.view_feeds()
        elif choice == '2':
            self.add_feed()
        elif choice == '3':
            self.update_feed()
        elif choice == '4':
            self.delete_feed()
        elif choice == '5':
            self.view_all_transactions()
        elif choice == '6':
            self.view_all_users()
        elif choice == '7':
            self.logout()
        else:
            print("Invalid option!")
    
    def view_feeds(self):
        feeds = self.db.get_all_feeds()
        if feeds:
            print("\n--- Available Feeds ---")
            for feed in feeds:
                print(f"ID: {feed.id} | Name: {feed.name} | Price: ${feed.price:.2f} | Stock: {feed.stock_quantity}")
        else:
            print("No feeds available!")
    
    def purchase_feed(self):
        self.view_feeds()
        try:
            feed_id = int(input("Enter feed ID to purchase: "))
            quantity = int(input("Enter quantity: "))
            
            transaction = self.db.create_transaction(self.current_user.id, feed_id, quantity)
            if transaction:
                print(f"Purchase successful! Total: ${transaction.total_price:.2f}")
            else:
                print("Purchase failed! Check feed availability or stock.")
        except ValueError:
            print("Invalid input!")
    
    def view_my_transactions(self):
        transactions = self.db.get_user_transactions(self.current_user.id)
        if transactions:
            print("\n--- My Transactions ---")
            for t in transactions:
                print(f"Date: {t.date.strftime('%Y-%m-%d %H:%M')} | Feed: {t.feed.name} | Qty: {t.quantity} | Total: ${t.total_price:.2f}")
        else:
            print("No transactions found!")
    
    def add_feed(self):
        name = input("Enter feed name: ")
        try:
            price = float(input("Enter price: "))
            stock = int(input("Enter stock quantity: "))
            feed = self.db.create_feed(name, price, stock)
            print(f"Feed '{feed.name}' added successfully!")
        except ValueError:
            print("Invalid input!")
    
    def update_feed(self):
        self.view_feeds()
        try:
            feed_id = int(input("Enter feed ID to update: "))
            name = input("Enter new name (or press Enter to skip): ") or None
            price = input("Enter new price (or press Enter to skip): ")
            price = float(price) if price else None
            stock = input("Enter new stock (or press Enter to skip): ")
            stock = int(stock) if stock else None
            
            feed = self.db.update_feed(feed_id, name, price, stock)
            if feed:
                print("Feed updated successfully!")
            else:
                print("Feed not found!")
        except ValueError:
            print("Invalid input!")
    
    def delete_feed(self):
        self.view_feeds()
        try:
            feed_id = int(input("Enter feed ID to delete: "))
            if self.db.delete_feed(feed_id):
                print("Feed deleted successfully!")
            else:
                print("Feed not found!")
        except ValueError:
            print("Invalid input!")
    
    def view_all_transactions(self):
        transactions = self.db.get_all_transactions()
        if transactions:
            print("\n--- All Transactions ---")
            for t in transactions:
                print(f"User: {t.user.name} | Feed: {t.feed.name} | Qty: {t.quantity} | Total: ${t.total_price:.2f} | Date: {t.date.strftime('%Y-%m-%d %H:%M')}")
        else:
            print("No transactions found!")
    
    def view_all_users(self):
        users = self.db.get_all_users()
        if users:
            print("\n--- All Users ---")
            for user in users:
                print(f"ID: {user.id} | Name: {user.name} | Role: {user.role}")
        else:
            print("No users found!")
    
    def logout(self):
        print("Goodbye!")
        self.db.close()
        exit()