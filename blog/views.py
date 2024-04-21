from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from django.core.paginator import Paginator, Page, EmptyPage

from .models import Post, Tag
from .utils import *
from .forms import TagForm, PostForm, RegistrationForm, LoginForm, CommentForm
from django.contrib import messages
from typing import List, Type, Any, Union


def authentification(request: HttpRequest) -> HttpResponse:
    """
    Renders the authentification page.
    """
    return render(request, 'blog/authentification.html')


class RegisterUser(CreateView):
    """
    Registers a new user.
    """
    form_class: RegistrationForm = RegistrationForm
    template_name: str = 'blog/registration.html'
    success_url: str = reverse_lazy('login_url')

    def form_invalid(self, form):
        """
        Displays an error message if the passwords don't match.
        """
        response: Any = super().form_invalid(form)
        if form.errors.get('password2') == ['Пароли не совпадают']:
            messages.error(self.request, 'Пароли не совпадают')
        return response


class LoginUser(LoginView):
    """
    Logs in a user.
    """
    form_class: LoginForm = LoginForm
    template_name: str = 'blog/login.html'

    def form_invalid(self, form):
        """
        Displays an error message if the login credentials are invalid.
        """
        response: Any = super().form_invalid(form)
        messages.error(self.request, 'Неверный логин или пароль')
        return response

    def get_success_url(self) -> str:
        """
        Returns the URL to redirect to after successful login.
        """
        return reverse_lazy('posts_list_url')


def logout_confirm(request: HttpRequest) -> HttpResponse:
    """
    Asks the user to confirm the logout.
    """
    return render(request, 'blog/logout.html')


def logout_user(request: HttpRequest) -> HttpResponse:
    """
    Logs out the user.
    """
    logout(request)
    return redirect('login_url')


def posts_list(request: HttpRequest) -> HttpResponse:
    """
    Renders a paginated list of all the posts in the database.
    The posts are ordered by the date created, newest first.

    Returns HTTP response object, containing the rendered template.
    """
    search_query: str = request.GET.get('search', '')

    if search_query:
        posts: List[Post] = Post.objects.filter(
            Q(title__icontains=search_query) |
            Q(body__icontains=search_query)
        )
    else:
        posts: List[Post] = Post.objects.all()

    paginator: Paginator = Paginator(posts, 6)

    page_number: int = request.GET.get('page', 1)
    page: Union[Page, EmptyPage] = paginator.get_page(page_number)

    is_paginated: bool = page.has_other_pages()

    if page.has_previous():
        prev_url: str = f'?page={page.previous_page_number()}'
    else:
        prev_url: str = ''

    if page.has_next():
        next_url: str = f'?page={page.next_page_number()}'
    else:
        next_url: str = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }
    return render(request, 'blog/index.html', context=context)


class PostDetail(View):
    """
    Displays details and comments of a Post object.
    """
    model: Type[Any] = Post
    template: str = 'blog/post_detail.html'

    def get(self, request: Any, slug: str) -> Any:
        """
        Gets an object and renders it using a template.
        A response containing the mapping of an object using a template.
        """
        post: Any = get_object_or_404(self.model, slug__iexact=slug)
        comments: Any = Comment.objects.filter(post=post)
        form: Any = CommentForm()
        context: dict = {
            self.model.__name__.lower(): post,
            'admin_object': post,
            'detail': True,
            'comments': comments,
            'form': form,
        }
        return render(request, self.template, context)

    def post(self, request: Any, slug: str) -> Any:
        """
        Handles POST requests for adding comments to an object.
        """
        text: Any = get_object_or_404(self.model, slug__iexact=slug)
        form: Any = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = text
            comment.author = request.user
            comment.save()
            return redirect('add_comment', slug=text.slug)
        else:
            comments: Any = Comment.objects.filter(post=text)
            context: dict = {
                self.model.__name__.lower(): text,
                'admin_object': text,
                'detail': True,
                'comments': comments,
                'form': form,
            }
            return render(request, self.template, context)


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    """
    Controller for creating a new blog post.
    """
    form_model: Type[Any] = PostForm
    template: str = 'blog/post_create_form.html'
    raise_exception: bool = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    """
    Controller for updating a blog post.
    """
    model: Type[Any] = Post
    form_model: Type[Any] = PostForm
    template: str = 'blog/post_update_form.html'
    raise_exception: bool = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    """
    Controller for deleting a blog post.
    """
    model: Type[Any] = Post
    template: str = 'blog/post_delete_form.html'
    redirect_url: str = 'posts_list_url'
    raise_exception: bool = True


def tags_list(request: HttpRequest) -> HttpResponse:
    """
    Returns a response containing a list of all the tags.
    A response containing a list of all the tags.
    """
    tags: List[Tag] = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


class TagDetail(ObjectDetailMixin, View):
    """
    Displays the details of a Tag object.
    """
    model: Type[Any] = Tag
    template: str = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    """
    Controller for creating a new tag.
    """
    form_model: Type[Any] = TagForm
    template: str = 'blog/tag_create.html'
    raise_exception: bool = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    """
    Controller for updating a tag.
    """
    model: Type[Any] = Tag
    form_model: Type[Any] = TagForm
    template: str = 'blog/tag_update_form.html'
    raise_exception: bool = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    """
    Controller for deleting a tag.
    """
    model: Type[Any] = Tag
    template: str = 'blog/tag_delete_form.html'
    redirect_url: str = 'tags_list_url'
    raise_exception: bool = True
