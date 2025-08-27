from models import Session, User, Feed, Transaction

class DatabaseManager:
    def __init__(self):
        self.session = Session()
    
    def close(self):
        self.session.close()
    
    # User operations
    def create_user(self, username, name, password, role='user'):
        user = User(username=username, name=name, password=password, role=role)
        self.session.add(user)
        self.session.commit()
        return user
    
    def authenticate_user(self, username, password):
        user = self.session.query(User).filter(User.username == username).first()
        return user if user and user.password == password else None
    
    def get_user_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()
    
    def get_all_users(self):
        return self.session.query(User).all()
    
    # Feed operations
    def create_feed(self, name, price, stock_quantity):
        feed = Feed(name=name, price=price, stock_quantity=stock_quantity)
        self.session.add(feed)
        self.session.commit()
        return feed
    
    def get_all_feeds(self):
        return self.session.query(Feed).all()
    
    def get_feed_by_id(self, feed_id):
        return self.session.query(Feed).filter(Feed.id == feed_id).first()
    
    def update_feed(self, feed_id, name=None, price=None, stock_quantity=None):
        feed = self.get_feed_by_id(feed_id)
        if feed:
            if name: feed.name = name
            if price: feed.price = price
            if stock_quantity is not None: feed.stock_quantity = stock_quantity
            self.session.commit()
        return feed
    
    def delete_feed(self, feed_id):
        feed = self.get_feed_by_id(feed_id)
        if feed:
            self.session.delete(feed)
            self.session.commit()
            return True
        return False
    
    # Transaction operations
    def create_transaction(self, user_id, feed_id, quantity):
        feed = self.get_feed_by_id(feed_id)
        if feed and feed.stock_quantity >= quantity:
            total_price = feed.price * quantity
            transaction = Transaction(
                user_id=user_id,
                feed_id=feed_id,
                quantity=quantity,
                total_price=total_price
            )
            feed.stock_quantity -= quantity
            self.session.add(transaction)
            self.session.commit()
            return transaction
        return None
    
    def get_user_transactions(self, user_id):
        return self.session.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    def get_all_transactions(self):
        return self.session.query(Transaction).all()