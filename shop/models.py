from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категориялар"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=200, verbose_name="Жарыянын аты")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Баасы (сом)")
    image = models.ImageField(upload_to='products/', blank=True, verbose_name="Товардын сүрөтү")
    description = models.TextField(verbose_name="Толук мүнөздөмөсү")

    # Сатуучунун маалыматтары
    seller_name = models.CharField(max_length=100, verbose_name="Сатуучунун аты", default="Колдонуучу")
    seller_phone = models.CharField(max_length=20, verbose_name="Сатуучунун телефону", default="")
    location = models.CharField(max_length=150, verbose_name="Дареги (Жайгашкан жери)", default="Бишкек")

    # Категорияга жараша ар кандай мүнөздөмөлөрдү сактоочу JSON талаасы
    dynamic_properties = models.JSONField(default=dict, blank=True, verbose_name="Категориялык мүнөздөмөлөр")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Кошулган убактысы")
    available = models.BooleanField(default=True, verbose_name="Активдүү жарыя")

    class Meta:
        verbose_name = "Жарыя (Товар)"
        verbose_name_plural = "Жарыялар (Товарлар)"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# 🚨 АДМИНКА ТАППАЙ ЖАТКАН ЖОГОЛГОН ORDER МОДЕЛИ УШУЛ ЖЕРГЕ КОШУЛДУ:
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Кайсы товар")
    customer_name = models.CharField(max_length=100, verbose_name="Кардардын аты")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон номери")
    customer_address = models.TextField(verbose_name="Жеткирүү дареги (Адрес)", default="")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Заказ түшкөн убакыт")
    status = models.BooleanField(default=False, verbose_name="Аткарылды ушул заказ")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказдар"

    def __str__(self):
        return f"{self.customer_name} - {self.product.name}"
