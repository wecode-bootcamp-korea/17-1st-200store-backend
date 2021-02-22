import json
from datetime     import datetime, timedelta
from pytz         import utc

from django.views import View
from django.http  import JsonResponse

from .models      import Product # image_url 추가하면 구성해주기
from order.models import Order

def isNew(create_at, compare_date):
    return True if compare_date < create_at  else False

def checkBestList():
    best_query = Product.objects.all().only('id').order_by('-total_sales')[:20]
    return [best.id for best in best_query]

def isBest(checkList, id):
    return True if id in checkList else False 

def isSale(sale):
    return True if sale > 0 else False

class MainView(View):
    def get(self, request):
        compare_date = utc.localize(datetime.utcnow()) + timedelta(days=-30)
        checkBest    = checkBestList()

        best_query = Product.objects.all().only('id', 'name', 'image_url', 'category', 'price', 'sale','create_at').order_by('-total_sales')[:4]
        best_list  = [{
            'id'       : best.id,
            'name'     : best.name,
            'imageUrl' : best.image_url,
            'category' : best.category.id,
            'price'    : best.price,
            'sale'     : best.sale,
            'isNew'    : isNew(best.create_at, compare_date),
            'isBest'   : isBest(checkBest, best.id),
            'isSale'   : isSale(best.sale)
        } for best in best_query]

        new_query  = Product.objects.all().only('id', 'name', 'image_url', 'category', 'price', 'sale','create_at').order_by('-sale')[:8]
        new_list   = [{
            'id'       : new.id,
            'name'     : new.name,
            'imageUrl' : new.image_url,
            'category' : new.category.id,
            'price'    : new.price,
            'sale'     : new.sale,
            'isNew'    : isNew(new.create_at, compare_date),
            'isBest'   : isBest(checkBest, new.id),
            'isSale'   : isSale(new.sale)
        } for new in new_query]

        sale_query = Product.objects.filter(sale__gt=0).only('id', 'name', 'image_url', 'category', 'price', 'sale','create_at')[:8]
        sale_list  = [{
            'id'       : sale.id,
            'name'     : sale.name,
            'imageUrl' : sale.image_url,
            'category' : sale.category.id,
            'price'    : sale.price,
            'sale'     : sale.sale,
            'isNew'    : isNew(sale.create_at, compare_date),
            'isBest'   : isBest(checkBest, sale.id),
            'isSale'   : isSale(sale.sale)
        } for sale in sale_query]

        return JsonResponse({
            'message' : 'SUCCESS',
            'data'    : {
                'best' : best_list,
                'new'  : new_list,
                'sale' : sale_list 
            }}, status=200)