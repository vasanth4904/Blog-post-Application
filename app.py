from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

# ---------------- Blog Post Model ----------------
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False, default='Anonymous')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# ---------------- Web Routes ----------------
@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template("index.html", posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        new_post = Post(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("create.html")

@app.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template("post.html", post=post)

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

# ---------------- API Routes ----------------
@app.route('/api/posts', methods=['GET', 'POST'])
def api_posts():
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'title' not in data or 'content' not in data:
            return {"error": "Title and content required"}, 400
        new_post = Post(
            title=data['title'],
            content=data['content'],
            author=data.get('author', 'Anonymous')
        )
        db.session.add(new_post)
        db.session.commit()
        return {
            "id": new_post.id,
            "title": new_post.title,
            "content": new_post.content,
            "author": new_post.author,
            "date_created": new_post.date_created.isoformat()
        }, 201
    all_posts = Post.query.order_by(Post.date_created.desc()).all()
    return [{
        "id": p.id,
        "title": p.title,
        "content": p.content,
        "author": p.author,
        "date_created": p.date_created.isoformat()
    } for p in all_posts]

@app.route('/api/posts/<int:id>', methods=['GET','PUT','DELETE'])
def api_post_detail(id):
    post = Post.query.get_or_404(id)
    if request.method == 'GET':
        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": post.author,
            "date_created": post.date_created.isoformat()
        }
    elif request.method == 'PUT':
        data = request.get_json()
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        post.author = data.get('author', post.author)
        db.session.commit()
        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": post.author,
            "date_created": post.date_created.isoformat()
        }
    elif request.method == 'DELETE':
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted"}

# ---------------- Run Server ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create database tables if not exist
    app.run(debug=True, port=8000)
