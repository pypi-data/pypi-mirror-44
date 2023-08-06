from . import clsserver, clsprinter
import logging
import requests

logger = logging.getLogger('pyrepetier')

__version__ = '3.0.0'


class Repetier():
    """Repetier Server Class"""

    def __init__(self, **kwargs):
        """Init the communications"""
        url = kwargs.pop('url', None)
        port = kwargs.pop('port', 3344)
        api_key = kwargs.pop('apikey', None)
        self._baseurl = url + ':' + str(port)
        self._apikey = 'apikey=' + api_key
        self._detail = {}
        self._conn_ok = False

        reqUrl = self._baseurl + '/printer/list/?' + self._apikey
        response = requests.get(reqUrl)
        if response.status_code != 200:
            self._conn_ok = False
        else:
            try:
                data = response.json()
                if data['error'] == "Authorization required":
                    self._conn_ok = False
            except:
                self._conn_ok = True

    def _request(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            logger.warning("Invalid response from API")
            return False
        else:
            return response.json()

    def info(self):
        if self._conn_ok is False:
            return False

        data = self._request(self._baseurl + '/printer/info/?' + self._apikey)
        if data is not False:
            return clsserver.Server(data['name'],
                                 data['servername'],
                                 data['serveruuid'],
                                 data['version'])
        else:
            return False

    def getprinters(self):
        """Get printer SLUG list"""
        if self._conn_ok is False:
            return False

        printer_list = []

        data = self._request(self._baseurl + '/printer/info/?' + self._apikey)
        i = 0
        for printer in data['printers']:
            prn = clsprinter.Printer(i,
                                     self._baseurl,
                                     self._apikey,
                                     printer['active'],
                                     printer['name'],
                                     printer['online'],
                                     printer['slug'])
            printer_list.append(prn)
            i += 1

        self._printer_list = printer_list
        return printer_list