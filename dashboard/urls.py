from django.urls import path, include
from .views import (
    AddNewWallet,
    Dashboard,
    DepositView,
    EditWallet,
    DeleteWallet,
    HomeView,
    TradeView,
    TradeViewSet,
    ProfileView,
    TradeCreateAPIView,
    TransactionsView,
    WithdrawalView,
)

urlpatterns = [
    path("", HomeView.as_view()),
    path("dashboard/", Dashboard.as_view()),
    path("dashboard/profile/", ProfileView.as_view()),
    path("dashboard/transactions/", TransactionsView.as_view()),
    path("dashboard/deposit/", DepositView.as_view()),
    path("dashboard/withdraw/", WithdrawalView.as_view()),
    path("dashboard/wallets/add/", AddNewWallet.as_view()),
    path("dashboard/wallets/<id>/edit/", EditWallet.as_view()),
    path("dashboard/wallets/<id>/delete/", DeleteWallet.as_view()),
    path("api/trade/<amount>/", TradeView.as_view()),
    path("api/trades/", TradeCreateAPIView.as_view(), name="trade-create"),
]  # Allauth URLs
