from mongoengine import Document, StringField, IntField, DateTimeField, ListField


class User(Document):
    user_name = StringField(required=True, unique=False)
    email = StringField(required=True, unique=True)
    otp = IntField()
    otp_creation_time = DateTimeField()
    password = StringField()
    business_name = StringField(required= False, default = "")
    notified_emails = ListField(required = False, default = [])
