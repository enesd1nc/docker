from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Category(db.Model):
    """Kategori modeli - Notları gruplamak için"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    color = db.Column(db.String(7), default='#3B82F6')  # Hex renk kodu
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişki
    notes = db.relationship('Note', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'created_at': self.created_at.isoformat(),
            'note_count': len(self.notes)
        }


class Note(db.Model):
    """Not modeli - Ana veri yapısı"""
    __tablename__ = 'notes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    tags = db.Column(db.String(500))  # Virgülle ayrılmış etiketler
    is_favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'category_color': self.category.color if self.category else None,
            'tags': self.tags.split(',') if self.tags else [],
            'is_favorite': self.is_favorite,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
