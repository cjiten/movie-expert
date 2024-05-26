from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from Movie.models import Movie
from Spec.models import Genre
from Settings.models import Org

import os
import requests

# Create your views here.

def MovieView(request):
    Movies = Movie.objects.filter(is_published=True).order_by('-updated_date')
    # set up search
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            Movies = Movies.filter(title__icontains=keyword)
    # set up pagination
    p = Paginator(Movies, 10)
    page = request.GET.get('page')
    Movies = p.get_page(page)
    data = {
        'Movies': Movies
    }
    return render(request, 'Movie/MovieView.html', data)

def MovieDetailView(request, slug):
    MovieDetail = get_object_or_404(Movie, slug=slug, is_published=True)
    data = {
        'MovieDetail': MovieDetail
    }
    return render(request, 'Movie/MovieDetailView.html', data)


@login_required(login_url='/movie/')
def MovieAddView(request):
    org = Org.objects.first()
    if request.method == 'POST':
        tmdb_id = request.POST.get('tmdb_id')

        reqUrl = f"https://api.themoviedb.org/3/movie/{tmdb_id}?language=en-US"

        headersList = {
        "accept": "application/json",
        "Authorization": f"Bearer {org.tmdb_token}"
        }

        payload = ""

        movie_details = requests.request("GET", reqUrl, data=payload,  headers=headersList)
        update_movie = Movie.objects.filter(tmdb_id=tmdb_id).first()

        if movie_details.status_code == 200:
            data = movie_details.json()
            genre_data = data["genres"]

            genre_list = []
            for genre_data in genre_data:
                genre_id = genre_data.get("id")
                genre_name = genre_data.get("name")
                if genre_id and genre_name:
                    genre = Genre.objects.filter(genre_id=genre_id).exists()
                    try:
                        genre = Genre.objects.get(genre_id=genre_id)
                    except Genre.DoesNotExist:
                        genre = Genre.objects.create(genre_id=genre_id, name=genre_name)
                    genre_list.append(genre)

            # Check if the poster image already exists
            img_path = data["poster_path"]
            poster_path = f"media/posters{img_path}"
            if not os.path.exists(poster_path):
                # Save the poster image locally
                poster_url = "https://image.tmdb.org/t/p/original" + img_path
                poster_response = requests.get(poster_url)
                if poster_response.status_code == 200:
                    with open(f"media/posters/movie{img_path}", 'wb') as f:
                        f.write(poster_response.content)

            if update_movie:
                # Update the existing movie
                update_movie.imdb_id = data["imdb_id"]
                update_movie.adult = data["adult"]
                update_movie.title = data["title"]
                update_movie.original_title = data["original_title"]
                update_movie.overview = data["overview"]
                update_movie.release_date = data["release_date"]
                update_movie.runtime = data["runtime"]
                update_movie.status = data["status"]
                update_movie.tagline = data["tagline"]
                update_movie.poster_path = f"posters/movie{img_path}"
                update_movie.genre.clear()
                update_movie.genre.add(*genre_list)
                update_movie.save()
            else:
                # Create a new movie
                create_movie = Movie.objects.create(
                tmdb_id = data["id"],
                imdb_id = data["imdb_id"],
                adult = data["adult"],
                title = data["title"],
                original_title = data["original_title"],
                overview = data["overview"],
                release_date = data["release_date"],
                runtime = data["runtime"],
                status = data["status"],
                tagline = data["tagline"],
                poster_path = f"posters/movie{img_path}"
                )
                create_movie.genre.add(*genre_list)
                create_movie.save()
        else:
            messages.success(request, 'Request was not successful. Status code:', movie_details.status_code)

        messages.success(request, 'Movie Created Successfully')
        return render(request, 'Movie/MovieAddView.html')
    return render(request, 'Movie/MovieAddView.html')