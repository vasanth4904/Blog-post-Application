# Flask Blog CRUD Application 📝

A simple blog application built with **Flask** and **SQLite**, supporting both **web interface** and **REST API**.  
You can create, read, update, and delete blog posts from the browser or via **Postman API**.

---

## 🚀 Features
- Create, Read, Update, Delete (CRUD) blog posts
- Web interface using Flask templates
- REST API endpoints for integration / Postman testing
- SQLite database with SQLAlchemy ORM

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/flask-blog-crud.git
   cd flask-blog-crud

2. **Create virtual environment (optional but recommended)**

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. **Install dependencies**

pip install flask flask_sqlalchemy

4. **Run the application**

python app.py

App will run at http://127.0.0.1:8000



---



 ## 🌐 Web Routes

/ → Show all posts

/create → Create new post

/post/<id> → View a single post

/delete/<id> → Delete a post


## 📡 API Routes

**Get all posts**
GET /api/posts

**Get a single post**
GET /api/posts/<id>

**Create a new post**
POST /api/posts
Content-Type: application/json

{
  "title": "First Post",
  "content": "This is my first blog post",
  "author": "Vasanth"
}

**Update a post**
PUT /api/posts/<id>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated Content",
  "author": "Updated Author"
}

**Delete a post**
DELETE /api/posts/<id>
