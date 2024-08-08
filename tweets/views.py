import random

from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .forms import TweetForm
from .models import Tweet

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    # request.POST is a dict containing the info coming through the form. content of a tweet can be accessed via 
    # requst.POST.get('content')
    if form.is_valid():
        # save method creates a model object, but the commit argument being false force it not to save it to the db.
        obj = form.save(commit=False)
        # do other form related logic, now 'obj' is a Tweet model instance not been saved.
        obj.save()
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