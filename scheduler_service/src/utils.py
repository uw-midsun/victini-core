import requests


def connected_to_internet():
    try:
        request = requests.get("http://www.google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False


if __name__ == "__main__":
    pass
