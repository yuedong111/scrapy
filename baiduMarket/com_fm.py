from swiftclient.shell import *
import os
import time
import sys
import random
import hashlib
#hashlib.md5('haha').hexdigest()


#LOCAL_STORAGE_PATH = '/root/test-swift/test/'
LOCAL_STORAGE_PATH = '/tmp/'


SWIFT_CONTAINER_NUM = 100
SWIFT_AUTHURL='http://172.18.203.11:5000/v2.0/'
SWIFT_USER='android:android'
SWIFT_KEY='111111'
SWIFT_OS_OPTIONS={'region_name': None, 'tenant_id': None, 'auth_token': None, 'endpoint_type': None, 'tenant_name': None, 'service_type': None, 'object_storage_url': None}
SWIFT_PROXY_1 = '172.18.202.21:8080'
SWIFT_PROXY_2 = '172.18.202.22:8080'
SWIFT_LBS = '172.18.202.11:8000'
SWIFT_PROXY = SWIFT_PROXY_2

RETRY_NUM = 5
SWIFT_CONFIG={'android_pipeline':{'user':'android:android','key':'111111','container':None},'ra':{'user':'android:android','key':'111111','container':'ra'},'default':{'user':'android:android','key':'111111','container':'default'},'crawl_webpage':{'user':'android:android','key':'111111','container':'crawl_webpage'}}

swift_functions = {}




#-1:upload fail,-2 file open fail
def upload_file_by_swift(conn,container,obj,filepath):
    res = -1
    try:
        put_headers = {'x-object-meta-mtime': "%f" % getmtime(filepath)} 
        file_length = os.path.getsize(filepath)
    except:
        return -3
    upload_count = 0
    while (upload_count < RETRY_NUM):
        try:
            etag = conn.put_object(container, obj, open(filepath, 'rb'),content_length=file_length, headers=put_headers)
        except Exception  as err:
            if (err.http_status == 404):
                print err
                try:
                    conn.put_container(container)
                except Exception as err:
                    print err
                    upload_count +=1
                continue
            else:    
                print err
                upload_count +=1
                time.sleep(2)
                continue
        m = hashlib.md5()
        m.update(open(filepath,'rb').read())
        if (etag != m.hexdigest()):
            upload_count += 1
            time.sleep(2)
            continue
        res = file_length
        break 
    return res

#-1:download fail,-2 faile not found,-3 file write fail
def download_file_by_swift(conn,container,obj,filepath):
    res = -1
    download_count = 0
    while(download_count < RETRY_NUM):
        try:
            headers, body = conn.get_object(container, obj, resp_chunk_size=65536)
        except Exception as e:
            if (e.http_status == 404):
                print e
                return -2
            else:
                print "download_apk_by_swift err,",e
                download_count += 1
                time.sleep(2)
        try:
            fp = open(filepath,"w+")
            file_len = 0
            for chunk in body:
                fp.write(chunk)
                file_len+=len(chunk)
            fp.close()
        except Exception as e:
            print e
            return -3
        if (file_len == int(headers['content-length'])):
            res=file_len
            break
        else:
            print "download_apk_by_swift err,file_len not match"
            download_count += 1
            time.sleep(2)
            continue
    return res


def delete_file_by_swift(conn,container,obj):
    res = -1
    delete_count = 0
    while(delete_count < RETRY_NUM):
        try:
             #conn.delete_object(container, obj, query_string=query_string)
             conn.delete_object(container, obj)
             res = 0
             break
        except Exception as e:
            if (e.http_status == 404):
                print e
                return -2
            else:
                print "delete_file_by_swift err,",e
                delete_count += 1
                time.sleep(2)
    return res

def stat_file_by_swift(conn,container,obj): 
    try:
        file_info = conn.head_object(container, obj)
        return file_info
    except Exception as e:
        if (e.http_status == 404):
            print e
            #file not exist
            return -2
        else:
            print e
            #swift err
            return -1

#argv[0] is upload file filepath in local file system
#argv[1] is upload filename in swift compose by "md5 hash" and suffix ".xxx",ex:"9864a4.apk"
#return:0 success, other fail
def swift_android_upload(conn,config,argv):
    filepath = argv[0]
    md5_filename = argv[1]
    filehash = md5_filename.split('.')[0]
    container_name = str(int(filehash,16)%SWIFT_CONTAINER_NUM)
    res = upload_file_by_swift(conn,container_name,md5_filename,filepath)
    if(res >= 0):
        return 0
    else:
        return res


#argv[0] is upload filename in swift compose by "md5 hash" and suffix ".xxx",ex:"9864a4.apk"
#argv[1] is upload file filepath in local file system
#return:0 success, other fail
def swift_android_download(conn,config,argv):
    md5_filename = argv[0]
    filepath = argv[1]
    filehash = md5_filename.split('.')[0]
    container_name = str(int(filehash,16)%SWIFT_CONTAINER_NUM)
    res = download_file_by_swift(conn,container_name,md5_filename,filepath)
    if (res >=0):
        return 0
    else:
        return res

#argv[0] is upload filename in swift compose by "md5 hash" and suffix ".xxx",ex:"9864a4.apk"
#return:0 success, other fail
def swift_android_delete(conn,config,argv):
    md5_filename = argv[0]
    filehash = md5_filename.split('.')[0]
    container_name = str(int(filehash,16)%SWIFT_CONTAINER_NUM)
    res = delete_file_by_swift(conn,container_name,md5_filename)
    if (res >=0):
        return 0
    else:
        return res

def swift_android_stat(conn,config,argv):
    md5_filename = argv[0]
    filehash = md5_filename.split('.')[0]
    container_name = str(int(filehash,16)%SWIFT_CONTAINER_NUM)
    file_info = stat_file_by_swift(conn,container_name,md5_filename)
    return file_info

#argv[0] is upload file filepath in local file system
#argv[1] is upload filename in swift 
#return:0 success, other fail
def swift_ra_upload(conn,config,argv):
    filepath = argv[0]
    filename = argv[1]
    container_name = config['container'] 
    res = upload_file_by_swift(conn,container_name,filename,filepath)
    print(filepath,filename,container_name)
    print("swift_ra_upload %s"%(res))
    if(res >= 0):
        return 0
    else:
        return res

#argv[0] is upload filename in swift 
#argv[1] is upload file filepath in local file system
#return:0 success, other fail
def swift_ra_download(conn,config,argv):
    filename = argv[0]
    filepath = argv[1]
    container_name = config['container'] 
    res = download_file_by_swift(conn,container_name,filename,filepath)
    if (res >=0):
        return 0
    else:
        return res


#argv[0] is upload filename in swift
#return:0 success, other fail
def swift_ra_delete(conn,config,argv):
    filename = argv[0]
    container_name = config['container'] 
    res = delete_file_by_swift(conn,container_name,filename)
    if (res >=0):
        return 0
    else:
        return res

#get status of filename
#argv[0] is filename
#return:-1 file not exist,-2 swift err
#return a list of fileinfo
def swift_ra_stat(conn,config,argv):
    filename = argv[0]
    container_name = config['container']
    file_info = stat_file_by_swift(conn,container_name,filename)
    return file_info

#argv[0] is upload file filepath in local file system
#argv[1] is upload filename in swift 
#return:0 success, other fail
def swift_default_upload(conn,config,argv):
    filepath = argv[0]
    filename = argv[1]
    container_name = config['container'] 
    res = upload_file_by_swift(conn,container_name,filename,filepath)
    if(res >= 0):
        return 0
    else:
        return res

#argv[0] is upload filename in swift 
#argv[1] is upload file filepath in local file system
#return:0 success, other fail
def swift_default_download(conn,config,argv):
    filename = argv[0]
    filepath = argv[1]
    container_name = config['container'] 
    res = download_file_by_swift(conn,container_name,filename,filepath)
    if (res >=0):
        return 0
    else:
        return res

#argv[0] is upload filename in swift
#return:0 success, other fail
def swift_default_delete(conn,config,argv):
    filename = argv[0]
    container_name = config['container'] 
    res = delete_file_by_swift(conn,container_name,filename)
    if (res >=0):
        return 0
    else:
        return res

#get status of filename
#argv[0] is filename
#return:-1 file not exist,-2 swift err
#return a list of fileinfo
def swift_default_stat(conn,config,argv):
    filename = argv[0]
    container_name = config['container']
    file_info = stat_file_by_swift(conn,container_name,filename)
    return file_info


def swift_crawl_webpage_upload(conn,config,argv):
    filepath = argv[0]
    md5_filename = argv[1]
    #filehash = argv[1]
    #filehash = md5_filename.split('.')[0]
    #container_name = str(int(filehash,16)%SWIFT_CONTAINER_NUM)
    container_name = config['container']
    res = upload_file_by_swift(conn,container_name,md5_filename,filepath)
    if(res >= 0):
        return 0
    else:
        return res


def swift_crawl_webpage_download(conn,config,argv):
    filename = argv[0]
    filepath = argv[1]
    container_name = config['container'] 
    res = download_file_by_swift(conn,container_name,filename,filepath)
    if (res >=0):
        return 0
    else:
        return res

def swift_crawl_webpage_delete(conn,config,argv):
    filename = argv[0]
    container_name = config['container'] 
    res = delete_file_by_swift(conn,container_name,filename)
    if (res >=0):
        return 0
    else:
        return res

def swift_crawl_webpage_stat(conn,config,argv):
    filename = argv[0]
    container_name = config['container']
    file_info = stat_file_by_swift(conn,container_name,filename)
    return file_info



swift_functions['android_pipeline'] = {'upload':swift_android_upload,'download':swift_android_download,'delete':swift_android_delete,'stat':swift_android_stat}
swift_functions['ra'] = {'upload':swift_ra_upload,'download':swift_ra_download,'delete':swift_ra_delete,'stat':swift_ra_stat}
swift_functions['default'] = {'upload':swift_default_upload,'download':swift_default_download,'delete':swift_default_delete,'stat':swift_default_stat}
swift_functions['crawl_webpage'] = {'upload':swift_crawl_webpage_upload,'download':swift_crawl_webpage_download,'delete':swift_crawl_webpage_delete,'stat':swift_crawl_webpage_stat}





# storage_type: "android_pipeline","varas-ra"
#for "android_pipeline": 
#op.download(app_name,app_path):download app
#app_name is the md5name of app,like FFFFF.apk, app_path is the path for app to save in local file system
#op.upload(app_path,app_name):upload app
#op.stat(app_name):get app info
class Swift_Op():
    def __init__(self,storage_type):
        self.swift_conn = Connection(authurl=SWIFT_AUTHURL,user=SWIFT_CONFIG[storage_type]['user'],key=SWIFT_CONFIG[storage_type]['key'],retries=5,auth_version='2',os_options=SWIFT_OS_OPTIONS,snet=False,cacert=None,insecure=False,ssl_compression=True)
        try:
            self.function = swift_functions[storage_type]
            self.config = SWIFT_CONFIG[storage_type]
        except Exception as e:
            print e
            self.function = swift_functions['default']
            self.config = SWIFT_CONFIG['default']
        #print(self.function)

    def upload(self,*argv):
        return self.function['upload'](self.swift_conn,self.config,argv)

    def download(self,*argv):
        #print("argv is ",argv)
        #print self.function
        #print(argv[1:])
        return self.function['download'](self.swift_conn,self.config,argv)

    def delete(self,*argv):
        #print self.function
        #print(argv[1:])
        return self.function['delete'](self.swift_conn,self.config,argv)

    def file_status(self,*argv):
        return self.function['stat'](self.swift_conn,self.config,argv)
        

class com_fm(Swift_Op):
    pass

if __name__ == '__main__':
    test_conn = Connection(authurl=SWIFT_AUTHURL,user="admin:admin",key="admin_pass",retries=5,auth_version='2',os_options=SWIFT_OS_OPTIONS,snet=False,cacert=None,insecure=False,ssl_compression=True)
    #op = Swift_Op("android_pipeline")
    op = com_fm("android_pipeline")
    filepath="/run/shm/ttt"
    #res = op.download("012004e96f714b49b2cd27ecf941a470.apk")
    res = op.download("012004e96f714b49b2cd27ecf941a470.apk",filepath)
    #res = op.upload("/run/shm/ttt.apk")
    put_headers = {'x-object-meta-mtime': "%f" % getmtime(filepath)}
    ttt = test_conn.put_object("test", "ttt.apk", open(filepath, 'rb'),content_length=os.path.getsize(filepath), headers=put_headers)
    if (ttt=="012004e96f714b49b2cd27ecf941a470"):
        print("success upload")
    print(res)
    print(ttt)
