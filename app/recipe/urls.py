"""
URLs mapping for the recipe api.
"""

from django.urls import include, path
from recipe import views
from rest_framework.routers import DefaultRouter

recipeRouter = DefaultRouter()
recipeRouter.register("", views.RecipeViewSet)

tagsRouter = DefaultRouter()
tagsRouter.register("", views.TagViewSet)

app_name = "recipe"

urlpatterns = [
    path("recipe/", include(recipeRouter.urls)),
    path("tags/", include(tagsRouter.urls)),
]
