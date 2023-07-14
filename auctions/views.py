import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Auction, Bid, Category, Watchlist, Comment
from .forms import AuctionForm
from django.contrib import messages
from django.db.models import Max

# Create your views here.


def home(request):
    featured_items = Auction.objects.all()
    count = 6
    if featured_items.count() < 6:
        count = featured_items.count()
    featured_items = random.sample(list(featured_items), count)
    context = {"featured_items": featured_items}
    return render(request, "Home.html", context)


def auctions(request, ):
    auctions = Auction.objects.all()
    context = {'auctions': auctions}
    return render(request, 'auctions/auctions.html', context)


def auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    bids = auction.bids.all()
    highest_bid = bids.order_by('-amount').first()
    num_bids = bids.count()

    if request.method == 'POST':
        if 'bid_amount' in request.POST:
            bid_amount = float(request.POST['bid_amount'])
            if bid_amount >= auction.starting_bid and (highest_bid is None or bid_amount > highest_bid.amount):
                auction.current_bid = bid_amount
                auction.save()
                bid = Bid(auction=auction, bidder=request.user, amount=bid_amount)
                bid.save()
            else:
                messages.error(request, "Your bid amount must be greater than the current highest bid.")
        elif 'comment' in request.POST:
            comment_content = request.POST['comment']
            comment = Comment(auction=auction, user=request.user, text=comment_content)
            comment.save()
        return redirect('auction_detail', pk=pk)

    comments = Comment.objects.filter(auction=auction)
    context = {
        'auction': auction,
        'comments': comments,
        'num_bids': num_bids,
        'highest_bid': highest_bid.amount if highest_bid else None,
        'current_bid': auction.current_bid,
    }
    return render(request, 'auctions/single-auction.html', context)

@login_required(login_url="login")
def createAuction(request):

    form = AuctionForm()

    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('auctions')

    context = {'form': form}
    return render(request, "auctions/auction_form.html", context)


@login_required(login_url="login")
def category_list(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})

@login_required(login_url="login")
def category_auctions(request, slug):
    category = get_object_or_404(Category, slug=slug)
    active_auctions = category.auction_set.filter(is_active=True)
    return render(request, "auctions/category_auctions.html", {"category": category, "active_auctions": active_auctions})

@login_required(login_url="login")
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    context = {'watchlist_items': watchlist_items}
    return render(request, 'auctions/watchlist.html', context)

@login_required(login_url="login")
def add_to_watchlist(request, pk):
    watchlist_item = Watchlist(user=request.user, pk=id)
    watchlist_item.save()
    return redirect('watchlist')


@login_required(login_url="login")
def remove_from_watchlist(request, pk):
    watchlist_item = Watchlist.objects.get(user=request.user, pk=id)
    watchlist_item.delete()
    return redirect('watchlist')


