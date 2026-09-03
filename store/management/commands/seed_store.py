import shutil
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Creates sample categories and products for Annapurna Foods'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Sweets',
                'slug': 'sweets',
                'description': 'Traditional Indian sweets made for every celebration.',
            },
            {
                'name': 'Namkeen',
                'slug': 'namkeen',
                'description': 'Crunchy, savoury snacks for every occasion.',
            },
            {
                'name': 'Masales',
                'slug': 'masales',
                'description': 'Freshly blended spices for authentic home cooking.',
            },
            {
                'name': 'Pickle',
                'slug': 'pickle',
                'description': 'Tangy Indian pickles prepared with traditional spices.',
            },
            {
                'name': 'Dry Fruits',
                'slug': 'dry-fruits',
                'description': 'Premium nuts and dry-fruit specialities.',
            },
            {
                'name': 'Festive Combos',
                'slug': 'festive-combos',
                'description': 'Thoughtful assortments for celebrations and gifting.',
            },
            {
                'name': 'Gift Hampers',
                'slug': 'gift-hampers',
                'description': 'Curated luxury hampers for festivals and celebrations.',
            },
        ]

        category_objects = {}

        for category_data in categories:
            category, created = Category.objects.update_or_create(
                slug=category_data['slug'],
                defaults=category_data,
            )
            category_objects[category.slug] = category

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Created category: {category.name}'
                ))

        products = [
            {
                'name': 'Kaju Katli',
                'slug': 'kaju-katli',
                'category': 'sweets',
                'description': 'Smooth cashew fudge with an elegant silver finish.',
                'price': '950.00',
                'discount_price': '875.00',
                'stock': 50,
                'rating': '5.00',
                'is_best_seller': True,
                'is_new': False,
                'is_featured': True,
                'image_file': 'kaju-katli.jpg',
            },
            {
                'name': 'Besan Laddu',
                'slug': 'besan-laddu',
                'category': 'sweets',
                'description': 'A rich, traditional laddu made with slow-roasted gram flour and pure ghee.',
                'price': '520.00',
                'discount_price': None,
                'stock': 45,
                'rating': '4.90',
                'is_best_seller': True,
                'is_new': False,
                'is_featured': True,
                'image_file': 'besan-laddu.jpg',
            },
            {
                'name': 'Motichoor Laddu',
                'slug': 'motichoor-laddu',
                'category': 'sweets',
                'description': 'Delicate saffron boondi pearls shaped into festive laddus.',
                'price': '580.00',
                'discount_price': '540.00',
                'stock': 40,
                'rating': '4.90',
                'is_best_seller': True,
                'is_new': False,
                'is_featured': False,
                'image_file': 'motichoor-laddu.jpg',
            },
            {
                'name': 'Mix Namkeen',
                'slug': 'mix-namkeen',
                'category': 'namkeen',
                'description': 'A crunchy blend of savoury sev, lentils, nuts and spices.',
                'price': '320.00',
                'discount_price': None,
                'stock': 65,
                'rating': '4.80',
                'is_best_seller': True,
                'is_new': False,
                'is_featured': True,
                'image_file': 'mix-namkeen.jpg',
            },
            {
                'name': 'Ratlami Sev',
                'slug': 'ratlami-sev',
                'category': 'namkeen',
                'description': 'Spicy, thin gram-flour sev with classic Ratlami flavours.',
                'price': '340.00',
                'discount_price': None,
                'stock': 55,
                'rating': '4.80',
                'is_best_seller': True,
                'is_new': False,
                'is_featured': False,
                'image_file': 'ratlami-sev.jpg',
            },
            {
                'name': 'Moong Dal',
                'slug': 'moong-dal',
                'category': 'namkeen',
                'description': 'Lightly salted and crisp fried moong dal snack.',
                'price': '280.00',
                'discount_price': None,
                'stock': 70,
                'rating': '4.70',
                'is_best_seller': False,
                'is_new': False,
                'is_featured': False,
                'image_file': 'moong-dal.jpg',
            },
            {
                'name': 'Mango Pickle',
                'slug': 'mango-pickle',
                'category': 'pickle',
                'description': 'Tangy raw mango pickle with aromatic Indian spices.',
                'price': '360.00',
                'discount_price': None,
                'stock': 38,
                'rating': '4.90',
                'is_best_seller': True,
                'is_new': False,
                'is_featured': True,
                'image_file': 'mango-pickle.jpg',
            },
            {
                'name': 'Garam Masala',
                'slug': 'garam-masala',
                'category': 'masales',
                'description': 'A fragrant, balanced spice blend for everyday Indian cooking.',
                'price': '250.00',
                'discount_price': None,
                'stock': 80,
                'rating': '4.80',
                'is_best_seller': False,
                'is_new': False,
                'is_featured': True,
                'image_file': 'garam-masala.jpg',
            },
            {
                'name': 'Annapurna Chaat Masala',
                'slug': 'annapurna-chaat-masala',
                'category': 'masales',
                'description': 'A zesty and tangy blend that brightens every snack.',
                'price': '230.00',
                'discount_price': None,
                'stock': 90,
                'rating': '4.90',
                'is_best_seller': False,
                'is_new': True,
                'is_featured': True,
                'image_file': 'chaat-masala.jpg',
            },
            {
                'name': 'Family Celebration Combo',
                'slug': 'family-celebration-combo',
                'category': 'festive-combos',
                'description': 'A complete festive feast with Kaju Katli, Besan Laddus, crispy Ratlami Sev, and savory Namkeen for the whole family.',
                'price': '1499.00',
                'discount_price': '1349.00',
                'stock': 40,
                'rating': '4.90',
                'is_best_seller': True,
                'is_new': False,
                'is_featured': True,
                'image_file': 'family-celebration-combo.jpg',
            },
            {
                'name': 'Premium Diwali Box',
                'slug': 'premium-diwali-box',
                'category': 'festive-combos',
                'description': 'A golden celebratory assortment created for festive gatherings, loaded with motichoor laddus, kaju katli, and dry fruits.',
                'price': '2499.00',
                'discount_price': '2249.00',
                'stock': 30,
                'rating': '5.00',
                'is_best_seller': True,
                'is_new': True,
                'is_featured': True,
                'image_file': 'premium-festive-box.jpg',
            },
            {
                'name': 'Royal Celebration Hamper',
                'slug': 'royal-celebration-hamper',
                'category': 'festive-combos',
                'description': 'An abundant selection of our finest Indian delicacies, sweets, savouries, and whole dry fruits in an ornate showcase.',
                'price': '3999.00',
                'discount_price': '3699.00',
                'stock': 15,
                'rating': '5.00',
                'is_best_seller': True,
                'is_new': False,
                'is_featured': True,
                'image_file': 'royal-grand-tier-hamper.jpg',
            },
            {
                'name': 'Premium Festive Box',
                'slug': 'premium-festive-box',
                'category': 'festive-combos',
                'description': 'An elegant assortment of sweets, namkeen and dry fruits for gifting.',
                'price': '2499.00',
                'discount_price': '2299.00',
                'stock': 25,
                'rating': '5.00',
                'is_best_seller': False,
                'is_new': True,
                'is_featured': True,
                'image_file': 'premium-festive-box.jpg',
            },
            {
                'name': 'California Almonds (Badam)',
                'slug': 'california-almonds',
                'category': 'dry-fruits',
                'description': 'Hand-picked, crunchy, naturally sweet California almonds packed with nutrition.',
                'price': '850.00',
                'discount_price': '799.00',
                'stock': 60,
                'rating': '4.90',
                'is_best_seller': True,
                'is_new': False,
                'is_featured': True,
                'image_file': 'california-almonds.jpg',
            },
            {
                'name': 'Royal Whole Cashews (Kaju)',
                'slug': 'royal-whole-cashews',
                'category': 'dry-fruits',
                'description': 'Jumbo king-size whole cashews, rich, buttery and roasted to perfection.',
                'price': '920.00',
                'discount_price': '860.00',
                'stock': 50,
                'rating': '5.00',
                'is_best_seller': True,
                'is_new': False,
                'is_featured': True,
                'image_file': 'royal-cashews.jpg',
            },
            {
                'name': 'Roasted Salted Pistachios (Pista)',
                'slug': 'roasted-salted-pistachios',
                'category': 'dry-fruits',
                'description': 'Naturally opened, lightly salted and roasted premium green pistachios.',
                'price': '1150.00',
                'discount_price': '1050.00',
                'stock': 40,
                'rating': '4.90',
                'is_best_seller': False,
                'is_new': True,
                'is_featured': True,
                'image_file': 'roasted-pistachios.jpg',
            },
            {
                'name': 'Golden Afghani Raisins (Kishmish)',
                'slug': 'golden-afghani-raisins',
                'category': 'dry-fruits',
                'description': 'Plump, seedless golden raisins with exquisite natural sweetness.',
                'price': '450.00',
                'discount_price': '399.00',
                'stock': 75,
                'rating': '4.80',
                'is_best_seller': False,
                'is_new': False,
                'is_featured': False,
                'image_file': 'golden-raisins.jpg',
            },
            {
                'name': 'Kashmiri Walnut Kernels (Akhrot)',
                'slug': 'kashmiri-walnut-kernels',
                'category': 'dry-fruits',
                'description': 'Crisp, brain-healthy halved walnut kernels sourced directly from Kashmir.',
                'price': '980.00',
                'discount_price': '890.00',
                'stock': 45,
                'rating': '4.90',
                'is_best_seller': False,
                'is_new': True,
                'is_featured': True,
                'image_file': 'kashmiri-walnuts.jpg',
            },
            {
                'name': 'Royal Heritage Gift Hamper',
                'slug': 'royal-heritage-gift-hamper',
                'category': 'gift-hampers',
                'description': 'Handcrafted velvet-lined keepsake chest filled with silver-leaf sweets, cashews, almonds, and pure saffron.',
                'price': '3499.00',
                'discount_price': '3199.00',
                'stock': 20,
                'rating': '5.00',
                'is_best_seller': True,
                'is_new': False,
                'is_featured': True,
                'image_file': 'royal-heritage-hamper.jpg',
            },
            {
                'name': 'Diwali Celebration Gift Box',
                'slug': 'diwali-celebration-gift-box',
                'category': 'gift-hampers',
                'description': 'Opulent red & gold festive box filled with fresh motichoor laddus, kaju katli, assorted dry fruits, and glowing diyas.',
                'price': '2199.00',
                'discount_price': '1999.00',
                'stock': 35,
                'rating': '4.90',
                'is_best_seller': True,
                'is_new': True,
                'is_featured': True,
                'image_file': 'diwali-celebration-hamper.jpg',
            },
            {
                'name': 'Grand Dry Fruit & Mithai Basket',
                'slug': 'grand-dry-fruit-mithai-basket',
                'category': 'gift-hampers',
                'description': 'Luxury wicker hamper basket overflowing with premium almonds, cashews, pistachios, and ornate sweet gift boxes.',
                'price': '2899.00',
                'discount_price': '2650.00',
                'stock': 25,
                'rating': '4.90',
                'is_best_seller': False,
                'is_new': False,
                'is_featured': True,
                'image_file': 'dryfruit-mithai-basket.jpg',
            },
            {
                'name': 'Royal Three-Tier Celebration Showcase',
                'slug': 'royal-three-tier-celebration-showcase',
                'category': 'gift-hampers',
                'description': 'Multi-tiered celebratory showcase featuring artisanal sweets, gourmet savouries, and glass jars of whole dry fruits.',
                'price': '4299.00',
                'discount_price': '3899.00',
                'stock': 15,
                'rating': '5.00',
                'is_best_seller': False,
                'is_new': True,
                'is_featured': True,
                'image_file': 'royal-grand-tier-hamper.jpg',
            },
        ]

        for product_data in products:
            category_slug = product_data.pop('category')
            image_file = product_data.pop('image_file', None)
            category = category_objects[category_slug]

            product, created = Product.objects.update_or_create(
                slug=product_data['slug'],
                defaults={
                    **product_data,
                    'category': category,
                },
            )

            # Attach the image if the file exists in media/products/
            if image_file:
                image_path = settings.MEDIA_ROOT / 'products' / image_file
                if image_path.exists():
                    product.image.name = f'products/{image_file}'
                    product.save(update_fields=['image'])

            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{action} product: {product.name}')

        self.stdout.write(self.style.SUCCESS(
            'Sample Annapurna Foods data is ready.'
        ))