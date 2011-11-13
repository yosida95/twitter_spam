#-*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template
import consumer
import tweepy
import time
import models
import fcntl
import re


auth = tweepy.OAuthHandler(consumer.KEY, consumer.SECRET)


def index(request):
    fp = open('/var/www/live.ysd95.be/htdocs/root/count.log', 'r')
    fcntl.flock(fp.fileno(), fcntl.LOCK_SH)
    count = int(fp.read())
    fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
    fp.close()

    return direct_to_template(request, 'index.html', extra_context={
        'is_signedup': True if 'access_token' in request.session else False,
        'click_count': count,
    })


def signin(request):
    auth_url = re.sub('authorize', 'authenticate',
        auth.get_authorization_url())
    request.session['request_token'] = (auth.request_token.key,
        auth.request_token.secret)
    return HttpResponseRedirect(auth_url)


def oauth(request):
    verifier = request.GET.get('oauth_verifier', '')

    token = request.session.get('request_token', '')
    auth.set_request_token(token[0], token[1])
    del request.session['request_token']

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        return direct_to_template(request, 'oauth_failure.html')
    else:
        request.session['access_token'] = (auth.access_token.key,
            auth.access_token.secret)
        return HttpResponseRedirect('/')


def post(request):
    if 'access_token' in request.session and request.method == 'POST':
        form = models.PostForm(request.POST)
        if form.is_valid():
            access_token = request.session.get('access_token', ['', ''])
            auth.set_access_token(access_token[0], access_token[1])

            fp = open('/var/www/live.ysd95.be/htdocs/root/count.log', 'r+')
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
            count = int(fp.read()) + 1
            fp.seek(0)
            fp.truncate()
            fp.write(str(count))
            fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
            fp.close()

            api = tweepy.API(auth_handler=auth)
            api.update_status("@red_kanchi 直ちに爆発せよ！！！ http://%s/?%.2f #reaju_bomb" % (
                request.get_host(), time.time()))
            return direct_to_template(request, 'posted.html', extra_context={
                'form': models.PostForm()})
    return HttpResponseRedirect('http://%s/' % request.get_host())


def signout(request):
    request.session.flush()
    return HttpResponseRedirect('/')
