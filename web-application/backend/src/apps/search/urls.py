from django.urls import path, include
from . import views

urlpatterns = [
    path("files", views.search, name="search"),
    path('files/<str:id>', views.retrieve_file_details, name='file_detail'),
    path("files/<str:id>/upvote", views.upvote_handler, name="upvote"),
    path("files/<str:id>/downvote", views.downvote_handler, name="downvote"),
]
