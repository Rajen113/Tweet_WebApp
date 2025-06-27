from django.shortcuts import render 
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request ,'index.html')


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

@login_required
def tweet_create(request):
    print(request.method)
    if request.method == 'POST':
        print("Received POST request for tweet creation")
        print("Request data:", request.POST)
        form = TweetForm(request.POST, request.FILES)
        print("Form data:", form.data)
        # breakpoint()  # Removed for production use
        if form.is_valid():
            print("Form is valid, saving tweet")
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if tweet.user != request.user:
        messages.error(request, "You are not authorized to edit this tweet.")
        return redirect('tweet_list')
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

def tweet_detail(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    print(tweet)
    return render(request, 'tweet_detail.html', {'tweet': tweet})

def signup_view(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('tweet_list')
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

def login_view(request):
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('tweet_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})