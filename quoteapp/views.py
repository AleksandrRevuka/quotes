from typing import List, Tuple

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse

from .forms import AuthorForm, QuoteForm, TagForm
from .models import Author, Quote, Tag


def main(request: HttpRequest, page: int = 1) -> TemplateResponse:
    """
    The main function is the main view for the quoteapp. It displays a list of quotes,
    and allows users to navigate through them using pagination. The top tags are also displayed.

    :param request: Pass the request object to the view
    :param page: Determine which page of the paginated list to display
    :return: A rendered template with the quotes and top tags
    """
    quotes = Quote.objects.all()
    page_object, top_tags = get_page_and_top_tags(quotes, page)
    return render(request, "quoteapp/index.html", {"quotes": page_object, "top_tags": top_tags})


def get_info_author(request: HttpRequest, author) -> TemplateResponse:
    """
    The get_info_author function takes a request and an author name as arguments.
    It then uses the Author model to get the author object with that fullname,
    and renders it in a template called 'quoteapp/author_detail.html'

    :param request: Get the request from the user
    :param author: Get the author object from the database
    :return: The author_detail
    """
    author = Author.objects.get(fullname=author)
    return render(request, "quoteapp/author_detail.html", {"author": author})


def look_for_tag(request: HttpRequest, tag_name: str, page: int = 1) -> TemplateResponse:
    """
    The look_for_tag function takes a request and tag_name as arguments.
    It then gets the Tag object with the name of tag_name, and uses it to filter
    the quotes that have that tag. It then calls get_page_and_top tags on those quotes,
    and returns a render call with the page object (a list of quotes) and top tags.

    :param request: Pass the request object to the view
    :param tag_name: Get the tag object from the database
    :param page: Determine which page of the quotes to display
    :return: A page with all quotes that have the tag_name
    """

    tag = Tag.objects.get(name=tag_name)
    quotes_with_tag = Quote.objects.filter(tags=tag)
    page_object, top_tags = get_page_and_top_tags(quotes_with_tag, page)
    return render(request, "quoteapp/look_for_tag.html", {"tag_name": tag_name, "quotes": page_object, "top_tags": top_tags})


def get_top_tags() -> List[Tag]:
    """
    The get_top_tags function returns the top 10 tags in the database.
    It does this by first querying for all tags, and then annotating each tag with a count of how many quotes it has.
    Then it orders those tags by their quote counts (descending), and slices off the first 10.

    :return: The top 10 tags, based on the number of quotes associated with each tag
    """
    top_tags = Tag.objects.alias(num_quotes=Count("quote")).order_by("-num_quotes")[:10]
    return top_tags


def get_page_and_top_tags(quotes: List[Quote], page: int) -> Tuple[Paginator, List[Tag]]:
    """
    The get_page_and_top_tags function takes a list of quotes and a page number,
    and returns the paginated quotes for that page as well as the top tags.


    :param quotes: Pass the quotes list to the paginator
    :param page: Get the current page of quotes
    :return: A tuple of two objects:
    """
    paginator = Paginator(quotes, per_page=10)
    page_object = paginator.get_page(page)
    top_tags = get_top_tags()
    return page_object, top_tags


def add_tag(request: HttpRequest) -> TemplateResponse:
    """
    The add_tag function is a view that handles the creation of new tags.
    It uses the TagForm to validate and save data from POST requests, and it
    renders an empty form for GET requests.

    :param request: Get the request object, which is used to determine if the method is post or get
    :return: A response object, which is the result of calling render()
    """
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag_name = form.cleaned_data['name']
            if not Tag.objects.filter(name=tag_name).exists():
                form.save()
            return redirect(to="quoteapp:main")
        else:
            return render(request, "quoteapp/add_tag.html", {"form": form})

    return render(request, "quoteapp/add_tag.html", {"form": TagForm()})


def add_author(request: HttpRequest) -> TemplateResponse:
    """
    The add_author function is a view that allows the user to add an author.
    It takes in a request object and returns either the form for adding an author, or
    the main page if the form was submitted successfully.

    :param request: Get the data from the form
    :return: A redirect to the main page
    """
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quoteapp:main")
        else:
            return render(request, "quoteapp/add_author.html", {"form": form})

    return render(request, "quoteapp/add_author.html", {"form": AuthorForm()})


def add_quote(request: HttpRequest) -> TemplateResponse:
    """
    The add_quote function is a view that allows the user to add a quote.
    The function first gets all of the tags from the database and passes them into
    the template. If there is POST data, it creates an instance of QuoteForm with
    that data and checks if it's valid. If so, it saves that form as new_quote, then
    gets all of the tags selected by using request.POST to get their primary keys (pks)
    and filters Tag objects for those pks in choice_tags; finally, we set new_quote's tags to be choice_tags.

    :param request: Get the request object from the view
    :return: A redirect to the main page
    """
    tags = Tag.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_tags = Tag.objects.filter(pk__in=request.POST.getlist("tags"))
            new_quote.tags.set(choice_tags)

            return redirect(to="quoteapp:main")
        else:
            return render(request, "quoteapp/add_quote.html", {"tags": tags, "form": form})

    return render(request, "quoteapp/add_quote.html", {"tags": tags, "form": QuoteForm()})


def search_data(request: HttpRequest, data: str, page: int = 1) -> TemplateResponse:
    """
    The search_data function takes in a request and data, which is the search query.
    It then searches for tags that start with the search query, and finds all quotes that have those tags.
    Then it searches for authors whose fullname contains the search query, and finds all quotes by those authors.
    Finally it combines these two sets of quotes into one set of unique quotes (no duplicates),
    and returns a TemplateResponse object containing this set of unique quotes.

    :param request: HttpRequest: Get the request object from the view
    :param data: str: Pass the search data from one page to another
    :param page: int: Determine which page of the paginator to display
    :return: A templateresponse object
    """

    if page == 1:
        if request.POST.get("search_input"):
            data = request.POST.get("search_input")

    tags = Tag.objects.filter(name__istartswith=data)
    quotes = Quote.objects.filter(tags__in=tags)

    authors = Author.objects.filter(fullname__iregex=data)
    quotes = quotes.union(Quote.objects.filter(author__in=authors))

    page_object, top_tags = get_page_and_top_tags(quotes, page)
    return render(request, "quoteapp/search.html", {"quotes": page_object, "top_tags": top_tags, "data": data})
