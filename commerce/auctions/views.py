from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required



def index(request):
    listings = Listing.objects.filter(closed=False)
    return render(request, "auctions/index.html", {
        "listings" : listings ,
    })



def close_auction(request, listing_id):
    listing  = Listing.objects.get(pk=listing_id)    
    listing.closed = True
    listing.save()
    return HttpResponseRedirect(reverse("display_listing", args=(listing_id,)))



def closed_listings(request):
    listings = Listing.objects.filter(closed=True)
    return render(request, "auctions/closed_listing.html", {
        "listings" : listings ,
    })



def create_listing(request):
    if request.method == "POST":
        user = request.user
        title  = request.POST["title"]
        describtion = request.POST["describtion"]
        image_url = request.POST["image_url"]
        category  = request.POST["category"]

        price = Bid(price=int(request.POST["price"]), user=user)
        price.save()

        listing = Listing(title=title, describtion=describtion, owner=user, price=price, image_url=image_url, category=category)
        listing.save()

        
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html")    



def display_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    owner = request.user.username == listing.owner.username
    comments = listing.comments.all()
    listing_in_watchlist = request.user in listing.watchlist.all()
    return render(request, "auctions/display_listing.html", {
        "listing" : listing ,
        "owner" : owner ,
        "comments" : comments ,
        "listing_in_watchlist" : listing_in_watchlist ,
    })



def add_watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.add(user)

    return HttpResponseRedirect(reverse("display_listing", args=(listing_id,)))



def remove_watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.remove(user)

    return HttpResponseRedirect(reverse("display_listing", args=(listing_id,)))



def display_watchlist(request):
    user = request.user
    listings = user.watchlistings.all()
    return render(request, "auctions/watchlist.html", {
        "listings" : listings ,
    })



def new_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    current_price = listing.price.price
    new_price = price = int(request.POST["price"])

    if new_price > current_price:
        updated_bid = Bid(price=new_price, user=request.user)
        updated_bid.save()

        listing.price = updated_bid
        listing.save()

        return render(request, "auctions/display_listing.html", {
            "listing" : listing ,
            "message" : "Bid Was updated Successfully!" ,
            "updated" : True ,
        })
    else:
        return render(request, "auctions/display_listing.html", {
            "listing" : listing ,
            "message" : "Bid Not High Enough!" ,
            "updated" : False ,
        })



def comments(request, listing_id):
    writer = request.user
    comment = request.POST["comment"]
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment(comment=comment, writer=writer, listing=listing)
    comments.save()

    return HttpResponseRedirect(reverse("display_listing", args=(listing_id,)))


def category(request):
    category = request.POST["category"]
    listing = Listing.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "listing" : listing ,
    })


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
