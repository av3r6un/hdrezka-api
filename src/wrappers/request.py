from requests import Response, JSONDecodeError


class ResponseBody:
  _status: int = None
  _body = None
  _headers: dict = None
  _message: str = None
  _text: str = None

  def __init__(self, response: Response):
    if hasattr(response, 'text'):
      self._headers = response.headers
      self._status = response.status_code
      try:
        self._body = response.json()
        self._text = None
      except JSONDecodeError:
        self._text = response.text
        self._body = None
    if hasattr(response, 'message'):
      self._message = response.message

  @property
  def status(self) -> int:
    return self._status
  
  @property
  def body(self) -> dict:
    return self._body if self._body else {}
  
  @property
  def text(self) -> str:
    return self._text if self._text else ''
  
  @property
  def headers(self) -> dict:
    return self._headers
  
  @property
  def message(self) -> str:
    return self._message
  
  def __repr__(self) -> str:
    return f'<Response[{self.status}]'
  
  def __str__(self) -> str:
    return f'Response [{self.status}]\nMessage: {self.message}' if self._message else f'Response [{self.status}]\nBody: {self.body}\nText: {self.text}'
