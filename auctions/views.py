from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from products.forms import ItemForm
from products.models import Item
from .models import Auction, Bet
from .forms import BetForm, AuctionCreateForm, AuctionUpdateForm

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.http import JsonResponse
from django.shortcuts import get_object_or_404


class AuctionDetailView(FormMixin, DetailView):
    model = Auction
    template_name = 'auctions/auction.html'
    context_object_name = 'auction'
    form_class = BetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bets = Bet.objects.filter(auction=self.object).order_by('-bet_amount')
        context['last_bets'] = bets[:5]
        context['min_bet'] = bets.first().bet_amount if bets is None else self.object.base_price
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Assuming you have a logged-in user
        user = self.request.user

        if user.is_anonymous:
            return redirect('access')

        # Get the current highest bet for the auction
        highest_bet = Bet.objects.filter(auction=self.object).order_by('-bet_amount').first()

        # Check if the entered bet amount is greater than the current highest bet
        bet_amount = form.cleaned_data['bet_amount']
        if highest_bet and bet_amount <= highest_bet.bet_amount or bet_amount < self.object.base_price:
            form.add_error('bet_amount', 'Your bet must be higher than the current highest bet.')
            return self.form_invalid(form)

        # Creating a new bet
        Bet.objects.create(user=user, auction=self.object, bet_amount=bet_amount)

        # You might want to add additional logic here, such as updating the auction's highest bet, etc.

        return HttpResponseRedirect(self.request.path)  # Redirect to the same page after successful bet

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class AuctionsListView(ListView):
    model = Auction
    template_name = 'auctions/auctions.html'


class UserAuctions(View):
    template_name = 'auctions/user_auctions.html'

    def get(self, request, *args, **kwargs):
        auctions = Auction.objects.filter(item__owner=request.user)
        return render(request, self.template_name, {'auctions': auctions})


class AuctionUpdateView(LoginRequiredMixin, View):
    template_name = 'auctions/user_auction.html'
    login_url = 'access'

    def get(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        form = AuctionUpdateForm(instance=auction, user=request.user)
        return render(request, self.template_name, {'form': form, 'auction': auction})

    def post(self, request, pk):
        auction = get_object_or_404(Auction, pk=pk)
        form = AuctionUpdateForm(request.POST, instance=auction, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-auctions')
        return render(request, self.template_name, {'form': form, 'auction': auction})


class AuctionCreateView(LoginRequiredMixin, View):
    template_name = 'auctions/user_auction.html'
    login_url = 'access'

    def get(self, request):
        form = AuctionCreateForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuctionCreateForm(request.POST,request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-auctions')
        return render(request, self.template_name, {'form': form})


def GetBetById(request, bet_id):
    bet = get_object_or_404(Bet, id=bet_id)
    data = {
        'id': bet.id,
        'user': {
            'id': bet.user.id,
            'username': bet.user.username,
            'photo': bet.user.photo.url if bet.user.photo else None,
        },
        'auction_id': bet.auction.id,
        'bet_amount': bet.bet_amount,
    }

    return JsonResponse(data)


def GetBetsByAuctionId(request, auction_id):
    bets = Bet.objects.filter(auction__id=auction_id)
    data = []

    for bet in bets:
        try:
            data.append({
                'id': bet.id,
                'user': {
                    'id': bet.user.id,
                    'username': bet.user.username,
                    'photo': bet.user.photo.url if bet.user.photo else None,
                } if bet.user else None,

                'bet_amount': bet.bet_amount,
            })
        except Exception as e:
            continue

    return JsonResponse(data, safe=False)
