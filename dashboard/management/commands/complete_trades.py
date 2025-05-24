from random import choice
from django.core.management.base import BaseCommand
from django.utils import timezone
from dashboard.models import Trade


class Command(BaseCommand):
    help = "Check and close completed trades"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        trades = Trade.objects.filter(status="ongoing")

        for trade in trades:
            end_time = trade.created_at + trade.duration
            if now >= end_time:
                # Assume conclusion is already set somehow (e.g., random, strategy)
                trade.conclusion = choice(
                    [
                        "profit",
                        "profit",
                        "profit",
                        "profit",
                        "loss",
                        "profit",
                        "profit",
                        "profit",
                        "profit",
                        "loss",
                    ]
                )
                trade.status = "closed"
                profit = trade.profit_value()

                trade.profile.balance += profit
                trade.profile.save()
                trade.save()

                # self.stdout.write(
                #     f"Trade #{trade.id} closed. Profit: {profit}, New Balance: {trade.profile.balance}"
                # )
