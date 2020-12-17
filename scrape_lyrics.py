# loads 'track_and_genre.csv' and 'scraped_lyrics.csv'
# saves 'scraped_lyrics.csv' on every successful lyric
import pandas as pd
from urllib.request import Request, urlopen
from urllib.parse import quote
import json
import time

df = pd.read_csv('track_and_genre.csv')

def search(artist, title):
    # assemble search url and encode the spaces
    search_url = f'https://api.lyrics.ovh/suggest/{quote(artist + " " + title)}'.replace(' ', '%20')
    req = Request(search_url)
    resp = urlopen(req)
    return json.load(resp)

def suggest_nearest(artist, title):
    search_results = search(artist, title)
    if search_results['total'] == 0:
        raise Exception('No results')
    artist = search_results['data'][0]['artist']['name']
    title = search_results['data'][0]['title']
    
    return artist, title

def get_lyrics(artist, title):
    # assemble lyrics url and encode the spaces
    lyrics_url = f'https://api.lyrics.ovh/v1/{quote(artist)}/{quote(title)}'.replace(' ', '%20')
    req = Request(lyrics_url, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0'})
    resp = urlopen(req)
    resp_json = json.load(resp)
    # empty lyrics -> None
    return resp_json['lyrics']

def get_lyrics_retry(artist, title):
    # retry enough times to cover 60 second rate limit window
    lyrics = ""
    for timeout in [1, 4, 10, 20, 25, 15]:
        time.sleep(timeout)
        lyrics = get_lyrics(artist, title)
        if lyrics != "":
            return lyrics
    raise Exception('Could not get lyrics (does the song even exist?)')

lyrics = pd.DataFrame(columns=['track_id', 'searched_artist', 'searched_title', 'lyrics'])    
try:
    lyrics = pd.read_csv('scraped_lyrics.csv')
except:
    print('Could not load lyrics file, overwritting!')
    time.sleep(20)

print('Starting scraping process...')    

for i, entry in df.iterrows():
    if entry.track_id in lyrics.track_id.values:
        print('Lyrics found for entry', entry.track_id, 'skipping')
        continue
    
    try:
        suggested_artist, suggested_track = suggest_nearest(entry.artist, entry.song)
        resolved_lyrics = get_lyrics_retry(suggested_artist, suggested_track)

        lyrics = lyrics.append({
            'track_id': entry.track_id,
            'searched_artist': suggested_artist,
            'searched_title': suggested_track,
            'lyrics': resolved_lyrics
        }, ignore_index=True)
    except Exception as e:
        print('Encountered exception, skipping entry', entry.track_id, e)
        
        lyrics = lyrics.append({
            'track_id': entry.track_id,
            'searched_artist': None,
            'searched_title': None,
            'lyrics': None
        }, ignore_index=True)
    
    lyrics.to_csv('scraped_lyrics.csv')

print('Finished!')
