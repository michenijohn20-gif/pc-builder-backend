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