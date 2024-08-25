from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from .models import *
from django.contrib import messages

#                 HOME Settings
def home(request):
    return render(request,"home.html")

def navbar(request):
    return render(request, 'navigation.html')

def about(request):
    return render(request,"about.html")

#                   Admin setup (login, Dashboard)
def adminLogin(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                msg = "User login successfully"
                return redirect('admin_dashboard')
            else:
                msg = "Invalid Credentials"
        except:
            msg = "Invalid Credentials"
    dic = {'msg': msg}
    return render(request, 'admin_login.html', dic)


def adminHome(request):
    return render(request, 'admin_base.html')


def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

#                       Add - View and delete the category like Fashion
def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        messages.success(request, "Category added")
        return redirect("view_category")
    return render(request, 'add_category.html', locals())

def view_category(request):
    category = Category.objects.all()
    return render(request, 'view_category.html', locals())

def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('view_category')

#               Add - View -  Edit - Delete Product like In fashion category, product : Shirts
def add_product(request):
    category = Category.objects.all()
    if request.method == "POST":
        main_category = request.POST['category'] #gtes cat id i.id
        name = request.POST['name']
        price = request.POST['price']
        desc = request.POST['desc']
        image = request.FILES['image']
        catobj = Category.objects.get(id=main_category) # id = int id i.id
        # i.catehory.name = i.1.id.name
        Product.objects.create(name=name, price=price, category=catobj, description=desc, image=image)
        messages.success(request, "Product added")
    return render(request, 'add_product.html', locals())
        
def view_product(request):
    product = Product.objects.all()
    return render(request, 'view_product.html', locals())


def edit_product(request, pid):
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        desc = request.POST['desc']
        try:
            image = request.FILES['image']
            product.image = image
            product.save()
        except:
            pass
        catobj = Category.objects.get(id=cat)
        Product.objects.filter(id=pid).update(name=name, price=price,  category=catobj, description=desc)
        messages.success(request, "Product Updated")
        return redirect('view_product')

    return render(request, 'edit_product.html', locals())

def delete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect('view_product')
        
#                User Registration 
# Validation : password and mobile no length, email must be unique
def signup(request):
    if request.method == "POST":
        uname = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['mobile']
        image = request.FILES['image']
        if User.objects.filter(email=email).exists():
            messages.error(request,"This Email ID is already Registered.")
        else:

            user = User.objects.create_user(username=email,first_name=uname, password=password)
            UserData.objects.create(user=user, mobile=mobile, address=address, image=image)
            mydict = {'username':email}
            user.save()
            messages.success(request, "Registeration Successful")
            return redirect('userlogin')
    return render(request, 'signup.html')

def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User login successfully")
            return redirect('about')
        else:
            messages.success(request,"Invalid Credentials")
    return render(request, 'login.html', locals())

# Logout of user
def logoutuser(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('about')

# User views products
def user_product(request,pid):
    if pid == 0:
        product = Product.objects.all()
    else:
        category = Category.objects.get(id=pid)
        product = Product.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "user-product.html", locals())

# can zoom the image and views other products
def product_detail(request, pid):
    try:

        product = Product.objects.get(id=pid)
        latest_product = Product.objects.filter().exclude(id=pid).order_by('-id')[:10]
        return render(request, "product_detail.html", locals())
    except:
        pass

# user can add items to the cart and increase or decrease the quantity
def addToCart(request, pid):
    myli = {"objects":[]}
    try:
        cart = Cart.objects.get(user=request.user)
        myli = json.loads((str(cart.product)).replace("'", '"'))
        try:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
        except:
            myli['objects'].append({str(pid):1})
        cart.product = myli
        cart.save()
    except:
        myli['objects'].append({str(pid): 1})
        cart = Cart.objects.create(user=request.user, product=myli)
    return redirect('cart')

def incredecre(request, pid):
    cart = Cart.objects.get(user=request.user)
    if request.GET.get('action') == "incre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) + 1
    if request.GET.get('action') == "decre":
        myli = json.loads((str(cart.product)).replace("'", '"'))
        if myli['objects'][0][str(pid)] == 1:
            del myli['objects'][0][str(pid)]
        else:
            myli['objects'][0][str(pid)] = myli['objects'][0].get(str(pid), 0) - 1
    cart.product = myli
    cart.save()
    return redirect('cart')


    
def deletecart(request, pid):
    try:
        carts = Cart.objects.filter(user=request.user)
        for cart in carts:
            product_data = (cart.product).replace("'", '"')
            product_items = json.loads(product_data)['objects'][0]
            if str(pid) in product_items:
                del product_items[str(pid)]
                cart.product = json.dumps({'objects':[product_items]})
            else:
                cart.product = json.dumps({'objects':[{}]})
            cart.save()
            break
        return redirect('cart')
    except Cart.DoesNotExist:
        return redirect('cart')
    
    return redirect('cart')

# making cart
import json
def cart(request):
    try:
        # Fetch all carts for the logged-in user
        carts = Cart.objects.filter(user=request.user)
        
        products = []
        total_price = 0

        for cart in carts:
            # Parse the cart's product data
            product_data = (cart.product).replace("'", '"')
            product_items = json.loads(product_data)['objects'][0]

            # Retrieve product details from the database and calculate total price
            for product_id, quantity in product_items.items():
                product = Product.objects.get(id=product_id)
                total = product.price * quantity
                total_price += total
                
                products.append({
                    'product': product,
                    'quantity': quantity,
                    'total': total
                })

        lengthpro = len(products)

    except Cart.DoesNotExist:
        products = []
        total_price = 0
        lengthpro = 0
        

    return render(request, 'cart.html', {
        'products': products,
        'total_price': total_price,
        'lengthpro': lengthpro,
    })

# book the order of user by confirming the details of it 
def booking(request):
    user = UserData.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)
    total = 0
    productid = (cart.product).replace("'", '"')
    productid = json.loads(str(productid))
    try:
        productid = productid['objects'][0]
    except:
        messages.success(request, "Cart is empty, Please add product in cart.")
        return redirect('cart')
    for i,j in productid.items():
        product = Product.objects.get(id=i)
        total += int(j) * int(product.price)
    if request.method == "POST":
        book = Booking.objects.create(user=request.user, product=cart.product, total=total)
        cart.product = {'objects':[]}
        cart.save()
        messages.success(request, "Book Order Successfully")
        return redirect('about')
    return render(request, "booking.html", locals())

# user can view the order at myOrder page
def myOrder(request):
    order = Booking.objects.filter(user=request.user)
    return render(request, "my-order.html", locals())

# user track by progressbar
def user_order_track(request, pid):
    order = Booking.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    return render(request, "user-order-track.html", locals())

# cancel the order
def change_order_status(request, pid):
    order = Booking.objects.get(id=pid)
    status = request.GET.get('status')
    if status:
        order.status = status
        order.save()
        messages.success(request, "Order status changed.")
    return redirect('myorder')

# admin manages the orders
def manage_order(request):
    action = request.GET.get('action', 0)
    order = Booking.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Booking.objects.filter()
        order_status = 'All'
    return render(request, 'manage_order.html', locals()) 

def delete_order(request, pid):
    order = Booking.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('/manage-order/?action='+request.GET.get('action'))

# view the users
def manage_user(request):
    user = UserData.objects.all()
    return render(request, 'manage_user.html', locals())

def delete_user(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('manage_user') 

# ------------------------------------------- queries ----------------------------

from django.shortcuts import render
from collections import Counter
from .models import Booking, Product
import ast

# 3. product name and no of orders by excluding the products with fewer than 5 orders
def query3(request):
    # Fetch all booking records
    bookings = Booking.objects.all()

    # Create a counter to count occurrences of each product
    product_counter = Counter()

    # Iterate over each booking and count products by their IDs
    for booking in bookings:
        try:
            # Print the raw product field for debugging
            print(f"Raw booking product data (ID {booking.id}): {booking.product}")

            # Parse the product field safely
            product_data = ast.literal_eval(booking.product)

            # Print parsed product data for debugging
            print(f"Parsed booking product data (ID {booking.id}): {product_data}")

            # Ensure 'objects' key exists and is a list
            product_objects = product_data.get('objects', [])
            if isinstance(product_objects, list):
                for product_object in product_objects:
                    # Extract product ID (keys of the dictionary are product IDs)
                    for product_id, quantity in product_object.items():
                        try:
                            product_id = int(product_id)  # Convert to integer if necessary
                            print(f"Found product ID: {product_id}")
                            product_counter.update([product_id])
                        except ValueError:
                            print(f"Error: Invalid product ID format in booking {booking.id}")
            else:
                print(f"Error: Expected a list of products, but got {type(product_objects)} in booking {booking.id}")
        except Exception as e:
            print(f"Error processing booking {booking.id}: {e}")

    # Filter out products with fewer than 5 orders
    filtered_products = {product_id: count for product_id, count in product_counter.items() if count >= 5}

    # Debugging filtered products
    print(f"Filtered products with 5 or more orders: {filtered_products}")

    # Retrieve product objects based on IDs
    products_with_orders = []
    for product_id, count in filtered_products.items():
        try:
            # Retrieve product object by ID
            product = Product.objects.get(id=product_id)
            products_with_orders.append((product, count))
        except Product.DoesNotExist:
            print(f"Product with ID '{product_id}' not found in database.")
        except Exception as e:
            print(f"Error retrieving product with ID '{product_id}': {e}")

    # Print the final products_with_orders list
    print(f"Final products with orders: {products_with_orders}")

    # Pass the data to the template
    context = {
        'product_orders': products_with_orders,
    }

    return render(request, 'query3.html', context)

# ---> 1. user wise - product - wise ordering quantity with total item value
# 2 tables : 1. where total order products and total quantity is display
# and second table where it shows which products are have which quantity in detail
from django.shortcuts import render
from .models import Booking, Product
import json
def query_1(request):
    bookings = Booking.objects.all()
    user_product_data = {}
    user_summary_data = {}

    for booking in bookings:
        user = booking.user.first_name
        product_data_str = booking.product

        # Replace single quotes with double quotes to make it valid JSON
        product_data_str = product_data_str.replace("'", '"')

        # Print the updated string for debugging
        print(f"Corrected product data string: {product_data_str}")

        try:
            # Convert to JSON format and extract the objects list
            products = json.loads(product_data_str).get('objects', [])
            print(f"Parsed products: {products}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            continue

        # Initialize user_product_data and user_summary_data if not present
        if user not in user_summary_data:
            user_summary_data[user] = {'total_products': 0, 'total_quantity': 0, 'total_value': 0}

        if user not in user_product_data:
            user_product_data[user] = {}

        # Use a set to accumulate distinct products for this user
        if 'distinct_products' not in user_summary_data[user]:
            user_summary_data[user]['distinct_products'] = set()

        # Process each product in the booking
        for product_data in products:
            for product_id, quantity in product_data.items():
                try:
                    product = Product.objects.get(id=int(product_id))
                    print(f"Found product: {product.name}, quantity: {quantity}")
                except Product.DoesNotExist:
                    print(f"Product with ID {product_id} does not exist.")
                    continue

                # Update user_product_data for individual products
                if product.name not in user_product_data[user]:
                    user_product_data[user][product.name] = {'quantity': 0, 'total_value': 0}

                # Update the quantity and total value for each product
                user_product_data[user][product.name]['quantity'] += quantity
                user_product_data[user][product.name]['total_value'] += quantity * product.price

                # Update total quantity and total value in summary
                user_summary_data[user]['total_quantity'] += quantity
                user_summary_data[user]['total_value'] += quantity * product.price

                # Add the product to the distinct_products set
                user_summary_data[user]['distinct_products'].add(product_id)

        # Update total_products after processing all bookings for the user
        user_summary_data[user]['total_products'] = len(user_summary_data[user]['distinct_products'])

    # Remove the distinct_products set from the summary data before rendering
    for user in user_summary_data:
        del user_summary_data[user]['distinct_products']

    print("Final user_product_data:", user_product_data)
    print("Final user_summary_data:", user_summary_data)

    context = {
        'user_product_data': user_product_data,
        'user_summary_data': user_summary_data
    }
    return render(request, 'query_1.html', context)

# ----------> query 2 . weekly order of first quater
from django.shortcuts import render
from datetime import datetime, timedelta
from collections import defaultdict

# Set date range for the first quarter of 2024
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 3, 31, 23, 59, 59)

# Weekly Orders Query without Postgres
def query2(request):
    # Filter bookings within Q1 of 2024
    bookings = Booking.objects.filter(created__range=[start_date, end_date])
    
    # Generate all weeks of Q1 2024
    all_weeks = defaultdict(int)  # Default dict with all weeks of Q1
    
    # Loop through Q1 weeks and initialize with 0 orders
    current_date = start_date
    while current_date <= end_date:
        week_number = int(current_date.strftime('%U'))+1  # Get week number
        all_weeks[week_number] = 0  # Initialize with 0 orders
        current_date += timedelta(days=7)  # Move to next week
    
    # Count the number of orders per week
    for booking in bookings:
        week_number = int(booking.created.strftime('%U'))  + 1 # Get week number of the booking
        all_weeks[week_number] +=1
          # Increment order count for that week
    
    # Convert the dictionary to a sorted list for display
    weekly_orders = sorted(all_weeks.items())
    
    context = {
        'weekly_orders': weekly_orders
    }
    
    return render(request, 'query2.html', context)

# 4 products sold more than 7 times or have not sold yet 

from django.shortcuts import render
from .models import Booking, Product
import ast  # For parsing the Python-like string format
from collections import defaultdict
from datetime import datetime

def orders_summary(request):
    # Initialize a dictionary to store product details
    product_data = defaultdict(lambda: {'total_orders': 0, 'total_quantity': 0})

    # Define the date range (January 1 to August 31)
    start_date = datetime(2024, 1, 1)
    # as it takes system data which is current date. so it cant have date of january month. we can customize it later
    end_date = datetime(2024, 8, 31, 23, 59, 59)

    # Fetch bookings that were created within the defined date range
    bookings = Booking.objects.filter(created__range=(start_date, end_date))

    for booking in bookings:
        print(f"Processing Booking ID: {booking.id}, Product Data: {booking.product}")
        
        try:
            # Parse the product field as a Python dictionary
            product_list = ast.literal_eval(booking.product)
            print(f"Parsed product list: {product_list}")

            # Assuming product_list is a dictionary with a key 'objects' containing a list of products
            for product_obj in product_list.get('objects', []):
                # Here the key is the product ID, and the value is the quantity
                for product_id_str, quantity in product_obj.items():
                    product_id = int(product_id_str)  # Convert to int
                    product_quantity = int(quantity)  # Extract quantity

                    try:
                        # Fetch the product name from the Product model
                        product = Product.objects.get(id=product_id)
                        product_name = product.name  # Get the product's name

                        print(f"Product ID: {product_id}, Name: {product_name}, Quantity: {product_quantity}")

                        # Update the total orders and quantity for each product
                        product_data[product_name]['total_orders'] += 1
                        product_data[product_name]['total_quantity'] += product_quantity

                    except Product.DoesNotExist:
                        print(f"Product with ID {product_id} does not exist.")
                        continue

        except (SyntaxError, ValueError) as e:
            # Log the error for debugging
            print(f"Error processing booking ID {booking.id}: {e}")
            continue

    # Fetch all products to ensure that every product is included in the final data
    all_products = Product.objects.all()
    for product in all_products:
        if product.name not in product_data:
            # Add product to the dictionary with zero orders and quantity if not already present
            product_data[product.name] = {'total_orders': 0, 'total_quantity': 0}

    # Filter products where total orders = 0 and total quantity > 7
    filtered_product_data = {
        name: details for name, details in product_data.items()
        if details['total_orders'] == 0 or details['total_quantity'] > 7
    }

    # Print the final filtered data for verification
    print(f"Final filtered product data: {filtered_product_data}")

    # Prepare context data for the template
    context = {
        'product_data': filtered_product_data,  # Pass the filtered products to the template
    }
    
    return render(request, 'orders_summary.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_datetime
from .models import Booking

# beacuse it default takes current date but we require Date of Jan month 
# thus we manually edit the date from current date 26-8-2024 to 26-1-2024
def update_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.method == 'POST':
        created_str = request.POST.get('created')
        updated_str = request.POST.get('updated')

        if created_str:
            created_date = parse_datetime(created_str)
            if created_date:
                booking.created = created_date
        if updated_str:
            updated_date = parse_datetime(updated_str)
            if updated_date:
                booking.updated = updated_date
        
        booking.save()
        return redirect('about')  # Redirect to a list view or any other page

    context = {
        'booking': booking,
    }
    return render(request, 'update_booking.html', context)