from src.wrappers import RezkaStreams as Streams
from base64 import b64encode, b64decode
from itertools import product
from .request import Req
import time


class RezkaStreams:
  base_url = 'https://hdrezka.ag/'
  streams: Streams = None

  def __init__(self) -> None:
    self._request = Req(debug=True)
    self.url = self.base_url + '/ajax/get_cdn_series/'

  @staticmethod
  def _clear_trash(data) -> str:
    trashList = ['@', '#', '!', '^', '$']
    trashCodesSet = []
    for i in range(2, 4):
      startchar = ''
      for chars in product(trashList, repeat=i):
        data_bytes = startchar.join(chars).encode('utf-8')
        trash_combo = b64encode(data_bytes)
        trashCodesSet.append(trash_combo)
    
    arr = data.replace('#h', '').split('//_//')
    trash_string = ''.join(arr)

    for i in trashCodesSet:
      temp = i.decode('utf-8')
      trash_string = trash_string.replace(temp, '')
    
    final_string = b64decode(trash_string+"==")
    return final_string.decode('utf-8')
  
  def get_stream(self, id, season, episode, translation=None, index=0) -> Streams:
    attempt = 0
    max_attempts = 4
    while attempt <= max_attempts:
      data = {'action': 'get_stream', 'translator_id': translation, 'season': season, 'episode': episode, 'id': id}
      params = {'t': int(time.time_ns() / 1000000)}
      info = self._request.send(self.url, 'POST', data=data, params=params, timeout=40)
      if info.body['success']:
        subtitles = info.body['subtitle'].split(',') if info.body.get('subtitle') else None
        try:
          info = self._clear_trash(info.body['url']).split(',')
          break
        except UnicodeDecodeError or info.body['error']:
          print('New attempt: ', attempt)
          attempt += 1
      else:
        print(info.body)
        break
    else:
      import sys
      print('Failed to receive answer from server!')
      sys.exit(-1)
    self.streams = Streams(translation, subtitles, season, episode)
    for i in info:
      temp = i.split('[')[1].split(']')
      quality = str(temp[0])
      links = filter(lambda x: x.endswith('.mp4'), temp[1].split(' or '))
      for video in links:
        self.streams.add({'quality': quality, 'url': video})

    return self.streams

