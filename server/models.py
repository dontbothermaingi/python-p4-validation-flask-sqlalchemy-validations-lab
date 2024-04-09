from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name")
        return name
    
    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if not phone_number or len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number should be exactly 10 digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("title")
    def validate_title(self, key, title):
        if not any(phrase in title for phrase in ["Won't Believe", "Secret", "Top", "Guess"]):
            raise ValueError("Post title must contain one of the specified clickbait phrases")
        return title
    
    @validates("content")
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content should be at least 250 characters long")
        return content
    
    @validates("summary")
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary should be a maximum of 250 characters")
        return summary
    
    @validates("category")
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Post category should be either Fiction or Non-Fiction")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
