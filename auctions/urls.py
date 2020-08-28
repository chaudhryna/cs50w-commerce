from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("categories", views.categories, name="categories"),
    path("watchlist/<int:pk>", views.watchlist, name="watchlist"),
    path("<str:category>", views.listings_by_category, name="listings_by_category"),
    path("listing_detail/<str:title>", views.listing_detail, name="listing_detail"),
]
