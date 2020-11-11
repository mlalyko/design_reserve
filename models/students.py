from mongoengine import *

connect('design_reserve_db')


class Rating(EmbeddedDocument):
    registrations = IntField()
    confirmations = IntField()
    visits = IntField()


class Students(Document):
    chat_id = IntField()
    username = StringField()
    first_name = StringField()
    last_name = StringField()
    registrations = ListField(ObjectIdField())
    awaiting = ListField(ObjectIdField())
    rating = EmbeddedDocumentField(Rating)
