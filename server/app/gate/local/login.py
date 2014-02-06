#coding:utf8

from app.gate.model.usermanager import UserManager
from app.gate.model.user import User
from app.share.db import table_user
from app.share.constants import *
from app.share.locale.i18n import *

def loginToServer(dynamicId, username, password, deviceId):
    '''
    perform login operation, by username and password,
    if user name doesn't exist, new user will be added
    @param dynamicId: connection id
    @param username: user name
    @param password: password
    @param deviceId: device id
    @return: dict, and keys can be:
        errno: the error code, defined in constants.py, E_OK means no error
        errmsg: the error message, only exists when errno is not E_OK
        data: extra info of user, only exists when errno is E_OK, you can add anything you want
    '''

    # user name can't be empty
    if not username:
        return { KEY_ERRNO : E_EMPTY_USERNAME, KEY_ERRMSG : L('Empty username') }

    # device id can't be empty
    if not deviceId:
        return { KEY_ERRNO : E_NOT_MOBILE, KEY_ERRMSG : L('Not a mobile device') }

    # password can't be empty
    if not password:
        return { KEY_ERRNO : E_EMPTY_PASSWORD, KEY_ERRMSG : L('Empty password') }

    # get user record from db
    userInfo = table_user.getUserInfoByName(username)

    # check user existence, if not exist, create new
    if not userInfo:
        table_user.newUser(username, password, deviceId)

    # if user is already logged in, update dynamic id
    oldUser = UserManager().getUserByName(username)
    if oldUser:
        oldUser.dynamicId = dynamicId
        return { KEY_ERRNO : E_OK, KEY_DATA : oldUser.getLoginExtraData() }

    # if user is not logged in, create user model
    user = User(username, password, dynamicId)

    # zero id means error
    if user.id == 0:
        return { KEY_ERRNO : E_DB_ERROR, KEY_ERRMSG : L('Database error') }

    # if user is blocked
    if user.blocked:
        return { KEY_ERRNO : E_BLOCKED, KEY_ERRMSG : L('User is blocked') }

    # if password is error
    if userInfo and userInfo[KEY_PASSWORD] != password:
        return { KEY_ERRNO : E_WRONG_PASSWORD, KEY_ERRMSG : L('Wrong password') }

    # add user model and success
    UserManager().addUser(user)
    return { KEY_ERRNO : E_OK, KEY_DATA : user.getLoginExtraData() }

def queryBind(dynamicId, deviceId):
    '''
    query whether a deviceId has associated user, if yes, user name list will be returned
    @param dynamicId: dynamic id of client connection
    @param deviceId: device id of client device
    @return: dict, errno will always be E_OK, and data contains user name array
    '''

    # query user by device id
    users = table_user.getUserInfosByDeviceId(deviceId)

    # get user name list
    usernames = [u[KEY_USERNAME] for u in users]

    # return
    return { KEY_ERRNO : E_OK, KEY_DATA : { KEY_USERNAMES : usernames } }