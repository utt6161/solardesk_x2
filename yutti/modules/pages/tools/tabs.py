from collections import namedtuple
Tab = namedtuple('Tab',
    [
        'tickets',
        'firms',
        'users',
    ])
firms_tab = Tab('','active','')
users_tab = Tab('','','active')
tickets_tab = Tab('active','','')

# second layer of tabs

Request_tabs = namedtuple('Request_tabs',
    [
        'theme',
        'description',
        'username',
        'status'
    ])

theme = Request_tabs('active','','','')
description = Request_tabs('','active','','')
username = Request_tabs('','','active','')
status = Request_tabs('','','','active')


User_tabs = namedtuple('User_tabs',
    [
        'username',
        'email',
        'phone_number',
        'firm',
        'status'
    ])

login = User_tabs('active','','','','')
email = User_tabs('','active','','','')
phone_number = User_tabs('','','active','','')
firm = User_tabs('','','','active','')
verified = User_tabs('','','','','active')