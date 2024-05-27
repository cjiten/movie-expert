import os
import requests
import asyncio
import aiohttp
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from Settings.models import Org
from Tv.models import Series, Season, Episode
from Spec.models import Genre

async def fetch_seasons_data(tmdb_id, org_token):
    req_url = f"https://api.themoviedb.org/3/tv/{tmdb_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {org_token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(req_url, headers=headers) as response:
            data = await response.json()
            return data.get("seasons", [])

async def fetch_season_data(tmdb_id, season_number, org_token):
    req_url = f"https://api.themoviedb.org/3/tv/{tmdb_id}/season/{season_number}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {org_token}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(req_url, headers=headers) as response:
            return await response.json()

async def download_image(url, path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(path, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)

def add_episode(season, episode_data, tmdb_id):
    img_path = episode_data.get("still_path")
    if img_path:
        poster_url = f"https://image.tmdb.org/t/p/original{img_path}"
        poster_path = f"media/posters/tv/episode/{tmdb_id}{img_path}"
        if not os.path.exists(poster_path):
            asyncio.run(download_image(poster_url, poster_path))

    Episode.objects.update_or_create(
        season=season,
        episode_number=episode_data.get("episode_number"),
        defaults={
            'title': episode_data.get("name", ""),
            'overview': episode_data.get("overview", ""),
            'runtime': episode_data.get("runtime", ""),
            'release_date': episode_data.get("air_date", ""),
            'poster_path': f"posters/tv/episode/{tmdb_id}{img_path}" if img_path else None
        }
    )

async def process_season(tmdb_id, season_data, org_token):
    season_number = season_data.get("season_number")
    series = Series.objects.get(tmdb_id=tmdb_id)
    img_path = season_data.get("poster_path")
    if img_path:
        poster_url = f"https://image.tmdb.org/t/p/original{img_path}"
        poster_path = f"media/posters/tv/season/{tmdb_id}{img_path}"
        if not os.path.exists(poster_path):
            asyncio.run(download_image(poster_url, poster_path))

    season, _ = Season.objects.update_or_create(
        series=series,
        season_number=season_number,
        defaults={
            'title': season_data.get("name", ""),
            'overview': season_data.get("overview", ""),
            'release_date': season_data.get("air_date", ""),
            'poster_path': f"posters/tv/season/{tmdb_id}{img_path}" if img_path else None
        }
    )

    episodes_data = await fetch_episodes_data(tmdb_id, season_number, org_token)
    for episode_data in episodes_data:
        add_episode(season, episode_data, tmdb_id)

@login_required(login_url='/tv/')
def SeriesAddView(request):
    org = Org.objects.first()
    if request.method == 'POST':
        tmdb_id = request.POST.get('tmdb_id')
        try:
            series_data = asyncio.run(fetch_series_data(tmdb_id, org.tmdb_token))
            if series_data:
                genre_list = []
                for genre_data in series_data['genres']:
                    genre_obj, _ = Genre.objects.get_or_create(genre_id=genre_data['id'], defaults={'name': genre_data['name']})
                    genre_list.append(genre_obj)

                img_path = series_data.get("poster_path")
                if img_path:
                    poster_url = f"https://image.tmdb.org/t/p/original{img_path}"
                    poster_path = f"media/posters/tv/series{img_path}"
                    if not os.path.exists(poster_path):
                        asyncio.run(download_image(poster_url, poster_path))

                series, created = Series.objects.update_or_create(
                    tmdb_id=series_data["id"],
                    defaults={
                        'adult': series_data["adult"],
                        'title': series_data["name"],
                        'original_title': series_data["original_name"],
                        'overview': series_data["overview"],
                        'release_date': series_data["first_air_date"],
                        'status': series_data["status"],
                        'tagline': series_data["tagline"],
                        'type': series_data["type"],
                        'poster_path': f"posters/tv/series{img_path}"
                    }
                )
                series.genre.set(genre_list)

                seasons_data = asyncio.run(fetch_seasons_data(tmdb_id, org.tmdb_token))
                tasks = [process_season(tmdb_id, season_data, org.tmdb_token) for season_data in seasons_data]
                await asyncio.gather(*tasks)

                messages.success(request, 'Series Created Successfully')
            else:
                messages.error(request, 'No data found for this series')
        except Exception as e:
            messages.error(request, f'Error occurred: {str(e)}')

    return render(request, 'Tv/SeriesAddView.html')
