from typing import Type
from unicodedata import name
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import model_to_dict

User = get_user_model()


class Deposit(models.Model):
    TYPE= (
        ("savings", "Savings"),
        ("current", "Current")
    )
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    # account_balance = models.ForeignKey(User,on_delete=models.CASCADE)
    # account_num = models.ForeignKey(User,on_delete=models.CASCADE)
    account_type = models.CharField(max_length=355, choices=TYPE)

    def __str__(self) -> str:
        return f"You have successfully deposited the sum of {self.amount} and your balance is {self.account_balance}"

        # return f"{self.amount} by {self.user}"

class Transfer(models.Model):
    name = models.CharField(max_length=50, blank=True)
    account_num = models.FloatField(max_length=50, blank=True)
    branch_name = models.CharField(max_length=50, blank=True)
    amount = models.FloatField()
    


    def __str__(self) -> str:
        return f"{self.amount} transferred to {self.name} was successful"


class Withdraw(models.Model):
    amount = models.FloatField()
    # account_num = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # account_balance = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"You have successfully withdrawn {self.amount} from your account"

