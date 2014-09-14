import requests

def get_oauth_token(client_id,client_secret,code):
    code_url="https://github.com/login/oauth/access_token"
    
    data={'client_id':client_id,
          'client_secret':client_secret,
          'code':code
    }

    header={'Accept':'application/json'}
    token_req=requests.post(code_url,data=data,headers=header)

    return token_req.json()['access_token']

def get_userid(token):
    user_url="https://api.github.com/user"

    header={'Authorization':"token "+token}

    userid_req=requests.get(user_url,headers=header)
    
    return userid_req.json()['login']
