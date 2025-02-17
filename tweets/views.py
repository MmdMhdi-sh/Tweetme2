from django.conf import settings
from django.shortcuts import render


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def is_ajax(request):
    return (request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest') or (request.META.get('X-Requested-With') == 'XMLHttpRequest')


def home_view(request, *args, **kwargs):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, "pages/home.html", context={"username": username}, status=200)

def tweets_list_view(request, *args, **kwargs):
    return render(request, "tweets/list.html")

def tweets_detail_view(request, tweet_id, *args, **kwargs):
    return render(request, "tweets/detail.html", context={"tweet_id": tweet_id})

