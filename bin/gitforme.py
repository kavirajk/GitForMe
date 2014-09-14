import web
import thread
from db_model import *
import requests
import json
from auth_helpers import *
from fetch_helpers import *
from multiprocessing import Pool # for fetching git commits in background 



urls=(
    '/','Index',
    '/Login','Login',
    '/Fetch','Fetch'
)


app=web.application(urls,globals())
render=web.template.render("templates")

class Index:
    def GET(self):
        return render.login()


class Login:

    def __init__(self):
        self.userid=None
        self.token=None

    def GET(self):
        
        code=web.input().code
        client_id='483f8af623f62e704356'
        client_secret='4e0fbf477a02c2a05f37cfb39ac73572af4a3563'

        self.token=get_oauth_token(client_id,client_secret,code)
        self.userid=get_userid(self.token)


        if userid_exists(self.userid)!=True:
            put_token(self.userid,self.token)

        keep_fetching_commits(self.userid,self.token)

        return render.view(self.userid)

class Fetch:

    def __init__(self):
        self.userid=None

    def POST(self):
        self.userid=web.input().userid
        if self.userid == None:
            return "UnAuthorized"
            
        commits=get_commits(self.userid)
        return render.fetch(commits)

def keep_fetching():
    while True:
        fetch_commits()
        time.sleep(60)

if __name__=='__main__':
    thread.start_new_thread(app.run,())
    keep_fetching()
    
