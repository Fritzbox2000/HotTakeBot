# HotTakeBot

- [HotTakeBot](#hottakebot)
  - [Usage](#usage)
  - [Running it for yourself](#running-it-for-yourself)
    - [Install the python modules](#install-the-python-modules)
    - [Create an openai account and a twitter account](#create-an-openai-account-and-a-twitter-account)
    - [Set up the environment variables](#set-up-the-environment-variables)
  - [Final notes](#final-notes)

This is a small python bot for tweeting out auto generated text from openai

## Usage

So I don't really know anything about licenses, so just kinda go wild I guess. It'd be appreciated if you were to edit the code though, even if it's just the prompt you send to openai

## Running it for yourself

### Install the python modules

You are going to need a few python modules, in your environment (I would suggest virtual environment) you will need to run these 4 commands  
`python -m pip install requests_oauthlib`  
`python -m pip install openai`  
`python -m pip install python-dotenv` (I don't use just plain `dotenv` as it doesn't seem to work with python 3.10.4 which is what I am on, this fixes that though)  
`python -m pip install schedule`  

### Create an openai account and a twitter account

Nice and simple, create both accounts, make sure you save all the api keys you are given (you will need a few of them) also make sure you make your twitter account a developer account this [website](https://developer.twitter.com/en/docs/tutorials/how-to-create-a-twitter-bot-with-twitter-api-v2) will help

### Set up the environment variables

Then you need to create a .env file in the same directory as main.py inside you will need  
`API_KEY=` which should equal the openai key given by your openai account  
`TWITTER_API_KEY=` which is the given when you create your developer account for twitter (along with two other keys)  
`TWITTER_API_SECRET_KEY=` similar to the one above but *secret*  
`TWITTER_ACCESS_TOKEN=` These are gotten by using the api url "https://api.twitter.com/oauth/authorize" it's a bit of a pain and I got mine from following (copying) the code from [this repo](https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/Manage-Tweets/create_tweet.py) and just saving the output of access_token and access_token_secret.  
`TWITTER_SECRET_ACCESS_TOKEN=` Same as above  

Ok you are **good to go!**

## Final notes

So yeah that's kinda it, a simple bot, with generally poorly written code, plans for the future are to rewrite to be more efficient (both in python, and then some other languages) It doesn't *need* to be more efficient it runs a function once a day and doesn't work it *real* time. Still if it is running on my server in the background, i'd prefer it to have a low footprint
