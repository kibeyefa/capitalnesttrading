from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Deposit, Withdrawal, Transaction


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # print(instance)
    if created:
        Profile.objects.create(
            user=instance, first_name=instance.first_name, last_name=instance.last_name
        )


@receiver(post_save, sender=Deposit)
def create_transaction_from_deposit(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            reference=instance.reference,
            date=instance.date,
            description=f"Deposit of ${instance.amount}",
            amount=instance.amount,
            transaction_type="deposit",
            method="deposit",  # You can customize this
            profile=instance.profile,
        )


@receiver(post_save, sender=Deposit)
def update_balance_on_verified_deposit(sender, instance, created, **kwargs):
    if instance.status == "verified" and not instance.completed and instance.profile:
        profile = instance.profile
        profile.balance += instance.amount
        profile.save()

        instance.completed = True
        instance.save(update_fields=["completed"])


@receiver(post_save, sender=Withdrawal)
def create_transaction_from_withdrawal(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            reference=instance.reference,
            date=instance.date,
            description=f"Withdrawal of ${instance.amount}",
            amount=instance.amount,
            transaction_type="withdrawal",
            method="withdrawal",  # You can customize this
            profile=instance.profile,
        )


@receiver(post_save, sender=Withdrawal)
def update_balance_on_verified_withrawal(sender, instance, created, **kwargs):
    if instance.status == "verified" and not instance.completed and instance.profile:
        profile = instance.profile
        profile.balance -= instance.amount
        profile.save()

        instance.completed = True
        instance.save(update_fields=["completed"])
