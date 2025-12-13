from flask import Flask, render_template, request, jsonify
from models import db, Note, Category
import os
import markdown
from datetime import datetime

app = Flask(__name__)

# Veritabanı konfigürasyonu
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'postgresql://notesuser:securepass123@db:5432/cloudnotes'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanını başlat
db.init_app(app)

# Veritabanı tablolarını oluştur
with app.app_context():
    db.create_all()
    # İlk kategoriyi oluştur
    if Category.query.count() == 0:
        default_categories = [
            Category(name='Genel', color='#3B82F6'),
            Category(name='İş', color='#EF4444'),
            Category(name='Kişisel', color='#10B981'),
            Category(name='Öğrenim', color='#F59E0B')
        ]
        for cat in default_categories:
            db.session.add(cat)
        db.session.commit()

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

# ============ KATEGORİ API ============

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Tüm kategorileri getir"""
    categories = Category.query.all()
    return jsonify([cat.to_dict() for cat in categories])

@app.route('/api/categories', methods=['POST'])
def create_category():
    """Yeni kategori oluştur"""
    data = request.json
    category = Category(
        name=data['name'],
        color=data.get('color', '#3B82F6')
    )
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201

@app.route('/api/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    """Kategori sil"""
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted'}), 200

# ============ NOT API ============

@app.route('/api/notes', methods=['GET'])
def get_notes():
    """Tüm notları getir (filtreleme ile)"""
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '')
    favorite = request.args.get('favorite', type=bool)
    
    query = Note.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search:
        query = query.filter(
            db.or_(
                Note.title.ilike(f'%{search}%'),
                Note.content.ilike(f'%{search}%'),
                Note.tags.ilike(f'%{search}%')
            )
        )
    
    if favorite:
        query = query.filter_by(is_favorite=True)
    
    notes = query.order_by(Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@app.route('/api/notes/<int:id>', methods=['GET'])
def get_note(id):
    """Tek bir notu getir"""
    note = Note.query.get_or_404(id)
    return jsonify(note.to_dict())

@app.route('/api/notes', methods=['POST'])
def create_note():
    """Yeni not oluştur"""
    data = request.json
    note = Note(
        title=data['title'],
        content=data['content'],
        category_id=data.get('category_id'),
        tags=data.get('tags', ''),
        is_favorite=data.get('is_favorite', False)
    )
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201

@app.route('/api/notes/<int:id>', methods=['PUT'])
def update_note(id):
    """Notu güncelle"""
    note = Note.query.get_or_404(id)
    data = request.json
    
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    note.category_id = data.get('category_id', note.category_id)
    note.tags = data.get('tags', note.tags)
    note.is_favorite = data.get('is_favorite', note.is_favorite)
    note.updated_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify(note.to_dict())

@app.route('/api/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    """Notu sil"""
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted'}), 200

@app.route('/api/notes/<int:id>/favorite', methods=['PATCH'])
def toggle_favorite(id):
    """Favori durumunu değiştir"""
    note = Note.query.get_or_404(id)
    note.is_favorite = not note.is_favorite
    db.session.commit()
    return jsonify(note.to_dict())

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """İstatistikleri getir"""
    total_notes = Note.query.count()
    total_categories = Category.query.count()
    favorite_notes = Note.query.filter_by(is_favorite=True).count()
    
    return jsonify({
        'total_notes': total_notes,
        'total_categories': total_categories,
        'favorite_notes': favorite_notes
    })

@app.route('/api/markdown-preview', methods=['POST'])
def markdown_preview():
    """Markdown önizleme"""
    data = request.json
    html = markdown.markdown(
        data['content'],
        extensions=['fenced_code', 'tables', 'nl2br']
    )
    return jsonify({'html': html})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
