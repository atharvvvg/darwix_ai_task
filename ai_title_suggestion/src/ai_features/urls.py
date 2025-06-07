from django.urls import path
from .views import SuggestTitlesView

urlpatterns = [
    path('suggest-titles/', SuggestTitlesView.as_view(), name='suggest-titles'),
] 