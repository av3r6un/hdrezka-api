from .request import Req

class RezkaMedia:
  base_url = 'https://hdrezka.ag'

  def __init__(self, url) -> None:
    self.url = self.base_url + url
    self._request = Req()

  def _parse_page(self, text):
    pass

  def main(self):
    text = self._request.send(self.url, 'GET').text
    self.info = self._parse_page(text)
    return self.info
