import web
from db_model import *
import requests
import json


urls=(
    '/','Login',
    '/Fetch','Fetch'
)


app=web.application(urls,globals())
render=web.template.render("templates")

class Login:

    def GET(self):
        return render.login()


class Fetch:

    token=None

    def GET(self):
        url="https://github.com/login/oauth/access_token"
        code=web.input().code
        data={'client_id':'483f8af623f62e704356',
              'client_secret':'4e0fbf477a02c2a05f37cfb39ac73572af4a3563',
              'code':code}
        header={'Accept':'application/json'}
        res=requests.post(url,data=data,headers=header)
        Fetch.token= res.json()['access_token']
        
        return render.view()
 
    def POST(self):
        #import pdb;pdb.set_trace()
        url="https://api.github.com/user/repos"
        # generate token
        userid=web.input().userid
        token=get_token(userid)
        if(token==None):
            put_token(userid,Fetch.token)
#        token=get_token(userid)
        
        #token=Fetch.token

        token="token "+token
        header={'Authorization':token}

        # getting the user repos using OAuth token

        repos=requests.get(url,headers=header)
        r_names=[]
        for repo in repos.json():
            r_names.append(repo['name'].encode('ascii'))

        # getting commit msg for all the repos

        c_url="https://api.github.com/repos/"+userid
        all_commits=[]

        ### Testing only ###

        r_names=['speakup']


        time=get_latest_time()

        
        for r_name in r_names:
            if time!=None:
                r_url=c_url+"/"+r_name+"/commits?since="+time.isoformat()
            else:
                r_url=c_url+"/"+r_name+"/commits"
                
            commits=requests.get(r_url,headers=header).json()
            all_commits.append(commits)

        
        #putting the commits into the db
#        return all_commits[0][0]

        put_commits(commits)


        # fetching the updated data from db and rendering it

        commits=get_commits()


        return render.fetch(commits)
        
 



if __name__=='__main__':
    app.run()

    while(True):
        web.seeother("/Fetch")
        sleep(300)
