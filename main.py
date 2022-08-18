from requests_oauthlib import OAuth1Session
import openai 
from dotenv import load_dotenv
import schedule
import os
import time
import json

def get_hot_take() -> str:
    """Generates a hot take from openai using text-davinci-002 and the promt: "Hot Take:"

    Returns:
        str: Purely text string hot take, meta-data from openai removed
    """
    # get api key
    load_dotenv()
    openai.api_key = os.getenv("API_KEY")
    # Get the hot take
    # we will use "text-davinci-002" as the model as it can handle the task, 
    # others maybe good though, maybe research?
    output = openai.Completion.create(
        model="text-davinci-002",
        prompt="Hot Take:", # change this if you want different posts :)
        max_tokens = 260/4, # tokens are openai values of text length that the AI 
        # understands words / character groups in they have a rough character
        # length of 4 and as such are roughly 3/4's of a word, I've found though that
        # they are quite often longer thann that so I reduced my max char length to 260
        temperature = 0.9, # How random it is
        echo = True # Include "Hot take:" in the result
    )
    return output.choices[0].text

def clean_hot_take(hot_take : str) -> str:
    """Cleans up a hot take string, into a more readable format for twitter (removes double line spaces). Does NOT make sure it is twitter compliant / PC, that'd be kinda hard

    Args:
        hot_take (str): The hot take to be cleaned  

    Returns:
        str: The clean hot take
    """
    hot_take = hot_take.replace("\n\n", "\n")
    # check for length
    return hot_take

def break_tweet(hot_take : str) -> list:
    """Twitter supports 280 length posts, if the generator creates a string
    longer than that it needs to be turned into multiple posts, each one 
    replying to the last one. There is no uniform way of showing that your 
    post is a thread it is a purely user created idea, as such I chose to 
    add a little 🧵(n/m) where n is the post number and m is the total posts
    made in that thread this is added to the end of each post and posts are
    split somewhere on a space so no words are split, technically there can be
    many wacky places where this splits so this is certainly a function to look
    into later in the future

    Args:
        hot_take (str): A string which is the hot take

    Returns:
        list: A list of strings which will be each of the posts in the thread
    """
    # count the number of characters
    hot_take_list = []
    if (len(hot_take) > 260):
        # each post in the thread should be 253 characters long, leaving space
        # for " 🧵(n/m)" we then need to calculate n and m for each one and 
        # place that at the end making sure to not intersect words
        hot_take = hot_take.split(" ")
        thread = ""
        counter = 1
        for word in hot_take:
            if len(thread) + len(word) + 1 > 253:
                # end this thread add on the relevant stuff and move onto the next
                hot_take_list.append(thread+f" 🧵({counter}/")
                thread = ""
                counter += 1
            thread += word + " "
        hot_take_list.append(thread + f" 🧵({counter}/") # final word
        #has been added so finish up this thread

        # add the m to the end of each element in the thread
        for index, entry in enumerate(hot_take_list):
            hot_take_list[index] = entry + f"{str(counter)})"
        return hot_take_list
    else:
        return [hot_take] # the hot take was short enough already, good job :)

def tweet_hot_take(text: str) -> None:
    """Tweet out whatever is in text

    Args:
        text (str): The hot take to be tweeted

    Raises:
        Exception: Aghhhh Some api_keys are wrong, go fix these or twitter is not responding
        you might have sent too long of a tweet, if you've edited break_tweet() 
        that might be the issue
    """
    load_dotenv()
    hot_take = break_tweet(text)

    # get all the keys
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret_key = os.getenv("TWITTER_API_SECRET_KEY")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_SECRET_ACCESS_TOKEN")

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

    last_tweet_id = (json.loads(response.content))['data']['id'] # if i'm going ot make a thread I need to know which post I am replying to.

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
    """Just do it!
    """
    hot_take = get_hot_take()

    hot_take = clean_hot_take(hot_take)

    print(hot_take) # I'm too lazy to check twitter, just tell me what you think magic box

    tweet_hot_take(hot_take)

if __name__ == "__main__":
    #"""
    # I've not used schedule before so this is new, stackoverflow gave me this one though
    schedule.every().day.at("10:00").do(do_job)

    while True:

        schedule.run_pending()

        time.sleep(60)# makes sure it only runs ONCE a day
    #"""
    do_job()
    # TODO: maybe deal with comments at some point
    pass
