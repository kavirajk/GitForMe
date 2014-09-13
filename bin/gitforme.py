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

    def POST(self):
        url="https://api.github.com/user/repos"
        userid=web.input().userid
        password=web.input().password

        print userid,password

        # generate token

        url="https://api.github.com/authorizations"
        auth=(userid,password)

        data={"scopes":["repos"]}

#        response=requests.post(url,data=json.dumps(data),auth=auth)

#    token=response['token']

        print token
                
        token=get_token(userid)
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
