from incomes.models import Income
from spendings.models import Spending
from accounts.models import User
from datetime import timedelta
from django.utils import timezone

Instances = {}


def get_user_context(
    i, is_admin=False, is_staff=False, is_manager=False, is_superuser=False
):
    kw = {}
    first_name = f"user_{i}"
    last_name = "_finance"
    mobile = f"{9090909090+i}"
    email = f"{first_name + last_name}@dispostable.com"
    kw["first_name"] = first_name
    kw["last_name"] = last_name
    kw["mobile"] = mobile
    kw["email"] = email
    kw["username"] = first_name + " " + last_name

    if is_admin:
        kw["is_admin"] = True
    elif is_staff:
        kw["is_staff"] = True
    elif is_manager:
        kw["is_manager"] = True
    elif is_superuser:
        kw["is_superuser"] = True
    return kw


def create_users(user_count=2):
    global Instances
    users = []
    password = "temp"
    for i in range(user_count):
        kw = get_user_context(i)
        user, c = User.objects.get_or_create(**kw)
        user.set_password(password)
        user.save()
        users.append(user.id)
    Instances["users"] = users


def create_incomes(temp):
    global Instances
    users = Instances.get("users")
    incomes = []
    for u in users:
        for i in range(temp):
            income, c = Income.objects.get_or_create(
                user_id=u,
                source=f"Job_{i}",
                salary=20000 + i,
            )
            income.created_at = timezone.now() - timedelta(weeks=4 * i)
            print(timezone.now() - timedelta(weeks=4 * i))
            income.save()
            incomes.append(income.id)
        if "incomes" not in Instances:
            Instances["incomes"] = [{u: incomes}]
        else:
            Instances["incomes"].append({u: incomes})


def create_spendings(temp):
    global Instances
    users = Instances.get("users")
    spendings = []
    for u in users:
        for i in range(temp):
            spending, c = Spending.objects.get_or_create(
                user_id=u,
                spent_on=f"Party_{i}",
                spent_money=(5000 + i),
            )
            spending.created_at = timezone.now() - timedelta(weeks=4 * i)
            spending.save()
            spendings.append(spending.id)
        if "spendings" not in Instances:
            Instances["spendings"] = [{u: spendings}]
        else:
            Instances["spendings"].append({u: spendings})


def run():
    temp = 20
    create_users()
    create_incomes(temp)
    create_spendings(temp)
    print("creates Instances:", Instances)
