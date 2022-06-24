from app import db, login
from flask_login import UserMixin
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), index=True, unique=True)
    created_at = db.Column(db.DateTime, default = dt.utcnow())
    password = db.Column(db.String(200))
    token = db.Column(db.String, index=True, unique=True)
    token_exp = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)
    cart = db.relationship('Item', secondary='shopping_cart', backref='user_cart', lazy="dynamic")


# |---------TOKEN METHODS---------->
    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        #give the user their token if it is not expired
        if self.token and self.token_exp > current_time + timedelta(seconds=60):
            return self.token
        #if the token DNE or token is exp
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    def revoke_token(self):
        self.token_exp = dt.utcnow() - timedelta(seconds=61)

    @staticmethod
    def check_token(token):
        u = User.query.filter_by(token=token).first()
        if not u or u.token_exp < dt.utcnow():
            return None
        return u

# |--------- END TOKEN METHODS---------->

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    #salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)
    
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    def save(self):
        db.session.add(self)
        db.session.commit() 
    
    def item_to_add(self, item):
        self.cart.append(item)
        db.session.commit()
        
    def item_to_delete(self, item):
        if item in self.cart:
            self.cart.remove(item)
            db.session.commit()
    
    def clear_cart(self):
        while len(list(self.cart)) >0:
            for item in self.cart:
                self.cart.remove(item)
        db.session.commit()
        

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class ShoppingCart(db.Model):
    __tablename__ = 'shopping_cart'
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    def __repr__(self):
        return f'<Product: {self.item_id} | {self.cart_id}>'
    
    def from_dict(self, data):
        self.item_id = data['item_id']
        self.user_id = data['user_id']
        self.qty = data['qty']
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()