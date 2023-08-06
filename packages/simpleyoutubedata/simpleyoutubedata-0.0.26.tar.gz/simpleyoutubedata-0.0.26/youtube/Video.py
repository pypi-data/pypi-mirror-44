from __future__ import unicode_literals

if __name__ == "__main__":
    raise

class Video:
    OtherProps = {}

    def __init__(self, data):
        self.id = data["id"]["videoId"]
        self.kind = data["id"]["kind"].split("#")[1]

        s = data["snippet"]

        self.publishedAt = s["publishedAt"]
        self.channelId = s["channelId"]
        self.title = s["title"]
        self.description = s["description"]

        self.thumbnails = s["thumbnails"]
        self.channelTitle = s["channelTitle"]
        self.liveBroadcastContent = s["liveBroadcastContent"]

        if self.title == "Private video" and self.description == "This video is private.":
            self.private = True
        else:
            self.private = False

        self.OriginalData = data

def _GetFromId(client, kwargs):
    response = client.videos().list(**kwargs).execute()

    if len(response['items']) < 0:
        raise Exception("Invalid video ID.")

    return Video(response['items'][0])

def GetFromId(client, id):
    kwargs = {
        'id': id,
        'part': 'snippet'
    }

    return _GetFromId(client, kwargs)
