from django.contrib import admin
from .models import Category, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'current_price',
        'stock',
        'rating',
        'is_best_seller',
        'is_new',
        'is_featured',
    )
    list_filter = (
        'category',
        'is_best_seller',
        'is_new',
        'is_featured',
    )
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = (
        'stock',
        'is_best_seller',
        'is_new',
        'is_featured',
    )
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description', 'image')
        }),
        ('Pricing and Stock', {
            'fields': ('price', 'discount_price', 'stock', 'rating')
        }),
        ('Homepage Visibility', {
            'fields': ('is_best_seller', 'is_new', 'is_featured')
        }),
        ('System Information', {
            'fields': ('created_at',)
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity', 'item_total')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'full_name',
        'phone',
        'total_amount',
        'payment_method',
        'payment_status',
        'order_status',
        'created_at',
    )
    list_filter = (
        'order_status',
        'payment_method',
        'payment_status',
        'created_at',
    )
    search_fields = (
        'order_id',
        'full_name',
        'phone',
        'city',
        'pincode',
    )
    readonly_fields = (
        'order_id',
        'subtotal',
        'discount_amount',
        'coupon_code',
        'delivery_charge',
        'tax_amount',
        'total_amount',
        'created_at',
        'updated_at',
    )
    inlines = [OrderItemInline]
    ordering = ('-created_at',)