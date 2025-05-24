from django.contrib import admin
from .models import (
    Profile,
    Wallet,
    CreditCard,
    BankAccount,
    Deposit,
    Withdrawal,
    Transaction,
    Trade,
)


# Inline admins for Wallet and BankAccount
class WalletInline(admin.TabularInline):
    model = Wallet
    extra = 1
    can_delete = True
    show_change_link = True


class BankAccountInline(admin.TabularInline):
    model = BankAccount
    extra = 1
    can_delete = True
    show_change_link = True


# Profile admin with inlines
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "account_is_active", "balance")
    search_fields = ("user__username", "first_name", "last_name")
    list_filter = ("account_is_active",)
    inlines = [WalletInline, BankAccountInline]


# Wallet admin (optional if included inline)
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("name", "address")


# BankAccount admin (optional if included inline)
@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = (
        "bank_name",
        "account_number",
        "bank_location",
        "swiss_code",
        "profile",
    )


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ("name", "card", "expiring_date", "cvv", "profile")


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ("reference", "date", "amount", "status", "profile")
    list_filter = ("status",)
    search_fields = ("reference", "profile__user__username")


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ("reference", "date", "amount", "status", "profile")
    list_filter = ("status",)
    search_fields = ("reference", "profile__user__username")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "date",
        "description",
        "amount",
        "transaction_type",
        "method",
        "profile",
    )
    list_filter = ("transaction_type",)
    search_fields = ("reference", "profile__user__username")


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = (
        # "id",
        # "profile",
        # "amount",
        "status",
        "conclusion",
        "duration",
        "profit_margin",
        "created_at",
        "profit_display",
    )
    list_filter = ("status", "conclusion", "created_at")
    search_fields = ("profile__user__username", "profile__user__email")
    readonly_fields = ("created_at", "profit_display")

    def profit_display(self, obj):
        return obj.profit_value()

    profit_display.short_description = "Profit/Loss"

    def has_add_permission(self, request):
        return True  # or False to prevent manual trade creation

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
