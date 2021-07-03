from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


from .models import Group, Post, Follow
from .forms import PostForm, CommentForm

User = get_user_model()



def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,
                  'index.html',
                  {'page': page}
                  )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'page': page})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    posts_count = posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = False
    if request.user.is_authenticated:
        if Follow.objects.filter(author__following__user=request.user).exists():
            following = True
    return render(request, 'profile.html', {'author': author,
                                            'page': page, 
                                            'posts_count': posts_count, 
                                            'following': following}
                  )


def post_view(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    comments = post.comments.all()
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    posts_count = posts.count()
    form = CommentForm()
    return render(request, 'post.html', {'author': author,
                                         'posts_count': posts_count,
                                         'post': post,
                                         'comments': comments,
                                         'form': form}
                  )

@login_required
def post_edit(request, username, post_id):
    edit_post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=edit_post)
    if edit_post.author != request.user:
        return redirect('post', username, edit_post.pk)
    if form.is_valid():
        form.save()
        return redirect('post', username, edit_post.pk)
    context = {'form': form, 'is_edit': True, 'post_id': post_id, 'edit_post': edit_post}
    return render(request, 'new_post.html', context)

def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию, 
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request, 
        "misc/404.html", 
        {"path": request.path}, 
        status=404
    )

def server_error(request):
    return render(request, "misc/500.html", status=500)

@login_required
def add_comment(request, username, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('post', username, post_id)

@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('index')
    return render(request, 'new_post.html', {'form': form,
                                             'is_edit': False})

@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {'page': page})

@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    if user != author:
        try:
            follow = Follow.objects.get(user=user, author=author)
        except Exception:
            follow = Follow(user=user, author=author)
            follow.save()
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(user=user, author=author)
    follow.delete()
    return redirect('profile', username=username)