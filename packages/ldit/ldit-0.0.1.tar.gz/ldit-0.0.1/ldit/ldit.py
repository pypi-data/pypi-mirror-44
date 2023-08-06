import json
import requests


def list_tags(image, cli=False):
    """
    Return a list of tags of a given Docker Hub image.
    Example:
    In : list_tags('google/debian')
    Out: ['jessie', 'wheezy']
    In : list_tags('python')
    Out: ['31', 'rawhide', '30', '29', 'latest' ...]
    """

    if cli:
        print("The image '{}' on Docker Hub got following tag(s):".format(image))

    if image.find('/') == -1:
        image = 'library/'+image

    tags = []

    page = 1

    while True:
        url = "https://registry.hub.docker.com/v2/repositories/{}/tags/?page={}".format(
            image, page)
        request = requests.get(url)

        if request.status_code == 200:
            result = json.loads(request.text)
            for i in range(len(result["results"])):
                if cli:
                    print(result["results"][i]["name"])
                else:
                    tags.append(result["results"][i]["name"])
            page += 1
        else:
            break

    if cli == False:
        return tags

