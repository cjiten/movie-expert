from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from Settings.models import Org
from Spec.models import Genre
from Tv.models import Series, Season, Episode

import os
import requests

# Create your views here.

def SeriesView(request):
    Seriess = Series.objects.filter(is_published=True).order_by('-updated_date')
    # set up search
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            Seriess = Seriess.filter(title__icontains=keyword)
    # set up pagination
    p = Paginator(Seriess, 10)
    page = request.GET.get('page')
    Seriess = p.get_page(page)
    data = {
        'Seriess': Seriess
    }
    return render(request, 'Tv/SeriesView.html', data)

def SeriesDetailView(request, slug):
    SeriesDetail = get_object_or_404(Series, slug=slug, is_published=True)
    Seasons = Season.objects.filter(series=SeriesDetail, is_published=True)
    data = {
        'SeriesDetail': SeriesDetail,
        'Seasons': Seasons,
    }
    return render(request, 'Tv/SeriesDetailView.html', data)

def SeasonDetailView(request, slug, season_slug):
    SeriesDetail = get_object_or_404(Series, slug=slug, is_published=True)
    SeasonDetail = get_object_or_404(Season, series=SeriesDetail, season_number=season_slug, is_published=True)
    Episodes = Episode.objects.filter(season=SeasonDetail, is_published=True)
    data = {
        'SeasonDetail': SeasonDetail,
        'SeriesDetail': SeriesDetail,
        'Episodes': Episodes,
    }
    return render(request, 'Tv/SeasonDetailView.html', data)

@login_required(login_url='/tv/')
def SeriesAddView(request):
    org = Org.objects.first()
    if request.method == 'POST':
        tmdb_id = request.POST.get('tmdb_id')

        reqUrl = f"https://api.themoviedb.org/3/tv/{tmdb_id}?language=en-US"

        headersList = {
        "accept": "application/json",
        "Authorization": f"Bearer {org.tmdb_token}"
        }

        payload = ""

        series_details = requests.request("GET", reqUrl, data=payload,  headers=headersList, verify=False)
        update_series = Series.objects.filter(tmdb_id=tmdb_id).first()

        if series_details.status_code == 200:
            data = series_details.json()
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
            poster_path = f"media/posters/tv{img_path}"
            if not os.path.exists(poster_path):
                # Save the poster image locally
                poster_url = "https://image.tmdb.org/t/p/original" + img_path
                poster_response = requests.get(poster_url)
                if poster_response.status_code == 200:
                    with open(f"media/posters/tv/series{img_path}", 'wb') as f:
                        f.write(poster_response.content)

            if update_series:
                # Update the existing movie
                update_series.adult = data["adult"]
                update_series.title = data["name"]
                update_series.original_title = data["original_name"]
                update_series.overview = data["overview"]
                update_series.release_date = data["first_air_date"]
                update_series.status = data["status"]
                update_series.tagline = data["tagline"]
                update_series.type = data["type"]
                update_series.poster_path = f"posters/tv/series{img_path}"
                update_series.genre.clear()
                update_series.genre.add(*genre_list)
                update_series.save()
            else:
                # Create a new movie
                create_series = Series.objects.create(
                tmdb_id = data["id"],
                adult = data["adult"],
                title = data["name"],
                original_title = data["original_name"],
                overview = data["overview"],
                release_date = data["first_air_date"],
                status = data["status"],
                tagline = data["tagline"],
                type = data["type"],
                poster_path = f"posters/tv/series{img_path}"
                )
                create_series.genre.add(*genre_list)
                create_series.save()

            # Add seasons for the series
            seasons = data.get("seasons", [])
            for season_data in seasons:
                season_number = season_data.get("season_number")
                if season_number:
                    add_season(tmdb_id, season_number, org.tmdb_token)
        else:
            messages.success(request, 'Request was not successful. Status code:', series_details.status_code)

        messages.success(request, 'Series Created Successfully')
        return render(request, 'Tv/SeriesAddView.html')
    return render(request, 'Tv/SeriesAddView.html')

def add_season(tmdb_id, season_number, tmdb_token):
    reqUrl = f"https://api.themoviedb.org/3/tv/{tmdb_id}/season/{season_number}?language=en-US"
    
    headersList = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_token}"
    }

    response = requests.get(reqUrl, headers=headersList, verify=False)
    
    if response.status_code == 200:
        data = response.json()
        series = get_object_or_404(Series, tmdb_id=tmdb_id)

        img_path = data.get("poster_path")
        if img_path:
            poster_path = f"media/posters/tv/season/{tmdb_id}{img_path}"
            if not os.path.exists(poster_path):
                poster_url = f"https://image.tmdb.org/t/p/original{img_path}"
                poster_response = requests.get(poster_url)
                if poster_response.status_code == 200:
                    os.makedirs(os.path.dirname(poster_path), exist_ok=True)
                    with open(poster_path, 'wb') as f:
                        f.write(poster_response.content)

        update_season = Season.objects.filter(series=series, season_number=season_number).first()
        
        if update_season:
            update_season.title = data.get("name", "")
            update_season.overview = data.get("overview", "")
            update_season.release_date = data.get("air_date", "")
            update_season.poster_path = f"posters/tv/season/{tmdb_id}{img_path}"
            update_season.save()
        else:
            Season.objects.create(
                series=series,
                title=data.get("name", ""),
                overview=data.get("overview", ""),
                season_number=season_number,
                release_date=data.get("air_date", ""),
                poster_path=f"posters/tv/season/{tmdb_id}{img_path}"
            )
        # Add seasons for the series
        episodes = data.get("episodes", [])
        for episode_data in episodes:
            episode_data
            if episode_data:
                add_episode(series, episode_data, season_number, tmdb_id)

def add_episode(series, episode_data, season_number, tmdb_id):
    season = get_object_or_404(Season, series=series, season_number=season_number)
    episode_number = episode_data.get("episode_number")

    img_path = episode_data.get("still_path")
    if img_path:
        poster_path = f"media/posters/tv/episode/{tmdb_id}{img_path}"
        if not os.path.exists(poster_path):
            poster_url = f"https://image.tmdb.org/t/p/original{img_path}"
            poster_response = requests.get(poster_url)
            if poster_response.status_code == 200:
                os.makedirs(os.path.dirname(poster_path), exist_ok=True)
                with open(poster_path, 'wb') as f:
                    f.write(poster_response.content)

    update_episode = Episode.objects.filter(season=season, episode_number=episode_number).first()
        
    if update_episode:
        update_episode.season = season
        update_episode.title = episode_data.get("name", "")
        update_episode.overview = episode_data.get("overview", "")
        update_episode.runtime = episode_data.get("runtime", "")
        update_episode.episode_number = episode_data.get("episode_number", "")
        update_episode.release_date = episode_data.get("air_date", "")
        update_episode.poster_path = f"posters/tv/episode/{tmdb_id}{img_path}"
        update_episode.save()
    else:
        Episode.objects.create(
            season = season,
            title = episode_data.get("name", ""),
            overview = episode_data.get("overview", ""),
            runtime = episode_data.get("runtime", ""),
            episode_number = episode_data.get("episode_number", ""),
            release_date = episode_data.get("air_date", ""),
            poster_path = f"posters/tv/episode/{tmdb_id}{img_path}"
        )