from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Join Table for many-to-many relationship (Builds <-> Components)
build_components = db.Table('build_components',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('build_id', db.Integer, db.ForeignKey('builds.id', ondelete='CASCADE')),
    db.Column('component_id', db.Integer, db.ForeignKey('components.id', ondelete='CASCADE')),
    db.Column('quantity', db.Integer, default=1),
    db.Column('added_at', db.DateTime, default=datetime.utcnow)
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    builds = db.relationship('Build', backref='owner', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
    # Relationships
    components = db.relationship('Component', backref='category', lazy=True)


class Component(db.Model):
    __tablename__ = 'components'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    socket = db.Column(db.String(50))  # Used for your compatibility checks!
    image_url = db.Column(db.String(255))


class GPU(db.Model):
    __tablename__ = 'gpus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    specs = db.Column(db.JSON, nullable=False, default=dict)
    vram = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255))


class RAM(db.Model):
    __tablename__ = 'rams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    specs = db.Column(db.JSON, nullable=False, default=dict)
    capacity = db.Column(db.String(50), nullable=False)
    speed = db.Column(db.String(50))
    image_url = db.Column(db.String(255))


class Build(db.Model):
    __tablename__ = 'builds'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    total_price = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-Many Relationship
    components = db.relationship('Component', secondary=build_components, lazy='subquery',
        backref=db.backref('builds', lazy=True))