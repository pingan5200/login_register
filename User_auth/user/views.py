from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import JsonResponse

from captcha.models import CaptchaStore
from .forms import CaptchaTestForm
from .forms import UserForm


# Create your views here.
# 用户登录
def loginView(request):
    if request.method == 'POST':
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            print(username)
            password = form.cleaned_data['password']
            print(password)
            if User.objects.filter(username=username):
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        tips = '登录成功'
                        return render(request, 'home.html')
                else:
                    tips = '密码错误，请重新输入'
                    return render(request, 'login.html', locals())
            else:
                tips = '用户不存在，请注册'
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())
    form = CaptchaTestForm()
    return render(request, 'login.html', locals())


# ajax接口，实现动态验证验证码
def ajax_val(request):
    if request.is_ajax():
        response = request.GET['response']
        hashkey = request.GET['hashkey']
        cs = CaptchaStore.objects.filter(response=response, hashkey=hashkey)
        # 若存在cs,验证成功，否则验证失败
        if cs:
            json_data = {'status': 1}
        else:
            json_data = {'status': 0}
        return JsonResponse(json_data)
    else:
        json_data = {'status': 0}
        return JsonResponse(json_data)


# 注册
def registerView(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # 如果数据合法，保存到user
            user = form.save(commit=False)
            print(form.cleaned_data)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'login.html', locals())
        else:
            return render(request, 'register.html', locals())
    else:
        form = UserForm()
        return render(request, 'register.html', locals())
