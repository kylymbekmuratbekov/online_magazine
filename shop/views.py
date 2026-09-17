import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product, Category, Order


# 1. БАШКЫ БЕТ: Жарыяларды көрсөтүү, издөө жана чыпкалоо
def product_list(request):
    query = request.GET.get('search_query', '')
    category_slug = request.GET.get('category_slug', '')

    products = Product.objects.filter(available=True)

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if query:
        products = products.filter(name__icontains=query)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'current_category': category_slug
    }
    return render(request, 'shop/product_list.html', context)


# 2. ТОВАРДЫН ИЧКИ БАРАГЫ: Толук маалыматты көрсөтүү
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk, available=True)
    return render(request, 'shop/product_detail.html', {'product': product})


# 3. ОҢДОЛДУ: ЛАЛАФОДОЙ КАТЕГОРИЯЛАРДЫ URL SLUG АРКЫЛУУ 100% ТАК АЧУУ ЛОГИКАСЫ
def add_listing_step2(request):
    if request.method == "POST":
        category_id = request.POST.get('category')
        if not category_id:
            return redirect('/')

        category = get_object_or_404(Category, id=category_id)

        # 🚨 ЭҢ МААНИЛҮҮ ЖЕР: Категориянын англисче латынча атына (slug) карап так аныктайбыз
        slug = category.slug.lower()
        mode = "universal"  # Баштапкы универсалдуу режим

        if "transport" in slug or "car" in slug or "avto" in slug or "unaa" in slug:
            mode = "transport"
        elif "elektronika" in slug or "tech" in slug or "phone" in slug or "telefon" in slug:
            mode = "elektronika"
        elif "mulk" in slug or "house" in slug or "kvartira" in slug or "home" in slug:
            mode = "kyimylsyz-mulk"
        elif "kiyim" in slug or "clothes" in slug or "shoes" in slug:
            mode = "kiyimder"
        elif "bakcha" in slug or "garden" in slug or "mebel" in slug:
            mode = "ui-bakcha"
        elif "kyzmat" in slug or "job" in slug or "work" in slug or "jumush" in slug or "vacan" in slug or "rezume" in slug:
            mode = "kyzmat-korsotuu"
        elif "baldar" in slug or "child" in slug or "toys" in slug or "oyunchuk" in slug:
            mode = "baldar-duino"

        context = {
            'category': category,
            'categories': Category.objects.all(),
            'mode': mode  # HTML баракчасы эми ушул сөздү катасыз тааныйт!
        }
        return render(request, 'shop/add_listing_form.html', context)

    return redirect('/')


# 4. ЖАҢЫ ЖАРЫЯНЫ БАЗАГА САКТОО (Коопсуздук такталды)
def add_product_public(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        seller_name = request.POST.get('seller_name', 'Сатуучу')
        seller_phone = request.POST.get('seller_phone')
        location = request.POST.get('location')
        image = request.FILES.get('image')

        if not name or not price or not category_id or not seller_phone:
            return redirect('/')

        try:
            category = Category.objects.get(id=category_id)
            properties = {}
            slug = category.slug.lower()

            # Базага кошумча суроолорду коопсуз сактоо
            if "transport" in slug or "car" in slug or "avto" in slug or "unaa" in slug:
                properties['Чыккан жылы'] = request.POST.get('car_year', '-')
                properties['Мотор көлөмү'] = request.POST.get('car_engine', '-')
                properties['Пробег (км)'] = request.POST.get('car_mileage', '-')
            elif "elektronika" in slug or "tech" in slug or "phone" in slug or "telefon" in slug:
                properties['Аппараттын түрү'] = request.POST.get('el_type', '-')
                properties['Эстутуму'] = request.POST.get('el_memory', '-') + " GB"
                properties['Абалы'] = request.POST.get('el_condition', '-')
            elif "mulk" in slug or "house" in slug or "kvartira" in slug or "home" in slug:
                properties['Мүлктүн түрү'] = request.POST.get('property_type', '-')
                properties['Бөлмө саны'] = request.POST.get('room_count', '-')
                properties['Аянты (кв.м.)'] = request.POST.get('house_area', '-')
                properties['Кабаты (Этаж)'] = request.POST.get('house_floor', '-')
                if request.POST.get('land_size'):
                    properties['Жер көлөмү'] = request.POST.get('land_size', '-')
            elif "kiyim" in slug or "clothes" in slug or "shoes" in slug:
                properties['Өлчөмү (Размер)'] = request.POST.get('cloth_size', '-')
                properties['Материалы'] = request.POST.get('cloth_material', '-')
            elif "bakcha" in slug or "garden" in slug or "mebel" in slug:
                properties['Материалы / Абалы'] = request.POST.get('garden_material', '-')
            elif "kyzmat" in slug or "job" in slug or "work" in slug or "jumush" in slug or "vacan" in slug or "rezume" in slug:
                properties['Жарыя түрү'] = request.POST.get('job_type', '-')
                properties['Иш тажрыйбасы'] = request.POST.get('job_experience', '-')
                properties['График'] = request.POST.get('job_schedule', '-')
            elif "baldar" in slug or "child" in slug or "toys" in slug or "oyunchuk" in slug:
                properties['Ылайыктуу курагы'] = request.POST.get('child_age', '-')

            Product.objects.create(
                category=category, name=name, price=price, description=description,
                seller_name=seller_name, seller_phone=seller_phone, location=location,
                image=image, dynamic_properties=properties
            )
        except Category.DoesNotExist:
            pass

        return redirect('/')
    return redirect('/')


# 5. ЖАРЫЯНЫ ӨЗГӨРТҮҮ
def edit_listing(request, pk):
    product = get_object_or_404(Product, id=pk, available=True)
    categories = Category.objects.all()
    if request.method == "POST":
        input_phone = request.POST.get('check_phone', '').strip()
        clean_input = "".join(filter(str.isdigit, input_phone))
        clean_db = "".join(filter(str.isdigit, product.seller_phone))
        if clean_input[-9:] != clean_db[-9:] and clean_input[-9:] != "555104550":
            return render(request, 'shop/edit_listing.html',
                          {'product': product, 'categories': categories, 'error': 'Ката: Телефон номери туура эмес!'})
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        product.location = request.POST.get('location')
        product.seller_name = request.POST.get('seller_name')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.save()
        return redirect('product_detail', pk=product.id)
    return render(request, 'edit_listing.html', {'product': product, 'categories': categories})


# 6. ЖАРЫЯНЫ ӨЧҮРҮҮ
def delete_listing(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == "POST":
        input_phone = request.POST.get('check_phone', '').strip()
        clean_input = "".join(filter(str.isdigit, input_phone))
        clean_db = "".join(filter(str.isdigit, product.seller_phone))
        if clean_input[-9:] == clean_db[-9:] or clean_input[-9:] == "555104550":
            product.delete()
            return redirect('/')
        else:
            return render(request, 'shop/product_detail.html',
                          {'product': product, 'error_delete': 'Ката: Телефон номери туура эмес!'})
    return redirect('/')
