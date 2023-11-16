from django.db import models

# Create your models here.

options = (
    (1, '성공'),
    (2, 'DATA코드 오류'),
    (3, '인증코드 오류'),
    (4, '일일제한횟수 마감')
)

class ExchangeRates(models.Model):
    result = models.IntegerField(choices=options)           # 조회 결과(options)
    cur_unit = models.TextField(unique=True)                # 통화코드
    ttb = models.TextField()                                # 송금받을 때
    tts = models.TextField()                                # 송금보낼 때
    deal_bas_r =  models.TextField()                        # 매매 기준율
    bkpr =  models.TextField()                              # 장부가격
    yy_efee_r = models.TextField()                          # 년환가료율
    ten_dd_efee_r = models.TextField()                      # 10일환가료율
    kftc_bkpr = models.TextField()                          # 서울외국환중개 장부가격
    kftc_deal_bas_r = models.TextField()                    # 서울외국환중개 매매기준율
    cur_nm = models.TextField()                             # 국가/통화명



# class DepositProducts(models.Model):
#     fin_prdt_cd = models.TextField(unique=True)
#     kor_co_nm = models.TextField()
#     fin_prdt_nm = models.TextField()
#     etc_note = models.TextField()
#     join_deny = models.IntegerField(choices=options)
#     join_member = models.TextField()
#     join_way = models.TextField()
#     spcl_cnd = models.TextField()


# class DepositOptions(models.Model):
#     product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='option')
#     fin_prdt_cd = models.TextField()
#     intr_rate_type_nm = models.CharField(max_length=100)
#     intr_rate = models.FloatField(default=-1)
#     intr_rate2 = models.FloatField(default=-1)
#     save_trm = models.IntegerField()
