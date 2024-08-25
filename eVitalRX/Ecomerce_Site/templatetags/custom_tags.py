from django import template
from Ecomerce_Site.models import Product
import json
register = template.Library()

@register.filter(name='productimage')
def productimage(pid):
    data = Product.objects.get(id=pid)
    return data.image.url

@register.filter(name='productname')
def productname(pid):
    data = Product.objects.get(id=pid)
    print(data)
    return data.name

@register.filter(name='productprice')
def productprice(pid):
    data = Product.objects.get(id=pid)
    print(data)
    return data.price

@register.simple_tag()
def producttotalprice(pid, qty):
    data = Product.objects.get(id=pid)
    return int(qty) * int(data.price)

@register.filter()
def get_product(productli):
    try:
        productli = productli.replace("'", '"')
        myli = json.loads(str(productli))['objects'][0]
        print(myli)
        pro_li = []
        for i, j in myli.items():
            pro_li.append(int(i))
        product = Product.objects.filter(id__in=pro_li)
        print(product)
        return product
    except:
        return None

@register.simple_tag
def get_qty(pro, bookid):
    try:
        book = Booking.objects.get(id=bookid)
        productli = book.product.replace("'", '"')
        myli = json.loads(str(productli))['objects'][0]
        return myli[str(pro)]
    except:
        return 0