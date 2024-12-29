from yoomoney import Quickpay, Client

import lib.kb as kb
from lib.db import DataBase
import lib.text as text
from lib.env import cfg

# quickpay = Quickpay(
#     receiver="410019014512803",
#             quickpay_form="shop",
#             targets="Sponsor this project",
#             paymentType="SB",
#             sum=150,
# ) 

# print(quickpay.base_url)
# print(quickpay.redirected_url) 

def deposite_url(user_id, sum):
    quickpay = Quickpay(
        receiver=user_id,
            quickpay_form="shop",
            targets="Sponsor this project",
            paymentType="SB",
            sum=sum,
            label=user_id,
) 
    return quickpay.base_url

def check_payment(label):
      pass