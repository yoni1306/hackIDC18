import os
import tornado.web
import logging
import random
import sspi
import struct
import shutil
import Config
import hashlib
import traceback
from xml.etree import ElementTree
from ElasticSearch import ESQueries
from ElasticSearch.ESMain import ESMain


class BaseHandler(tornado.web.RequestHandler, ):
    def __init__(self, application, request):
        """
        Base handler , handle with get/post requests.
        @param application: Tornado application.
        @param request: Client request.
        """
        super(BaseHandler, self).__init__(application, request)
        self.url_origin = self.request.headers['Origin']
        self.set_header('Access-Control-Allow-Origin', self.url_origin)
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.es = ESMain()
        self.s = sspi.ServerAuth('NTLM')
        self.error_occurred = False

    def get(self):
        """
        Handle get-requests.
        """
        pass

    def post(self):
        """
        Handle post-requests.
        """
        pass

    def negotiate(self):
        if 'Authorization' not in self.request.headers:
            self.s.reset()
            self.send_error(401, 1, url_origin=self.url_origin)
            return None
        else:
            a = self.request.headers['Authorization'][5:].decode('base64')
            try:
                c, b = self.s.authorize(a)
            except sspi.error:
                c, b = 0, ''
            if not c:
                try:
                    l, _, o = struct.unpack('hhh', a[36:42])
                    return a[o:o + l].decode('utf-16')
                except Exception as e:
                    logging.warning("couldn't open ntlm authentication. error: %s" % e)
            self.send_error(401, 2, b, self.url_origin)

    def check_result(self, result, msg=''):
        """
        Check if the result of ESearch is empty.
        @param result: Result of ESearch
        @param msg: Message for special cases that we want to add message to the log.
        """
        if None in result:
            self.send_error(404, url_origin=self.url_origin)
            logging.warning('Query return empty result. Msg: %s' % msg)

    def create_id(self, index):
        """
        Create unique id, and check that he doesnt already exist.
        @param index: Name of the index to check on it, if the id is already exist.
        @return: New unique id.
        """
        new_id = random.randrange(0, 2 ** 30)
        return_field = {Config.Columns.ID: Config.JsonKeys.ID}
        query = ESQueries.GET_DETAILS_PER_ID % new_id
        full_query = ESQueries.QUERY_STRUCTURE % query
        result = self.es.get_query_result_in_response_format(index, full_query, return_field)
        if None != result[0]:
            new_id = self.create_id(index)
        return int(new_id)

    def create_md5(self, content):
        hasher = hashlib.md5()
        hasher.update(content)
        return hasher.hexdigest()

    def send_to_alexandria(self, content):
        try:
            md5_command_name, md5_command_path, md5_remote_command_path = self.create_alexandria_file(content)
            shutil.move(md5_command_path, md5_remote_command_path)
            return md5_command_name

        except Exception as e:
            logging.error(Config.Messages.ERROR_MESSAGE % (Config.Handlers.BASE_HANDLER,
                                                           Config.Requests.POST,
                                                           e,
                                                           traceback.format_exc()))
            self.send_error(405, url_origin=self.url_origin)

    @staticmethod
    def convert_ip_to_integer(ip):
        """
        Change string format of ip to int format of ip.
        @param ip: String format of ip.
        @return: Int format of ip.
        """
        return reduce(lambda a, b: a << 8 | b, map(int, ip.split(".")))

    @staticmethod
    def convert_integer_ip_to_str(ip):
        """
        Change int format of ip to string format of ip.
        @param ip: Int format of ip.s
        @return: String format of ip.
        """
        return ".".join(map(lambda n: str(ip >> n & 0xFF), [24, 16, 8, 0]))

    @staticmethod
    def find_device_id(device):
        """
        Get string device type, and find the device id.
        @param device: String device type.
        @return: Device id.
        """
        for device_type, content_type_id in Config.DEVICES.items():
            if device in device_type:
                return content_type_id
        content_type_id = len(Config.DEVICES) + 1
        logging.warning('Unknown device.')
        return content_type_id

