from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from blog.forms import BlogForm
from blog.models import Blog


def blog_list(request):
    blogs = Blog.objects.all().order_by("-create_at")

    q = request.GET.get("q")
    if q:
        blogs = blogs.filter(Q(title__icontains=q) | Q(content__icontains=q))

        blogs = blogs.filter(content__icontains=q).order_by("-create_at")

    paginator = Paginator(blogs, 10)
    page = request.GET.get("page")
    page_object = paginator.get_page(page)

    context = {
        "object_list": page_object.object_list,
        "page_obj": page_object,
    }

    return render(request, "blog_list.html", context)


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {
        "blog": blog,
    }
    return render(request, "blog_detail.html", context)


@login_required()
def blog_create(request):
    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return redirect(reverse(viewname="fb:detail", kwargs={"pk": blog.pk}))

    context = {"form": form}
    return render(request, "blog_form.html", context)


@login_required()
def blog_update(request, pk):
    if request.user.is_superuser:
        blog = get_object_or_404(Blog, pk=pk)
    else:
        blog = get_object_or_404(Blog, pk=pk, author=request.user)

    form = BlogForm(request.POST or None, request.FILES or None, instance=blog)
    if form.is_valid():
        blog = form.save()
        return redirect(reverse(viewname="fb:detail", kwargs={"pk": blog.pk}))

    context = {
        "form": form,
    }
    return render(request, "blog_form.html", context)


@login_required()
@require_http_methods(["POST"])
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()

    return redirect(reverse(viewname="fb:list"))
