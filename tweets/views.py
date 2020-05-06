from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Tweet
import random
from .forms import TweetForm
from django.utils.http import is_safe_url
from django.conf import settings

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)


def tweet_detail(request, tweet_id, *args, **kwargs):
    obj = get_object_or_404(Tweet, id=tweet_id)
    print('-------', obj)
    data = {
        'id': obj.id,
        'content': obj.content,
    }
    return JsonResponse(data)


def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [{'id': x.id, 'content': x.content, 'likes': random.randint(0, 10)} for x in qs]
    data = {
        'response': tweets_list

    }
    return JsonResponse(data)


def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = TweetForm()
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
    return render(request, 'components/form.html', context={'form': form})
