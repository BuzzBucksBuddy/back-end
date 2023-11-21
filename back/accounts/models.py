from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from products.models import SavingProducts, DepositProducts



class Favorite(models.Model):
    favorite = models.CharField(max_length=225, null=True)



class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=255, unique=True)
    profile_thumbnail = ProcessedImageField(
        upload_to = 'profile/',
        processors = [Thumbnail(100, 100)],
        format = 'JPEG',
        options = {'quality': 90},
        blank = True,
        null = True
    )
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='email address')
    mileage = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    money = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    # 리스트 데이터 저장을 위해 Text 형태로 저장
    # financial_products = models.TextField(blank=True, null=True)
    financial_products_dep = models.ManyToManyField(DepositProducts)
    financial_products_sav = models.ManyToManyField(SavingProducts)
    
    # # 한 필드에 모델 두개 참조
    # fp_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    # fp_object_id = models.PositiveIntegerField(blank=True, null=True)
    # content_object = GenericForeignKey('fp_content_type', 'fp_object_id')

    favorite = models.ManyToManyField(Favorite)
    # favorite = models.TextField(blank=True, null=True)
    # financial_products = models.JSONField(blank=True, null=True)
    # favorite = models.JSONField(blank=True, null=True)

    mbti = models.CharField(
        max_length=10,
        blank=True,
        null=True
        )

    main_bank = models.CharField(max_length=30, blank=True, null=True)
    # superuser fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_email, user_field, user_username

        # 기존 코드를 참고하여 새로운 필드들을 작성해줍니다.
        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password1 = data.get("password1")
        password2 = data.get("password2")
        email = data.get("email")
        username = data.get("username")
        nickname = data.get("nickname")
        age = data.get("age")
        money = data.get("money")
        salary = data.get("salary")
        financial_products_dep = data.get("financial_products_dep")
        financial_products_sav = data.get("financial_products_sav")
        

        profile_thumbnail = data.get("profile_thumbnail")
        mileage = data.get("mileage")
        favorite = data.get("favorite")
        mbti = data.get("mbti")
        main_bank = data.get("main_bank")

        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if nickname:
            user_field(user, "nickname", nickname)
        if age:
            user.age = age
        if money:
            user.money = money
        if salary:
            user.salary = salary
        if financial_products_dep:
            user.financial_products_dep = financial_products_dep
        if financial_products_sav:
            user.financial_products_sav = financial_products_sav
        if mileage:
            user.mileage = mileage
        if profile_thumbnail:
            user.profile_thumbnail = profile_thumbnail
        if favorite:
            user.favorite = favorite
        if mbti:
            user.mbti = mbti
        if main_bank:
            user.main_bank = main_bank

        # if financial_product:
        #     financial_products_values = user.financial_products or []
        #     financial_products_values.extend(financial_product.split(',')) 
        #     user_field(user, "financial_products", financial_products_values)
        # if favorite:
        #     favorite_values = user.favorite or []
        #     favorite_values.extend(favorite.split(',')) 
        #     user_field(user, "favorite", favorite_values)
        # if financial_product:
        #     fin = ''
        #     for i in financial_product:
        #         fin = str(i)
        #     # financial_products = user.financial_products.split(',')
        #     # financial_products.append(financial_product)
        #     # if len(financial_products) > 1:
        #     #     financial_products = ','.join(financial_products)
        #     user_field(user, "financial_products", fin)
        # if favorite:
        #     fav = ''
        #     for i in favorite:
        #         fav = str(i)
        #     print(fav)
        #     # user.favorite = fav.split(',')
        #     # user.favorite.append(favorite)
        #     # if len(favorite) > 1:
        #     #     favorite = ','.join(favorite)
        #     user_field(user, "favorite", fav)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user
    

