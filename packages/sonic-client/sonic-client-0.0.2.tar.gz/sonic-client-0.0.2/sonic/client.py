from enum import Enum
import socket
import re


class SonicServerError(Exception):
    """Generic Sonic Server exception"""
    pass


class ChannelError(Exception):
    """Sonic Channel specific exception"""
    pass


# Commands available on all channels + START that's available on the uninitialized channel
COMMON_CMDS = [
    'START',
    'PING',
    'HELP',
    'QUIT'
]

# Channels commands
ALL_CMDS = {
    # FIXME: unintialized entry isn't needed anymore.
    'UNINITIALIZED': [
        *COMMON_CMDS,
    ],
    'ingest': [
        *COMMON_CMDS,
        # PUSH <collection> <bucket> <object> "<text>" [LANG(<locale>)]?
        'PUSH',
        'POP',     # POP <collection> <bucket> <object> "<text>"
        'COUNT',   # COUNT <collection> [<bucket> [<object>]?]?
        'FLUSHC',  # FLUSHC <collection>
        'FLUSHB',  # FLUSHB <collection> <bucket>
        'FLUSHO',  # FLUSHO <collection> <bucket> <object>
    ],
    'search': [
        *COMMON_CMDS,
        # QUERY <collection> <bucket> "<terms>" [LIMIT(<count>)]? [OFFSET(<count>)]? [LANG(<locale>)]?
        'QUERY',
        'SUGGEST',  # SUGGEST <collection> <bucket> "<word>" [LIMIT(<count>)]?

    ]

}

# snippet from asonic code.


def quote_text(text):
    """Quote text and normalize it in sonic protocol context.

    Arguments:
        text str -- text to quote/escape

    Returns:
        str -- quoted text
    """
    if text is None:
        return ""
    return '"' + text.replace('"', '\\"').replace('\r\n', ' ') + '"'


def is_error(response):
    """Check if the response is Error or not in sonic context.

    Errors start with `ERR`
    Arguments:
        response {str} -- response string

    Returns:
        [bool] -- true if response is an error.
    """
    if response.startswith('ERR '):
        return True
    return False


def raise_for_error(response):
    """Raise SonicServerError in case of error response.

    Arguments:
        response {str} -- message to check if it's error or not.

    Raises:
        SonicServerError -- 

    Returns:
        str -- the response message
    """
    if is_error(response):
        raise SonicServerError(response)
    return response


def _parse_protocol_version(text):
    """Extracts protocol version from response message

    Arguments:
        text {str} -- text that may contain protocol version info (e.g STARTED search protocol(1) buffer(20000) )

    Raises:
        ValueError -- Raised when s doesn't have protocol information

    Returns:
        str -- protocol version.
    """
    matches = re.findall("protocol\((\w+)\)", text)
    if not matches:
        raise ValueError("{} doesn't contain protocol(NUMBER)".format(text))
    return matches[0]


def _parse_buffer_size(text):
    """Extracts buffering from response message

    Arguments:
        text {str} -- text that may contain buffering info (e.g STARTED search protocol(1) buffer(20000) )

    Raises:
        ValueError -- Raised when s doesn't have buffering information

    Returns:
        str -- buffering.
    """

    matches = re.findall("buffer\((\w+)\)", text)
    if not matches:
        raise ValueError("{} doesn't contain buffer(NUMBER)".format(text))
    return matches[0]


def _get_async_response_id(text):
    """Extract async response message id. 

    Arguments:
        text {str} -- text that may contain async response id (e.g PENDING gn4RLF8M )

    Raises:
        ValueError -- [description]

    Returns:
        str -- async response id
    """
    text = text.strip()
    matches = re.findall("PENDING (\w+)", text)
    if not matches:
        raise ValueError("{} doesn't contain async response id".format(text))
    return matches[0]


# Channels names
INGEST = 'ingest'
SEARCH = 'search'
CONTROL = 'control'


class SonicClient:

    def __init__(self, host: str, port: int, password: str, channel: str):
        self.host = host
        self.port = port
        self.password = password
        self.channel = channel
        self.__socket = None
        self.__reader = None
        self.__writer = None
        self.bufsize = 0
        self.protocol = 1

    @property
    def address(self):
        return self.host, self.port

    @property
    def _socket(self):
        if self.__socket is not None:
            return self.__socket
        self.__socket = socket.create_connection(self.address)
        return self.__socket

    @property
    def _reader(self):
        if self.__reader is not None:
            return self.__reader
        self.__reader = self._socket.makefile('r')
        return self.__reader

    @property
    def _writer(self):
        if self.__writer is not None:
            return self.__writer
        self.__writer = self._socket.makefile('w')
        return self.__writer

    def connect(self):
        resp = self._reader.readline()
        if 'CONNECTED' in resp:
            self.connected = True

        resp = self._execute_command("START", self.channel, self.password)
        self.protocol = _parse_protocol_version(resp)
        self.bufsize = _parse_buffer_size(resp)

        return True

    def __enter__(self):
        self.connect()
        return self

    def _close(self):
        resources = (self.__reader, self.__writer, self.__socket)
        for rc in resources:
            if rc is not None:
                rc.close()
        self.__reader = None
        self.__writer = None
        self.__socket = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()

    def format_command(self, cmd, *args):
        cmd_str = cmd + " "
        cmd_str += " ".join(args)
        cmd_str += "\n"  # specs says \n, asonic does \r\n
        return cmd_str

    def _execute_command(self, cmd, *args):
        if cmd not in ALL_CMDS[self.channel]:
            raise ChannelError(
                "command {} isn't allowed in channel {}".format(cmd, self.channel))

        cmd_str = self.format_command(cmd, *args)
        self._writer.write(cmd_str)
        self._writer.flush()
        resp = self._get_response()
        return resp

    def _get_response(self):
        return raise_for_error(self._reader.readline()).strip()


class CommonCommandsMixin:
    """Mixin of the commands used by all sonic channels."""

    def ping(self):
        """Send ping command to the server

        Returns:
            str -- PONG
        """
        return self._execute_command("PING")

    def quit(self):
        """Quit the channel

        """
        self._execute_command("QUIT")
        self._close()

    # TODO: check help.
    def help(self, *args):
        """Sends Help query."""
        return self._execute_command("HELP", *args)


class IngestClient(SonicClient, CommonCommandsMixin):
    def __init__(self, host: str, port: str, password: str):
        super().__init__(host, port, password, INGEST)

    def push(self, collection: str, bucket: str, object: str, text: str, lang: str=None):
        """Push search data in the index

        Arguments:
            collection {str} --  index collection (ie. what you search in, eg. messages, products, etc.)
            bucket {str} -- index bucket name (ie. user-specific search classifier in the collection if you have any eg. user-1, user-2, .., otherwise use a common bucket name eg. generic, default, common, ..)
            object {str} --  object identifier that refers to an entity in an external database, where the searched object is stored (eg. you use Sonic to index CRM contacts by name; full CRM contact data is stored in a MySQL database; in this case the object identifier in Sonic will be the MySQL primary key for the CRM contact)
            text {str} -- search text to be indexed can be a single word, or a longer text; within maximum length safety limits

        Keyword Arguments:
            lang {str} -- [description] (default: {None})

        Returns:
            [str] -- 'OK'
        """

        lang = "LANG({})".format(lang) if lang else ''
        text = quote_text(text)
        return self._execute_command("PUSH", collection, bucket, object, text, lang)

    def pop(self, collection: str, bucket: str, object: str, text: str):
        """Pop search data from the index

        Arguments:
            collection {str} --  index collection (ie. what you search in, eg. messages, products, etc.)
            bucket {str} -- index bucket name (ie. user-specific search classifier in the collection if you have any eg. user-1, user-2, .., otherwise use a common bucket name eg. generic, default, common, ..)
            object {str} --  object identifier that refers to an entity in an external database, where the searched object is stored (eg. you use Sonic to index CRM contacts by name; full CRM contact data is stored in a MySQL database; in this case the object identifier in Sonic will be the MySQL primary key for the CRM contact)
            text {str} -- search text to be indexed can be a single word, or a longer text; within maximum length safety limits

        Returns:
            [type] -- [description]
        """
        text = quote_text(text)
        return self._execute_command("POP", collection, bucket, object, text)

    def count(self, collection: str, bucket: str=None, object: str=None):
        """Count indexed search data 

        Arguments:
            collection {str} --  index collection (ie. what you search in, eg. messages, products, etc.)

        Keyword Arguments:
            bucket {str} -- index bucket name (ie. user-specific search classifier in the collection if you have any eg. user-1, user-2, .., otherwise use a common bucket name eg. generic, default, common, ..)
            object {str} --  object identifier that refers to an entity in an external database, where the searched object is stored (eg. you use Sonic to index CRM contacts by name; full CRM contact data is stored in a MySQL database; in this case the object identifier in Sonic will be the MySQL primary key for the CRM contact)

        Returns:
            [type] -- [description]
        """
        bucket = bucket or ''
        object = object or ''
        return self._execute_command('COUNT', collection, bucket, object)

    def flush_collection(self, collection: str):
        """Flush all indexed data from a collection

        Arguments:
            collection {str} --  index collection (ie. what you search in, eg. messages, products, etc.)

        Returns:
            [type] -- [description]
        """
        return self._execute_command('FLUSHC', collection)

    def flush_bucket(self, collection: str, bucket: str):
        """Flush all indexed data from a bucket in a collection

        Arguments:
            collection {str} --  index collection (ie. what you search in, eg. messages, products, etc.)
            bucket {str} -- index bucket name (ie. user-specific search classifier in the collection if you have any eg. user-1, user-2, .., otherwise use a common bucket name eg. generic, default, common, ..)


        Returns:
            [type] -- [description]
        """
        return self._execute_command('FLUSHB', collection, bucket)

    def flush_object(self, collection: str, bucket: str, object: str):
        """Flush all indexed data from an object in a bucket in collection

        Arguments:
            collection {str} --  index collection (ie. what you search in, eg. messages, products, etc.)
            bucket {str} -- index bucket name (ie. user-specific search classifier in the collection if you have any eg. user-1, user-2, .., otherwise use a common bucket name eg. generic, default, common, ..)
            object {str} --  object identifier that refers to an entity in an external database, where the searched object is stored (eg. you use Sonic to index CRM contacts by name; full CRM contact data is stored in a MySQL database; in this case the object identifier in Sonic will be the MySQL primary key for the CRM contact)


        Returns:
            [type] -- [description]
        """
        return self._execute_command('FLUSHO', collection, bucket, object)

    def flush(self, collection: str, bucket: str=None, object: str=None):
        """Flush indexed data in a collection, bucket, or in an object.

        Arguments:
            collection {str} --  index collection (ie. what you search in, eg. messages, products, etc.)

        Keyword Arguments:
            bucket {str} -- index bucket name (ie. user-specific search classifier in the collection if you have any eg. user-1, user-2, .., otherwise use a common bucket name eg. generic, default, common, ..)
            object {str} --  object identifier that refers to an entity in an external database, where the searched object is stored (eg. you use Sonic to index CRM contacts by name; full CRM contact data is stored in a MySQL database; in this case the object identifier in Sonic will be the MySQL primary key for the CRM contact)

        Returns:
            [type] -- [description]
        """
        if not bucket and not object:
            return self.flush_collection(collection)
        elif bucket and not object:
            return self.flush_bucket(collection, bucket)
        elif object and bucket:
            return self.flush_object(collection, bucket, object)


class SearchClient(SonicClient, CommonCommandsMixin):
    def __init__(self, host: str, port: int, password: str):
        """Create Sonic client that operates on the Search Channel

        Arguments:
            host {str} -- valid reachable host address
            port {int} -- port number
            password {str} -- password (defined in config.cfg file on the server side)

        """
        super().__init__(host, port, password, SEARCH)

    def query(self, collection: str, bucket: str, terms: str, limit: int=None, offset: int=None, lang: str=None):
        """Query the database 

        Arguments:
            collection {str} -- index collection (ie. what you search in, eg. messages, products, etc.)
            bucket {str} -- index bucket name (ie. user-specific search classifier in the collection if you have any eg. user-1, user-2, .., otherwise use a common bucket name eg. generic, default, common, ..)
            terms {str} --  text for search terms

        Keyword Arguments:
            limit {[type]} -- a positive integer number; set within allowed maximum & minimum limits
            offset {[type]} -- a positive integer number; set within allowed maximum & minimum limits
            lang {[type]} -- an ISO 639-3 locale code eg. eng for English (if set, the locale must be a valid ISO 639-3 code; if not set, the locale will be guessed from text).

        Returns:
            list -- list of objects ids.
        """
        limit = "LIMIT({})".format(limit) if limit else ''
        lang = "LANG({})".format(lang) if lang else ''
        offset = "OFFSET({})".format(offset) if offset else ''

        terms = quote_text(terms)
        self._execute_command(
            'QUERY', collection, bucket, terms, limit, offset, lang)
        resp_result = self._get_response()
        return resp_result.split()[3:]

    def suggest(self, collection: str, bucket: str, word: str, limit: int=None):
        """auto-completes word. 

        Arguments:
            collection {str} -- index collection (ie. what you search in, eg. messages, products, etc.)
            bucket {str} -- index bucket name (ie. user-specific search classifier in the collection if you have any eg. user-1, user-2, .., otherwise use a common bucket name eg. generic, default, common, ..)
            word {str} --  word to autocomplete


        Keyword Arguments:
            limit {[type]} -- a positive integer number; set within allowed maximum & minimum limits (default: {None})

        Returns:
            list -- list of suggested words.
        """
        limit = "LIMIT({})".format(limit) if limit else ''
        word = quote_text(word)
        self._execute_command(
            'SUGGEST', collection, bucket, word, limit)
        resp_result = self._get_response()
        return resp_result.split()[3:]


def test_ingest():
    with IngestClient("127.0.0.1", '1491', 'dmdm') as ingestcl:
        print(ingestcl.ping())
        print(ingestcl.protocol)
        print(ingestcl.bufsize)
        ingestcl.push("wiki", "articles", "article-1",
                      "for the love of god hell")
        ingestcl.push("wiki", "articles", "article-2",
                      "for the love of satan heaven")
        ingestcl.push("wiki", "articles", "article-3",
                      "for the love of lorde hello")
        ingestcl.push("wiki", "articles", "article-4",
                      "for the god of loaf helmet")


def test_search():
    with SearchClient("127.0.0.1", '1491', 'dmdm') as querycl:
        print(querycl.ping())
        print(querycl.query("wiki", "articles", "for"))
        print(querycl.query("wiki", "articles", "love"))
        print(querycl.suggest("wiki", "articles", "hell"))


if __name__ == "__main__":
    test_ingest()
    test_search()
