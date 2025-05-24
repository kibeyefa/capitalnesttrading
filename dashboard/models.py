from django.db import models
from django_extensions.db.fields import RandomCharField
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    account_is_active = models.BooleanField(default=False)
    balance = models.FloatField(default=0.0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


# Withdrawal Models
class Wallet(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )


class CreditCard(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    card = models.CharField(max_length=255)
    expiring_date = models.CharField(max_length=4)
    cvv = models.CharField(max_length=4)
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )


class BankAccount(models.Model):
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    bank_location = models.TextField()
    swiss_code = models.CharField(max_length=255)
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )


class Deposit(models.Model):
    reference = RandomCharField(
        max_length=12, uppercase=True, primary_key=True, unique=True, length=12
    )
    date = models.DateField(auto_now=False, auto_now_add=True)
    amount = models.FloatField()
    status = models.CharField(
        max_length=255,
        choices=(
            ("verified", "verified"),
            ("pending", "pending"),
        ),
        default="pending",
    )
    proof = CloudinaryField("image", folder="capitalnest/deposits/proofs")
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )
    completed = models.BooleanField(default=False)


class Withdrawal(models.Model):
    reference = RandomCharField(
        max_length=12, uppercase=True, primary_key=True, unique=True, length=12
    )
    date = models.DateField(auto_now=False, auto_now_add=True)
    amount = models.FloatField()
    status = models.CharField(
        max_length=255,
        choices=(
            ("verified", "verified"),
            ("pending", "pending"),
        ),
        default="pending",
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, blank=True, null=True)
    bank_account = models.ForeignKey(
        BankAccount, on_delete=models.SET_NULL, blank=True, null=True
    )
    proof = CloudinaryField("image", folder="capitalnest/withdrawal/proofs")
    wallet_type = models.CharField(
        max_length=255,
        choices=(
            ("btc", "btc"),
            ("usdt", "usdt"),
            ("eth", "eth"),
        ),
        default="usdt",
    )
    completed = models.BooleanField(default=False)


class Transaction(models.Model):
    reference = RandomCharField(
        max_length=12, uppercase=True, primary_key=True, unique=True, length=12
    )
    date = models.DateField(auto_now=False, auto_now_add=True)
    description = models.TextField()
    amount = models.FloatField()
    transaction_type = models.CharField(
        max_length=255,
        choices=(
            ("signup", "Signup Bonus"),
            ("referal", "Referal Bonus"),
            ("deposit", "Deposit"),
            ("withdrawal", "Withdrawal"),
        ),
    )
    method = models.CharField()
    status = models.CharField(
        max_length=255,
        choices=(
            ("verified", "verified"),
            ("pending", "pending"),
        ),
        default="pending",
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )


class Trade(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    id = RandomCharField(unique=True, length=12, primary_key=True, uppercase=True)

    amount = models.FloatField(default=0.0)  # Amount invested in the trade

    status = models.CharField(
        max_length=255,
        choices=(
            ("ongoing", "ongoing"),
            ("closed", "closed"),
        ),
    )

    conclusion = models.CharField(
        max_length=255,
        choices=(
            ("profit", "profit"),
            ("loss", "loss"),
            ("pending", "pending"),
        ),
    )

    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)

    profit_margin = models.FloatField(default=7.50)  # % profit or loss margin

    def profit_value(self):
        """
        Calculates the absolute profit/loss based on conclusion.
        """
        if self.conclusion == "profit":
            return round(self.amount * (self.profit_margin / 10), 2)
        elif self.conclusion == "loss":
            return -round(self.amount * (self.profit_margin / 10), 2)
        return 0.0  # Pending or unknown

    def __str__(self):
        return f"Trade #{self.id} - {self.profile} - {self.status}"
