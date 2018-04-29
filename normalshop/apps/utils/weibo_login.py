# _*_ coding:utf-8 _*_
__author__ = 'zjty'
__date__ = '2018/4/29 下午8:29'

App_Key = 434902534
App_Secret = "95a4c84709563168374d80afed407f43"


def get_auto_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_uri = "http://127.0.0.1:8000/complete/weibo/"
    auth_url = weibo_auth_url+"?client_id={client_id}&redirect_uri={re_url}".format(client_id=App_Key, re_url=redirect_uri)
    print(auth_url)


def get_access_token(code="6c294a8ed19360f7b40a09fe67221c93"):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    import requests
    re_dict = requests.post(access_token_url, data={
        "client_id": App_Key,
        "client_secret": App_Secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/complete/weibo/"
    })
    pass

if __name__ == '__main__':
    get_auto_url()
    get_access_token(code="6c294a8ed19360f7b40a09fe67221c93")
