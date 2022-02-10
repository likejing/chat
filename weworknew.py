# -*- coding: utf-8 -*-
from ctypes import *
import os
import json
import time
import traceback
import requests
import base64
import random
import win32gui
import win32con
import socket
import oss2
import uuid


version_num=321
C_ID = 0
wxloaderInstance = 0
root_json = {}
json_path = "./root.json"
images_path = "./images"
if os.path.isfile(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        root_json = json.load(f)
else:
    print("root.json文件丢失,10秒后退出")
    time.sleep(10)
    exit()

if not os.path.exists(images_path):
    print("图片目录不存在，已创建")
    os.makedirs(images_path)

root_url = "http://controlapi.xxx.xxx/"

img_root_url = "http://m-img.xxx.xxx/"

im_server_url = "http://im-serve.xxx.xxx/"

blg_hook_url = ""

add_hook_url = ""

shutdown_hook_url = ""

chat_url = root_url+"phpapi/"

task_url = root_url+'miniblg/api/task/getSendQueue'

update_task_url = root_url+'miniblg/api/task/updateCorpCustomer'

update_status_url = root_url+'miniblg/api/task/updateSendTask'

update_customer_url = root_url+"miniblg/api/customer/updateCustomer"

update_customer_status_url = root_url+"miniblg/api/customer/updateCustomerStatus"


newblg_url=root_url

client_list = {}    #key  userid  value client_id

userid_list={}      #key  client_id  value userid

user_info_list={}   #key  user_id  value user_info

add_num={}  #key user_id value add_num

customer_count={} #key user_id value  count
if "filter_list" in root_json:
    filter_list = root_json['filter_list']
else:
    filter_list = []

if "username" in root_json:
    username = root_json['username']
else:
    username = ''

if "chat_username" in root_json:
    chat_username = root_json['chat_username']
else:
    chat_username = ''

if "device_name" in root_json:
    device_name = root_json['device_name']
else:
    device_name = ''

if "py_version" in root_json:
    py_version = root_json['py_version']
else:
    py_version = 101


    

global_chat_id = ""

verifytext = '你好'

send_status = 1

ip = ""

presenter_id={}

is_open=True

timestamp=0#time.time()

login_timestamp=time.time()

model=1  #默认是1  自动连接模式

def get_mac_address():
    node = uuid.getnode()

    mac = uuid.UUID(int = node).hex[-12:]
    return mac

mac= get_mac_address()

def stable_get(url):
    try:
        req = requests.get(url, timeout=10)
        return req
    except requests.exceptions.RequestException as e:
        time.sleep(10)
        print(e)
        return False

def upload_qrcode2ali():
    
    return True


def gettoken(corpid, corpsecret):
    
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (
        corpid, corpsecret)

    res = requests.get(url)

    time.sleep(1)

    if(res.status_code == 200):
        ret = json.loads(res.text).get('errcode')
        if(ret == 0):
            access_token = json.loads(res.text).get('access_token')
            return access_token
        else:
            print(json.loads(res.text).get('errmsg'))
            return False
    else:
        print(res.status_code)
        return False

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


if get_host_ip():
    ip = get_host_ip()


def get_handle_id(title):
    '''
    根据标题找句柄
    :param title: 标题
    :return:返回句柄所对应的ID
    '''
    jh = []
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t != "":
            if title in t:
                jh.append(h)

    if len(jh) == 0:
        pass
    else:
        return jh


def send_text(hook_url, content):

    headers = {"Content-Type": "application/json"}

    # text 类型消息
    text_msg = {
        "msgtype": "text",
        "text": {
            "content": content.encode("utf-8").decode("latin1"),
            "mentioned_list": ["@all"],
            # "mentioned_mobile_list":["@all"]
        }
    }

    res = requests.post(url=hook_url, data=json.dumps(
        text_msg, ensure_ascii=False), headers=headers)
    res.encoding = "utf-8"
    if res.status_code == 200:
        print(res.text)


def send_markdown(hook_url, content):

    headers = {"Content-Type": "application/json"}

    # text 类型消息
    text_msg = {
        "msgtype": "markdown",
        "markdown": {
            "content": content.encode("utf-8").decode("latin1"),
            # "mentioned_list":["@all"],
            # "mentioned_mobile_list":["@all"]
        }
    }

    res = requests.post(url=hook_url, data=json.dumps(
        text_msg, ensure_ascii=False), headers=headers)
    res.encoding = "utf-8"
    if res.status_code == 200:
        print(res.text)

# 判断用户是否存在，并获取userid
def get_chat_userid(phone_num):

    data = {"phone_num": phone_num}
    url = chat_url+"get_chat_userid.php"

    res = requests.post(url, data=data)

    time.sleep(1)

    if(res.status_code == 200):
        code = json.loads(res.text).get('code')
        if(code == 200):
            user_id = json.loads(res.text).get('userid')
            return user_id
        else:
            print(json.loads(res.text).get('msg'))
            return False
    else:
        print('网络请求出错')
        return False

# 判断用户是否存在，并获取userid（mobile字段）
def get_userid(chat_id):

    data = {"chat_id": chat_id}
    url = chat_url+"get_userid.php"

    res = requests.post(url, data=data)

    time.sleep(1)

    if(res.status_code == 200):
        code = json.loads(res.text).get('code')
        if(code == 200):
            user_id = json.loads(res.text).get('userid')
            related_from = json.loads(res.text).get('related_from')
            # print(user_id)
            return {"user_id": user_id, "related_from": related_from}
        else:
            print(json.loads(res.text).get('msg'))
            return False
    else:
        print('网络请求出错')
        return False

#通过corpId获取企业的contact_secret
def getContactSecret(corpShortName):

    url = chat_url+"getSecret.php?corpShortName=%s" % corpShortName

    res = requests.get(url)

    time.sleep(1)

    if(res.status_code == 200):
        code = json.loads(res.text).get('code')
        if(code == 200):
            secrets = json.loads(res.text).get('secrets')
            return secrets
        else:
            print(json.loads(res.text).get('msg'))
            return False
    else:
        print('网络请求出错')
        return False

def update_user(access_token, userid, name,media_id):
    
    url = "https://qyapi.weixin.qq.com/cgi-bin/user/update?access_token=%s" % access_token

    data_arr = {"userid": userid, "name": name,"alias":name,"avatar_mediaid":media_id}

    res = requests.post(url, data=json.dumps(data_arr), headers={
                        'Content-Type': 'application/json'})

    time.sleep(1)

    if(res.status_code == 200):
        ret = json.loads(res.text).get('errcode')
        if(ret == 0):
            print(userid+'修改完成')
            return True
        else:
            print(userid+json.loads(res.text).get('errmsg'))
            return False
    else:
        return False

# 添加好友
def add_friend(chat_id, phone_num):

    data = {"chat_id": chat_id, "phone_num": phone_num}
    url = chat_url+"add_friend.php"

    res = requests.post(url, data=data)

    time.sleep(1)

    if(res.status_code == 200):
        code = json.loads(res.text).get('code')
        if(code == 200):
            print("添加好友成功")
            return True
        else:
            print(json.loads(res.text).get('msg'))
            return False
    else:
        print('网络请求出错')
        return False

#删除好友或者拉黑
def delete_friend(chat_id, phone_num):

    data = {"chat_id": chat_id, "phone_num": phone_num}
    url = chat_url+"delete_friend.php"

    res = requests.post(url, data=data)

    time.sleep(1)

    if(res.status_code == 200):
        code = json.loads(res.text).get('code')
        if(code == 200):
            print("删除好友成功")
            return True
        else:
            print(json.loads(res.text).get('msg'))
            return False
    else:
        print('网络请求出错')
        return False

# 创建用户
def new_user(phone_num, nickname, related_from):

    data = {
        'nickname': nickname,
        'mobile': phone_num,
        'password': 'admin123',
        "related_from": related_from,
        'sms_code': send_verify_code(phone_num),
        'platform': 'web',
    }
    url = im_server_url+"api/v1/auth/register"

    res = requests.post(url, data=data)

    time.sleep(1)

    if(res.status_code == 200):
        code = json.loads(res.text).get('code')
        if(code == 200):
            print(json.loads(res.text).get('message'))
            return True
        else:
            print(json.loads(res.text).get('message'))
            return False
    else:
        print('网络请求出错')
        return False

# 创建用户
def send_verify_code(phone_num):

    data = {
        'mobile': phone_num,
        'type': 'user_register',
    }

    url = im_server_url+"api/v1/auth/send-verify-code"

    res = requests.post(url, data=data)

    time.sleep(1)

    if(res.status_code == 200):
        code = json.loads(res.text).get('code')
        if(code == 200):
            sms_code = json.loads(res.text).get('data').get('sms_code')
            print(sms_code)
            return sms_code
        else:
            print(json.loads(res.text).get('message'))
    else:
        print('网络请求出错')

# 登录用户
def login(phone_num):

    url = im_server_url+"api/v1/auth/login"
    data = {
        'mobile': phone_num,
        'password': 'admin123',
        'platform': 'web',
    }

    res = requests.post(url, data=data)

    time.sleep(1)

    if(res.status_code == 200):
        code = json.loads(res.text).get('code')
        if(code == 200):
            ac = json.loads(res.text).get('data').get('authorize').get(
                'type')+" "+json.loads(res.text).get('data').get('authorize').get('access_token')
            print(ac)
            return ac
        else:
            print(json.loads(res.text).get('message'))
    else:
        print('网络请求出错')

# 发送消息
def post_message(receiver_id, text, Authorization):

    url = im_server_url+"api/v1/talk/message/text"
    data = {
        'talk_type': 1,
        'receiver_id': receiver_id,
        'text': text,
    }
    headers = {
        'Authorization': Authorization,
    }

    res = requests.post(url, data=data, headers=headers)

    time.sleep(1)

    if(res.status_code == 200):
        code = json.loads(res.text).get('code')
        if(code == 200):
            return True
        else:
            print(json.loads(res.text).get('message'))
    else:
        print('网络请求出错')

# 发送图片消息
def post_img_message(receiver_id, img_path, Authorization):

    url = im_server_url+"api/v1/talk/message/image"
    data = {
        'talk_type': 1,
        'receiver_id': receiver_id,
    }
    headers = {
        'Authorization': Authorization,
    }

    img_files = {"image": (img_path.split(
        "/")[-1], open(img_path, 'rb'), "image/%s" % img_path.split(".")[-1])}

    res = requests.post(url, data=data, headers=headers, files=img_files)

    time.sleep(1)

    if(res.status_code == 200):
        code = json.loads(res.text).get('code')
        if(code == 200):
            return True
        else:
            print(json.loads(res.text).get('message'))
    else:
        print('网络请求出错')

# 获取未读消息  测试版
def get_unread_message(user_id):
    global login_timestamp
    global wxloaderInstance

    url = newblg_url+"/phpapi/chat/get_unread_test.php?user_id=%s&device_name=%s&user_sum=%s&ip=%s&user_name=%s&chat_user_name=%s&mac=%s&version_num=%s" % (
        user_id, device_name, len(client_list), ip, username,chat_username,mac,version_num)

    res = stable_get(url) 

    if res and res.status_code == 200:
        code = json.loads(res.text).get('code')
        if(code == 200):
            if(json.loads(res.text).get('add_user')==1 and time.time()-login_timestamp>60):
                login_timestamp=time.time()
                win_handles = get_handle_id("企业微信")
                if win_handles:
                    for win_handle in win_handles:
                        win32gui.PostMessage(win_handle, win32con.WM_CLOSE, 0, 0)
                        time.sleep(1)
                wxloaderInstance.openWechatClient()
            return json.loads(res.text).get('data')
        else:
            print(json.loads(res.text).get('msg'))
    else:
        print('网络请求出错')

# 获取聊天系统中的客户列表
def get_cus_list(user_id):

    url = newblg_url+"/phpapi/chat/get_cus_list.php?user_id=%s"  % user_id

    res = stable_get(url) 

    if res and res.status_code == 200:
        code = json.loads(res.text).get('code')
        if(code == 200):
            return json.loads(res.text)
        else:
            
            print(json.loads(res.text).get('msg'))
            return 0
    else:
        print('网络请求出错')
        return 0

# 标为已读
def read_message(message_id):

    url = root_url+"records/update/"+str(message_id)

    res = requests.post(url)

    time.sleep(1)

    if(res.status_code == 200):
        code = json.loads(res.text).get('code')
        if(code == 0):
            print("read")
        else:
            print(json.loads(res.text).get('message'))
    else:
        print('网络请求出错')

# 获取发送任务
def get_task(username, imei):
    #imei是发送账号的userid
    url = task_url+"?userName=%s&imei=%s&device_name=%s&user_sum=%s&ip=%s&chat_user_name=%s&mac=%s&avatar=%s&corpId=%s&mobile=%s&account=%s&name=%s" % (username,imei,device_name,len(client_list), ip,
    chat_username,mac,user_info_list[imei]["avator_url"],user_info_list[imei]["corp_id"],user_info_list[imei]["mobile"],user_info_list[imei]["acctid"], base64.b64decode(user_info_list[imei]["name"]).decode())

    res = stable_get(url)

    if res and res.status_code == 200:
        ret = json.loads(res.text).get('ret')  
        if(ret == "ok"):
            data_arr = json.loads(res.text).get('data_arr')
            return data_arr
        else:
            print("暂无发送任务")
            return False
    else:
        print('网络请求出错')
        return False

# 更新发送记录+
def update_send_id(id):
    url = update_task_url+"?idList="+str(id)

    res = stable_get(url)

    if res and res.status_code == 200:
        ret = json.loads(res.text).get('ret')
        if(ret == "ok"):
            print("发送状态更新成功")
            return True
        else:
            print(json.loads(res.text).get('msg'))
            return False
    else:
        print('网络请求出错')
        return False

# 更新发送任务状态
def update_send_status(corpName, corpTodaySend, imei, status):
    url = update_status_url+"?userName="+username+"&corpName="+corpName + \
        "&status="+str(status)+"&corpTodaySend=" + \
        str(corpTodaySend)+"&imei=" + imei

    res = stable_get(url)

    if res and res.status_code == 200:
        ret = json.loads(res.text).get('ret')
        if(ret == "ok"):
            print("发送状态更新成功")
            return True
        else:
            print(json.loads(res.text).get('msg'))
            return False
    else:
        print('网络请求出错')
        return False

# 更新微信信息及添加状态
def update_customer_data(mobile, sex, nick_name, avatar, user_id, customer_status):
    url = update_customer_url+"?mobile=%s&sex=%s&nick_name=%s&avatar=%s&user_id=%s&customer_status=%s" % (
        mobile, sex, nick_name.decode(), avatar, user_id, customer_status)

    res = stable_get(url)

    if res and res.status_code == 200:
        ret = json.loads(res.text).get('ret')
        if(ret == "ok"):
            print("客户状态信息更新成功")
            return True
        else:
            print(json.loads(res.text).get('msg'))
            return False
    else:
        print('网络请求出错')
        return False

# 更新添加状态
def update_customer_status(user_id,customer_status):
    url = update_customer_status_url + "?mobile=%s&customer_status=%s" % (user_id, customer_status)

    res = stable_get(url)

    if res and res.status_code == 200:
        ret = json.loads(res.text).get('ret')
        if(ret == "ok"):
            print("添加状态信息更新成功")
            return True
        else:
            print(json.loads(res.text).get('msg'))
            return False
    else:
        print('网络请求出错')
        return False


# 下载图片
def download_img(img_url):
    r = requests.get(img_url, stream=True)
    # print(r.status_code) # 返回状态码
    if r.status_code == 200:
        open(os.path.abspath('.')+"\\images\\"+img_url.split("/")
             [-1], 'wb').write(r.content)  # 将内容写入图片
        print("done")
    del r


# 更新登录二维码
def set_login_qrcode(img_url):

    data = {"username": username, "login_qrcode": img_url}
    url = chat_url+"/qrcode/set_login_qrcode.php"

    res = requests.post(url, data=data)

    time.sleep(1)

    if(res.status_code == 200):
        code = json.loads(res.text).get('code')
        if(code == 200):
            print("上传登录二维码成功")
            return True
        else:
            print(json.loads(res.text).get('msg'))
            return False
    else:
        print('网络请求出错')
        return False



def c_string(data):
    return c_char_p(data.encode('utf-8'))

# 连接回调函数
@WINFUNCTYPE(None, c_ulong)
def connect_callback(client_id):
    print(u'新的客户端连接: ')
    global C_ID
    global is_open
    global wxloaderInstance
    C_ID = client_id
    if is_open:
        #关闭自动更新
        is_open=False
        time.sleep(3)
        data = {
            'is_open': 0,
        }
        wxloaderInstance.sendMessage(client_id, 7001, data)
    print(client_id)

# 接收事件回调函数
@WINFUNCTYPE(None, c_ulong, c_char_p, c_ulong)
def recv_callback(client_id, data, length):
    global send_status
    global model
    global add_num
    global timestamp
    global wxloaderInstance
    jsonData = json.loads(data)
    if jsonData['type'] == 500:
        return
    if jsonData['type'] == 15000 and jsonData['data']['msgtype'] == 2 and jsonData['data']['conversation_id'][0:1] == "R":
        return 
    if jsonData['type'] == 15000 and jsonData['data']['msgtype'] == 80 and jsonData['data']['conversation_id'][0:1] == "R":
        return 
    print('[on_recv] client_id: {0}, message:{1}'.format(
        client_id, json.loads(data)))
    if jsonData['type'] == 13008 and jsonData['error'] == 30000:
        # 更新状态
        update_customer_status(jsonData['data']['sender_id'],"未发送")
    if jsonData['type'] == 10000 and model:#新客户端接入  发送获取信息命令
       
        wxloaderInstance.sendMessage(client_id, 2000, '')
        print("获取信息")
    if jsonData['type'] == 11000:
        print("获取到登录二维码")
        print(jsonData['data']['base64_encode_path'])
        img_dir = base64.b64decode(jsonData['data']['base64_encode_path']).decode('gbk', 'ignore')
        img_url = upload_qrcode2ali(img_dir)
        print(img_url.split("?")[0])
        set_login_qrcode(img_url.split("?")[0])
    if jsonData['type'] == 18003:#接收到图片
        Authorization = login(jsonData['data']['user_key'])
        if Authorization:  # 登录成功 //发给我自己
            post_img_message(
                global_chat_id, jsonData['data']['file_save_path'], Authorization)
        print("发送图片消息成功")
    if jsonData['type'] == 11001:#登录成功通知
        client_list[jsonData['data']['user_id']] = client_id
        wxloaderInstance.sendMessage(client_id, 2000, '')
    if jsonData['type'] == 12000 and jsonData['data']['user_id']:
        client_list[jsonData['data']['user_id']] = client_id
        userid_list[client_id]=jsonData['data']['user_id']
        print(base64.b64decode(jsonData['data']['corp_short_name']).decode())
        user_info_list[jsonData['data']['user_id']]=jsonData['data']
        add_num[userid_list[client_id]]=0
        customer_count[userid_list[client_id]]=0
    if jsonData['type'] == 12501 and jsonData['data']['total_count']!=customer_count[userid_list[client_id]] :
        if client_id not in presenter_id:
            for onedata in jsonData['data']['contact_list']:
                if onedata["user_id"][0:3]=='788':
                    presenter_id[client_id]=onedata["user_id"]
                    break
        cus_list=get_cus_list(userid_list[client_id])
        receiver_id=userid_list[client_id]
        if cus_list and cus_list["cus_count"] != jsonData['data']['total_count']:
            customer_count[userid_list[client_id]]=jsonData['data']['total_count']
            timestamp=time.time()
            cus_id_list=[one["mobile"] for one in cus_list["cus_list"]]
            for contact in jsonData['data']['contact_list']:
                if contact['user_id'] in cus_id_list or onedata["user_id"][0:3]=='168':
                    continue
                newsender_id=contact['user_id']+"_"+receiver_id
                chat_user_id = get_chat_userid(newsender_id)
                if not chat_user_id:
                    # 先创建用户
                    if contact['nickname']:
                        new_user_success = new_user(newsender_id, base64.b64decode(
                            contact['nickname']), userid_list[client_id])
                    else:
                        new_user_success = new_user(newsender_id, base64.b64decode(
                            contact['name']), userid_list[client_id])
                    if new_user_success:
                        # 添加好友
                        add_friend(int(global_chat_id), newsender_id)
                        # 更新状态
                        update_customer_status(contact['user_id'],"已添加")
                        # 发送机器人
                        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        send_text(add_hook_url, username +
                                "账号新增客户，请及时查看\n添加时间：%s" % now_time)
                    # 登录用户发送消息
                    Authorization = login(newsender_id)
                    if Authorization:  # 登录成功 //发给我自己
                        post_message(global_chat_id, "我通过了你的联系人验证请求，现在我们可以开始聊天了", Authorization)
                        print("发送成功")    
                else:
                    print("客户信息已保存")
    if jsonData['type'] == 13000 and jsonData['error'] == 30000 and jsonData['data']["error_desc"] == "添加好友过于频繁，请稍后再重试": 
        print("账号发送频繁")
        send_status = 3
        return
    if jsonData['type'] == 13000 and jsonData['error'] == 30000 and jsonData['data']["error_desc"] == "向微信好友发消息功能已被限制使用": 
        print("账号被限制，自动退出")
        send_status = 4
        wxloaderInstance.sendMessage(client_id, 2, data)
        return
    if jsonData['type'] == 13000 and jsonData['error'] == 0:
        # 头像  微信名  性别  手机号
        user_id = jsonData['data']['wx_user_info']['user_id']

        mobile = jsonData['data']['request_key']
        
        avatar = ''
        sex = 0
        nickname = base64.b64decode(jsonData['data']['wx_user_info']['name'])
        if user_id == 0:
            update_customer_data(mobile, sex, nickname, avatar, user_id, "不存在")
        nick = nickname.decode()
        if user_id and verifytext != "data_clearing":
            if filter_list:
                for filter_key in filter_list:
                    if filter_key in nick:
                        print("昵称包含过滤词")
                        update_customer_data(mobile, sex, nickname, avatar, user_id, "不存在")
                        return
            if client_id not in presenter_id:
                print("id不在通讯录里")
                send_status=6
              
                return 
            data = {
                "user_id": user_id,
                "verify_text": verifytext,
                "conversation_id":"",
                "presenter_id": presenter_id[client_id],
                "request_key" : mobile,
            }
            wxloaderInstance.sendMessage(client_id, 3008, data)
            update_customer_data(mobile, sex, nickname, avatar, user_id, "已发送")
            add_num[userid_list[client_id]]+=1
            print("%s发送成功次数:%s" % (userid_list[client_id],add_num[userid_list[client_id]]))
    if jsonData['type'] == 15000 and jsonData['data']['msgtype'] == 1011 and (jsonData['data']['system_msg_descrption'] == "wework://notfriend" or jsonData['data']['system_msg_descrption'] == "消息已发出，但被对方拒收了"):
        customer_id = jsonData['data']['conversation_id'][19:]
        receiver_id = jsonData['data']['conversation_id'][2:18]
        if global_chat_id and customer_id:
            print(customer_id)
            if delete_friend(int(global_chat_id),customer_id+"_"+receiver_id):
                print("删除好友成功")
            else:
                print("删除好友失败")
    
    if jsonData['type'] == 15000 and jsonData['data']['conversation_id'][0:1] != "R" and ( jsonData['data']['msgtype'] == 101 or jsonData['data']['msgtype'] == 2):
        if str(jsonData['data']['sender_id'])[0:4]=="1688":
            return
        receiver_id=jsonData['data']['conversation_id'][2:18]
        newsender_id=str(jsonData['data']['sender_id'])+"_"+receiver_id
        chat_user_id = get_chat_userid(newsender_id)
        if not chat_user_id:
            # 先创建用户
            new_user_success = new_user(newsender_id, base64.b64decode(
                jsonData['data']['sender_nickname']), jsonData['data']['conversation_id'][2:18])
            if new_user_success:
                # 添加好友
                add_friend(int(global_chat_id), newsender_id)
                # 更新状态
                update_customer_status(jsonData['data']['sender_id'],"已添加")
                # 发送机器人
                now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                send_text(add_hook_url, username +
                          "账号新增客户，请及时查看\n添加时间：%s" % now_time)
        # 登录用户发送消息
        Authorization = login(newsender_id)
        if Authorization:  # 登录成功 //发给我自己
            if jsonData['data']['msgtype'] == 101:
                data = {
                    "file_aeskey" : jsonData['data']['file_aeskey'],
                    "file_http_url" : jsonData['data']['file_middle_http_url'],
                    "file_save_path" : os.path.abspath('.')+"\\images\\"+str(jsonData['data']['sender_id'])+".png",
                    "file_size" : jsonData['data']['file_middle_size'],
                    "file_v1_data" : jsonData['data']['file_v1_data'],
                    "request_key" : newsender_id
                }
                wxloaderInstance.sendMessage(client_id, 8003, data)
                # post_img_message(
                #     global_chat_id, jsonData['data']['path'], Authorization)
            elif jsonData['data']['msgtype'] == 0 or jsonData['data']['msgtype'] == 2:
                post_message(global_chat_id, base64.b64decode(
                    jsonData['data']['content']), Authorization)
            print("发送成功")

# 断开连接回调函数
@WINFUNCTYPE(None, c_ulong)
def close_callback(client_id):
    C_ID = 0
    print(u'已断开')
    print(client_id)
    # if cli_id in  client_list.values():

    # 删除对应列表


class WeCom:
    # 加载器
    WXLOADER = None
    dll_path = ''

    def __init__(self, dll_path):
        self.dll_path = dll_path

        # 控制库地址
        loader_path = os.path.join(self.dll_path, 'WXCommand_wxwork.dll') 
        loader_path = os.path.realpath(loader_path)
        # print(loader_path)

        # 注入库地址
        inject_path = os.path.join(
            self.dll_path, 'VXWorkElf_3.1.7.3005_Release.vmp.dll')   
        inject_path = os.path.realpath(inject_path)
        self.WXLOADER = WinDLL(loader_path)
        self.WXLOADER.WXCmdInitDllPath(c_string(inject_path))
        out = create_string_buffer(20)
        self.WXLOADER.WXCmdGetLocalWechatVersion(out, 20)
        print(u'版本号:' + out.value.decode('utf-8'))

        # 初始化socket连接
        self.WXLOADER.WXCmdInitSocket(
            connect_callback, recv_callback, close_callback)

        # 运行
        self.WXLOADER.WXCmdRun()
        # self.WXLOADER.WXCmdStop()

    # 打开一个企业微信，此时会自动注入 VXWorkElf_v3.1.1.3002_release.dll 到企业微信
    def openWechatClient(self):
        print(u'open wechat:')
        self.WXLOADER.WXCmdOpenWechat()

    # 发送消息
    def sendMessage(self, client_id, message_type, params):
        # print(u'send message:')
        send_data = {'type': message_type, 'data': params}
        return self.WXLOADER.WXCmdSend(client_id, c_string(json.dumps(send_data, ensure_ascii=False)))
        # return self.WXLOADER.WXCmdSend(client_id, c_string(json.dumps(send_data)))
        # return self.WXLOADER.WXCmdSend(client_id, json.dumps(send_data, ensure_ascii=False, encoding='utf-8'))


# 上传图片素材


def upload_img(access_token, png_name):

    url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image" % access_token

    file = []

    if os.path.exists(png_name):
        file.append(('file', (png_name, open(png_name, 'rb'), 'image/jpg')))
    else:
        print('文件不存在')
        return False

    res = requests.post(url, files=file)

    time.sleep(1)

    if(res.status_code == 200):
        ret = json.loads(res.text).get('errcode')
        if(ret == 0):
            media_id = json.loads(res.text).get('media_id')
            return media_id
        else:
            return False
    else:
        return False

# 获取未读消息并处理
def unreaddata():
    unread_data = get_unread_message(global_chat_id)
    if unread_data:
        # print("获取到未读消息")
        for one_data in unread_data:
            cus_Id = one_data["mobile"][0:16]  # 发送员工的userid mobile存储
            # 会出现重复客户导致出错的情况   #和这个客户联系的员工的id
            inter_Id = one_data["related_from"]
            if inter_Id in client_list:
                print("已发送未读消息")
                cli_id = client_list[inter_Id]
              
                if one_data["msg_type"] == "2":
                    if one_data["save_dir"] != "":
                        img_url = img_root_url + \
                            one_data["save_dir"]
                        download_img(img_url)
                        wxloaderInstance.sendMessage(cli_id, 5003, {
                            "conversation_id": "S:"+inter_Id+"_"+cus_Id,
                            "path": os.path.abspath('.')+"\\images\\"+one_data["save_dir"].split("/")[-1],
                            "request_key" : "S:"+inter_Id+"_"+cus_Id
                        })
                    else:
                        print("图片消息获取出错")
                        pass
                else:
                    wxloaderInstance.sendMessage(cli_id, 5000, {
                        "conversation_id": "S:"+inter_Id+"_"+cus_Id,
                        "content": one_data['content'],
                        "request_key" : "S:"+inter_Id+"_"+cus_Id
                    })
                read_message(one_data["id"])

# 发送好友申请，或者清洗数据
def send_add():
    global verifytext
    global send_status
    global timestamp
    global wxloaderInstance
    # global username
    for imei in list(client_list.keys()):
        try:
            if imei:
                if  time.time()-timestamp>60 or client_list[imei] not in presenter_id:
                    timestamp=time.time()
                    wxloaderInstance.sendMessage(client_list[imei], 2501, '')
                    time.sleep(1)
                send_data = get_task(username, imei)
                if send_data:
                    print("获取到发送任务")
                    verifytext = send_data['sendTemplate']+str(random.randint(0,9))
                    sendTask = send_data['sendTask']
                    send_times = 0
                    send_status = 2
                    if os.path.exists("./headicon"):
                        headicon_list=os.listdir("./headicon")
                        name_list=[headfile[0:headfile.find(".")] for  headfile in headicon_list]
                        if(base64.b64decode(user_info_list[imei]["name"]).decode() not in name_list):
                            secrets=getContactSecret(base64.b64decode(user_info_list[imei]['corp_short_name']).decode())
                            if secrets:
                                thisname=name_list[random.randint(0,len(name_list))]
                                print(secrets)
                                access_token=gettoken(secrets["back_corp_id"],secrets["contact_secret"])
                                if access_token:
                                    meadia_id=upload_img(access_token,"./headicon/"+thisname+".jpg")
                                    if not meadia_id:
                                        meadia_id=""
                                    update_user(access_token,user_info_list[imei]["acctid"],thisname,meadia_id)
                    for one_data in sendTask:
                        if send_status != 2:  # 发送状态异常了
                            break
                        data={
                            "mobile" : one_data["phoneNum"],
                            "request_key" : one_data["phoneNum"]
                        }
                        wxloaderInstance.sendMessage(client_list[imei], 3000, data)
                        send_times += 1
                        # update_send_id(one_data["id"])
                        time.sleep(random.randint(5, 9))
                        win_handles = get_handle_id("封禁提示")
                        if win_handles:
                            for win_handle in win_handles:
                                win32gui.PostMessage(
                                    win_handle, win32con.WM_CLOSE, 0, 0)
                            print("当前账号发送频繁")
                        if random.randint(0, 9) % 3 == 0:
                            unreaddata()
                    update_send_status(
                        sendTask[0]["corpName"], send_times, imei, send_status)
                    if send_status == 2:
                        status_asset = "发送完成"
                    elif send_status == 3:
                        status_asset = "发送频繁"
                    elif send_status == 4:
                        status_asset = "账号异常"
                    else:
                        status_asset = send_status
                    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    send_markdown(blg_hook_url, "发送账号：%s\n发送机器名：%s\n当前机器帐号总数量：%s\n发送账号名：%s\n已发送数量：%s\n发送状态：%s\n发送完成时间：%s\n机器ip：%s\n" % (
                        username, device_name, len(client_list), imei, send_times, status_asset, now_time,ip))
                    time.sleep(30)
                time.sleep(3)
        except:
            pass
    

if __name__ == "__main__":
    updated=False
    try:
        win_handles = get_handle_id("企业微信")
        if win_handles:
            for win_handle in win_handles:
                win32gui.PostMessage(win_handle, win32con.WM_CLOSE, 0, 0)
                time.sleep(1)
        wxloaderInstance = WeCom('./')
        # 通过用户id打开企微进程。以这种方式打开企微进程可以自动登录
        if username:
            if not updated:#并且没有更新
                cmd = input(
                    "已缓存发送账号:"+username+",输入1回车使用缓存账号，若要更换账号，请直接输入账号并回车：")
                if cmd != "1":
                    username = cmd
                    root_json["username"] = username
                    with open(json_path, "w", encoding="utf-8") as wf:
                        json.dump(root_json, wf, ensure_ascii=False)
        else:
            username = input("请输入发送账号：")
            root_json["username"] = username
            with open(json_path, "w", encoding="utf-8") as wf:
                json.dump(root_json, wf, ensure_ascii=False)
        # 通过用户id打开企微进程。以这种方式打开企微进程可以自动登录
        if chat_username:
            if not updated:#并且没有更新
                cmd = input(
                    "已缓存聊天账号:"+chat_username+",输入1回车使用缓存账号，若要更换账号，请直接输入账号并回车：")
                if cmd != "1":
                    chat_username = cmd
                    root_json["chat_username"] = chat_username
                    with open(json_path, "w", encoding="utf-8") as wf:
                        json.dump(root_json, wf, ensure_ascii=False)
        else:
            chat_username = input("请输入聊天账号：")
            root_json["chat_username"] = chat_username
            with open(json_path, "w", encoding="utf-8") as wf:
                json.dump(root_json, wf, ensure_ascii=False)
        global_chat_id = get_chat_userid(chat_username)
        if global_chat_id:
            print("聊天账号id:%s" % global_chat_id)
        else:
            print("该账号未注册聊天系统账号，请先使用该手机号注册聊天系统账号,10秒后退出")
            time.sleep(10)
            exit()
        if device_name:
            if not updated:#并且没有更新
                cmd = input(
                    "已缓存机器名："+device_name+",输入1回车使用缓存机器名，若要修改机器名，请直接输入机器名并回车：")
                if cmd != "1":
                    device_name = cmd
                    root_json["device_name"] = device_name
                    with open(json_path, "w", encoding="utf-8") as wf:
                        json.dump(root_json, wf, ensure_ascii=False)
        else:
            device_name = input("请输入机器名：")
            root_json["device_name"] = device_name
            with open(json_path, "w", encoding="utf-8") as wf:
                json.dump(root_json, wf, ensure_ascii=False)
        console_title="版本号："+str(version_num)+";发送账号："+username+";聊天账号："+chat_username+";机器名："+device_name+";本机mac："+mac
        os.system("title %s" % console_title)
        if not updated:#并且没有更新
            multi = int(input("请输入需要多开的企业微信窗口数量,加载绑定已运行企业微信，直接输入0回车即可："))
            if multi !=0:
                model=0
            for mul in range(0, multi):
                wxloaderInstance.openWechatClient()
                time.sleep(1)
        while True:
            # 读取是否有未读消息，然后发送出去
            unreaddata()
            time.sleep(3)
            rad=random.randint(0, 10)
            if  rad % 4 == 0:
                send_add()
                time.sleep(3)
    except Exception as err:
        # print(err)
        # 发送机器人
        send_markdown(shutdown_hook_url, device_name +
                      "出现报错，请及时查看机器是否运行正常，报错日志查看errorlog.txt")
        traceback.print_exc(file=open('./errorlog.txt', 'a'))
        # with open("./errorlog.txt", "a", encoding="utf-8") as wf:
        #     wf.write(err)
        time.sleep(3)
    finally:
        time.sleep(3)
