from django.urls import path

from . import views

app_name = "quoteapp"

urlpatterns = [
    path("", views.main, name="main"),
    path("<int:page>", views.main, name="main"),
    path("author/<str:author>", views.get_info_author, name="get_info_author"),
    path("tag/<str:tag_name>/<int:page>", views.look_for_tag, name="look_for_tag"),
    path("tag/<str:tag_name>", views.look_for_tag, name="look_for_tag"),
    path("add_tag/", views.add_tag, name="add_tag"),
    path("add_author/", views.add_author, name="add_author"),
    path("add_quote/", views.add_quote, name="add_quote"),
    path("search_data/<str:data>", views.search_data, name="search_data"),
    path("search_data/<str:data>/<int:page>", views.search_data, name="search_data"),
]
