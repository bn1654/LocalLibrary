from django.shortcuts import render, redirect
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime
from .forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    

class LoanedBooksByAllListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10
    permission_required = "catalog.can_mark_returned"

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':

        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            return HttpResponseRedirect(reverse('all-borrowed') )
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'12.10.2016',}
    permission_required = "catalog.can_add_author"

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    permission_required = "catalog.can_update_author"

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = "catalog.can_delete_author"

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = "catalog.can_add_book"

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title','author','summary','ISBN', 'genre', 'language']
    permission_required = "catalog.can_update_book"

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = "catalog.can_delete_book"