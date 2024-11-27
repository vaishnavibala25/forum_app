from mongoengine import Document, StringField

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = StringField(required=False)  # Add this field
    bio = StringField(required=False)    # Add this field