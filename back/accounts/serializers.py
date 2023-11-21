from rest_framework import serializers
from allauth.account import app_settings as allauth_settings
from allauth.utils import get_username_max_length
from allauth.account.adapter import get_adapter
from .models import User, Favorite
from dj_rest_auth.registration.serializers import RegisterSerializer
from products.serializers import DepositProductsSerializer, SavingProductsSerializer
from django.contrib.auth import get_user_model

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
            model = Favorite
            fields = '__all__'


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
    financial_products_dep = DepositProductsSerializer(many=True, allow_null=True, required=False)
    financial_products_sav = SavingProductsSerializer(many=True, allow_null=True, required=False)
    # financial_products = serializers.ListField(child=serializers.CharField(), required=False)
    # financial_products = serializers.ListField(child=serializers.IntegerField(), required=False)

    profile_thumbnail = serializers.ImageField(required=False)
    # mileage = serializers.IntegerField(required=False)
    favorite = FavoriteSerializer(many=True, allow_null=True, required=False, read_only=True)
    # favorite = serializers.ListField(child=serializers.CharField(), required=False)
    # favorite = serializers.ListField(child=serializers.IntegerField(), required=False)
    mbti = serializers.CharField(
        max_length=10,
        required=False,
    )
    main_bank = serializers.CharField(max_length=30, required=False)


    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'age': self.validated_data.get('age', ''),
            'money': self.validated_data.get('money', ''),
            'salary': self.validated_data.get('salary', ''),
            'financial_products_dep': self.validated_data.get('financial_products_dep', ''),
            'financial_products_sav': self.validated_data.get('financial_products_sav', ''),
            # 'financial_products': self.validated_data.get('financial_products', ''),
            'profile_thumbnail': self.validated_data.get('profile_thumbnail', ''),
            'mileage': self.validated_data.get('mileage', ''),
            'favorite': self.validated_data.get('favorite', ''),
            'mbti': self.validated_data.get('mbti', ''),
            'main_bank': self.validated_data.get('main_bank', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            # 'password': self.validated_data.get('password', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        # 기존 User 정보 저장
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
       
        return user
    
    # def update(self, instance, validated_data):
    #     print("Validated: ", validated_data)


        # # 'password1' 및 'password2'가 데이터에 있는지 확인 후 액세스
        # password1 = self.cleaned_data.get('password1')
        # password2 = self.cleaned_data.get('password2')
        # if password1 is not None and password2 is not None:
        #     if password1 != password2:
        #         raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")



###### 유저 정보 수정 ######
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('nickname',
                  'profile_thumbnail', 
                  'money',  
                  'salary',  
                  'mbti',
                  'main_bank',
                  'mileage',
                )