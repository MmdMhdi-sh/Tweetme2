import random

from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..forms import TweetForm
from ..models import Tweet
from ..serializers import (
    TweetSerializer, 
    TweetActionSerializer,
    TweetCreateSerializer
    )

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def is_ajax(request):
    return (request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest') or (request.META.get('X-Requested-With') == 'XMLHttpRequest')

@api_view(['POST']) # only POST method 
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return JsonResponse({}, status=400)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    
    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet."}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet removed."}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are liking, unliking and retweeting
    '''
    serializer = TweetActionSerializer(data=request.data) # request.POST was empty. When using json data, use request.data
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    if action == 'like':
        obj.likes.add(request.user)
        serializer = TweetSerializer(obj)
        return Response(serializer.data, status=200)
    elif action == 'unlike':
        obj.likes.remove(request.user)
        serializer = TweetSerializer(obj)
        return Response(serializer.data, status=200)
    elif action == 'retweet':
        new_tweet = Tweet.objects.create(
            user=request.user, 
            parent=obj,
            content=content
            )
        serializer = TweetSerializer(new_tweet)
        # 201 because it actually creates a tweet
        return Response(serializer.data, status=201)
    return Response({}, status=200)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    username = request.GET.get("username")
    qs = Tweet.objects.all()
    if username != None:
        qs = qs.filter(user__username=username)
    serializer = TweetSerializer(qs, many=True)
    
    return Response(serializer.data)


def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if is_ajax(request):
            # status 401 is for not authorized
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    # request.POST is a dict containing the info coming through the form. Content of a tweet can be accessed via 
    # requst.POST.get('content')
    next_url = request.POST.get("next") or None
    print("next_url = ", next_url)
    if form.is_valid():
        # save method creates a model object, but the commit argument being false force it not to save it to the db.
        obj = form.save(commit=False)
        # do other form related logic, now 'obj' is a Tweet model instance not been saved. For example, adding the 
        # authenticated user to the obj.
        obj.user = user
        obj.save()
        if is_ajax(request):
            return JsonResponse(obj.serialize(), status=201) # 201 status is typically for created items 

        if next_url != None and url_has_allowed_host_and_scheme(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if is_ajax(request):
            return JsonResponse(form.errors, status=400)
    return render(request, "components/form.html", context={"form" : form})
        
        

def tweet_list_view_pure_django(request, *args, **kwargs):
    """
    REST API View
    Consume by JS
    Return json data
    """
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view_pure_django(request, tweet_id,*args, **kwargs):
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