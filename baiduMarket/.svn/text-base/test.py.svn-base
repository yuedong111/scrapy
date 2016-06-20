
from com_fm import *
import gzip

fd = open(url, "r")
content = fd.read()
fnew = gzip.GzipFile(mode="wb", fileobj=content)
fd.close()

zipfilemd5 = fnew.file_md5()

# insert it to swift
test_conn = Connection(authurl=SWIFT_AUTHURL,user="admin:admin",key="admin_pass",retries=5,auth_version='2',os_options=SWIFT_OS_OPTIONS,snet=False,cacert=None,insecure=False,ssl_compression=True)
op = com_fm("crawl_webpage")
apk_path = app_md5 + '.html'
res = op.upload(app_local_path, apk_path)
safe_remove(app_local_path)
 
