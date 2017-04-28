from django.contrib.auth.models import User
from omok_backend_rest.models import *
import json
import requests

History.objects.all().delete()

Room.objects.all().delete()
for i in range(0, 20):
    r2 = Room.objects.create()
    r2.save()

try:
    user = User.objects.create_user("omok_admin",
        password="omok_adminpassword")
    user.save()
except Exception:
    pass

for i in range(1, 10):
    try:
        user = User.objects.create_user("user{0}".format(i),
            password="user{0}password".format(i))
        user.save()
    except Exception:
        pass

print("Initialization Successful!")
