from django.urls import include, path
from recipe.views import RecipeDetailView, RecipeView

app_name = "recipe"

urlpatterns = [
    path(
        "recipes/",
        include(
            [
                path("", RecipeView.as_view(), name="recipe-list"),
                path("<int:id>/", RecipeDetailView.as_view(), name="recipe-detail"),
            ]
        ),
    ),
]
