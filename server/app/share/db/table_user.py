#coding:utf8

from firefly.dbentrust.dbpool import dbpool
from MySQLdb.cursors import DictCursor

def getUserInfoByName(username):
    '''
    get user record by user name
    '''
    sql = "SELECT * FROM user WHERE username = '%s'" % username
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass = DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def newUser(username, password, deviceId):
    '''
    insert a new user record into table, return True if success, or false if failed
    '''
    sql = "INSERT INTO user(`username`, `password`, `device_id`) VALUES ('%s','%s', '%s')" % (username, password, deviceId)
    conn = dbpool.connection()
    cursor = conn.cursor()
    count = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    if(count >= 1):
        return True
    return False

def getUserInfosByDeviceId(deviceId):
    '''
    get user info list by a device id
    @param deviceId: device id
    @return: a list of all matched user info
    '''
    sql = "SELECT * FROM user WHERE device_id = '%s'" % deviceId
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass = DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result