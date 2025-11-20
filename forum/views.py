from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import ForumPost, Comment
from .forms import ForumPostForm, CommentForm


def forum_list(request):
    """
    View to list all forum posts with search functionality.
    Accessible to all users (authenticated and anonymous).
    """
    query = request.GET.get('q', '')
    posts = ForumPost.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )

    # Pagination
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'total_posts': posts.count(),
    }
    return render(request, 'forum/forum_list.html', context)


def forum_detail(request, post_id):
    """
    View to display a single forum post with its comments.
    Accessible to all users.
    """
    post = get_object_or_404(ForumPost, id=post_id)
    comments = post.comments.all()

    # Comment form (only for authenticated users)
    comment_form = None
    if request.user.is_authenticated:
        if request.method == 'POST' and 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, "Your comment has been added.")
                return redirect('forum:forum_detail', post_id=post.id)
        else:
            comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'forum/forum_detail.html', context)


@login_required
def forum_create(request):
    """
    View to create a new forum post.
    Only accessible to authenticated users.
    """
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your post has been created successfully.")
            return redirect('forum:forum_detail', post_id=post.id)
    else:
        form = ForumPostForm()

    context = {
        'form': form,
        'title': 'Create New Post',
    }
    return render(request, 'forum/forum_create.html', context)


@login_required
def forum_search(request):
    """
    Dedicated search view for forum posts.
    Redirects to forum_list with query parameter.
    """
    query = request.GET.get('q', '').strip()
    if query:
        return redirect(f'/forum/?q={query}')
    else:
        return redirect('forum:forum_list')
