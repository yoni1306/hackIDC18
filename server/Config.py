#Elastic authentication params:
ELASTIC_SERVER_URL = 'http://elastic01-prod:9200/'
ELASTIC_MAX_VALUES_SIZE = 100000000
TIME_DIFF = 22*60*60*1000
TIME_DELTA = 7


# Insert log file path :
LOG_FILE_PATH = r'c:\DtkServerSide.txt'

# Config
CONFIG_FORMAT = '%(asctime)s - %(levelname)s %(module)s : %(message)s'
CONFIG_DATEFMT = "%Y-%m-%d %H:%M:%S"
DEFAULT_PORT = 80

#Devices
DEVICES = {'PC': 1, 'MOBILE': 2, 'MobPc': 3}


class Messages:
    ERROR_MESSAGE = '%s, %s-request. Msg: %s\r\n%s'
    REQUEST_INFO = 'server got request from: %s'
    DISMISS_PARAMS = 'Dismiss params. %s\r\n%s'
    CLIENT_GOT_QUERIES = 'User: %s, got queries: %s'
    CLIENT_GOT_RESPONSE = 'User: %s, got response: %s'


class Requests:
    GET = 'get'
    POST = 'post'


class Indexes:
    CLIENT_COOKIES = 'client_cookies'
    COOKIES = 'cookies'
    CONTENTS = 'contents'
    REQUESTS = 'requests'
    LOGS = 'logs'
    ERRORS = 'errors'
    DBO2CONTENT = 'dbo2content'
    DBO = 'dbo'
    BLACKLIST = 'blacklist'


class Queries:
    SELECT_QUERY = '''SELECT %s From %s '''


class Columns:
    ID = 'id'
    DBO_ID = 'dbo_id'



class JsonKeys:
    ID = 'id'
    RANGE_ID = 'range_id'


class Conditions:
    BASE_CONDITION = '{field} = {value}'
    DBO_ID_AND_DEVICE_ID_CONDITION = 'dbo_id = {dbo_id} and device_id = {device_id}'
    CONTENT_ID_AND_DEVICE_ID_CONDITION = 'content_id = {content_id} and device_id = {device_id}'


class Handlers:
    BASE_HANDLER = 'BaseHandler'
    COOKIES_HANDLER = 'CookiesHandler'
    CREATE_PROFILE_HANDLER = 'CreateProfileHandler'
    ID_HANDLER = 'IDHandler'
    RANGE_BLACKLIST_HANDLER = 'RangeBlacklistHandler'
    RANGE_HANDLER = 'RangeHandler'
    SET_COUNTER_HANDLER = 'SetCounterHandler'


