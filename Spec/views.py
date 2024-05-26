from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from Spec.models import Link, Genre, Category
from Movie.models import Movie
from Tv.models import Series
from Client.models import Client, ClientLink

import random
from itertools import chain

# Create your views here.

def HomeView(request):
    Movies = Movie.objects.filter(is_published=True).order_by('-updated_date')
    Seriess = Series.objects.filter(is_published=True).order_by('-updated_date')
    # set up search
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            Movies = Movies.filter(title__icontains=keyword)
            Seriess = Seriess.filter(title__icontains=keyword)
    # Limit the number of results after filtering
    Movies = Movies[:5]
    Seriess = Seriess[:5]
    data = {
        'Movies': Movies,
        'Seriess': Seriess,
    }
    return render(request, 'Spec/HomeView.html', data)

def LinkReceiveView(request, slug):
    try:
        link_id = get_object_or_404(Link, uuid=slug, is_active=True)
        make_link = link_id.link
        return redirect(make_link)
    except Exception as e:
        return redirect('MovieView')


def LinkSendView(request, slug):
    all_website = Client.objects.all()
    random_website = random.choice(all_website)

    website_links = ClientLink.objects.filter(website=random_website)
    random_website_links = random.choice(website_links)

    random_url = random_website_links.link
    uuid = str(random_website.my_uuid)

    url = random_url + '?check=' + uuid + '&mid=' + slug

    return redirect(url)

def GenerView(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    Movies = Movie.objects.filter(is_published=True, genre=genre).order_by('-updated_date')
    Seriess = Series.objects.filter(is_published=True, genre=genre).order_by('-updated_date')
    # Combine querysets
    genre_data = list(chain(Movies, Seriess))
    # set up pagination
    p = Paginator(genre_data, 10)
    page = request.GET.get('page')
    genre_data = p.get_page(page)
    data = {
        'genre_data': genre_data,
        'genre': genre,
    }
    return render(request, 'Spec/GenerView.html', data)


def CategoryView(request, slug):
    category = get_object_or_404(Category, slug=slug)
    Movies = Movie.objects.filter(is_published=True, category=category).order_by('-updated_date')
    Seriess = Series.objects.filter(is_published=True, category=category).order_by('-updated_date')
    # Combine querysets
    category_data = list(chain(Movies, Seriess))
    # set up pagination
    p = Paginator(category_data, 10)
    page = request.GET.get('page')
    category_data = p.get_page(page)
    data = {
        'category': category,
        'category_data': category_data,
    }
    return render(request, 'Spec/CategoryView.html', data)