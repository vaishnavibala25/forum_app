# models/reply_model.py
from mongoengine import Document, StringField, ReferenceField

class Reply(Document):
    content = StringField(required=True)
    post = ReferenceField('Post', required=True)  # Use string reference instead of direct import

    def _str_(self):
        return f'Reply(content={self.content}, post={self.post.title})'