from ..utils import ensure_http
from ..http import HTTPUserClient, Route
from ..errors import SpotifyException

from .common import (Image, Device, Context)
from .player import Player

from spotify import _types

Track = _types.track
Artist = _types.artist
Playlist = _types.playlist
Library = _types.library

REFRESH_TOKEN_URL = 'https://accounts.spotify.com/api/token?grant_type=refresh_token&refresh_token={refresh_token}'

class User:
    __slots__ = ('__client', '__data', 'http', 'library', '_player', 'id', 'href', 'uri', 'display_name', 'followers', '_refresh_task')

    def __init__(self, client, data, **kwargs):
        self.__client = client

        token = kwargs.pop('token', None)
        self.http = http = kwargs.pop('http', None)

        if http is None and token:
            self.http = http = HTTPUserClient(token)

        if http is not None:
            self.library = Library(client, self)

        self.id = data.pop('id')
        self.display_name = data.pop('display_name')
        self.followers = data.pop('followers', {}).get('total')
        self.href = data.pop('href')
        self.uri = data.pop('uri')

        self.__data = data

    def __repr__(self):
        return '<spotify.User: "%s">' % (self.display_name or self.id)

    def __str__(self):
        return self.uri

    def __eq__(self, other):
        return type(self) is type(other) and self.uri == other.uri

    def __ne__(self, other):
        return not self.__eq__(other)

    async def _get_top(self, klass, data):
        _str = {Artist: 'artists', Track: 'tracks'}[klass]
        data = {key: value for key, value in data.items() if key in ('limit', 'offset', 'time_range')}

        resp = await self.http.top_artists_or_tracks(_str, **data)

        return [klass(self.__client, item) for item in resp['items']]


    async def _refreshing_token(self, expires, token):
        while True:
            await asyncio.sleep(expires - 1)

            route = Route('POST', REFRESH_TOKEN_URL.format(refresh_token=token))
            data = await self.client.http.request(route, content_type='application/x-www-form-urlencoded')

            expires = data['expires_in']
            self.http.token = data['access_token']

    ### Alternate constructors

    @classmethod
    async def from_code(cls, client, code, *, redirect_uri, refresh=False):
        route = Route('POST', 'https://accounts.spotify.com/api/token')
        payload = {
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
            'code': code
        }

        raw = await client.http.request(route, content_type='application/x-www-form-urlencoded')

        token = raw['access_token']

        http = HTTPUserClient(token)
        data = await http.current_user()

        if refresh:
            expires_in = raw['expires_in']
            refresh_token = raw['refresh_token']
            self._refresh_task = self.client.loop.create_task(self._refreshing_token(expires_in, refresh_token))

        return cls(client, data=data, http=http, token=token)

    @classmethod
    async def from_token(cls, client, token, *, refresh=None):
        http = HTTPUserClient(token)
        data = await http.current_user()

        if refresh is not None:
            expires_in, refresh_token, = refresh
            self._refresh_task = self.client.loop.create_task(self._refreshing_token(expires_in, refresh_token))

        return cls(client, data=data, http=http, token=token)

    ### Attributes (read only)

    @property
    def refresh(self):
        return self._refresh_task

    @property
    def external_urls(self):
        return self.__data.get('external_urls')

    @property
    def images(self):
        return [Image(**image) for image in self.__data.get('images')]

    @property
    def birthdate(self):
        return self.__data.get('birthdate')

    @property
    def country(self):
        return self.__data.get('country')

    @property
    def email(self):
        return self.__data.get('email')

    ### Contextual methods

    @ensure_http
    async def currently_playing(self):
        '''Get the users currently playing track.'''
        data = await self.http.currently_playing()

        if data.get('item'):
            data['Context'] = Context(data.get('context'))
            data['item'] = Track(self.__client, data.get('item'))

        return data

    @ensure_http
    async def get_player(self):
        '''Get information about the users current playback.'''
        self._player = player = Player(self)

        player_data = await self.http.current_player()
        player.populate(player_data)
        return player

    @ensure_http
    async def get_devices(self):
        '''Get information about the users avaliable devices.'''
        data = await self.http.available_devices()
        return [Device(item) for item in data['devices']]

    @ensure_http
    async def recently_played(self):
        '''Get tracks from the current users recently played tracks.'''
        raw = []
        data = await self.http.recently_played()

        for track in data['items']:
            track['context'] = Context(track.get('context'))
            track['track'] = Track('_tracks', data.get('track'))

            raw.append(track)  # PlayHistory(track)
        return raw

    ### Playlist track omethods

    @ensure_http
    async def add_tracks(self, playlist, *tracks):
        '''Add one or more tracks to a user’s playlist.

        **parameters**

        - *playlist* (:class:`Playlist`)
            The playlist to modify

        - *tracks* (:class:`Track`)
            Tracks to add to the playlist
        '''

        tracks = [str(track) for track in tracks]

        playlist_id = playlist
        if not isinstance(playlist_id, str):
            playlist_id = playlist.id

        return await self.http.add_playlist_tracks(self.id, playlist_id, tracks=','.join(tracks))

    @ensure_http
    async def replace_tracks(self, playlist, *tracks):
        '''Replace all the tracks in a playlist, overwriting its existing tracks. This powerful request can be useful for replacing tracks, re-ordering existing tracks, or clearing the playlist.

        **parameters**

        - *playlist* (:class:`Playlist`)
            The playlist to modify

        - *tracks* (:class:`Track`)
            Tracks to place in the playlist
        '''
        tracks = [str(track) for track in tracks]

        playlist_id = playlist
        if not isinstance(playlist_id, str):
            playlist_id = playlist.id

        return await self.http.replace_playlist_tracks(self.id, playlist_id, tracks=','.join(tracks))

    @ensure_http
    async def remove_tracks(self, playlist, *tracks):
        '''Remove one or more tracks from a user’s playlist.

        **parameters**

        - *playlist* (:class:`Playlist`)
            The playlist to modify

        - *tracks* (:class:`Track`)
            Tracks to remove from the playlist
        '''
        tracks = [str(track) for track in tracks]

        playlist_id = playlist
        if not isinstance(playlist_id, str):
            playlist_id = playlist.id

        return await self.http.remove_playlist_tracks(self.id, playlist_id, tracks=','.join(tracks))

    @ensure_http
    async def reorder_tracks(self, playlist, start, insert_before, length=1, *, snapshot_id=None):
        '''Reorder a track or a group of tracks in a playlist.

        **parameters**

        - *playlist* (:class:`Playlist`)
            The playlist to modify

        - *start* (:class:`int`)
            The position of the first track to be reordered.

        - *insert_before* (:class:`int`)
            The position where the tracks should be inserted.

        - *length* (Optional :class:`int`)
            The amount of tracks to be reordered. Defaults to 1 if not set.

        - *snapshot_id* (Optional :class:`str`)
            The playlist’s snapshot ID against which you want to make the changes.
        '''
        playlist_id = playlist
        if not isinstance(playlist_id, str):
            playlist_id = playlist.id

        return await self.http.reorder_playlists_tracks(self.id, playlist_id, start, length, insert_before, snapshot_id=snapshot_id)

    ### Playlist methods

    @ensure_http
    async def edit_playlist(self, playlist, *, name=None, public=None, collaborative=None, description=None):
        '''Change a playlist’s name and public/private, collaborative state and description.

        **parameters**

        - *playlist* (:class:`Playlist`)
            The playlist to modify

        - *name* (Optional kwarg :class:`str`)
            The new name of the playlist.

        - *public* (Optional kwarg :class:`bool`)
            The public/private status of the playlist.
            `True` for public, `False` for private.

        - *collaborative* (Optional kwarg :class:`bool`)
            If `True`, the playlist will become collaborative and other users will be able to modify the playlist.

        - *description* (Optional kwarg :class:`str`)
            The new playlist description
        '''
        playlist_id = playlist
        if not isinstance(playlist_id, str):
            playlist_id = playlist.id

        data = {}

        if name:
            data['name'] = name

        if public:
            data['public'] = public

        if collaborative:
            data['collaborative'] = collaborative

        if description:
            data['description'] = description

        return await self.http.change_playlist_details(self.id, playlist_id, data)

    @ensure_http
    async def create_playlist(self, name, *, public=True, collaborative=False, description=None):
        '''Create a playlist for a Spotify user

        **parameters**

        - *name* (Required :class:`str`)
            The name of the playlist.

        - *public* (Optional kwarg :class:`bool`)
            The public/private status of the playlist.
            `True` for public, `False` for private.

        - *collaborative* (Optional kwarg :class:`bool`)
            If `True`, the playlist will become collaborative and other users will be able to modify the playlist.

        - *description* (Optional kwarg :class:`str`)
            The playlist description
        '''

        data = {
            'name': name,
            'public': public,
            'collaborative': collaborative
        }

        if description:
            data['description'] = description

        playlist_data = await self.http.create_playlist(self.id, data)
        return Playlist(self.__client, playlist_data)

    async def get_playlists(self, *, limit=20, offset=0):
        '''get the users playlists from spotify.

        **parameters**

         - *limit* (Optional :class:`int`)
             The limit on how many playlists to retrieve for this user (default is 20).

         - *offset* (Optional :class:`int`)
             The offset from where the api should start from in the playlists.
        '''
        if hasattr(self, 'http'):
            http = self.http
        else:
            http = self.__client.http

        data = await http.get_playlists(self.id, limit=limit, offset=offset)
        return [Playlist(self.__client, playlist_data) for playlist_data in data['items']]

    ### Other user methods

    @ensure_http
    async def top_artists(self, **data):
        '''Get the current user’s top artists based on calculated affinity.

        **parameters**

        - *limit* (:class:`int`)
            The number of entities to return. Default: 20. Minimum: 1. Maximum: 50.

        - *offset* (:class:`int`)
            The index of the first entity to return. Default: 0

        - *time_range* (:class:`str`)
            Over what time frame the affinities are computed. (long_term, short_term, medium_term)
        '''
        return await self._get_top(Artist, data)

    @ensure_http
    async def top_tracks(self, **data):
        '''Get the current user’s top tracks based on calculated affinity.

        **parameters**

        - *limit* (:class:`int`)
            The number of entities to return. Default: 20. Minimum: 1. Maximum: 50.

        - *offset* (:class:`int`)
            The index of the first entity to return. Default: 0

        - *time_range* (:class:`str`)
            Over what time frame the affinities are computed. (long_term, short_term, medium_term)
        '''
        return await self._get_top(Track, data)
