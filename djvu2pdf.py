import os
import sys
import subprocess
import time
import re
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
from watchdog.events import LoggingEventHandler

desktop_path = os.path.join(os.environ["HOME"], "Desktop")
def main():
    observer = get_observer(desktop_path)
  
    observer.start()
    run_until_interrupted(OnInterruptedListener(observer))
    observer.join()
  
def get_observer(path):
    observer = Observer()
    print("observer created")
    observer.schedule(event_handler=get_event_handler(), path=path)
    print("observer scheduled")
    return observer

def get_event_handler():
    def on_created(event):
        src_path = event.src_path
        # Execute the 'djvu2pdf' command in the desktop directory
        process = subprocess.Popen(["djvu2pdf", src_path], cwd=desktop_path)
        print(f"started converting: '{src_path}'")
        process.wait()
        print(f"finished converting: '{src_path}'")
        os.system(f'rm "{src_path}"')
        print(f"removed original file: {src_path}")

    handler = RegexMatchingEventHandler(regexes=[r".*[.]djvu"])
    handler.on_created = on_created

    return handler
  
def run_until_interrupted(onInterrupted):
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    onInterrupted()

def OnInterruptedListener(observer):
  def onInterrupted():
    observer.stop()
    print("observer stopped")
  return onInterrupted

if __name__ == "__main__":
  main()