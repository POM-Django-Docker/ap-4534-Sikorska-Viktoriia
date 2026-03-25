from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.db.models import Q
from .forms import BookForm
from authentication.decorators import role_required
from .models import Book
from author.models import Author
from django.shortcuts import render, redirect, get_object_or_404


@role_required(0, 1)
def book_list(request):
    name = request.GET.get("name", "").strip()
    author = request.GET.get("author", "").strip()

    books = Book.get_all()

    if name:
        books = books.filter(name__icontains=name)

    if author:
        books = books.filter(
            Q(authors__name__icontains=author) |
            Q(authors__surname__icontains=author) |
            Q(authors__patronymic__icontains=author)
        )

    authors = Author.objects.all().order_by("surname", "name")

    return render(request, "book/book_list.html", {
        "books": books.distinct().order_by("id"),
        "authors": authors,
        "name": name,
        "author_id": author,
    })

@role_required(0, 1)
def book_detail(request, pk):
    book = Book.get_by_id(pk)

    if book is None:
        raise Http404

    return render(request, "book/book_detail.html", {
        "book": book,
    })

@role_required(1)
def book_admin_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save() # Це автоматично створить об'єкт і збереже зв'язки ManyToMany (авторів)
            return redirect("book_list")
    else:
        form = BookForm()
    
    return render(request, "book/book_admin_create.html", {"form": form})

@role_required(1)
def book_admin_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book) # Наповнює форму існуючими даними книги

    return render(request, "book/book_admin_update.html", {"form": form, "book": book})

@role_required(1)
@require_http_methods(["POST"])
def book_admin_delete(request, pk):
    Book.delete_by_id(pk)
    return redirect("book_list")