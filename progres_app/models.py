from django.db import models, connection
from progres_app.handled_cursor import HandledCursor
from django.core.mail import send_mail

# Create your models here.


class User(models.Model):
    email = models.CharField(unique=True, max_length=64)
    password = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=32)
    adress_id = models.IntegerField()
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'users'

    # def login(self, email, password):
    #     cursor = connection.cursor()
    #     result = cursor.callfunc("demo.login", int, [email, password])
    #     print(result)
    #     return result

    # @staticmethod
    # def register(data):
    #     cursor = connection.cursor()
    #     result = cursor.callfunc("user_logic.register", str, [data['email'], data['password'], data['first_name'],
    #                                                     data['last_name'], data['phone'], data['address']])
    #     return json.loads(result)

    @staticmethod
    def register(data):
        handled_cursor = HandledCursor()
        parameters = []

        for param in data:
            parameters.append(data[param])
        handled_cursor.callproc("user_logic.register", parameters)

        register_token = handled_cursor.callfunc("user_logic.get_registration_token", str, [data["email"]])

        # send registration code via email
        subject = "Confirm account"
        body = "Here is your registration code: " + register_token + "\nThis code expires in 3 hours."
        sender = "progres@progres_app.com"
        recipients = [data["email"]]
        send_mail(subject, body, sender, recipients, fail_silently=False)

    def validate_user_registration(self, token):
        handled_cursor = HandledCursor()
        handled_cursor.callproc("user_logic.validate_user_registration", [self.id, token])

    def generate_registration_token(self):
        handled_cursor = HandledCursor()
        handled_cursor.callproc("user_logic.generate_registration_token", [self.email])

        # send registration code via email
        # register_token = handled_cursor.callfunc("user_logic.get_registration_token", str, [self.email])
        # subject = "Confirm account"
        # body = "Here is your registration code: " + register_token + "\nThis code expires in 3 hours."
        # sender = "progres@progres_app.com"
        # recipients = [self.email]
        # send_mail(subject, body, sender, recipients, fail_silently=False)




class Codes(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=32)
    success = models.CharField(unique=True, max_length=1)
    error = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'codes'
