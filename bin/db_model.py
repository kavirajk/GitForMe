import web
import requests

db=web.database(dbn='mysql',db='gitforme',user='root')

def get_token(userid):
    rows=db.select('users')

    for row in rows:
        return row.token

def put_commits(commits,userid):
    for commit in commits:
        db.insert('commits',sha=commit['sha'],
                  user=commit['commit']['committer']['email'],
                  repo=str(commit['commit']['url']),
                  message=commit['commit']['message'],
                  time=commit['commit']['committer']['date'],
                  userid=userid)
#        print commit['sha']

def get_commits(userid):
    rows=db.select('commits',order="time DESC",where="userid=$userid",vars=locals())
    return rows

def get_latest_time():
    rows=db.select('commits',order='time DESC')
    for row in rows:
        return row.time


def put_token(userid,token):
    db.insert('users',userid=userid,token=token)
    
def userid_exists(userid):
    rows=db.select('users',where="userid=$userid",vars=locals())

    if len(list(rows))==0:
        return False
    return True

    
def get_auths():
    rows=db.select('users')
    auths=[]
    for row in rows:
        auths.append((row.userid,row.token))

    return auths
