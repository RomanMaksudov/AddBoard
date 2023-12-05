from datetime import datetime

from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .forms import PostForm, ResponseForm
from .models import Post, UserResponse, Subscriber, Category
from .filters import PostFilter, ResponseFilter


class PostsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'posts.html'
    context_object_name = 'post'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    response_form = ResponseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        form = ResponseForm()
        post = get_object_or_404(Post, pk=pk)
        responses = post.reply.all()
        context['post'] = post
        context['responses'] = responses
        context['form'] = form
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostCreate(CreateView):
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'tank'
        return super().form_valid(form)


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'tank'
        return super().form_valid(form)


class ResponseList(ListView):
    raise_exception = True
    model = UserResponse
    template_name = 'responses.html'
    context_object_name = 'responses'
    paginate_by = 20


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ResponseCreate(CreateView):
    raise_exception = True
    form_class = ResponseForm
    model = UserResponse
    template_name = 'response_create.html'

    def post(self, request, pk, **kwargs):
        if request.method == 'POST':
            form = ResponseForm(request.POST or None)
            post_to_res = get_object_or_404(Post, id=pk)
            if form.is_valid():
                f = form.save(commit=False)
                f.res_user_id = self.request.user.id
                f.res_post_id = post_to_res.id
                form.save()
                return super().form_valid(form)
            else:
                return render(request, 'posts/response_create.html', {'form': form})
        else:
            form = ResponseForm()
            return render(request, 'posts/response_create.html', {'form': form})


class ResponseDelete(DeleteView):
    raise_exception = True
    model = UserResponse
    template_name = 'response_delete.html'
    success_url = reverse_lazy('responses')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Post.category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=Category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Post.category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
