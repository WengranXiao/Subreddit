
"""
Created on Wed Dec  1 13:40:59 2022

@author: Wengran Xiao
"""

import requests
import json
import time


# First create an app in Reddit and get the app ID and secret key
# Get access token

from secretkey import token

# API requests: get the data of the top 200 subreddits
api_url = 'https://oauth.reddit.com/subreddits/search'
headers = {'Authorization': token, 'User-Agent': 'community_rec_system by VivienXiao'}    
payload = {'q': 'COVID', 'limit': 50, 'sort': 'relevance'}


#construct cache
def open_cache(CACHE_FILENAME):
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(CACHE_FILENAME,cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()
    
    
cache_file=open_cache("507finalapi.json") 
if cache_file=={}:
    dataset = requests.get(api_url, headers=headers,params=payload).json()
    save_cache("507finalapi.json",dataset)
else:
    dataset=cache_file


# List of subreddits' name
subname=[]
for i in range(len(dataset['data']['children'])):
    subname.append(dataset['data']['children'][i]['data']['display_name'])
subname=subname[1:]
del subname[30]

datalist=[]
for i in range(len(dataset['data']['children'])):
    datalist.append(dataset['data']['children'][i])
datalist=datalist[1:]
del datalist[30]

#print(subname)
#print(subname[30])



class subreddits():
    def __init__(self, data):
        self.display_name=data['data']['display_name']
        self.over18=data['data']['over18']
        self.subscribers=data['data']['subscribers']
        self.accept_followers=data['data']['accept_followers']
        self.allow_images=data['data']['allow_images']
        self.allow_videos=data['data']['allow_videos']
        self.created_time="None"

classlist=[]
for i in datalist:
    classlist.append(subreddits(i))
#print(classlist)


# scrape data for the created time
from bs4 import BeautifulSoup

base_url = "https://www.reddit.com/r/"
headers = {'User-Agent': 'SI507final'}



def make_url_request_using_cache(CACHE_FILE_NAME,url, cache):
    if (url in cache.keys()): 
        return cache[url]
    else:
        time.sleep(1)
        response = requests.get(url, headers=headers)
        cache[url] = response.text
        save_cache(CACHE_FILE_NAME,cache)
        return cache[url]


CACHE_DICT = open_cache('507finalsrape.json')


for i in range(len(subname)):
    url=base_url+subname[i] 
    response=make_url_request_using_cache('507finalsrape.json',url, CACHE_DICT)
    soup = BeautifulSoup(response, 'html.parser')
    timecreated = soup.find("span", class_="_1d4NeAxWOiy0JPz7aXRI64")
    classlist[i].created_time=timecreated.text[-4:]

#print(classlist[3].created_time)
#print(classlist[3].display_name)

tree_cache=open_cache("507finaltree.json")

if tree_cache=={}:
    
    tree=\
        ("Do you prefer a subreddit that have more than 70000 subscribers?",
            ("Do you prefer a subreddit that was created before 2019?", ([],None,None), ([],None,None)),
            ("Do you prefer a subreddit that was created before 2019?", ([],None,None), ([],None,None)))
        
    
    for i in classlist:
        answerlist=[]
        if int(i.subscribers)>70000:
            answerlist.append(1)
        else:
            answerlist.append(2)
        if int(i.created_time)<2019:
            answerlist.append(1)
        else:
            answerlist.append(2)    
        tree[answerlist[0]][answerlist[1]][0].append(i.display_name)
    
    save_cache("507finaltree.json",tree)
    
else:
    tree=tree_cache



'''
def isLeaf(tree):
    if tree[1]==None and tree[2]==None:
        return True
    return False

def yes(prompt):
    if prompt in ["y", "yup", "sure","yes"]:
        return True
    return False

def Play(tree):    
    if not isLeaf(tree):
        prompt=input(f'{tree[0]}')
        if yes(prompt):
            Play(tree[1])
        else:
            Play(tree[2])
    else:
        print(tree[0])
    
Play(tree) 
    
'''
    















    
