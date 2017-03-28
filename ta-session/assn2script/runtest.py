import debttest
import requests
from time import sleep
from random import randint

def get_id(users_json, uname):
    for user_json in users_json:
        if user_json["username"] == uname:
            return user_json["id"]
    print('Cannot find user {0}! Did you run "python manage.py shell < inittest.py"?'.format(uname))
    exit(1)

def get_json_or_error(link):
    sleep(0.05)
    try:
        res = requests.get(link).json()
        return res
    except Exception:
        print("ERROR: Cannot get {0}".format(link))
        exit(1)

def check_key(debt_json, key):
    if key not in debt_json:
        print("{0} not in {1}.".format((key, debt_json)))
        exit(1)


userN = 10
user_pairs = debttest.create_users(userN)
# get id of each user
print("1. Getting users list.")
users_json = get_json_or_error("http://localhost:8000/users/")

users = [ (uname, upwd, get_id(users_json, uname)) for (uname, upwd) in user_pairs ]

# remove existing debts
print("2. Checking GET http://localhost:8000/debts/")
debts_old = get_json_or_error("http://localhost:8000/debts/")

print("3. Checking DELETE http://localhost:8000/debts/")
for debt in debts_old:
    print("\tDeleting debt {0}".format(debt["id"]))
    try:
        requests.delete("http://localhost:8000/debts/{0}".format(debt["id"]))
    except Exception:
        print("ERROR: Cannot send delete to http://localhost:8000/debts/{0}.".format(debt["id"]))
        exit(1)

# create debts
debts = []
debtN = 40
print("4. Checking POST http://localhost:8000/debts/ by creating {0} debts.".format(debtN))
for i in range(0, debtN):
    amnt = randint(1, 1000)
    borrower = users[randint(0, len(users) - 1)][2]
    while True:
        lender = users[randint(0, len(users) - 1)][2]
        if lender != borrower:
            break
    payload = {'amount':amnt, 'borrower':borrower, 'lender':lender}
    debts.append(payload)
    try:
        requests.post("http://localhost:8000/debts/", data=payload)
    except Exception:
        print("ERROR: Cannot post http://localhost:8000/debts/")
        exit(1)

debts_json = get_json_or_error("http://localhost:8000/debts/")
if len(debts_json) != len(debts):
    print("ERROR: GET http://localhost:8000/debts/ has more or less items than debts")
    exit(1)

for debt in debts:
    found = False
    for debt_json in debts_json:
        check_key(debt_json, "borrower")
        check_key(debt_json, "lender")
        check_key(debt_json, "id")
        check_key(debt_json, "created")
        check_key(debt_json, "amount")
        if debt_json["borrower"] == debt["borrower"] and debt_json["lender"] == debt["lender"] and debt_json["amount"] == debt["amount"]:
            found = True
            debt["id"] = debt_json["id"]
            debt["created"] = debt_json["created"]
            break
    if not found:
        print("ERROR: Not found : {0}".format(debt))
        exit(1)

print("5. Checking GET http://localhost:8000/debts/id/")
for debt in debts:
    debt_json = get_json_or_error("http://localhost:8000/debts/{0}/".format(debt["id"]))
    if debt != debt_json:
        print("ERROR: Not equivalent : {0} != {1}".format((debt, debt_json)))
        exit(1)

print("6. Checking PUT http://localhost:8000/debts/id/")
for debt in debts:
    # swap borrower and lender
    debt["lender"], debt["borrower"] = debt["borrower"], debt["lender"]
    try:
        requests.put("http://localhost:8000/debts/{0}/".format(debt["id"]), data=debt)
    except Exception:
        print("ERROR: Cannot put http://localhost:8000/debts/{0}/".format(debts["id"]))
        exit(1)
    debt_refreshed = get_json_or_error("http://localhost:8000/debts/{0}/".format(debt["id"]))
    if (debt_refreshed["borrower"] == debt["borrower"] and debt_refreshed["lender"] == debt["lender"] and
            debt_refreshed["amount"] == debt["amount"] and debt_refreshed["created"] == debt["created"]):
        pass
    else:
        print("ERROR: PUT http://localhost:8000/debts/{0}/ didn't update value".format(debt["id"]))
        print("From /debts/{0}/ : {1}, sent data : {2}".format(debt["id"], debt_refreshed, debt))
        exit(1)

print("7. Checking DELETE http://localhost:8000/debts/id/")
debt0 = debts[0]
del debts[0]
try:
    requests.delete("http://localhost:8000/debts/{0}/".format(debt0["id"]))
except Exception:
    print("ERROR: Cannot delete http://localhost:8000/debts/{0}/".format(debts["id"]))
    exit(1)

print("8. Checking GET http://localhost:8000/users/")
users_json = get_json_or_error("http://localhost:8000/users/")
debts_json = get_json_or_error("http://localhost:8000/debts/")
for user_json in users_json:
    debt_ids_as_borrower = [debt["id"] for debt in debts_json if debt["borrower"] == user_json["id"]]
    debt_ids_as_lender = [debt["id"] for debt in debts_json if debt["lender"] == user_json["id"]]
    # Check user_json["debts_as_borrower"] and user_json["debts_as_lender"]
    if set(debt_ids_as_borrower) != set(user_json["debts_as_borrower"]):
        print("ERROR: debts that user {0} is a borrower does not match".format(user_json["id"]))
        print("From /users/ : {0}, Filtered from /debts/ : {1}".format((user_json["debts_as_borrower"], debt_ids_as_borrower)))
        exit(1)
    if set(debt_ids_as_lender) != set(user_json["debts_as_lender"]):
        print("ERROR: debts that user {0} is a lender does not match".format(user_json["id"]))
        print("From /users/ : {0}, Filtered from /debts/ : {1}".format((user_json["debts_as_lender"], debt_ids_as_lender)))
        exit(1)

print("9. Checking GET http://localhost:8000/usersum/")
users_json = get_json_or_error("http://localhost:8000/usersum/")
debts_json = get_json_or_error("http://localhost:8000/debts/")
for user_json in users_json:
    borrowed_amounts = [debt["amount"] for debt in debts_json if debt["borrower"] == user_json["id"]]
    borrowed_sum = sum(borrowed_amounts)
    lended_amounts = [debt["amount"] for debt in debts_json if debt["lender"] == user_json["id"]]
    lended_sum = sum(lended_amounts)
    if borrowed_sum != user_json["borrowed_money"]:
        print("ERROR: total borrowed money does not match on user {0}".format(user_json["id"]))
        print("From /users/ : {0}, Sum from /debts/ : {1}".format((user_json["borrowed_money"], borrowed_sum)))
        exit(1)
    if lended_sum != user_json["lended_money"]:
        print("ERROR: total lended money does not match on user {0}".format(user_json["id"]))
        print("From /users/ : {0}, Sum from /debts/ : {1}".format((user_json["lended_money"], lended_sum)))
        exit(1)

print("TEST SUCCESSFUL")
