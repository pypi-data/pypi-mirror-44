class Server():
    """Server info."""

    def __init__(self,
                 name,
                 servername,
                 serveruuid,
                 version):
        self._name = name
        self._servername = servername
        self._serveruuid = serveruuid
        self._version = version
    
    @property
    def name(self):
        return self._name

    @property
    def servername(self):
        return self._servername

    @property
    def serveruuid(self):
        return self._serveruuid

    @property
    def version(self):
        return self._version