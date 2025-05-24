import random

# serializers.py
from rest_framework import serializers
from .models import Trade


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ["id", "amount", "duration"]

    def create(self, validated_data):
        request = self.context.get("request")
        profile = request.user.profile
        amount = validated_data["amount"]

        if profile.balance < amount:
            raise serializers.ValidationError("Insufficient balance.")

        # Deduct balance and save
        profile.balance -= amount
        profile.save()

        return Trade.objects.create(
            profile=profile, status="ongoing", conclusion="pending", **validated_data
        )


class TradeCloseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ["id", "status", "conclusion"]
        read_only_fields = ["conclusion"]

    def validate(self, attrs):
        instance = self.instance
        if instance.status != "ongoing":
            raise serializers.ValidationError("Only ongoing trades can be closed.")
        return attrs

    def update(self, instance, validated_data):
        instance.status = "closed"
        instance.conclusion = random.choice(["profit", "loss"])
        instance.save()
        return instance
