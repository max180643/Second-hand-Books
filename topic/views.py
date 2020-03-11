from django.shortcuts import render, redirect
from book.models import Post
from django.contrib.auth.models import User
from topic.models import Message
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def create(request):
    context = {}

    # check POST request
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        book_price = request.POST.get('book_price')
        book_type = request.POST.get('book_type')
        book_image = request.FILES.get('book_image')

        # check field
        if book_name and book_price and book_type:
            user = User.objects.get(pk=request.user.id)
            post = Post.objects.create(
                create_by=user,
                text_book=book_name,
                type=book_type,
                price=book_price,
                picture=book_image
            )
            return redirect('index')
        else:
            error = "กรุณากรอกข้อมูลให้ครบทุกช่อง!"
            context['error'] = error

        # send data back
        context['book_name'] = book_name
        context['book_price'] = book_price
        context['book_type'] = book_type

    return render(request, template_name='topic/create.html', context=context)


def topic(request, topic_id):
    context = {}
    if request.method == 'POST':
        comment = request.POST.get('comment')
        # check not empty comment
        if comment:
            user = User.objects.get(pk=request.user.id)
            topic = Post.objects.get(pk=topic_id)
            Message.objects.create(
                message=comment,
                post_id=topic,
                create_by=user
            )
            return redirect('topic', topic_id=topic_id)
        else:
            return redirect('topic', topic_id=topic_id)
    else:
        # check exist and status != close
        if Post.objects.filter(pk=topic_id).exclude(status=2).exists():
            post = Post.objects.get(pk=topic_id) # get topic object
            comment = Message.objects.filter(post_id=topic_id).order_by('create_date')
            context['post'] = post      
            context['comment'] = comment         
            if post.type == '1':
                context['type_name'] = "ประกาศขาย"
                context['by_user'] = "ผู้ขาย"
            elif post.type == '2':
                context['type_name'] = "ประกาศรับซื้อ"
                context['by_user'] = "ผู้รับซื้อ"
            # check topic owner
            if request.user.id == post.create_by.id:
                context['owner'] = True
            # check authen can comment
            if request.user.is_authenticated:
                context['login'] = True
        else:
            return redirect('index')
    return render(request, template_name='topic/topic.html', context=context)

@login_required
def manage(request):
    context = {}
    user_id = request.user.id
    post = Post.objects.filter(create_by=user_id).order_by('-id')
    context['post'] = post
    return render(request, template_name='topic/manage.html', context=context)

@login_required
def hide_topic(request, id):
    if Post.objects.filter(pk=id).exists():
        post = Post.objects.get(pk=id)
        if request.user.id == post.create_by.id:
            post.status = '2'
            post.save()
            return redirect('manage')
        else:
            return redirect('index')
    else:
        return redirect('index')

@login_required
def show_topic(request, id):
    if Post.objects.filter(pk=id).exists():
        post = Post.objects.get(pk=id)
        if request.user.id == post.create_by.id:
            post.status = '1'
            post.save()
            return redirect('manage')
        else:
            return redirect('index')
    else:
        return redirect('index')

@login_required
def delete_topic(request, id):
    if Post.objects.filter(pk=id).exists():
        post = Post.objects.get(pk=id)
        if request.user.id == post.create_by.id:
            post.delete()
            return redirect('manage')
        else:
            return redirect('index')
    else:
        return redirect('index')