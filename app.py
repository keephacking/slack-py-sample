import os
from slack_sdk.rtm import RTMClient
from slack_sdk.web.legacy_client import LegacyWebClient
import json
import time

# This is to get token from my config.json
tokens = {}
with open('configs.json') as json_data:
    tokens = json.load(json_data)


@RTMClient.run_on(event="message")
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    print(data['text'])
    # if 'start' in data['text']:
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user']

    print('Post message-'+channel_id)
    result = web_client.chat_postMessage(
        channel=channel_id,
        # text=f"Hi <@{user}>!",
        text=f"Hi <@{user}>!, bot is active now.",
        thread_ts=thread_ts
    )
    print(result)


slack_token = tokens.get("slack_bot_token")  # os.environ["SLACK_API_TOKEN"]
print('Token-'+slack_token)

client = LegacyWebClient(token=slack_token)
# response = client.api_call(
#     api_method='chat.postMessage',
#     json={'channel': "D01K4FH6ETW", "text": "Hi Beena, This is a test."}
# )

usersListRes = client.users_list()
# print(usersListRes)

userIds = []
for user in usersListRes["members"]:
    try:
        if not user["is_bot"] and user["profile"]["email"]:
            userIds.append(user["id"])
    except:
        pass


print(userIds)

openRes = client.conversations_open(users=userIds)
# openRes = client.conversations_open(users=['U01K53KBBEC', 'U01KAV74U57'])
# print(openRes)

# send message in the app's channel
# response = client.api_call(
#     api_method='chat.postMessage',
#     json={'channel': openRes["channel"]["id"],
#           "text": "Tets for sending message to both Beena and Sachin."}
# )
# print(response)

# send message each users separately
for userId in userIds:
    response = client.api_call(
        api_method='chat.postMessage',
        json={'channel': userId,
              "text": "Tets for sending message."}
    )

# send message as slackbot
# response = client.api_call(
#     api_method='chat.postMessage',
#     json={'channel': userId, "text": "Hi Beena, This is a test."}
# )
# print(response)

rtm_client = RTMClient(token=slack_token)
rtm_client.start()
print("END")
