from src.wrappers import ResponseBody
from requests import Request, Session, JSONDecodeError, ConnectionError, ConnectTimeout
from fake_useragent import UserAgent
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


class Req:
  _headers = {
    'User-Agent': UserAgent().random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cookie': os.getenv('Cookie')
  }
  _base_uri: str = None

  def __init__(self, debug=False):
    self.debug = debug
    self._session = Session()
    self._request = Request(headers=self._headers)

  def _send(self, url, method, params=None, data=None, timeout=15):
    self._request.url = url
    self._request.method = method
    self._request.params = params
    self._request.data = data
    prepared_request = self._request.prepare()
    try:
      with self._session as resp:
        info = resp.send(prepared_request, timeout=timeout)
      if self.debug:
        print(info.request.body, info.request.headers, info.url)
      return ResponseBody(info)
    except (ConnectionError, ConnectTimeout, JSONDecodeError) as err:
      print(err)
      return None
  
  def send(self, url, method, params=None, data=None, timeout=None) -> ResponseBody:
    return self._send(url, method, params, data, timeout)
  
