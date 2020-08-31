from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from .forms import ListingForm, CommentForm, BidForm

def index(request):
    context = {'listings': Listing.objects.filter(status="Active").order_by('-created')}
    return render(request, "auctions/index.html", context)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new_listing(request):
    if request.method == 'POST':

        form = ListingForm(request.POST, request.FILES)
        
        if form.is_valid():
             
            new_listing = form.save(commit=False)
            new_listing.listed_by = request.user

            new_listing.save()

            return redirect('index')
    else:
        form = ListingForm()

    return render(request, "auctions/new_listing.html", {'form' : form})

def categories(request):
    context = {'categories': Listing.objects.filter(status="Active").values('category').annotate(total=Count('category')).order_by('category')}
    return render(request, "auctions/categories.html", context)

def listings_by_category(request, category):
    request.session['category'] = category
    context = {'listings': Listing.objects.filter(category=category), 'title': category}
    return render(request, "auctions/listings_by_category.html", context)


def listing_detail(request, title):
    listing = Listing.objects.get(title=title)
    bid_form = BidForm()
    num_bids = Bid.objects.filter(listing=listing).count()
    highest_bidder = ""

    if num_bids > 0:
        highest_bidder = Bid.objects.filter(listing__title=title).order_by('bid_price').last().user 
    

    if request.method == "POST":

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.listing = listing
            new_comment.save()
            return redirect('listing_detail', title)
    else:
        comment_form = CommentForm()

    comments = Comment.objects.filter(listing=listing).order_by('-created')

    if listing.status == 'Closed' and request.user == listing.winner:
        messages.success(request, 'You won the auction!')

    context = {'listing': listing, 'comment_form' : comment_form, 'comments': comments, 'bid_form': bid_form, 'num_bids': num_bids, 'highest_bidder': highest_bidder}

    return render(request, "auctions/listing_detail.html", context)

def bid(request, title=None):

    if request.method == "POST":
        listing = Listing.objects.get(title=title)
        last_bid = Bid.objects.filter(listing=listing).last()

        bid_form = BidForm(request.POST)
            
        if bid_form.is_valid():
            new_bid = bid_form.save(commit=False)
            
            if (new_bid.bid_price < listing.price):
                messages.error(request, "You're bid is too low!")
                bid_form = BidForm()
            else:
                new_bid.user = request.user
                new_bid.listing = listing
                listing.price = new_bid.bid_price
                listing.bids.add(request.user)  
                listing.save()
                new_bid.save()
                highest_bidder = Bid.objects.last().user 
                messages.success(request, "Great bid!")
            return redirect("listing_detail", title)
        else:
            bid_form = BidForm()

    return redirect("listing_detail", title)

def watchlisted(request, title=None):
    user = request.user
    
    if request.method == "POST":
        listing_id = request.POST.get('listing_id')
        listing_obj = Listing.objects.get(id=listing_id)

        if user in listing_obj.watchlisted.all():
            listing_obj.watchlisted.remove(user)
            messages.success(request, 'The listing was removed from your list!')
        else:
            listing_obj.watchlisted.add(user)
            messages.success(request, 'The listing was added to your list!')

        watchlist, created = Watchlist.objects.get_or_create(user=user, listing_id=listing_id)

        if not created:
            if watchlist.value == 'Add':
                watchlist.value = 'Remove'
            else: 
                watchlist.value = 'Add'

        watchlist.save()

    return redirect("listing_detail", title)

def watchlist(request):
    user = request.user
    
    watchlist_items = Watchlist.objects.filter(user=user).exclude(value='Remove').order_by('listing__title')
    context = {'watchlist_items': watchlist_items}
    return render(request, "auctions/watchlist.html", context)

def closed(request, title=None):
    if request.method == "POST":
        listing_id = request.POST.get('listing_id')
        listing_obj = Listing.objects.get(id=listing_id)

        if listing_obj.status == 'Active':
            listing_obj.status = 'Closed'
            listing_obj.winner = Bid.objects.last().user
            messages.success(request, 'The listing is now closed!')

        listing_obj.save()

    return redirect("listing_detail", title)

def closed_listings(request):
    context = {'listings': Listing.objects.filter(status="Closed").order_by('-created')}
    return render(request, "auctions/closed_listings.html", context)

