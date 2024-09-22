from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



class Season(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]

    SOIL_DRAINAGE_CHOICES = [
        ('well_drained', 'Well-drained'),
        ('poorly_drained', 'Poorly-drained'),
        ('moist', 'Moist'),
    ]

    LIFESPAN_CHOICES = [
        ('annual', 'Annual'),
        ('biennial', 'Biennial'),
        ('perennial', 'Perennial'),
    ]

    TYPE_CHOICES = [
        ('seeds', 'Seeds'),
        ('bulbs', 'Bulbs'),
       
    ]

    LIGHT_EXPOSURE_CHOICES = [
        ('full_sun', 'Full Sun'),
        ('partial_shade', 'Partial Shade'),
        ('shade', 'Shade'),
    ]

    season = models.ForeignKey('Season', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    planting_start = models.IntegerField(choices=MONTH_CHOICES, 
                                        validators=[MinValueValidator(1), 
                                        MaxValueValidator(12)])
    planting_end = models.IntegerField(choices=MONTH_CHOICES, 
                                      validators=[MinValueValidator(1), 
                                      MaxValueValidator(12)])
    flowering_start = models.IntegerField(choices=MONTH_CHOICES, 
                                        validators=[MinValueValidator(1), 
                                        MaxValueValidator(12)])
    flowering_end = models.IntegerField(choices=MONTH_CHOICES, 
                                       validators=[MinValueValidator(1), 
                                       MaxValueValidator(12)])
    soil_drainage = models.CharField(max_length=50, choices=SOIL_DRAINAGE_CHOICES)
    lifespan = models.CharField(max_length=50, choices=LIFESPAN_CHOICES)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    light_exposure = models.CharField(max_length=50, choices=LIGHT_EXPOSURE_CHOICES)
    recommendation_1 = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='first_recommendation')
    recommendation_2 = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='second_recommendation')
    recommendation_3 = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='third_recommendation')

    def __str__(self):
        return self.name

    def get_planting_period(self):
        return f"{self.get_planting_start_display()} to {
            self.get_planting_end_display()}"

    def get_flowering_period(self):
        return f"{self.get_flowering_start_display()} to {
            self.get_flowering_end_display()}"

    