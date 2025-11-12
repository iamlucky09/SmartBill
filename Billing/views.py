from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Invoice, InvoiceItem
import json

# Get all invoices
def invoice_list(request):
    invoices = list(Invoice.objects.values())
    return JsonResponse({'invoices': invoices}, safe=False)


#  Get single invoice detail
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    items = list(invoice.items.values())
    data = {
        'invoice': {
            'id': invoice.id,
            'invoice_number': invoice.invoice_number,
            'subtotal': float(invoice.subtotal),
            'discount': float(invoice.discount),
            'tax': float(invoice.tax),
            'total': float(invoice.total),
            'payment_method': invoice.payment_method,
            'created_at': invoice.created_at,
        },
        'items': items
    }
    return JsonResponse(data)


#  Create new invoice via POST request
@csrf_exempt  # (Only for testing in Postman)
@transaction.atomic
def create_invoice(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))

        payment_method = body.get('payment_method')
        discount = body.get('discount', 0)
        tax = body.get('tax', 0)
        notes = body.get('notes', '')

        invoice = Invoice.objects.create(
            user_id=body.get('user_id'),
            payment_method=payment_method,
            discount=discount,
            tax=tax,
            notes=notes
        )

        items = body.get('items', [])
        for item in items:
            InvoiceItem.objects.create(
                invoice=invoice,
                product=item['product'],
                quantity=item['quantity'],
                unit_price=item['unit_price']
            )

        # Update totals
        invoice.update_totals()
        invoice.save()

        return JsonResponse({'message': 'Invoice created successfully', 'invoice_id': invoice.id}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
