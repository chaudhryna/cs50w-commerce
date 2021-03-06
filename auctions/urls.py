from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("<str:category>", views.listings_by_category, name="listings_by_category"),
    path("listing_detail/<str:title>", views.listing_detail, name="listing_detail"),
    path("watchlisted/<str:title>", views.watchlisted, name="watchlisted"),
    path("closed/<str:title>", views.closed, name="closed"),
    path("bid/<str:title>", views.bid, name="bid"),
]
