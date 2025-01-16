from django.shortcuts import render
#from django.http import HttpResponse
from .models import Product, Order, CustomUser, OrderItem, Location, Invoice
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
import json
# Create your views here.

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        purchase_details = request.POST.getlist ('purchaseDetails')

        user = CustomUser.objects.get(username=username)
        # Create an order for the user
        #django handles fk relatioship itself, userid not needed, date ordered is to current time when create is called
        order = Order.objects.create(customer=user, total_price=0)


        # Process and save the purchase details here
        for index, detail_str in enumerate(purchase_details):
            # Now you have the purchase detail as a dictionary, you can access its individual properties
            detail_dict = json.loads(detail_str)
            #jason load converts json string to dictionary
            product_name = detail_dict['productName']
            quantity = detail_dict['quantity']
            price = detail_dict['price']
            total = detail_dict['total']

            # Retrieve the Product object corresponding to the product name
            product = Product.objects.get(name=product_name)

            # Determine if this is the last item
            is_last_item = index == len(purchase_details) - 1

            # Create an order item for the current product
            order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity, price=total, last_item=is_last_item)

            # Update the total price of the order
            order.total_price += order_item.price * order_item.quantity
            order.save()


        # Return a JSON response indicating success
        return JsonResponse({'message': 'Order successfully placed!', 'order_id': order.id})
    
    else:
        return render(request, 'home.html')
    
def about(request):
    return render(request, 'about.html')

def order(request):
    if request.method == 'POST': #default method ->GET
        # Retrieve data from the POST request
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        country = request.POST.get('country')
        city = request.POST.get('city')
        area = request.POST.get('area')
        street = request.POST.get('street')
        houseno = request.POST.get('houseNumber')

        # Create a CustomUser object with the form data
        
        user = CustomUser(
            first_name=firstname,
            last_name=lastname,
            email=email,
            street=street,
            city=city,
            state='',  # Add state if needed
            postal='',  # Add postal if needed
            country=country
        )
        user.save()
    
        prod = Product (
            name = firstname,
            description = country,
            price = 25.3
        )
        prod.save()

    
        # Save the CustomUser object to the database
        
    
        # For demonstration purposes, let's return the data back to the template
        return redirect('home')
    else:

        products = Product.objects.all().values('name', 'price').order_by('id')
        # Handle the case when the form is not submitted via POST
        return render(request, 'order.html', {'products': products})

def location(request):
    if request.method == 'POST':
        user_loc = request.POST.get('location').lower()
        

        if Location.objects.filter(name = user_loc).exists():
            loc = Location.objects.get (name = user_loc)
            return JsonResponse({'message': 'location found', 'loc_id': loc.id})
    
        else:
            return JsonResponse({'message': 'location not found', 'loc_id': -1})

    else:
        return render (request, 'location.html')
    

    #locations = Location.objects.values_list('name', flat=True)  # Extracting only the names
    #return render (request, 'location.html', {'locations': locations})

def userpage (request):

    if request.method == 'POST':
        # Retrieve form data from request.POST
        username = request.POST.get('username')
        password = request.POST.get('password')

    # Check if the username exists
        if not CustomUser.objects.filter(username=username).exists():
           # messages.info(request, 'Username does not exist.')
            return JsonResponse({'message': 'Username does not exist.'})
        
    # Check if the password is correct
        user = CustomUser.objects.get(username=username)
        if not check_password(password, user.password):
            return JsonResponse({'message': 'Wrong password entered.'})

        # Authentication successful
        messages.info(request, 'Logged in successfully.')
        return JsonResponse({'message': 'Logged in successfully.'})
    
    else:
        return render(request, 'user_page.html')

def signuppage (request):
    if request.method == 'POST':
        # Retrieve form data from request.POST
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        city = request.POST.get('city')
        area = request.POST.get('area')
        street = request.POST.get('street')
        house = request.POST.get('house')

        if CustomUser.objects.filter (email = email).exists():
            #messages.info(request, 'Email Already In Use')
            return JsonResponse({'message': 'Email already in use'})

        
        if CustomUser.objects.filter (username = username).exists():
            #messages.info(request, 'Username Already In Use')
            return JsonResponse({'message': 'Username already in use'})
        

        user = CustomUser.objects.create(username = username, first_name = firstname, last_name = lastname, 
                                        password= make_password(password), email = email, street = street, city= city,
                                        house = house, area = area, telephone=telephone)
        user.save()
        return JsonResponse({'message': 'Account created successfully!'})

    else:
        return render(request, 'signup_page.html')
    


def invoice(request):
    invoice_details = None
    order_id = request.GET.get('order_id')

    if order_id:
        invoice_details = Invoice.objects.filter(order_id=order_id)
        invoice_details_first = invoice_details.first()
        customer_data = {
                'first_name': invoice_details_first.first_name,
                'last_name': invoice_details_first.last_name,
                'house': invoice_details_first.house,
                'street': invoice_details_first.street,
                'area': invoice_details_first.area,
                'city': invoice_details_first.city,
                'date_ordered': invoice_details_first.date_ordered.date(),
            }
        # Calculate the total price
        total_price = sum(item.total_price for item in invoice_details)
    
    else:
        invoice_details = None
        customer_data = None
        total_price = 0

    return render(request, 'invoice.html', {'invoice_details': invoice_details, 'customer_data': customer_data, 'total_price': total_price})


    