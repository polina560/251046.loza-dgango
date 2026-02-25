# serializers.py
from rest_framework import serializers

from account.models import UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'uid', 'rid', 'clan',
                  'referral_code', 'created_at']


