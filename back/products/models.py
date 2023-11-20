from django.db import models


options = (
    (1, '제한없음'),
    (2, '서민전용'),
    (3, '일부제한')
)


class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)  # 예금 상품 코드
    dcls_month = models.TextField()  # 공시 제출월
    fin_co_no = models.TextField()  # 금융회사코드
    kor_co_nm = models.TextField()  # 금융회사명
    fin_prdt_nm = models.TextField()  # 금융상품명
    etc_note = models.TextField()  # 기타 유의사항
    join_deny = models.IntegerField(choices=options)  # 가입 제한
    join_member = models.TextField()  # 가입 대상
    join_way = models.TextField()  # 가입 방법
    spcl_cnd = models.TextField()  # 우대 조건
    max_limit = models.IntegerField(blank=True, null=True)  # 최고 한도
    mtrt_int = models.TextField()  # 만기 후 이자율


class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='dep_option')  # 외래 키
    fin_prdt_cd = models.TextField()  # 예금 상품 코드
    intr_rate_type = models.CharField(max_length=100)  # 저축금리 유형
    intr_rate_type_nm = models.CharField(max_length=100)  # 저축금리 유형명
    intr_rate = models.FloatField(default=-1, blank=True, null=True)  # 저축 금리
    intr_rate2 = models.FloatField(default=-1, blank=True, null=True)  # 최고 우대 금리
    save_trm = models.IntegerField()  # 저축 기간 (단위: 개월)
    
    
class SavingProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)  # 적금 상품 코드
    dcls_month = models.TextField()  # 공시 제출월
    fin_co_no = models.TextField()  # 금융회사코드
    kor_co_nm = models.TextField()  # 금융회사명
    fin_prdt_nm = models.TextField()  # 금융상품명
    etc_note = models.TextField()  # 기타 유의사항
    join_deny = models.IntegerField(choices=options)  # 가입 제한
    join_member = models.TextField()  # 가입 대상
    join_way = models.TextField()  # 가입 방법
    spcl_cnd = models.TextField()  # 우대 조건
    max_limit = models.IntegerField(blank=True, null=True)  # 최고 한도
    mtrt_int = models.TextField()  # 만기 후 이자율


class SavingOptions(models.Model):
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE, related_name='sav_option')  # 외래 키
    fin_prdt_cd = models.TextField()  # 적금 상품 코드
    intr_rate_type = models.CharField(max_length=100)  # 저축금리 유형
    intr_rate_type_nm = models.CharField(max_length=100)  # 저축금리 유형명
    intr_rate = models.FloatField(default=-1, blank=True, null=True)  # 저축 금리
    intr_rate2 = models.FloatField(default=-1, blank=True, null=True)  # 최고 우대 금리
    rsrv_type = models.TextField(default=-1, blank=True, null=True)  # 적립 유형
    rsrv_type_nm = models.TextField(default=-1, blank=True, null=True)  # 적립 유형명
    save_trm = models.IntegerField()  # 저축 기간 (단위: 개월)