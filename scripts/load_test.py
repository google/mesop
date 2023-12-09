import gevent
import requests
from gevent import monkey

# Patch sockets to make them asynchronous
monkey.patch_all()


def fetch(url):
  response = requests.get(url)
  print(f"Response: {response.text}")


def main():
  url = "http://localhost:8080/ui?request=GikvY29tcG9uZW50cy90ZXh0X2lucHV0L2UyZS90ZXh0X2lucHV0X2FwcAoA"  # Replace with your Flask server URL
  num_requests = 10  # Number of concurrent requests

  # Spawn a set of greenlets
  jobs = [gevent.spawn(fetch, url) for _ in range(num_requests)]

  # Wait for all greenlets to complete
  gevent.joinall(jobs)


if __name__ == "__main__":
  main()
