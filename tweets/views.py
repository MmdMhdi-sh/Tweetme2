import random

from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme


from .forms import TweetForm
from .models import Tweet

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    # request.POST is a dict containing the info coming through the form. content of a tweet can be accessed via 
    # requst.POST.get('content')
    next_url = request.POST.get("next") or None
    print("next_url = ", next_url)
    if form.is_valid():
        # save method creates a model object, but the commit argument being false force it not to save it to the db.
        obj = form.save(commit=False)
        # do other form related logic, now 'obj' is a Tweet model instance not been saved.
        obj.save()
        if next_url != None and url_has_allowed_host_and_scheme(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, "components/form.html", context={"form" : form})
        
        

def tweet_list_view(request, *args, **kwargs):
    """
    REST API View
    Consume by JS
    Return json data
    """
    qs = Tweet.objects.all()
    tweets_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 12312)} for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view(request, tweet_id,*args, **kwargs):
    """
    REST API View
    Consume by JS
    Return json data
    """
    data = {
        "id": tweet_id,
        # "image_path": obj.image.url
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
    except:
        data["message"] = "Not Found"
        status = 404
    return JsonResponse(data, status=status)