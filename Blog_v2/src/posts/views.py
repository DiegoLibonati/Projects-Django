from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView,CreateView, UpdateView, DeleteView
from .models import Post, Comment, PostView, Like
from .forms import PostForm, CommentForm
# Create your views here.

class PostListView(ListView):
    model = Post

class PostDetailView(DetailView):
    model = Post

    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST or None)
        if form.is_valid:
            post = self.get_object()
            comment = form.instance
            comment.user = self.request.user
            comment.post = post
            form.save()
            comment.save()
            return redirect("detail", slug=post.slug)

        return redirect("detail", slug=self.get_object().slug)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form':CommentForm()
        })

        return context

    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)

        if self.request.user.is_authenticated: # si el usuario esta autentificado deja la vista
            PostView.objects.get_or_create(user = self.request.user, post=object)

        return object

class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context

class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context

class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_queryset = Like.objects.filter(user=request.user, post=post)

    if like_queryset.exists():
        like_queryset[0].delete()
        return redirect("detail", slug=slug)

    Like.objects.create(user=request.user, post=post)
    return redirect("detail", slug=slug)

