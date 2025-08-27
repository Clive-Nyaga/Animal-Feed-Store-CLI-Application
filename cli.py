from database import DatabaseManager

class CLI:
    def __init__(self):
        self.db = DatabaseManager()
        self.current_user = None
    
    def start(self):
        print("Welcome to Animal Feed Store!")
        self.login()
        
        while True:
            try:
                if self.current_user.role == 'admin':
                    self.admin_menu()
                else:
                    self.user_menu()
            except KeyboardInterrupt:
                print("\nGoodbye!")
                self.db.close()
                break
            except Exception as e:
                print(f"Error: {e}")
                continue
    
    def login(self):
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        
        try:
            choice = input("Choose option: ").strip()
            
            if choice == '1':
                username = input("Enter your username: ").strip()
                password = input("Enter your password: ").strip()
                if not username or not password:
                    print("Username and password cannot be empty!")
                    self.login()
                    return
                user = self.db.authenticate_user(username, password)
                if user:
                    self.current_user = user
                    print(f"Welcome back, {user.name}!")
                else:
                    print("Invalid credentials!")
                    self.login()
            elif choice == '2':
                username = input("Enter a username: ").strip()
                if not username:
                    print("Username cannot be empty!")
                    self.login()
                    return
                if self.db.get_user_by_username(username):
                    print("Username already exists!")
                    self.login()
                    return
                name = input("Enter your name: ").strip()
                if not name:
                    print("Name cannot be empty!")
                    self.login()
                    return
                password = input("Enter your password: ").strip()
                if not password:
                    print("Password cannot be empty!")
                    self.login()
                    return
                role = input("Enter role (user/admin) [default: user]: ").lower().strip()
                if role not in ['user', 'admin']:
                    role = 'user'
                user = self.db.create_user(username, name, password, role)
                self.current_user = user
                print(f"Registration successful! Username: {user.username}")
            elif choice == '3':
                self.logout()
            else:
                print("Invalid option! Please choose 1, 2, or 3.")
                self.login()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            self.logout()
        except Exception as e:
            print(f"Error during login: {e}")
            self.login()
    
    def user_menu(self):
        print(f"\n--- User Menu ({self.current_user.name}) ---")
        print("1. View Available Feeds")
        print("2. Purchase Feed")
        print("3. View My Transactions")
        print("4. Logout")
        
        try:
            choice = input("Choose option (or 'b' to go back): ").strip()
            
            if choice == '1':
                self.view_feeds()
                input("\nPress Enter to continue...")
            elif choice == '2':
                self.purchase_feed()
                input("\nPress Enter to continue...")
            elif choice == '3':
                self.view_my_transactions()
                input("\nPress Enter to continue...")
            elif choice == '4':
                self.logout()
            elif choice.lower() == 'b':
                return
            else:
                print("Invalid option! Please choose 1-4 or 'b'.")
        except (EOFError, KeyboardInterrupt):
            print("\nReturning to menu...")
        except Exception as e:
            print(f"Error: {e}")
    
    def admin_menu(self):
        print(f"\n--- Admin Menu ({self.current_user.name}) ---")
        print("1. View Available Feeds")
        print("2. Add New Feed")
        print("3. Update Feed")
        print("4. Delete Feed")
        print("5. View All Transactions")
        print("6. View All Users")
        print("7. Logout")
        
        try:
            choice = input("Choose option (or 'b' to go back): ").strip()
            
            if choice == '1':
                self.view_feeds()
                input("\nPress Enter to continue...")
            elif choice == '2':
                self.add_feed()
                input("\nPress Enter to continue...")
            elif choice == '3':
                self.update_feed()
                input("\nPress Enter to continue...")
            elif choice == '4':
                self.delete_feed()
                input("\nPress Enter to continue...")
            elif choice == '5':
                self.view_all_transactions()
                input("\nPress Enter to continue...")
            elif choice == '6':
                self.view_all_users()
                input("\nPress Enter to continue...")
            elif choice == '7':
                self.logout()
            elif choice.lower() == 'b':
                return
            else:
                print("Invalid option! Please choose 1-7 or 'b'.")
        except (EOFError, KeyboardInterrupt):
            print("\nReturning to menu...")
        except Exception as e:
            print(f"Error: {e}")
    
    def view_feeds(self):
        try:
            feeds = self.db.get_all_feeds()
            if feeds:
                print("\n--- Available Feeds ---")
                for feed in feeds:
                    print(f"ID: {feed.id} | Name: {feed.name} | Price: ${feed.price:.2f} | Stock: {feed.stock_quantity}")
            else:
                print("No feeds available!")
        except Exception as e:
            print(f"Error loading feeds: {e}")
    
    def purchase_feed(self):
        self.view_feeds()
        try:
            feed_input = input("Enter feed ID to purchase (or 'b' to go back): ").strip()
            if feed_input.lower() == 'b':
                return
            
            try:
                feed_id = int(feed_input)
            except ValueError:
                print("Please enter a valid feed ID number.")
                return
            
            quantity_input = input("Enter quantity (or 'b' to go back): ").strip()
            if quantity_input.lower() == 'b':
                return
            
            try:
                quantity = int(quantity_input)
                if quantity <= 0:
                    print("Quantity must be greater than 0.")
                    return
            except ValueError:
                print("Please enter a valid quantity number.")
                return
            
            transaction = self.db.create_transaction(self.current_user.id, feed_id, quantity)
            if transaction:
                print(f"Purchase successful! Total: ${transaction.total_price:.2f}")
            else:
                print("Purchase failed! Check feed availability or stock.")
        except Exception as e:
            print(f"Error during purchase: {e}")
    
    def view_my_transactions(self):
        transactions = self.db.get_user_transactions(self.current_user.id)
        if transactions:
            print("\n--- My Transactions ---")
            for t in transactions:
                print(f"Date: {t.date.strftime('%Y-%m-%d %H:%M')} | Feed: {t.feed.name} | Qty: {t.quantity} | Total: ${t.total_price:.2f}")
        else:
            print("No transactions found!")
    
    def add_feed(self):
        try:
            name = input("Enter feed name: ").strip()
            if not name:
                print("Feed name cannot be empty!")
                return
            
            price_input = input("Enter price: ").strip()
            try:
                price = float(price_input)
                if price <= 0:
                    print("Price must be greater than 0.")
                    return
            except ValueError:
                print("Please enter a valid price number.")
                return
            
            stock_input = input("Enter stock quantity: ").strip()
            try:
                stock = int(stock_input)
                if stock < 0:
                    print("Stock quantity cannot be negative.")
                    return
            except ValueError:
                print("Please enter a valid stock number.")
                return
            
            feed = self.db.create_feed(name, price, stock)
            print(f"Feed '{feed.name}' added successfully!")
        except Exception as e:
            print(f"Error adding feed: {e}")
    
    def update_feed(self):
        self.view_feeds()
        try:
            feed_input = input("Enter feed ID to update: ").strip()
            try:
                feed_id = int(feed_input)
            except ValueError:
                print("Please enter a valid feed ID number.")
                return
            
            name = input("Enter new name (or press Enter to skip): ").strip() or None
            
            price = None
            price_input = input("Enter new price (or press Enter to skip): ").strip()
            if price_input:
                try:
                    price = float(price_input)
                    if price <= 0:
                        print("Price must be greater than 0.")
                        return
                except ValueError:
                    print("Please enter a valid price number.")
                    return
            
            stock = None
            stock_input = input("Enter new stock (or press Enter to skip): ").strip()
            if stock_input:
                try:
                    stock = int(stock_input)
                    if stock < 0:
                        print("Stock quantity cannot be negative.")
                        return
                except ValueError:
                    print("Please enter a valid stock number.")
                    return
            
            feed = self.db.update_feed(feed_id, name, price, stock)
            if feed:
                print("Feed updated successfully!")
            else:
                print("Feed not found!")
        except Exception as e:
            print(f"Error updating feed: {e}")
    
    def delete_feed(self):
        self.view_feeds()
        try:
            feed_input = input("Enter feed ID to delete: ").strip()
            try:
                feed_id = int(feed_input)
            except ValueError:
                print("Please enter a valid feed ID number.")
                return
            
            confirm = input(f"Are you sure you want to delete feed ID {feed_id}? (y/N): ").strip().lower()
            if confirm != 'y':
                print("Delete cancelled.")
                return
            
            if self.db.delete_feed(feed_id):
                print("Feed deleted successfully!")
            else:
                print("Feed not found!")
        except Exception as e:
            print(f"Error deleting feed: {e}")
    
    def view_all_transactions(self):
        try:
            transactions = self.db.get_all_transactions()
            if transactions:
                print("\n--- All Transactions ---")
                for t in transactions:
                    print(f"User: {t.user.name} ({t.user.username}) | Feed: {t.feed.name} | Qty: {t.quantity} | Total: ${t.total_price:.2f} | Date: {t.date.strftime('%Y-%m-%d %H:%M')}")
            else:
                print("No transactions found!")
        except Exception as e:
            print(f"Error loading transactions: {e}")
    
    def view_all_users(self):
        try:
            users = self.db.get_all_users()
            if users:
                print("\n--- All Users ---")
                for user in users:
                    transaction_count = len(self.db.get_user_transactions(user.id))
                    print(f"Username: {user.username} | Name: {user.name} | Role: {user.role} | Transactions: {transaction_count}")
            else:
                print("No users found!")
        except Exception as e:
            print(f"Error loading users: {e}")
    
    def logout(self):
        print("Goodbye!")
        self.db.close()
        exit()