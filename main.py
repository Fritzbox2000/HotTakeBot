from requests_oauthlib import OAuth1Session
import openai 
from dotenv import load_dotenv
import schedule
import os
import time
import json

def get_hot_take() -> str:
    # get api key
    load_dotenv()
    openai.api_key = os.getenv("API_KEY")
    # we will use "text-davinci-002" as the model as it can handle the task, 
    # others maybe good though, maybe research?
    output = openai.Completion.create(
        model="text-davinci-002",
        prompt="Hot Take:",
        max_tokens = 266, # tokens are openai values of text length that the AI 
        # understands words / character groups in they have a rough character
        # length of 4 and as such are roughly 3/4's of a word,
        temperature = 0.9,
        echo = True
    )
    return output.choices[0].text

def clean_hot_take(hot_take : str) -> str:
    hot_take = hot_take.replace("\n\n", "\n")
    # check for length
    return hot_take

def break_tweet(hot_take : str) -> list:
    # count the number of characters
    hot_take_list = []
    if (len(hot_take) > 260):
        pass
        # this needs to be a thread
        # each post in the thread should be 253 characters long, leaving space for " 🧵(n/m)" we then need to calculate n and m for each one and place that at the end making sure to not intersect words
        hot_take = hot_take.split(" ")
        finished = False
        thread = ""
        counter = 1
        for word in hot_take:
            if len(thread) + len(word) + 1 > 253:
                # end this thread add on the relevant stuff and move onto the next
                hot_take_list.append(thread+f" 🧵({counter}/)")
                thread = ""
                counter += 1
            thread += word + " "
        hot_take_list.append(thread + f" 🧵({counter}/)")
        for index, entry in enumerate(hot_take_list):
            hot_take_list[index] = entry[: len(entry)-1] + str(counter) + entry[len(entry)-1:]
        return hot_take_list
    else:
        return [hot_take]

def tweet_hot_take(text: str) -> None:
    load_dotenv()
    # break up tweet
    hot_take = break_tweet(text)
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret_key = os.getenv("TWITTER_API_SECRET_KEY")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_SECRET_ACCESS_TOKEN")
    #print(api_key)
    #print(api_secret_key)
    #print(access_token)
    #print(access_token_secret)

    payload = {"text":hot_take[0]}
    oauth = OAuth1Session(
    api_key,
    client_secret=api_secret_key,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
    )

    # Making the request
    
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))
    last_tweet_id = (json.loads(response.content))['data']['id']
    if len(hot_take) > 1:
        # post the rest of the thread in the comments
        # in theory it should only make a post that is at max a length of 2 thread (including the start post), but it might go up to 3
        for thread in hot_take[1:]:
            payload = {"text":thread,'reply':{'in_reply_to_tweet_id':last_tweet_id}}
            oauth = OAuth1Session(
            api_key,
            client_secret=api_secret_key,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
            )

            # Making the request
            
            response = oauth.post(
                "https://api.twitter.com/2/tweets",
                json=payload,

            )

            if response.status_code != 201:
                raise Exception(
                    "Request returned an error: {} {}".format(response.status_code, response.text)
                )

            print("Response code: {}".format(response.status_code))
            last_tweet_id = (json.loads(response.content))['data']['id']
    return 

def do_job() -> None:
    hot_take = get_hot_take()
    hot_take = clean_hot_take(hot_take)
    print(hot_take)
    # post hot take to twitter
    tweet_hot_take(hot_take)

if __name__ == "__main__":
    #"""
    schedule.every().day.at("10:00").do(do_job)

    while True:
        schedule.run_pending()
        time.sleep(60)
    #"""
    do_job()
    # maybe deal with comments 
    # ========================
    # deal with when it should trigger
    pass
