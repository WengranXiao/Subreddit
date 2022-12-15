
"""
Created on Wed Dec  1 13:40:59 2022

@author: Wengran Xiao
"""

import requests
import json
import time

#Construct cache functions
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

def make_url_request_using_cache(CACHE_FILE_NAME,url, cache):
    if (url in cache.keys()): 
        return cache[url]
    else:
        time.sleep(1)
        response = requests.get(url, headers=headers)
        cache[url] = response.text
        save_cache(CACHE_FILE_NAME,cache)
        return cache[url]
    
    

#Import the access token I got in secretkey.py
from secretkey import token

# OAuth API requests: get the data of the top 50 subreddits and stored them using cache
api_url = 'https://oauth.reddit.com/subreddits/search'
headers = {'Authorization': token, 'User-Agent': 'community_rec_system by VivienXiao'}    
payload = {'q': 'COVID', 'limit': 50, 'sort': 'relevance'}


cache_file=open_cache("507finalapi.json") 
if cache_file=={}:
    dataset = requests.get(api_url, headers=headers,params=payload).json()
    save_cache("507finalapi.json",dataset)
else:
    dataset=cache_file


# Build a list of subreddits' name and a list of information
subname=[]
for i in range(len(dataset['data']['children'])):
    subname.append(dataset['data']['children'][i]['data']['display_name'])
subname=subname[1:]
del subname[30]    # some subreddits do not exist anymore, I have to delete them by hand

datalist=[]
for i in range(len(dataset['data']['children'])):
    datalist.append(dataset['data']['children'][i])
datalist=datalist[1:]
del datalist[30]



# Construct a class for the subreddits
# With the data gotten from API, I know the name, number of subscribers and other info of the subreddits
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



# However, the created time of the subreddits is not included.
# So I scrape data from the websites of the 50 subreddits, and use cache to store
# I combined the scraped data to the class 
from bs4 import BeautifulSoup

base_url = "https://www.reddit.com/r/"
headers = {'User-Agent': 'SI507final'}

CACHE_DICT = open_cache('507finalsrape.json')

for i in range(len(subname)):
    url=base_url+subname[i] 
    response=make_url_request_using_cache('507finalsrape.json',url, CACHE_DICT)
    soup = BeautifulSoup(response, 'html.parser')
    timecreated = soup.find("span", class_="_1d4NeAxWOiy0JPz7aXRI64")
    classlist[i].created_time=timecreated.text[-4:]



# Finally, build the tree and store it 
tree_cache=open_cache("507finaltree.json")

if tree_cache=={}:
# An empty tree   
    tree=\
        ("subscribers",
            ("created time", 
             ("allow video",
              ("allow images",
               ("accept followers",([],None,None),([],None,None)),
               ("accept followers",([],None,None),([],None,None))),
              ("allow images",
               ("accept followers",([],None,None),([],None,None)),
               ("accept followers",([],None,None),([],None,None)))),
             ("allow video",
              ("allow images",
               ("accept followers",([],None,None),([],None,None)),
               ("accept followers",([],None,None),([],None,None))),
              ("allow images",
               ("accept followers",([],None,None),([],None,None)),
               ("accept followers",([],None,None),([],None,None))))),
            ("created time", 
             ("allow video",
              ("allow images",
               ("accept followers",([],None,None),([],None,None)),
               ("accept followers",([],None,None),([],None,None))),
              ("allow images",
               ("accept followers",([],None,None),([],None,None)),
               ("accept followers",([],None,None),([],None,None)))), 
             ("allow video",
              ("allow images",
               ("accept followers",([],None,None),([],None,None)),
               ("accept followers",([],None,None),([],None,None))),
              ("allow images",
               ("accept followers",([],None,None),([],None,None)),
               ("accept followers",([],None,None),([],None,None))))))
        
# Append subreddits to the list in the leaves according to the attributes    
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
        if i.allow_videos==True:
            answerlist.append(1)
        else:
            answerlist.append(2) 
        if i.allow_images==True:
            answerlist.append(1)
        else:
            answerlist.append(2)
        if i.accept_followers==True:
            answerlist.append(1)
        else:
            answerlist.append(2)
        
        tree[answerlist[0]][answerlist[1]][answerlist[2]][answerlist[3]][answerlist[4]][0].append(i.display_name)
       
    fw = open("507finaltree.json","w")
    fw.write(str(tree))
    fw.close()
    
    #save_cache("507finaltree.json",tree)
else:
    tree=tree_cache















    
