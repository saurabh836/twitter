# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, ListView, UpdateView, RedirectView
from .socialnetwork.tw_search import Twi_Pos
from .socialnetwork.mytwython import lis_findin_dict as lfd
from .socialnetwork.fb_search import TwitterTweet
from .forms import UserForm, LoginForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



@method_decorator(login_required, name='dispatch')
class IndexView(View):
    template_name = 'smedia/index.html'
    tp = Twi_Pos()
    # lists = lfd(a, 'text')

    def get(self, request):
        a = self.tp.pos("#lalbaugcharaja")
        tt = TwitterTweet("#lalbaugcharaja")
        pst_cnt = tt.get_tweet_month()
        # pst_cnt = len(a)
        username = request.session.get('username')
        return render(request, self.template_name, {'username': username, 'pst_cnt': pst_cnt, 'lists': a})
        # else:
        #     return render(request, self.template_name, {'username': username})

    def post(self, request):
        # request.session['username'] = username
        # username = request.session.get('username')
        return render(request, self.template_name, {})


class LogoutView(RedirectView):
    url = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class LoginView(View):
    form_class = LoginForm
    template_name = 'smedia/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        print request.POST
        form = request.POST
        username = form['username']
        password = form['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            return HttpResponseRedirect('index')
            # return render(request, 'smedia/index.html', {"username": username})
        else:
            return HttpResponseRedirect("login")


class UserFormView(View):
    form_class = UserForm
    template_name = 'smedia/signup.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #  process for data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("index")
                else:
                    return HttpResponse("login")
            else:
                return HttpResponseRedirect("register")
        else:
            return HttpResponse(request, self.template_name, {'form': form})
