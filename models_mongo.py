from mongoengine import Document, StringField, ReferenceField, ListField, DateTimeField, CASCADE


class AuthorM(Document):
    fullname = StringField(required=True, unique=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()


class QuoteM(Document):
    content = StringField(required=True)
    author = ReferenceField(AuthorM, reverse_delete_rule=CASCADE)
    tags = ListField(StringField())
