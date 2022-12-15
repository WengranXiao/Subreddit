# Subreddit_Recommendation_System
This is a full-stack project for SI507 final. It is a website with a recommendation system that can recommend the most appropriate subreddits related to COVID to users. Users only have to answer three questions regarding what type of subreddits they want. 

The purpose of this project is to provide users with a convenient way to get information and news related to covid-19, vaccination, anti-convid medicine, etc. I hope this website will facilitate citizens' daily life during the pandemic.
## Guidance for using the project:
Requiered packages: flask, requests, json, time, bs4

Private keys are not committed to Github. I have uploaded the secretkey.py into Canvas.

The three large json files (one of web api, one of web scraping and one of tree) are not in Github. I uploaded them into Canvas.

## Data structure
The data structure of this project is a tree. In each level of the tree, there is a question, such as “Do you want a subreddit with more than 1000 followers?”, “Do you want a subreddit created before 2020?”, etc. The user’s answer towards the questions will lead to different branches of the tree. Finally, the tree will direct to different leaves, which presents different recommendations of subreddits.
