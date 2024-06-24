from django.db import models

# Create your models here.

from django.core.validators import RegexValidator

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
    published_year = models.IntegerField()
    genre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} by {self.author} (Genre: {self.genre}, Published: {self.published_year.year} ISBN: {self.isbn})"
    


