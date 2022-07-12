from multiprocessing import context
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView, DeleteView
from .forms import PostCreateForm
from .models import Post
# Create your views here.

class BlogListView(View):
    def get(self, request, *args, **kwargs):

        posts = Post.objects.all()

        context = {
            'posts':posts,
            'postslen': len(posts)
        }

        return render(request, 'blog_list.html', context)

class BlogCreateView(View):
    def get(self, request, *args, **kwargs):

        form = PostCreateForm()

        context = {
            'form':form
        }
        return render(request, 'blog_create.html', context)

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            form = PostCreateForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')

                p, created = Post.objects.get_or_create(title=title, content=content)
                p.save()
                return redirect('blog:home')

        context = {

        }
        return render(request, 'blog_create.html', context)

class BlogDetailView(View):
    def get(self, request, pk,*args, **kawrgs):
        post = get_object_or_404(Post, pk=pk)

        words = []
        post_reduce = post.content.split(" ")
        post_len = len(post_reduce)

        if len(post_reduce) > 100:
            for idx, p in enumerate(post_reduce):
                if idx > 100:
                    break
                else:
                    words.append(p)

        context = {
            'post':post,
            'postwithoutreadmore': " ".join(words),
            'completepost': post.content,
            'post_len': post_len,
        }

        return render(request, 'blog_detail.html', context)

class BlogUpdateView(UpdateView):
    model= Post
    fields= ['title', 'content']
    template_name = 'blog_update.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('blog:detail', kwargs={'pk':pk})

class BlogDeleteView(DeleteView):
    model=Post
    template_name = 'blog_delete.html'
    success_url = reverse_lazy('blog:home')
