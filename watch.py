import time
import urllib
import http.client

# Watch Dog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Headers
headers = {
  'Content-type': 'application/json; charset=UTF-8'
}

# Directory to watch
directory = '/home/ruel/Downloads'


# Handler
class Handler(FileSystemEventHandler):

  @staticmethod
  def on_any_event(event):
    # Directory Events
    if event.is_directory:
      return None
    elif event.event_type == 'created':
      # Connection
      conn = http.client.HTTPConnection('localhost:8080')

      params = urllib.parse.urlencode({
        'file': event.src_path
      })
      conn.request('POST', '/', params, headers)
      # Reponse data
      # conn.getresponse().read()
      # Close connection
      conn.close()



# Watcher
class Watcher:

  def __init__(self):
    self.observer = Observer()

  def run(self):
    self.observer.schedule(Handler(), directory, recursive=True)
    self.observer.start()
    
    try:
      while True:
        time.sleep(1)
    except:
      self.observer.stop()
      print('Error')

    self.observer.join()


if __name__ == '__main__':
  w = Watcher()
  w.run()
