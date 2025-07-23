"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.template.defaultfilters import title
from django.urls import path
from django.http import HttpResponse, Http404
from django.shortcuts import render,redirect

movie_list = [
    {'title': '파묘', 'director': '장재현'},
    {'title': '웡카', 'director': '폴 킹'},
    {'title': '듄:part2', 'director': '드니 빌뇌브'},
    {'title': '시민덕희', 'director': '박영주'},
]

def index(request):
    return HttpResponse("<h1>살려줘</h1>")

def book_list(request):
    return render(request,'book_list.html', {'range':range(0, 10)})

def book(request, num):
    return render(request, 'book_detail.html', {'num':num})

def language(request, lang):
    return HttpResponse(f'{lang} 언어 페이지')

def movies(request):
    return render(request, 'movies.html', {'movie_list': movie_list})

def movie_detail(request, index):
    if index > len(movie_list) - 1:
        raise Http404

    movie = movie_list[index]
    context = {'movie': movie}
    return render(request, 'movie.html', context)

def gugu(request, num):
    if num < 2:
        return redirect('/gugu/2')
    context = {
        'num': num,
        'results': [num * i for i in range(1, 10)]
    }

    return render(request, 'gugu.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('book_list/', book_list),
    path('book_list/<int:num>/', book),
    path('language/<str:lang>', language),
    path('movie/', movies),
    path('movie/<int:index>/', movie_detail),
    path('gugu/<int:num>/', gugu)
]
