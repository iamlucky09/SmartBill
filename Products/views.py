# from django.shortcuts import render,redirect,get_object_or_404
# from django.http import HttpResponse,JsonResponse
# from .models import Product as pro
# from django.views.decorators.csrf import csrf_exempt
# # Create your views here.
# @csrf_exempt
# def Products(request):
#     if request.method == 'POST':
#         name=request.POST.get('name')
#         category=request.POST.get('category')
#         price=request.POST.get('price')
#         stock=request.POST.get('stock')
#         description=request.POST.get('description')

#         if not name or not category or not description or not price or not stock:
#             return HttpResponse("All fields are required.", status=400)
            
#         print("Title:", name)
#         pro.objects.create(
#             name=name,
#             category=category,
#             price=price,
#             stock=stock,
#             description=description,
#         )
#         return HttpResponse("Book added successfully ")
#     return HttpResponse("Send a request with book details.")

# # show page view
# @csrf_exempt
# def showpage(request):
#     # select * from tablename
#     # for fetching all the data from the table 
#     all = pro.objects.all()
#     data=list(all.values())
#     return JsonResponse(data,safe=False)

from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import Product
from django.views.decorators.csrf import csrf_exempt
import json
from .models import StockTransaction
from django.http import JsonResponse
from django.views import View # view can gives your class the ability to handle HTTP methods like GET, POST, PUT, DELETE, etc.

@csrf_exempt
def Products(request):  # Changed function name to capital P
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Required fields
        required_fields = ["name", "category", "price", "stock", "description"]
        if not all(field in data and data[field] for field in required_fields):
            return JsonResponse({"error": "All fields are required"}, status=400)

        # Create product
        product = Product.objects.create(
            name=data["name"],
            category=data["category"],
            price=data["price"],
            stock=data["stock"],
            description=data["description"],
        )
        return JsonResponse({"success": f"Product '{product.name}' added successfully."})
    
    elif request.method == 'GET':
        products = Product.objects.all()
        data = list(products.values())
        return JsonResponse(data, safe=False)

    return JsonResponse({"message": "Send a POST request with product details."})

@csrf_exempt
def ProductDetail(request, product_id):
    # Retrieve the product or return 404
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'PUT':
        # UPDATE
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Update fields if provided
        product.name = data.get("name", product.name)
        product.category = data.get("category", product.category)
        product.price = data.get("price", product.price)
        product.stock = data.get("stock", product.stock)
        product.description = data.get("description", product.description)
        product.save()

        return JsonResponse({"success": f"Product '{product.name}' updated successfully."})

    elif request.method == 'DELETE':
        # DELETE
        product.delete()
        return JsonResponse({"success": f"Product with id {product_id} deleted successfully."})

    elif request.method == 'GET':
        # GET SINGLE PRODUCT
        data = {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "stock": product.stock,
            "description": product.description,
        }
        return JsonResponse(data)
    
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator

# @method_decorator(csrf_exempt, name='dispatch')
# class StockTransactionView(View):
    
#     def get(self, request):
#         # Get filters from URL query parameters
#         product_id = request.GET.get('product')
#         transaction_type = request.GET.get('transaction_type')
#         ordering = request.GET.get('ordering', '-created_at')

#         # Start with all transactions
#         queryset = StockTransaction.objects.all()

#         # Apply filters if provided
#         if product_id:
#             queryset = queryset.filter(product_id=product_id)
#         if transaction_type:
#             queryset = queryset.filter(transaction_type=transaction_type)

#         # Apply ordering
#         queryset = queryset.order_by(ordering)

#         # Convert queryset to list of dicts
#         data = list(queryset.values(
#             'id',
#             'product__name',
#             'transaction_type',
#             'quantity',
#             'previous_stock',
#             'new_stock',
#             'notes',
#             'created_at'
#         ))

#         # Return JSON response
#         return JsonResponse(data, safe=False)
import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import StockTransaction, Product

@method_decorator(csrf_exempt, name='dispatch')
class StockTransactionView(View):

    def get(self, request):
        product_id = request.GET.get('product')
        transaction_type = request.GET.get('transaction_type')
        ordering = request.GET.get('ordering', '-created_at')

        queryset = StockTransaction.objects.all()
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        queryset = queryset.order_by(ordering)

        data = list(queryset.values(
            'id',
            'product__name',
            'transaction_type',
            'quantity',
            'previous_stock',
            'new_stock',
            'notes',
            'created_at'
        ))

        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)

            # Validate required fields
            required_fields = ['product_id', 'transaction_type', 'quantity', 'previous_stock', 'new_stock']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': f'Missing field: {field}'}, status=400)

            # Get product instance
            try:
                product = Product.objects.get(id=data['product_id'])
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=404)

            # Create stock transaction
            transaction = StockTransaction.objects.create(
                product=product,
                transaction_type=data['transaction_type'],
                quantity=data['quantity'],
                previous_stock=data['previous_stock'],
                new_stock=data['new_stock'],
                notes=data.get('notes', '')
            )

            # Return the created transaction
            return JsonResponse({
                'id': transaction.id,
                'product': transaction.product.name,
                'transaction_type': transaction.transaction_type,
                'quantity': transaction.quantity,
                'previous_stock': transaction.previous_stock,
                'new_stock': transaction.new_stock,
                'notes': transaction.notes,
                'created_at': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
