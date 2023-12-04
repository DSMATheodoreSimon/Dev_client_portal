from django.urls import path
from .views import HomePageView, ArticleDetailView, afficher_formulaire, soumission_reussie, RegisterView

urlpatterns = [
    path('',HomePageView.as_view(), name='home'),
    path('article/<int:pk>/',ArticleDetailView.as_view(), name='detail_article'),
    path('formulaire/<int:pk>/', afficher_formulaire, name='afficher_formulaire'),
    path('soumission-reussie/<int:pk>/', soumission_reussie, name='soumission_reussie'),
    path('register/', RegisterView.as_view(), name='register'),
] 
