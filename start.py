from src import RezkaSearch, RezkaStreams


if __name__ == '__main__':
  kwd = 'Люцифер'
  search_engine = RezkaSearch()
  search = search_engine.search(kwd)
  stream_engine = RezkaStreams()
  streams = stream_engine.get_stream(search.items[kwd].id, 1, 1, 238)
  streams.name = search.items[kwd].name
  print(streams, streams.highest)
