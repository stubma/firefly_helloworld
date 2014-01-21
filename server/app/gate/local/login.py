#coding:utf8

from app.gate.model.usermanager import UserManager
from app.gate.model.user import User
from app.share.db import table_user

def loginToServer(dynamicId, username, password):
    '''
    perform login operation, by username and password,
    if user name doesn't exist, new user will be added
    '''

    # get user record from db
    userInfo = table_user.getUserInfoByName(username)

    # check user existence, if not exist, create new
    if not userInfo and username and password:
        table_user.newUser(username, password)

    # if user is already logged in, update dynamic id
    oldUser = UserManager().getUserByName(username)
    if oldUser:
        oldUser.setDynamicID(dynamicId)
        return { 'result' : True, 'message' : 'login_success', 'data' : oldUser.getLoginExtraData() }

    # if user is not logged in, create user model
    user = User(username, password, dynamicId)

    # zero id means error
    if user.id == 0:
        return { 'result' : False, 'message' : 'db_error' }

    # if user is blocked
    if user.isBlocked():
        return { 'result' : False, 'message' : 'blocked' }

    # add user model and success
    UserManager().addUser(user)
    return { 'result' : True, 'message' : 'login_success', 'data' : user.getLoginExtraData() }


