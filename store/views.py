import uuid
from decimal import Decimal
from django.contrib import messages
from django.db import models, transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Order, OrderItem, Product


def home(request):
    categories = [
        {'name': 'Sweets', 'slug': 'sweets', 'image': '/media/categories/sweets.jpg', 'url': '/category/sweets/'},
        {'name': 'Namkeen', 'slug': 'namkeen', 'image': '/media/categories/namkeen.jpg', 'url': '/category/namkeen/'},
        {'name': 'Masales', 'slug': 'masales', 'image': '/media/categories/masales.jpg', 'url': '/category/masales/'},
        {'name': 'Pickle', 'slug': 'pickle', 'image': '/media/categories/pickle.jpg', 'url': '/category/pickle/'},
        {'name': 'New Launches', 'slug': 'new-launches', 'image': '/media/categories/new-launches.jpg', 'url': '/new-launches/'},
        {'name': 'Festive Combos', 'slug': 'festive-combos', 'image': '/media/categories/festive-combos.jpg', 'url': '/festive-combos/'},
        {'name': 'Dry Fruits', 'slug': 'dry-fruits', 'image': '/media/categories/dry-fruits.jpg', 'url': '/category/dry-fruits/'},
        {'name': 'Gift Hampers', 'slug': 'gift-hampers', 'image': '/media/categories/gift-hampers.jpg', 'url': '/category/gift-hampers/'},
    ]

    best_sellers = Product.objects.filter(is_best_seller=True).select_related('category')[:4]
    if not best_sellers.exists():
        best_sellers = Product.objects.all().select_related('category')[:4]

    festive_combos = Product.objects.filter(category__slug='festive-combos').exclude(slug='premium-festive-box')[:3]
    if not festive_combos.exists():
        festive_combos = Product.objects.filter(category__slug='festive-combos')[:3]

    return render(request, 'home.html', {
        'categories': categories,
        'best_sellers': best_sellers,
        'festive_combos': festive_combos,
    })


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def product_list(request, products=None, page_title='Our Products'):
    if products is None:
        products = Product.objects.select_related('category').all()

    sort = request.GET.get('sort')

    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')

    return render(request, 'products.html', {
        'products': products,
        'page_title': page_title,
        'selected_sort': sort or 'newest',
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category).select_related('category')

    sort = request.GET.get('sort')

    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')

    return render(request, 'category.html', {
        'category': category,
        'products': products,
        'selected_sort': sort or 'newest',
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category'),
        slug=slug
    )

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=product.pk)[:4]

    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products,
    })


def new_launches(request):
    products = Product.objects.filter(is_new=True).select_related('category')
    return product_list(request, products, 'New Launches')


def festive_combos(request):
    products = Product.objects.filter(
        category__slug='festive-combos'
    ).select_related('category')
    return product_list(request, products, 'Festive Combos')


def add_to_cart(request):
    if request.method != 'POST':
        return redirect('store:product_list')

    product = get_object_or_404(Product, id=request.POST.get('product_id'))
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('accept', '')

    try:
        quantity = max(1, int(request.POST.get('quantity', 1)))
    except (TypeError, ValueError):
        quantity = 1

    if product.stock == 0:
        if is_ajax:
            return JsonResponse({'success': False, 'error': f'{product.name} is currently out of stock.'}, status=400)
        messages.error(request, f'{product.name} is currently out of stock.')
        return redirect('store:product_detail', slug=product.slug)

    cart = request.session.get('cart', {})
    product_id = str(product.id)
    current_quantity = cart.get(product_id, 0)

    cart[product_id] = min(current_quantity + quantity, product.stock)
    request.session['cart'] = cart
    request.session.modified = True

    if is_ajax:
        total_items = sum(cart.values())
        return JsonResponse({
            'success': True,
            'product_name': product.name,
            'quantity': cart[product_id],
            'total_items': total_items,
            'message': f'{product.name} was added to your cart.'
        })

    messages.success(request, f'{product.name} was added to your cart.')
    return redirect('store:cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    product_ids = cart.keys()

    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    cart_total = Decimal('0.00')

    for product in products:
        quantity = cart.get(str(product.id), 0)
        item_total = product.current_price * quantity
        cart_total += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
    })


def cart_action(request):
    if request.method != 'POST':
        return redirect('store:cart_detail')

    product_id = str(request.POST.get('product_id'))
    action = request.POST.get('action')
    cart = request.session.get('cart', {})

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('accept', '')

    if product_id not in cart:
        if is_ajax:
            return JsonResponse({'success': False, 'error': 'Item not found in cart'}, status=404)
        return redirect('store:cart_detail')

    product = get_object_or_404(Product, id=product_id)

    if action == 'increase' and cart[product_id] < product.stock:
        cart[product_id] += 1

    elif action == 'decrease':
        cart[product_id] -= 1
        if cart[product_id] <= 0:
            del cart[product_id]

    elif action == 'remove':
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    if is_ajax:
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_total = Decimal('0.00')
        total_items = sum(cart.values())
        item_qty = cart.get(product_id, 0)
        item_total = (product.current_price * item_qty) if item_qty > 0 else Decimal('0.00')

        for p in products:
            qty = cart.get(str(p.id), 0)
            cart_total += p.current_price * qty

        return JsonResponse({
            'success': True,
            'action': action,
            'product_id': product_id,
            'quantity': item_qty,
            'item_total': f"{item_total}",
            'cart_total': f"{cart_total}",
            'total_items': total_items,
            'is_empty': len(cart) == 0,
        })

    return redirect('store:cart_detail')

def search_products(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).select_related('category')

    return render(request, 'search_results.html', {
        'products': products,
        'query': query,
    })


def calculate_cart_checkout_data(request):
    """
    Strict server-side calculation of all checkout financial values.
    Never trusts prices or totals from the frontend.
    """
    cart = request.session.get('cart', {})
    if not cart:
        return None

    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids).select_related('category')

    cart_items = []
    subtotal = Decimal('0.00')
    total_quantity = 0

    for product in products:
        qty = cart.get(str(product.id), 0)
        if qty <= 0:
            continue
        line_total = product.current_price * qty
        subtotal += line_total
        total_quantity += qty
        cart_items.append({
            'product': product,
            'quantity': qty,
            'unit_price': product.current_price,
            'line_total': line_total,
            'in_stock': product.stock >= qty,
            'available_stock': product.stock,
        })

    if not cart_items:
        return None

    # Coupon Handling from session
    coupon_code = request.session.get('applied_coupon', '').strip().upper()
    discount_amount = Decimal('0.00')
    coupon_message = ''

    if coupon_code:
        if coupon_code == 'ANNAPURNA10':
            discount_amount = (subtotal * Decimal('0.10')).quantize(Decimal('0.01'))
            coupon_message = '10% Festive Discount Applied!'
        elif coupon_code == 'FESTIVE500':
            if subtotal >= Decimal('1999.00'):
                discount_amount = Decimal('500.00')
                coupon_message = '₹500 Grand Festive Discount Applied!'
            else:
                coupon_message = 'FESTIVE500 requires a minimum order of ₹1,999'
                coupon_code = ''
                if 'applied_coupon' in request.session:
                    del request.session['applied_coupon']
                    request.session.modified = True
        elif coupon_code == 'WELCOME50':
            discount_amount = min(Decimal('50.00'), subtotal)
            coupon_message = '₹50 Welcome Gift Applied!'
        else:
            coupon_message = 'Invalid coupon code'
            coupon_code = ''
            if 'applied_coupon' in request.session:
                del request.session['applied_coupon']
                request.session.modified = True

    # Free shipping on orders >= ₹999, else ₹99
    if subtotal >= Decimal('999.00'):
        delivery_charge = Decimal('0.00')
    else:
        delivery_charge = Decimal('99.00')

    # Tax (5% GST on packaged food goods)
    taxable_amount = max(Decimal('0.00'), subtotal - discount_amount)
    tax_amount = (taxable_amount * Decimal('0.05')).quantize(Decimal('0.01'))

    total_amount = taxable_amount + delivery_charge + tax_amount

    return {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'coupon_code': coupon_code,
        'coupon_message': coupon_message,
        'delivery_charge': delivery_charge,
        'is_free_delivery': delivery_charge == Decimal('0.00'),
        'free_delivery_threshold': Decimal('999.00'),
        'tax_amount': tax_amount,
        'total_amount': total_amount,
    }


def apply_coupon(request):
    """
    AJAX / POST view to apply or remove coupon codes.
    """
    if request.method != 'POST':
        return redirect('store:checkout')

    code = request.POST.get('coupon_code', '').strip().upper()
    action = request.POST.get('action', 'apply')
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('accept', '')

    if action == 'remove':
        if 'applied_coupon' in request.session:
            del request.session['applied_coupon']
            request.session.modified = True
        messages.info(request, 'Coupon removed.')
        if is_ajax:
            checkout_data = calculate_cart_checkout_data(request)
            return JsonResponse({
                'success': True,
                'message': 'Coupon removed.',
                'subtotal': f"{checkout_data['subtotal']:.2f}",
                'discount_amount': f"{checkout_data['discount_amount']:.2f}",
                'delivery_charge': f"{checkout_data['delivery_charge']:.2f}",
                'tax_amount': f"{checkout_data['tax_amount']:.2f}",
                'total_amount': f"{checkout_data['total_amount']:.2f}",
                'coupon_code': '',
            })
        return redirect('store:checkout')

    valid_coupons = {
        'ANNAPURNA10': '10% Festive Discount Applied!',
        'FESTIVE500': '₹500 Grand Festive Discount Applied!',
        'WELCOME50': '₹50 Welcome Gift Applied!',
    }

    if code in valid_coupons:
        # Check minimum order for FESTIVE500
        cart = request.session.get('cart', {})
        product_ids = cart.keys()
        current_subtotal = Decimal('0.00')
        for p in Product.objects.filter(id__in=product_ids):
            current_subtotal += p.current_price * cart.get(str(p.id), 0)

        if code == 'FESTIVE500' and current_subtotal < Decimal('1999.00'):
            msg = 'FESTIVE500 requires a minimum cart subtotal of ₹1,999.'
            messages.error(request, msg)
            if is_ajax:
                return JsonResponse({'success': False, 'message': msg}, status=400)
            return redirect('store:checkout')

        request.session['applied_coupon'] = code
        request.session.modified = True
        msg = f'Coupon "{code}" applied successfully!'
        messages.success(request, msg)
        success = True
    else:
        msg = 'Invalid coupon code. Try ANNAPURNA10, FESTIVE500, or WELCOME50.'
        messages.error(request, msg)
        success = False

    if is_ajax:
        checkout_data = calculate_cart_checkout_data(request)
        if success and checkout_data:
            return JsonResponse({
                'success': True,
                'message': msg,
                'coupon_code': code,
                'subtotal': f"{checkout_data['subtotal']:.2f}",
                'discount_amount': f"{checkout_data['discount_amount']:.2f}",
                'delivery_charge': f"{checkout_data['delivery_charge']:.2f}",
                'tax_amount': f"{checkout_data['tax_amount']:.2f}",
                'total_amount': f"{checkout_data['total_amount']:.2f}",
            })
        return JsonResponse({'success': False, 'message': msg}, status=400)

    return redirect('store:checkout')


def checkout(request):
    """
    Render and process order placement.
    Includes address validation, stock verification, atomic creation, stock deduction, and cart clearing.
    """
    checkout_data = calculate_cart_checkout_data(request)

    if not checkout_data or not checkout_data['cart_items']:
        messages.warning(request, 'Your cart is empty. Please add products before proceeding to checkout.')
        return redirect('store:cart_detail')

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        payment_method = request.POST.get('payment_method', 'cod').strip()
        terms_accepted = request.POST.get('terms_accepted')

        errors = []
        if not full_name:
            errors.append('Please enter your full recipient name.')
        clean_phone = phone.replace(' ', '').replace('-', '').replace('+91', '')
        if not clean_phone or len(clean_phone) < 10 or not clean_phone.isdigit():
            errors.append('Please provide a valid 10-digit mobile number.')
        if not address:
            errors.append('Please enter your complete delivery street address.')
        if not city:
            errors.append('Please enter your city.')
        if not state:
            errors.append('Please select or enter your state.')
        clean_pincode = pincode.replace(' ', '')
        if not clean_pincode or len(clean_pincode) < 6 or not clean_pincode.isdigit():
            errors.append('Please provide a valid 6-digit postal pincode.')
        if payment_method not in ['upi', 'card', 'netbanking', 'cod']:
            errors.append('Please select a valid payment method.')
        if not terms_accepted:
            errors.append('You must accept the Terms & Conditions to place your order.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'checkout.html', {
                'checkout_data': checkout_data,
                'form_data': request.POST,
            })

        # 2. Stock Verification
        for item in checkout_data['cart_items']:
            product = item['product']
            fresh_product = Product.objects.get(id=product.id)
            if fresh_product.stock < item['quantity']:
                messages.error(request, f'Sorry, {fresh_product.name} has only {fresh_product.stock} units remaining in stock.')
                return redirect('store:cart_detail')

        # 3. Atomic Order Creation & Inventory Reduction
        with transaction.atomic():
            # Generate human-readable unique order ID
            uid = uuid.uuid4().hex[:8].upper()
            order_id = f"APF-{uid[:4]}-{uid[4:]}"

            order = Order.objects.create(
                order_id=order_id,
                user=request.user if request.user.is_authenticated else None,
                full_name=full_name,
                phone=clean_phone,
                email=email,
                address=address,
                city=city,
                state=state,
                pincode=clean_pincode,
                payment_method=payment_method,
                payment_status='completed' if payment_method != 'cod' else 'pending',
                order_status='confirmed',
                subtotal=checkout_data['subtotal'],
                discount_amount=checkout_data['discount_amount'],
                coupon_code=checkout_data['coupon_code'],
                delivery_charge=checkout_data['delivery_charge'],
                tax_amount=checkout_data['tax_amount'],
                total_amount=checkout_data['total_amount'],
            )

            # Create OrderItems and deduct stock
            for item in checkout_data['cart_items']:
                product = item['product']
                img_url = product.image.url if product.image else ''
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    product_image=img_url,
                    price=item['unit_price'],
                    quantity=item['quantity'],
                    item_total=item['line_total'],
                )
                Product.objects.filter(id=product.id).update(
                    stock=models.F('stock') - item['quantity']
                )

            # Clear session cart and coupon
            if 'cart' in request.session:
                del request.session['cart']
            if 'applied_coupon' in request.session:
                del request.session['applied_coupon']
            request.session.modified = True

            return redirect('store:order_success', order_id=order.order_id)

    form_data = {}
    if request.user.is_authenticated:
        form_data['full_name'] = request.user.get_full_name() or request.user.username
        form_data['email'] = request.user.email

    return render(request, 'checkout.html', {
        'checkout_data': checkout_data,
        'form_data': form_data,
    })


def order_success(request, order_id):
    """
    Display confirmed order receipt with full address, items, and total.
    """
    order = get_object_or_404(
        Order.objects.prefetch_related('items'),
        order_id=order_id
    )
    return render(request, 'order_success.html', {
        'order': order,
    })