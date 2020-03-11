from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from book.models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    context = {}
    if request.method == 'POST':
        sell_search = request.POST.get('sell_search')
        buy_search = request.POST.get('buy_search')
        if sell_search and buy_search:
            # search
            context['sell_search'] = sell_search
            context['buy_search'] = buy_search
            sell_list = Post.objects.filter(type=1, text_book__icontains=sell_search).exclude(status=2).order_by('-create_date')
            buy_list = Post.objects.filter(type=2, text_book__icontains=buy_search).exclude(status=2).order_by('-create_date')
            context['sell_list'] = sell_list
            context['buy_list'] = buy_list
        elif sell_search:
            # search
            context['sell_search'] = sell_search
            sell_list = Post.objects.filter(type=1, text_book__icontains=sell_search).exclude(status=2).order_by('-create_date')
            # not search
            buy_list = Post.objects.filter(type=2).exclude(status=2).order_by('-create_date')
            context['sell_list'] = sell_list
            context['buy_list'] = buy_list
        elif buy_search:
            context['buy_search'] = buy_search
            buy_list = Post.objects.filter(type=2, text_book__icontains=buy_search).exclude(status=2).order_by('-create_date')
            # not search
            sell_list = Post.objects.filter(type=1).exclude(status=2).order_by('-create_date')
            context['sell_list'] = sell_list
            context['buy_list'] = buy_list
        else:
            sell_list = Post.objects.filter(type=1).exclude(status=2).order_by('-create_date')
            buy_list = Post.objects.filter(type=2).exclude(status=2).order_by('-create_date')
            context['sell_list'] = sell_list
            context['buy_list'] = buy_list
    else:
        sell_list = Post.objects.filter(type=1).exclude(status=2).order_by('-create_date')
        buy_list = Post.objects.filter(type=2).exclude(status=2).order_by('-create_date')
        context['sell_list'] = sell_list
        context['buy_list'] = buy_list
    return render(request, template_name='book/index.html', context=context)


def xlogin(request):
    context = {}

    # check already login
    if request.user.is_authenticated:
        return redirect('index')

    # check POST request
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ถ้า login สำเร็จมันจะ return object ของ user แต่ถ้า login ไม่สำเร็จจะ return null
        # เป็นแค่การ check ค่าใน DB ว่าตรงไหมเฉยๆ ยังไม่มีการสร้าง session
        user = authenticate(request, username=username, password=password)

        next_url = request.POST.get('next_url')

        if user:
            login(request, user)  # เป็นการสร้าง session
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            error = 'ชื่อผู้ใช้หรือรหัสผ่านผิด!'
            context['username'] = username
            context['error'] = error
            context['next_url'] = next_url

    # ได้แค่ 1 ครั้ง ตอน Required login
    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url

    return render(request, template_name='login.html', context=context)

@login_required
def xlogout(request):
    logout(request)
    return redirect('index')


def xregister(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # check field
        if User.objects.filter(username=username).exists():
            error = "ชื่อผู้ใช้นี้มีท่านอื่่นใช้งานแล้ว!"
            context['error'] = error
        elif User.objects.filter(email=email).exists():
            error = "อีเมลนี้มีท่านอื่่นใช้งานแล้ว!"
            context['error'] = error
        elif password1 == password2 and username and fname and lname and email and password1 and password2:
            # create user
            user = User.objects.create_user(
                username=username, 
                first_name=fname, 
                last_name=lname, 
                email=email, 
                password=password1)
            # auto login
            user = authenticate(request, username=username,
                                password=password1)  # check in DB
            login(request, user)  # เป็นการสร้าง session
            return redirect('index')
        elif password1 != password2:
            error = "รหัสผ่านทั้งสองช่องไม่ตรงกัน!"
            context['error'] = error
        else:
            error = "กรุณากรอกข้อมูลให้ครบทุกช่อง!"
            context['error'] = error

        # send data back
        context['username'] = username
        context['fname'] = fname
        context['lname'] = lname
        context['email'] = email

    return render(request, template_name='register.html', context=context)
