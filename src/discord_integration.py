import requests
import json

people = set()


def get_messages(channel_id):
    """Returns messages and then last message id"""
    with open("discordauth.txt") as f:
        auth = f.read()

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
                {"username": value["author"]["global_name"], "content": "[NOT A TEXT (call/image)]", "id": value["id"]})
        else:
            # people.add(value["author"]["username"])
            people.add(value["author"]["global_name"])
            # new_list.append({"username": value["author"]["username"], "content": value["content"], "id": value["id"]})
            new_list.append(
                {"username": value["author"]["global_name"], "content": value["content"], "id": value["id"]})
            # print(value, "\n")

    newnewlist = new_list.copy()
    # Reversed list!
    new_list.reverse()
    last_message = new_list[0]["id"]
    # print(new_list)
    return new_list


def send_message(msg, channel):
    with open("discordauth.txt") as f:
        auth = f.read()
    headers = {
        "authorization": f"{auth}"
    }
    r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages",
                      headers=headers,
                      json={"content": msg})
    # print(r.text)


def get_friends():
    with open("discordauth.txt") as f:
        auth = f.read()
    headers = {
        "authorization": f"{auth}"
    }
    r = requests.get(f"https://discord.com/api/v9/users/@me/relationships",
                      headers=headers)
    
    # for friend in r.json():
        
    #     print(friend["user"]["global_name"])
    
    return r.json()


def get_channel_from_id(user_id):
    with open("discordauth.txt") as f:
        auth = f.read()
    headers = {
        "authorization": f"{auth}"
    }
    r = requests.post(f"https://discord.com/api/v9/users/@me/channels",
                      headers=headers, json={"recipient_id": user_id})
    return r.json()["id"]
