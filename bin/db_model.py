import web
import requests

db=web.database(dbn='mysql',db='gitforme',user='root')

def get_token(userid):
    rows=db.select('users')

    for row in rows:
        return row.token

def put_commits(commits):
    for commit in commits:
        db.insert('commits',sha=commit['sha'],
                  userid=commit['commit']['committer']['email'],
                  repo=str(commit['commit']['url']),
                  message=commit['commit']['message'],
                  time=commit['commit']['committer']['date'])
#        print commit['sha']


def get_commits():
    rows=db.select('commits')
    return rows

def get_latest_time():
    rows=db.select('commits',order='time DESC')
    for row in rows:
        return row.time


def put_token(userid,token):
    db.insert('users',userid=userid,token=token)
    
