####################################################
# IMPORTS (LOCAL) ##################################
####################################################

from blog.models import BlogPost, User
from blog import db

####################################################
# FUNCTION TO GET THE NUMBER OF DIFFERENT CHARACTERS
####################################################

def num_char_different(str1, str2):
    if (str1 == str2):
        return 0

    if (not str1):
        return len(str2)
    elif (not str2):
        return len(str1)
    
    if (str1[0] == str2[0]):
        return num_char_different(str1[1:], str2[1:])
    
    str1_rem_val = num_char_different(str1[1:], str2)
    str2_rem_val = num_char_different(str1, str2[1:])
    both_rem_val = num_char_different(str1[1:], str2[1:])

    return 1 + min(str1_rem_val, str2_rem_val, both_rem_val)

####################################################
# FUNCTION TO GET THE SIMILARITY ###################
####################################################

def similarity(str1, str2):
    diff = num_char_different(str1.lower(), str2.lower())
    length = max(len(str1), len(str2))

    return (1 - (diff / length))

####################################################
# FUNCTION TO GET THE MATCHING BLOGS ###############
####################################################

def get_matches_blogs(string):
    res = []
    id_title = db.engine.execute(
        'select id, title\
         from BlogPost'
    )
    for identifier, title in id_title:
        sim = similarity(string, title)
        if (sim > 0.65):
            res.append((identifier, sim))
    
    res.sort(reverse=True, key=lambda x: x[1])
    return BlogPost.query.filter(BlogPost.id.in_([val[0] for val in res]))

####################################################
# FUNCTION TO GET THE MATCHING USERS ###############
####################################################

def get_matches_users(string):
    res = []
    id_username = db.engine.execute(
        'select id, username\
         from users'
    )
    for identifier, username in id_username:
        sim = similarity(string, username)
        if (sim > 0.65):
            res.append((identifier, sim))
    
    res.sort(reverse=True, key=lambda x: x[1])

    return User.query.filter(User.id.in_([val[0] for val in res]))

####################################################
# FUNCTION TO GET THE MATCHING BLOGS + USERS #######
####################################################

def search(string):
    users = get_matches_users(string)[:10]
    blogs = get_matches_blogs(string)[:10]
    
    return users, blogs