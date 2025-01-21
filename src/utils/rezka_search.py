from src.wrappers import SearchResponse
from bs4 import BeautifulSoup
from .request import Req
import re

class RezkaSearch:
  base_url = 'https://hdrezka.ag'

  def __init__(self, debug=True) -> None:
    self.debug = debug
    self.keyword = None
    self._request = Req()

  @staticmethod
  def _free_from_brackets(text: str) -> str:
    return re.sub(r'\(.*?\)', '', text).strip()
  
  @staticmethod
  def _count_pages(soup) -> int:
    pages_cont = soup.select_one('.b-content__inline_items > .b-navigation')
    if not pages_cont:
      return 1
    pages = pages_cont.find_all('a', href=True)
    page_numbers = [int(re.search(r'page=(\d+)', link['href']).group(1)) for link in pages]
    return max(page_numbers) if page_numbers else 1

  def _parse_page(self, html) -> list:
    items = []
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', attrs={'class': 'b-content__inline_item'})
    for result in results:
      ri = dict()
      ri['id'] = result.get('data-id')
      ri['url'] = result.get('data-url')
      ri['cover'] = result.select_one('.b-content__inline_item-cover > a > img').get('src')
      ri['ended'] = result.select_one('.b-content__inline_item-cover > a > span.info')
      ri['media_type'] = self._free_from_brackets(result.select_one('.b-content__inline_item-cover > a > span.cat > .entity').get_text())
      ri['name'] = result.select_one('.b-content__inline_item-link > a').get_text(strip=True)
      years, place, _ = result.select_one('.b-content__inline_item-link > div').get_text(strip=True).split(',')
      ri['year'] = years
      ri['country'] = place.strip()
      items.append(ri)
    pages = self._count_pages(soup) if len(results) >= 1 else 0
    return pages, items
  
  def search(self, keyword, **kwargs) -> SearchResponse:
    self.keyword = keyword
    url = self.base_url + '/search/'
    params = {'do': 'search', 'subaction': 'search', 'q': keyword}
    text = self._request.send(url, 'GET', params).text
    pages, info = self._parse_page(text)
    self.response = SearchResponse(keyword, pages, info)
    return self.response
    
  def next_page(self, page_num) -> SearchResponse:
    url = self.base_url + '/search/'
    page_num = 2 if not page_num else page_num
    params = {'do': 'search', 'subaction': 'search', 'q': self.keyword, 'page': page_num}
    text = self._request.send(url, 'GET', params).text
    _, info = self._parse_page(text)
    self.response.append(info)
    return self.response
  
