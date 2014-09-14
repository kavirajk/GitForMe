import requests
import time # for sleep
from db_model import *

def keep_fetching_commits(userid,token):

    r_names=[]
    all_commits=[]
    time_t=None

    repo_url="https://api.github.com/user/repos"
    header={'Authorization':"token "+token}

    repos=requests.get(repo_url,headers=header)

    for repo in repos.json():
        r_names.append(repo['name'])

    ## Testing pupose only ##

    r_names=['speakup']


    commit_url="https://api.github.com/repos/"+userid

    time_t=get_latest_time()

    for r_name in r_names:
        if time_t!=None:
            r_url=commit_url+"/"+r_name+"/commits?since="+time_t.isoformat()
        else:
            r_url=commit_url+"/"+r_name+"/commits"
            
        commits=requests.get(r_url,headers=header)

        if commits.ok == False:
            continue
            
        commits=commits.json()

        for commit in commits:
            all_commits.append(commit)

            
        if all_commits != []:
            put_commits(all_commits,userid)

def fetch_commits():
    auths=get_auths()

    for (userid,token) in auths:
        keep_fetching_commits(userid,token)
    
