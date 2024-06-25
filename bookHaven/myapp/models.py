from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

def validate_published_year(value):
    current_year = timezone.now().year
    if value < 1000 or value > current_year:
        raise ValidationError(
            f'{value} is not a valid year. Year must be between 1000 and {current_year}.'
        )

class Book(models.Model):
    isbn = models.CharField(
        max_length=19,
        validators=[RegexValidator(
            regex=r'^\d{3}-\d{3}-\d{5}-\d{3}-\d{1}$',
            message='ISBN must be in the format XXX-XXX-XXXXX-XXX-X'
        )]
    )
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_year = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(timezone.now().year)],
    )
    genre = models.CharField(max_length=100)
