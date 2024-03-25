from api import models
from api import delivery_serializers
import random
import string
import yagmail


def id_generate():
    id = str("".join(random.choices(string.ascii_uppercase+string.digits,k=11)))
    return id

def otp_generate():
    return int(random.randrange(1000,9999))

def validate_email(id):
    valid_data = models.Delivery_model.objects.all()
    valid_email = delivery_serializers.DeliverypersonSerializer(valid_data,many=True)
    data = False
    for i in valid_email.data:
        if id==i['email']:
            data = True
            break
    print("hii")
    return data
    
def validate_otp(id, otp):
    UserData = models.Delivery_model.objects.get(uid = id)
    data = delivery_serializers.DeliverypersonSerializer(UserData)
    valid = False
    if data.data['otp'] == otp:
        valid = True
    return valid

def verify_user(email, password):
    Data = models.Delivery_model.objects.get(email = email)
    data = delivery_serializers.DeliverypersonSerializer(Data)
    authentication = False
    if data.data['email'] == email and data.data['password'] == password:
        authentication = True
    print("hii")
    return authentication


def verify_user_otp(email):
    Data = models.Delivery_model.objects.get(email = email)
    data = delivery_serializers.DeliverypersonSerializer(Data)
    authentication = False
    if data.data['otp'] == data.data['user_otp']:
        authentication = True
    return authentication

def send_mail(receiver_email, otp):
    sender = 'abijithmailforjob@gmail.com'
    password = 'kgqzxinytwbspurf'
    subject = "Miogra Sign Up OTP"
    content = f"""
    OTP : {otp}
    """
    yagmail.SMTP(sender, password).send(
        to=receiver_email,
        subject=subject,
        contents=content
    )

def get_user_id(email):
    Data = models.Delivery_model.objects.get(email = email)
    data = delivery_serializers.DeliverypersonSerializer(Data)
    print(data.data["uid"])
    return data.data['uid']