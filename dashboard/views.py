from django.http import JsonResponse
from .models import (
    BankAccount,
    Profile,
    Transaction,
    Wallet,
    Withdrawal,
    Deposit,
    Trade,
)
from allauth.account.views import SignupView
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views import View
from .mixins import EmailVerifiedRequiredMixin
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import TradeSerializer
from rest_framework import generics, status
from rest_framework.response import Response


# Create your views here.
class HomeView(EmailVerifiedRequiredMixin, View):
    def get(self, request):
        return redirect("/dashboard/")

    # def post(self, request):
    #     return redirect("/dashboard/")


class Dashboard(EmailVerifiedRequiredMixin, View):
    def get(self, request):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        total_transactions = Transaction.objects.filter(profile=profile).count()
        pending_deposits = Deposit.objects.filter(
            profile=profile, status="pending"
        ).count()
        try:
            latest_withdrawal = Withdrawal.objects.filter(profile=profile).latest(
                "date"
            )
        except:
            latest_withdrawal = None

        return render(
            request,
            "dashboard/index.html",
            {
                "user": user,
                "profile": profile,
                "latest_withdrawal": latest_withdrawal,
                "total_transactions": total_transactions,
                "pending_deposits": pending_deposits,
            },
        )

    def post(self, request):
        pass


class ProfileView(EmailVerifiedRequiredMixin, View):
    template_name = "dashboard/profile.html"

    def get(self, request):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        wallets = Wallet.objects.filter(profile=profile)
        bank_accounts = BankAccount.objects.filter(profile=profile)
        transactions = Transaction.objects.filter(profile=profile)
        total_transactions = Transaction.objects.filter(profile=profile).count()
        pending_deposits = Deposit.objects.filter(
            profile=profile, status="pending"
        ).count()
        deposits = Deposit.objects.filter(profile=profile)
        withdrawals = Withdrawal.objects.filter(profile=profile)
        try:
            latest_withdrawal = Withdrawal.objects.filter(profile=profile).latest(
                "date"
            )
        except:
            latest_withdrawal = None

        return render(
            request,
            self.template_name,
            dict(
                profile=profile,
                wallets=wallets,
                bank_accounts=bank_accounts,
                transactions=transactions,
                pending_deposits=pending_deposits,
                total_transactions=total_transactions,
                latest_withdrawal=latest_withdrawal,
                deposits=deposits,
                withdrawals=withdrawals,
            ),
        )

    def post(self, request):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        first_name = self.request.POST.get("first_name")
        last_name = self.request.POST.get("last_name")
        profile.first_name = first_name
        profile.last_name = last_name
        profile.save()

        return redirect("/dashboard/profile/")


class AddNewWallet(EmailVerifiedRequiredMixin, View):
    def post(self, request):
        profile = Profile.objects.get(user=self.request.user)
        name, address = self.request.POST.get("name"), self.request.POST.get("address")
        wallet = Wallet.objects.create(name=name, address=address, profile=profile)
        wallet.save()

        return redirect("/dashboard/profile/")


class EditWallet(EmailVerifiedRequiredMixin, View):
    def post(self, request, id):
        name, address = self.request.POST.get("name"), request.POST.get("address")
        wallet = Wallet.objects.get(id=id)
        wallet.name = name
        wallet.address = address
        wallet.save()

        return redirect("/dashboard/profile/")


class DeleteWallet(EmailVerifiedRequiredMixin, View):
    def get(self, request, id):
        wallet = Wallet.objects.get(id=id)
        wallet.delete()

        return redirect("/dashboard/profile/")


class TransactionsView(ProfileView):
    template_name = "dashboard/transactions.html"


class DepositView(ProfileView):
    template_name = "dashboard/deposit.html"

    def post(self, request):
        profile = Profile.objects.get(user=self.request.user)
        amount = self.request.POST.get("amount")
        proof = self.request.FILES.get("proof")
        wallet_type = self.request.POST.get("wallet_type")
        deposit = Deposit.objects.create(
            profile=profile, amount=amount, proof=proof, wallet_type=wallet_type
        )
        return redirect("/dashboard/deposit/")


class WithdrawalView(ProfileView):
    template_name = "dashboard/withdrawal.html"

    def post(self, request):
        profile = Profile.objects.get(user=self.request.user)
        amount = self.request.POST.get("amount")
        proof = self.request.FILES.get("proof")
        wallet_type = self.request.POST.get("wallet_type")
        deposit = Withdrawal.objects.create(
            profile=profile, amount=amount, proof=proof, wallet_type=wallet_type
        )
        return redirect("/dashboard/withdraw/")


class TradeListView(View):
    template_name = "dashboard/trades.html"

    def get(self, request):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        wallets = Wallet.objects.filter(profile=profile)
        bank_accounts = BankAccount.objects.filter(profile=profile)
        transactions = Transaction.objects.filter(profile=profile)
        total_transactions = Transaction.objects.filter(profile=profile).count()
        pending_deposits = Deposit.objects.filter(
            profile=profile, status="pending"
        ).count()
        deposits = Deposit.objects.filter(profile=profile)
        withdrawals = Withdrawal.objects.filter(profile=profile)
        trades = Trade.objects.filter(profile=profile)
        try:
            latest_withdrawal = Withdrawal.objects.filter(profile=profile).latest(
                "date"
            )
        except:
            latest_withdrawal = None

        return render(
            request,
            self.template_name,
            dict(
                profile=profile,
                wallets=wallets,
                bank_accounts=bank_accounts,
                transactions=transactions,
                pending_deposits=pending_deposits,
                total_transactions=total_transactions,
                latest_withdrawal=latest_withdrawal,
                deposits=deposits,
                withdrawals=withdrawals,
                trades=trades,
            ),
        )


class CustomLoginView:
    pass


class TradeView(EmailVerifiedRequiredMixin, View):
    def get(self, request, amount):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        profile.balance -= float(amount)
        profile.save()

        return JsonResponse("Successful", safe=False)


class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            profile=self.request.user.profile
        )  # assumes Profile is linked via user


from .serializers import TradeSerializer


class TradeCreateAPIView(generics.CreateAPIView):
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {"request": self.request}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trade = serializer.save()

        # Get the user's profile
        profile = request.user.profile

        return Response(
            {
                "message": "Trade created successfully",
                "trade_id": trade.id,
                "balance": profile.balance,  # Return current balance
            },
            status=status.HTTP_201_CREATED,
        )


def custom_404_view(request, exception):
    return render(request, "dashboard/404.html", status=404)
