from rest_framework import serializers
from allauth.account import app_settings as allauth_settings
from allauth.utils import get_username_max_length
from allauth.account.adapter import get_adapter
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    # 추가할 필드들을 정의합니다.
    nickname = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=255
    )
    age = serializers.IntegerField(required=True)
    money = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)
    financial_products = serializers.ListField(child=serializers.IntegerField(), required=False)

    profile_thumbnail = serializers.ImageField(required=False)
    # mileage = serializers.IntegerField(required=False)
    favorite = serializers.ListField(child=serializers.IntegerField(), required=False)
    mbti = serializers.CharField(
        max_length=10,
        required=False,
    )
    main_bank = serializers.CharField(max_length=30, required=False)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'age': self.validated_data.get('age', ''),
            'money': self.validated_data.get('money', ''),
            'salary': self.validated_data.get('salary', ''),
            'financial_products': self.validated_data.get('financial_products', ''),
            'profile_thumbnail': self.validated_data.get('profile_thumbnail', ''),
            'mileage': self.validated_data.get('mileage', ''),
            'favorite': self.validated_data.get('favorite', ''),
            'mbti': self.validated_data.get('mbti', ''),
            'main_bank': self.validated_data.get('main_bank', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        return user