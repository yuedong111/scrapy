#!/usr/bin/python
# -*- coding: UTF-8 -*-

from scrapy.exceptions import DropItem
from scrapy import signals
from scrapy import log
from scrapy.xlib.pydispatch import dispatcher
import MySQLdb

#try:
#    from hashlib import md5
#except:
#    from md5 import md5
import hashlib
from md5 import md5

import subprocess
import time
import os
import gzip,urllib
from com_fm import *
import tool

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def safe_remove(path):
    try:
        os.remove(path)
    except Exception, e:
        e = str(e)
        print 'safe_remove except: ' + e

def str_md5(s):
    return  hashlib.sha1(s).hexdigest()

def sumfile(fobj):
    m = md5()
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()


def file_md5(filename):
    try:
       f = open(filename, 'rb')
    except:
       print 'open file fail'
       return ""
    if (len(f.read()) == 0):
        f.close()
        return ""
    f.seek(0)
    md5 = sumfile(f)
    f.close()
    return md5


def is_zipfile(fname):
    """ check file type is zip, return 1 is true """
    cmd = "/usr/bin/file " + fname
    pfd = os.popen(cmd)
    pcontent = pfd.read()
    pfd.close()
    txt = len(pcontent.split('Zip archive data'))
    if (txt > 1):
        return 1
    else:
        return 0


def getImgType(img_url):
    try:
        imgtype = img_url.split(".")[-1]
        if (imgtype in ['jpg', 'png', 'gif', 'bmp', 'jpeg']):
            imgtype = "." + imgtype
            return imgtype
        else:
            return ""
    except:
        return ""


def wget_file(download_url, path):
    cmd = "wget -q '" + download_url + "' -O " + path
    os.system(cmd)
    if (os.path.exists(path)):
        filemd5 = file_md5(path)
        return filemd5
    else:
        return ""


DW_TIMEOUT = 3600
def wget_file_with(download_url, path, referer_url, conn):
    cmd = "wget -q '"  + download_url + "' -O " + path + " --referer='" + referer_url + "'"
    p = subprocess.Popen(cmd, shell = True)
    duration = 0
    sh_ret = -1

    while (duration <= DW_TIMEOUT):
        if (p.poll() is not None):
            # finished
            print '> download finished'
            sh_ret = p.returncode
            break
        try:
            conn.ping()
        except Exception, (error, strerror):
            print 'ping except: %s' %s (strerror)
            if (errno == 2006): # mysql gone away
                print 'ERROR: MySQL server gone away, exit'                                
                # to ccy: reconnect db               

        print '> downloading: time cost ' + str(duration)
        time.sleep(5)
        duration = duration+5

    if (duration > DW_TIMEOUT):
        if (p.poll() is None):
            os.system("kill -9 " + str(p.pid))
        safe_remove(path)
        return ""

    if (os.path.exists(path)):
        filemd5 = file_md5(path)
        return filemd5
    else:
        return ""


class BaidumarketPipeline(object):

    _conn = None
    op = None
    wp = None

    def __init__(self):
        self._conn = None
        self.op = com_fm("android_pipeline")
        self.wp = com_fm("crawl_webpage")
        dispatcher.connect(self.init_db, signals.engine_started)
        dispatcher.connect(self.fini_db, signals.engine_stopped)

    def process_item(self, item, spider):

        if (item is None):
            return item

        _id = self.db_get_id(item['app_name'], item['app_version'], item['app_market'], item['last_update_date'])
        print '> select _id = ' + str(_id)
        if (_id != -1):
            # app exsit in db
            print u'> wait 5s <- (已存数据库) - -！'.encode('utf-8')
            time.sleep(5)
        else:
            # insert a new app
            app_name = item['app_name']
#            app_md5 = 
            app_keywords = item['app_keywords']
            app_url = item['app_url']
            app_icon_url = item['app_icon_url']
            icon_content_path = 'chenyi_say_None'
            app_size = item['app_size']
            app_version = item['app_version']
            download_times = item['download_times']
            download_url = item['download_url']
            app_author = item['app_author']
            os_version = item['os_version']
#            apk_path 
            
            app_description = item['app_description']
            app_description = tool.stzy(app_description)
            
            last_update_date = item['last_update_date']
            app_class = item['app_class']
            app_market = item['app_market']
            market_site = item['market_site']
            user_rate = item['user_rate']
            comments_num = item['comments_num']
#            webpage_path

            print '> ', app_name.encode('utf-8')

            # app_md5 = & apk_path = 
            # download apk and calc its md5
            app_local_path = str_md5(download_url)
            app_md5 = wget_file_with(item['download_url'], app_local_path, item['app_url'], self._conn)
            """
            if is_zipfile(app_local_path) == 0:
                data = urllib.urlopen(item['download_url']).read()
                safe_remove(app_local_path)
                fapk = file(app_local_path, "wb")
                fapk.write(data)
                f.close()
                app_md5 = file_md5(app_local_path)
            """
    
            if (app_md5 == "" or is_zipfile(app_local_path) == 0):
                log.msg("app download fail: %s" % (app_url))
                print 'app download fail: %s' % (app_url)
                safe_remove(app_local_path)
                print '\n'
                raise DropItem("app download fail: %s" % (app_url))

            # insert it to swift
            test_conn = Connection(authurl=SWIFT_AUTHURL,user="admin:admin",key="admin_pass",retries=5,auth_version='2',os_options=SWIFT_OS_OPTIONS,snet=False,cacert=None,insecure=False,ssl_compression=True)
            #op = com_fm("android_pipeline")
            apk_path = app_md5 + '.apk'
            res = self.op.upload(app_local_path, apk_path)
            safe_remove(app_local_path)
            
            # icon_content_path =
            # download icon, calc its md5, insert icon into swift
            icon_local_path = str_md5(app_icon_url)
            icon_type = getImgType(app_icon_url)
            icon_md5 = wget_file(app_icon_url, icon_local_path)
            if (icon_md5 == ""):
                log.msg("icon download fail: %s" % (app_icon_url))
                print 'icon download fail: %s' % (app_icon_url)
            else:
                icon_content_path = icon_md5 + icon_type
                res = self.op.upload(icon_local_path, icon_content_path)
            safe_remove(icon_local_path)

            # webpage_path = 
            # download webpage, calc its md5, insert webpage into swift
            webpage_path = 'chenyi_say_None'
            web_suf = os.path.splitext(app_url)[1]
            save_path = '/home/tmp.gz'
            fd = urllib.urlopen(app_url)
            content = fd.read()
            g = gzip.open(save_path,'wb')
            g.write(content)
            g.close()
            fd.close()
            webpage_md5 = file_md5(save_path)
            if len(webpage_md5) > 0:
                webpage_path = webpage_md5 + web_suf
                #wp = com_fm("crawl_webpage")
                res = self.wp.upload(save_path,webpage_path)
                if res == 0:
                    print 'webpage upload success: %s' % (app_url)
                else:
                    log.msg("webpage upload fail: %s" % (app_url))
                    print 'webpage upload fail: %s' % (app_url)
            else:
                log.msg("webpage_md5 calculate fail: %s" % (app_url))
                print 'webpage_md5 calculate fail: %s' % (app_url)
            """
            webpage_local_path = str_md5(app_url)
            webpage_md5 = wget_file(app_url, webpage_local_path)
            if (webpage_md5 == ""):
                log.msg("webpage download fail: %s" % (app_url))
                print 'webpage download fial: %s' % (app_url)
            else:
                webpage_path = webpage_md5 + '.html'
                res = op.upload(webpage_local_path, webpage_path)
            safe_remove(webpage_local_path)  
            """

            """
            # deal download_times =
            if (download_times.find(u'亿') != -1):
                download_times = str(int(float(download_times[:-1]) * 100000000))
            if (download_times.find(u'万') != -1) and (download_times.find(u'千万') == -1) and (download_times.find(u'百万') == -1) :
                download_times = str(int(float(download_times[:-1]) * 10000))
            if (download_times.find(u'千万') != -1):
                download_times = str(int(float(download_times[:-2]) * 10000000))
            if (download_times.find(u'百万') != -1):
                download_times = str(int(float(download_times[:-2]) * 1000000))
            """

            # insert date into db
            sql = 'insert into android_market_download (app_name, apk_md5, app_keywords, app_url, app_icon_url, icon_content_path, app_size, app_version, download_times, download_url, app_author, os_version, apk_path, app_description, last_update_date, app_class, app_market, market_site, user_rate, comments_num, webpage_path) values (' + '"' + app_name + '", "' + app_md5 + '", "' + app_keywords + '", "' + app_url + '", "' + app_icon_url + '", "' + icon_content_path + '", "' + app_size + '", "' + app_version + '", "' + download_times + '", "' + download_url + '", "' + app_author + '", "' + os_version + '", "' + apk_path + '", "' + app_description + '", "' + last_update_date + '", "' + app_class + '", "' + app_market + '", "' + market_site + '", ' + user_rate + ', ' + comments_num + ', "' + webpage_path + '"' + ')'
            print sql.encode('utf-8')

            self.keep_connect_db()

            try:
                cur = self._conn.cursor()
                cur.execute(sql)
                self._conn.commit()
                cur.close()
                print 'finish an item: ' + app_name
            except Exception, e:
                log.msg('insert into db except: ' + str(e))
                print 'insert into db except: ' + str(e)
                if (cur is not None):
                    cur.close()

        print '\n'

        return item


    def init_db(self):
        try:
            print '> start connect'
            self._conn = MySQLdb.connect("172.18.100.15", "market_crawl", "market_crawl", "varas_softwares")
            self._conn.set_character_set('utf8')
            self._conn.ping(True)
            print '> connect success'
            return True
        except Exception, e:
            e = str(e)
            self._conn = None
            print '> connect fail'
            print '> except: ' + e
            return False

    def fini_db(self):
        if (self._conn is not None):
            self._conn.commit()
            self._conn.close()
            self._conn = None
            print '> connect close'
        else:
            print '> connect is None'

    def keep_connect_db(self):
        try:
            self._conn.ping()
            print '> connect keep :-)'
        except Exception, (error, strerror):
            print '> reconnect db :-X'
            while (self.init_db() == False):
                print '> try connect db again'


    def db_get_id(self, app_name, app_version, app_market, last_update_date):
        sql = 'select id from android_market_download where app_name = "' + app_name + '" and app_version = "' + app_version + '" and app_market = "' + app_market + '" and last_update_date like "' + last_update_date + '%"'

        self.keep_connect_db()

        try:
            cur = self._conn.cursor()
            cur.execute(sql)
            row = cur.fetchone()
            print row
            if (row is not None):
                _id = row[0]
            else:
                _id = -1
            cur.close()
        except Exception, e:
            e = str(e)
            log.msg('select db fail: ' + e)
            print 'select db fail: ' + e
            if (cur is not None):
                cur.close()
        return _id
