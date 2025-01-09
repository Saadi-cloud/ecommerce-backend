from rest_framework.response import Response
from Products.models import Product, Cart, Checkout, CheckoutProduct
from .serializers import ProductSerializer, CartSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serialized_products = ProductSerializer(products, many=True)
    return Response(serialized_products.data)

@api_view(['POST'])
def add_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(["PUT"])
def updateProduct(request, pk):
    try:
        product_update = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=404)

    serializer = ProductSerializer(product_update, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
def deleteProduct(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=404)
    
    product.delete()
    return Response(status=204)


# functuonality of cart

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart
from Products.models import Product

@api_view(['POST'])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)  # Default quantity is 1

    # Check if the product exists
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    # Check if the product is already in the cart
    cart_item, created = Cart.objects.get_or_create(product=product)
    if not created:
        cart_item.quantity += int(quantity)  # Increment quantity if already exists
    else:
        cart_item.quantity = int(quantity)  # Set quantity for new entry

    cart_item.save()

    return Response({
        'message': 'Product added to cart!',
        'cart_item': {
            'id': cart_item.id,
            'product_name': cart_item.product.product_name,
            'price': cart_item.product.price,
            'quantity': cart_item.quantity,
        }
    })


@api_view(['GET'])
def get_cart_items(request):
    cart_items = Cart.objects.all()
    data = [
        {
            'id': item.id,
            'product_name': item.product.product_name,
            'price': item.product.price,
            'quantity': item.quantity,
            'total_price': item.quantity * item.product.price,
            'product_id': item.product.id,
        }
        for item in cart_items
    ]
    return Response(data)

       

@api_view(['PUT'])
def update_cart_item(request, cart_item_id):
    try:
        cart_item = Cart.objects.get(id=cart_item_id)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=404)

    quantity = request.data.get('quantity')
    if quantity:
        cart_item.quantity = int(quantity)
        cart_item.save()
        return Response({
            'message': 'Cart item updated!',
            'cart_item': {
                'id': cart_item.id,
                'product_name': cart_item.product.product_name,
                'price': cart_item.product.price,
                'quantity': cart_item.quantity,
            }
        })
    return Response({'error': 'Invalid data'}, status=400)



@api_view(['DELETE'])
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = Cart.objects.get(id=cart_item_id)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=404)

    cart_item.delete()
    return Response({'message': 'Product removed from cart!'})

@api_view(['POST'])
def checkout(request):
    # Customer details and payment type
    customer_name = request.data.get('customer_name')
    customer_address = request.data.get('customer_address')
    payment_type = request.data.get('payment_type')

    if not (customer_name and customer_address and payment_type):
        return Response({'error': 'All fields are required'}, status=400)

    # Get all cart items
    cart_items = Cart.objects.all()
    if not cart_items:
        return Response({'error': 'Cart is empty'}, status=400)

    # Calculate total price
    total_price = sum(item.quantity * item.product.price for item in cart_items)

    # Create a Checkout instance
    checkout_instance = Checkout.objects.create(
        customer_name=customer_name,
        customer_address=customer_address,
        payment_type=payment_type,
        total_price=total_price
    )

    # Add products to the Checkout instance and save in CheckoutProduct
    for item in cart_items:
        CheckoutProduct.objects.create(
            checkout=checkout_instance,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # Clear the cart
    cart_items.delete()

    return Response({
        'message': 'Checkout successful',
        'checkout_details': {
            'customer_name': checkout_instance.customer_name,
            'customer_address': checkout_instance.customer_address,
            'payment_type': checkout_instance.payment_type,
            'total_price': checkout_instance.total_price,
            'products': [
                {
                    'product_name': item.product.product_name,
                    'quantity': item.quantity,
                    'price': item.price
                } for item in checkout_instance.checkoutproduct_set.all()
            ],
            'created_at': checkout_instance.created_at
        }
    })





    