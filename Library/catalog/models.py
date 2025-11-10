from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Введите жанр книг")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги")
    ISBN = models.CharField('ISBN', max_length=13, help_text='13 символьное <a href="https://www.isbn-international.org/content/what-isbn">ISBN число</a>')
    genre = models.ManyToManyField(Genre, help_text="Выберете жанр книги")
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


