import requests
import json

people = set()

with open("discordauth.txt") as f:
    auth = f.read()



def get_messages(channel_id: int, limit: int=100):
    """Returns messages from a given channel
    Parameters:
    channel_id (int): Channel ID

    Returns:

    """

    headers = {
        "authorization": f"{auth}"
    }
    r = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=100", headers=headers)
    jsonn = json.loads(r.text)
    new_list = []
    for value in jsonn:
        if not value["content"]:
            people.add(value["author"]["global_name"])
            new_list.append(
                {"username": value["author"]["global_name"], "content": "[(call/image/other)]", "id": value["id"]})
        else:
            people.add(value["author"]["global_name"])
            new_list.append(
                {"username": value["author"]["global_name"], "content": value["content"], "id": value["id"]})

    # Reverse the list of messages
    new_list.reverse()
    return new_list


def send_message(msg, channel):
    headers = {
        "authorization": f"{auth}"
    }
    r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages",
                      headers=headers,
                      json={"content": msg})
    # print(r.text)


def get_friends():
    headers = {
        "authorization": f"{auth}"
    }
    r = requests.get(f"https://discord.com/api/v9/users/@me/relationships",
                      headers=headers)
    
    # for friend in r.json():
        
    #     print(friend["user"]["global_name"])
    
    return r.json()


def get_channel_from_id(user_id):
    headers = {
        "authorization": f"{auth}"
    }
    r = requests.post(f"https://discord.com/api/v9/users/@me/channels",
                      headers=headers, json={"recipient_id": user_id})
    return r.json()["id"]


def get_guilds():
    """ Returns all guilds (aka servers) that the user is in. """

    headers = {
        "authorization": f"{auth}"
    }
    r = requests.get(f"https://discord.com/api/v9/users/@me/guilds",
                    headers=headers)
    
    # You can get the icon of the server by: https://cdn.discordapp.com/icons/{id}/{icon_name}.
    # You get the rest of the info from this function.
    return r.json()
