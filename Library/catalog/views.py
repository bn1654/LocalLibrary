from django.shortcuts import render, redirect
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth import logout
import templates

def index(request):
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count() 
    return render(
    request,
    'catalog/index.html',
     context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
)
    
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorDetailView(generic.DetailView):
    model = Author

def logout_view(request):
    logout(request)
    return redirect('logged_out')

def logged_out_view(request):
    return render(request, './registration/logged_out.html')