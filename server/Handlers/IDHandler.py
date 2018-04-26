import Config
import logging
import traceback
import json
from ElasticSearch import ESQueries
from Handlers.BaseHandler import BaseHandler


class IDHandler(BaseHandler):
    def __init__(self, application, request):
        """
        Handle all the requests that approach to path: '/id'
        @param application: Tornado application.
        @param request: Client request
        """
        super(IDHandler, self).__init__(application, request)
        self.response = {}

    def get(self):
        """
        Handle get-requests.
        """
        try:
            logging.info(Config.Messages.REQUEST_INFO % self.request.host)
            client_user_name = self.negotiate()
            if client_user_name is not None:
                arguments = self.request.arguments

                if Config.JsonKeys.PORT in arguments:
                    self.get_dbo_id(ip_start=arguments[Config.JsonKeys.IP_START][0],
                                    ip_end=arguments[Config.JsonKeys.IP_END][0],
                                    port=arguments[Config.JsonKeys.PORT][0])
                elif Config.JsonKeys.URL_NAME in arguments:
                    self.get_content_id(url_name=arguments[Config.JsonKeys.URL_NAME][0])

                if None != self.response:
                    self.response = json.dumps(self.response)
                    logging.info(Config.Messages.CLIENT_GOT_RESPONSE % (client_user_name, self.response))
                    self.write(self.response)
                else:
                    self.send_error(404, url_origin=self.url_origin)
        except Exception as e:
            logging.error(Config.Messages.ERROR_MESSAGE % (Config.Handlers.ID_HANDLER,
                                                           Config.Requests.GET,
                                                           e,
                                                           traceback.format_exc()))

    def get_dbo_id(self, ip="0", ip_start="0", ip_end="0", port=str(Config.DEFAULT_PORT)):
        """
        Get range_id by ip/ip_start + ip_end, port.
        @param ip: Specific ip.
        @param ip_start: First ip in ip`s range.
        @param ip_end: Last ip in ip`s range.
        @param port: Specific port, the server communicate by.
        """
        return_field = {Config.Columns.ID: Config.JsonKeys.ID}

        int_ip = self.convert_ip_to_integer(ip)
        int_start_ip = self.convert_ip_to_integer(ip_start)
        int_end_ip = self.convert_ip_to_integer(ip_end)

        query = ESQueries.GET_DBO_ID % (port, int_ip, int_start_ip, int_end_ip)
        full_query = ESQueries.QUERY_STRUCTURE % query
        result = self.es.get_query_result_in_response_format(Config.Indexes.DBO, full_query, return_field)
        self.check_result(result)
        self.response = result

    def get_content_id(self, url_name=''):
        return_field = {Config.Columns.ID: Config.JsonKeys.ID}
        query = ESQueries.GET_CONTENT_ID_BY_NAME % url_name
        full_query = ESQueries.QUERY_STRUCTURE % query
        result = self.es.get_query_result_in_response_format(Config.Indexes.CONTENTS, full_query, return_field)

        self.check_result(result)
        self.response = result