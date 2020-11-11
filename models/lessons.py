from mongoengine import *

connect('design_reserve_db')


class SignedUpStudents(EmbeddedDocument):
    student = ObjectIdField()
    craft_thing = StringField()
    confirmation = BooleanField()
    probability_of_arrival = FloatField()


class Lessons(Document):
    date = DateField()
    slots = IntField()
    signed_up_students = ListField(EmbeddedDocumentField(SignedUpStudents))
    awaiting_students = ListField(ObjectIdField)
