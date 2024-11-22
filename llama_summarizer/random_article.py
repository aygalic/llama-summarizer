import requests


def get_random_wikipedia_article() -> tuple[str, str]:
    # API endpoint for a random article
    url = "https://en.wikipedia.org/w/api.php"

    # Parameters for the API request
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnlimit": "1",
        "rnnamespace": "0",
    }

    # Get the random article title
    response = requests.get(url, params=params)
    data = response.json()
    title = data["query"]["random"][0]["title"]

    # Parameters for getting the full content
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "explaintext": True,
        "exsectionformat": "plain",
    }

    # Get the full content
    response = requests.get(url, params=params)
    data = response.json()
    page = next(iter(data["query"]["pages"].values()))
    content = page["extract"]

    return title, content
