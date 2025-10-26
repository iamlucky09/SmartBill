from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer

from django.contrib.auth.models import User

class CustomerView(APIView):
    def get(self, request):
        # customers = Customer.objects.filter(user=request.user)
        customers = Customer.objects.all()
        data = [
            {
                "id": c.id,
                "name": c.name,
                "phone": c.phone,
                "email": c.email,
                "address": c.address,
            }
            for c in customers
        ]
        return Response(data)

    def post(self, request):
        data = request.data      
        customer = Customer.objects.create(
            # user=request.user,
            name=data.get("name"),
            phone=data.get("phone"),
            email=data.get("email"),
            address=data.get("address", "")
        )
        return Response(
            {"message": "Customer created successfully!", "id": customer.id},
            status=status.HTTP_201_CREATED
        )
    
