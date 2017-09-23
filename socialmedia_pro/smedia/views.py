# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, ListView, UpdateView, RedirectView
from .socialnetwork.tw_search import Twi_Pos
from .socialnetwork.mytwython import lis_findin_dict as lfd
from .socialnetwork.tw_crawler import TwitterTweet
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
        # a = self.tp.pos("#lalbaugcharaja")
        # pst_cnt = len(a)
        # username = request.session.get('username')
        return render(request, self.template_name, {})

    def post(self, request):
        key_w = request.POST.get('search_key')
        print "search Key = " + key_w
        tw_output = self.tp.pos(key_w)
        twitt_list = tw_output['pos_json']
        usr_cnt = tw_output['sname_cnt']
        print 'usr_cnt=' + str(usr_cnt)
        pst_cnt = len(twitt_list)
        username = request.session.get('username')
        return render(request, self.template_name, {'key_w': key_w, 'username': username, 'pst_cnt': pst_cnt, 'usr_cnt': usr_cnt, 'lists': twitt_list})


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
        form = request.POST
        username = form['username']
        password = form['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            return HttpResponseRedirect('index')
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
