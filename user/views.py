from datetime import datetime
from datetime import timedelta
from json     import JSONDecodeError
from jwt      import DecodeError

import bcrypt
import json
import jwt
import re

from django.http  import JsonResponse
from django.views import View

from my_settings import ALGORITHM
from my_settings import SECRET_KEY
from user.models import Coupon
from user.models import Grade
from user.models import User
from user.models import UserCoupon

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            account  = data.get('account', None)
            password = data.get('password', None)

            if not account:
                return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

            if not password:
                return JsonResponse({'message': 'BAD_REQUEST'}, status=400)

            if not User.objects.filter(account=account).exists():
                return JsonResponse({'message': 'INVALID_USER_ID'}, status=401)

            user = User.objects.get(account=account)
            decoded_hashed_password = user.password

            if not bcrypt.checkpw(password.encode('utf-8'), decoded_hashed_password.encode('utf-8')):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

            access_token = jwt.encode({'user_pk': user.pk}, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({'message': 'SUCCESS', 'ACCESS_TOKEN': access_token}, status=200)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)
