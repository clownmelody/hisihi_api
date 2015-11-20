from http.client import HTTPSConnection, HTTPConnection
import os
import platform
from io import StringIO
import time
from herovii.libs.util import get_content_type_by_filename, get_resource, is_oss_host, check_bucket_valid, is_ip, \
    get_assign

__author__ = 'bliss'


class OssAPI(object):
    """fuck ali python sdk don't support python 3
    rewrite SDK to fit python 3 by leilei
    """

    DefaultContentType = 'application/octet-stream'
    __version__ = '0.4.3'
    Version = __version__
    provider = 'OSS'
    AGENT = 'aliyun-sdk-python/%s (%s/%s/%s;%s)' % (__version__,
                                                    platform.system(), platform.release(),
                                                    platform.machine(), platform.python_version())

    def __init__(self, host='oss-cn-qingdao.aliyuncs.com', access_id='', secret_access_key='',
                 port=80, is_security=False, sts_token=None):
        self.SendBufferSize = 8192
        self.RecvBufferSize = 1024*1024*10
        self.host = host
        self.port = port
        self.access_id = access_id
        self.secret_access_key = secret_access_key
        self.show_bar = False
        self.is_security = is_security
        self.retry_times = 5
        self.agent = self.AGENT
        self.debug = False
        self.timeout = 60
        self.is_oss_domain = False
        self.sts_token = sts_token

    def put_object_from_bytes(self, bucket, name, input_bytes, content_type='', headers=None, params=None):
        if not headers:
            headers = {}
        if not content_type:
            content_type = get_content_type_by_filename(object)
        if not headers.get('Content-Type') and not headers.get('content-type'):
            headers['Content-Type'] = content_type
        headers['Content-Length'] = input_bytes.tell()
        res = self.put_object_from_fp(bucket, name, input_bytes, content_type, headers, params)
        input_bytes.close()
        return res

    # def put_object_from_string(self, bucket, name, input_content, content_type='', headers=None, params=None):
    #     method = "PUT"
    #     return self._put_object_from_string(bucket, name, input_content,
    #                                                 content_type, headers, params)

    def put_object_from_string(self, bucket, object,
                               input_content, content_type, headers, params):
        if not headers:
            headers = {}
        if not content_type:
            content_type = get_content_type_by_filename(object)
        if not headers.get('Content-Type') and not headers.get('content-type'):
            headers['Content-Type'] = content_type
        headers['Content-Length'] = str(len(input_content))
        fp = StringIO(input_content)
        res = self.put_object_from_fp(bucket, object, fp, content_type, headers, params)
        fp.close()
        return res

    def put_object_from_fp(self, bucket, name, fp, content_type=DefaultContentType,
                            headers=None, params=None):

        method = 'PUT'
        return self._put_or_post_object_from_fp(method, bucket, name, fp, content_type, headers, params)

    def _put_or_post_object_from_fp(self, method, bucket, name, fp,
                                    content_type=DefaultContentType, is_bytes=True, headers=None, params=None):
        tmp_object = name
        tmp_headers = {}
        tmp_params = {}
        if headers and isinstance(headers, dict):
            tmp_headers = headers.copy()
        if params and isinstance(params, dict):
            tmp_params = params.copy()

        fp.seek(os.SEEK_SET, os.SEEK_END)
        file_size = fp.tell()
        fp.seek(os.SEEK_SET)
        conn = self._open_conn_to_put_object(method, bucket, name, file_size, content_type, headers, params)
        total_len = 0
        l = fp.read(self.SendBufferSize)
        retry_times = 0
        while len(l) > 0:
            if retry_times > 100:
                print("reach max retry times: %s" % retry_times)
                raise ValueError()
            try:
                if is_bytes:
                    conn.send(l.encode('utf-8'))
                else:
                    conn.send(l)
                retry_times = 0
            except Exception as e:
                s = e
                retry_times += 1
                continue
            total_len += len(l)
            l = fp.read(self.SendBufferSize)
        res = conn.getresponse()
        return res

    def _open_conn_to_put_object(self, method, bucket, object,
                                 filesize, content_type=DefaultContentType, headers=None, params=None):
        '''
        NOT public API
        Open a connectioon to put object

        :type bucket: string
        :param

        :type filesize: int
        :param

        :type object: string
        :param

        :type input_content: string
        :param

        :type content_type: string
        :param: the object content type that supported by HTTP

        :type headers: dict
        :param: HTTP header

        Returns:
            Initialized HTTPConnection
        '''
        if not params:
            params = {}
        if not headers:
            headers = {}
        if self.sts_token:
            headers['x-oss-security-token'] = self.sts_token
        # object = convert_utf8(object)
        resource = "/%s/" % bucket
        if not bucket:
            resource = "/"
        # resource = convert_utf8(resource)
        resource = "%s%s%s" % (resource, object, get_resource(params))

        # object = oss_quote(object)
        url = "/%s" % object
        if bucket:
            headers['Host'] = "%s.%s" % (bucket, self.host)
            if not is_oss_host(self.host, self.is_oss_domain):
                headers['Host'] = self.host
        else:
            headers['Host'] = self.host
        if is_ip(self.host):
            url = "/%s/%s" % (bucket, object)
            headers['Host'] = self.host
        # url = append_param(url, params)
        date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

        if check_bucket_valid(bucket) and not is_ip(self.host):
            conn = self.get_connection(headers['Host'])
        else:
            conn = self.get_connection()
        conn.putrequest(method, url)
        if not headers.get('Content-Type') and not headers.get('content-type'):
            headers['Content-Type'] = content_type
        headers["Content-Length"] = filesize
        headers["Date"] = date
        headers["Expect"] = "100-Continue"
        headers['User-Agent'] = self.agent
        for k in headers.keys():
            conn.putheader(str(k), str(headers[k]))
        if '' != self.secret_access_key and '' != self.access_id:
            auth = self._create_sign_for_normal_auth(method, headers, resource)
            conn.putheader("Authorization", auth)
        conn.endheaders()
        return conn

    def get_connection(self, tmp_host=None):
        host = ''
        port = 80
        if not tmp_host:
            tmp_host = self.host
        host_port_list = tmp_host.split(":")
        if len(host_port_list) == 1:
            host = host_port_list[0].strip()
        elif len(host_port_list) == 2:
            host = host_port_list[0].strip()
            port = int(host_port_list[1].strip())
        if self.is_security or port == 443:
            self.is_security = True
            return HTTPSConnection(host=host, port=443, timeout=self.timeout)
        else:
            return HTTPConnection(host=host, port=port, timeout=self.timeout)

    def _create_sign_for_normal_auth(self, method, headers=None, resource="/"):
        auth_value = "%s %s:%s" % (self.provider, self.access_id,
                                   get_assign(self.secret_access_key, method,
                                   headers, resource, None, self.debug))
        return auth_value



