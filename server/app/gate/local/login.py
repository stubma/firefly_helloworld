#coding:utf8

from app.gate.model.usermanager import UserManager
from app.gate.model.user import User
from app.share.db import table_user
from app.share.constants import *
from app.share.locale.i18n import *

def loginToServer(dynamicId, username, password):
    '''
    perform login operation, by username and password,
    if user name doesn't exist, new user will be added

    a dict will be returned, and keys can be:
    errno: the error code, defined in constants.py, E_OK means no error
    errmsg: the error message, only exists when errno is not E_OK
    data: extra info of user, only exists when errno is E_OK, you can add anything you want
    '''

    # get user record from db
    userInfo = table_user.getUserInfoByName(username)

    # check user existence, if not exist, create new
    if not userInfo and username and password:
        table_user.newUser(username, password)

    # if user is already logged in, update dynamic id
    oldUser = UserManager().getUserByName(username)
    if oldUser:
        oldUser.dynamicId = dynamicId
        return { 'errno' : E_OK, 'data' : oldUser.getLoginExtraData() }

    # if user is not logged in, create user model
    user = User(username, password, dynamicId)

    # zero id means error
    if user.id == 0:
        return { 'errno' : E_DB_ERROR, 'errmsg' : L('Database error') }

    # if user is blocked
    if user.blocked:
        return { 'errno' : E_BLOCKED, 'errmsg' : L('User is blocked') }

    # if password is error
    if userInfo['password'] != password:
        return { 'errno' : E_WRONG_PASSWORD, 'errmsg' : L('Wrong password') }

    # add user model and success
    UserManager().addUser(user)
    return { 'errno' : E_OK, 'data' : user.getLoginExtraData() }


