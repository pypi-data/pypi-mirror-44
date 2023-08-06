import requests

class Printer():
    """Printer Class."""

    def __init__(self,
                 printer_id,
                 baseurl,
                 apikey,
                 active,
                 name,
                 online,
                 slug):
        self._printer_id = printer_id
        self._active = active
        self._name = name
        self._online = online
        self._slug = slug

        self._baseurl = baseurl
        self._apikey = apikey

        self._job = None
        self._pausestate = None
        self._paused = None

        self._activeextruder = 0
        self._debuglevel = 0
        self._extruder = None
        self._fans = None
        self._firmware = None
        self._firmwareurl = None
        self._flowmultiply = 100
        self._hasxhome = False
        self._hasyhome = False
        self._haszhome = False
        self._heatedbeds = None
        self._heatedchambers = None
        self._layer = 0
        self._lights = 0
        self._numextruder = 1
        self._poweron = False
        self._rec = False
        self._sdcardmounted = False
        self._speedmultiply = 100
        self._volumetric = False
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0

    def _request(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            logger.warning("Invalid response from API")
            return False
        else:
            return response.json()

    def get_data(self):
        """Get status and data for specific printer ID."""
        data = self._request(self._baseurl + '/printer/list/?' + self._apikey)
        for printer in data['data']:
            if printer['slug'] == self._slug:
                self._active = printer['active']
                self._job = printer['job']
                self._online = printer['online']
                self._pausestate = printer['pauseState']
                self._paused = printer['paused']

        rawdata = self._request(self._baseurl + '/printer/api/' + self._slug + '?a=stateList&' + self._apikey)
        data = None
        try:
            data = rawdata[self._slug]
        except:
            pass

        if data is None:
            return

        self._activeextruder = data['activeExtruder']
        self._debuglevel = data['debugLevel']
        self._firmware = data['firmware']
        self._firmwareurl = data['firmwareURL']
        self._flowmultiply = data['flowMultiply']
        self._hasxhome = data['hasXHome']
        self._hasyhome = data['hasYHome']
        self._haszhome = data['hasZHome']
        self._layer = data['layer']
        self._lights = data['lights']
        self._numextruder = data['numExtruder']
        self._poweron = data['powerOn']
        self._rec = data['rec']
        self._sdcardmounted = data['sdcardMounted']
        self._speedmultiply = data['speedMultiply']
        self._volumetric = data['volumetric']
        self._x = data['x']
        self._y = data['y']
        self._z = data['z']

        extruder_list = []
        fan_list = []
        bed_list = []
        chamber_list = []

        for extruder in data['extruder']:
            extruder_list.append(Temperature(extruder['error'],
                                             extruder['output'],
                                             extruder['tempRead'],
                                             extruder['tempSet']))
        self._extruder = extruder_list

        for bed in data['heatedBeds']:
            bed_list.append(Temperature(bed['error'],
                                        bed['output'],
                                        bed['tempRead'],
                                        bed['tempSet']))
        self._heatedbeds = bed_list

        for chamber in data['heatedChambers']:
            chamber_list.append(Temperature(chamber['error'],
                                            chamber['output'],
                                            chamber['tempRead'],
                                            chamber['tempSet']))
        self._heatedbeds = chamber_list

        for fan in data['fans']:
            fan_list.append(Fan(fan['on'],
                                fan['voltage']))
        self._fans = fan_list

    @property
    def slug(self):
        return self._slug

    @property
    def name(self):
        return self._name

    @property
    def active(self):
        return self._active

    @property
    def job(self):
        return self._job

    @property
    def online(self):
        return self._online

    @property
    def pausestate(self):
        return self._pausestate

    @property
    def paused(self):
        return self._paused

    @property
    def activeextruder(self):
        return self._activeextruder

    @property
    def debuglevel(self):
        return self._debuglevel

    @property
    def firmware(self):
        return self._firmware

    @property
    def firmwareurl(self):
        return self._firmwareurl

    @property
    def flowmultiply(self):
        return self._flowmultiply

    @property
    def hasxhome(self):
        return self._hasxhome

    @property
    def hasyhome(self):
        return self._hasyhome

    @property
    def haszhome(self):
        return self._haszhome

    @property
    def layer(self):
        return self._layer

    @property
    def lights(self):
        return self._lights

    @property
    def numextruder(self):
        return self._numextruder

    @property
    def poweron(self):
        return self._poweron

    @property
    def rec(self):
        return self._rec

    @property
    def sdcardmounted(self):
        return self._sdcardmounted

    @property
    def speedmultiply(self):
        return self._speedmultiply

    @property
    def volumetric(self):
        return self._volumetric

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def extruder(self):
        return self._extruder

    @property
    def fans(self):
        return self._fans

    @property
    def heatedbeds(self):
        return self._heatedbeds

    @property
    def heatedchambers(self):
        return self._heatedchambers

    @property
    def state(self):
        """Return state, for use in Home Assistant."""
        if self._online == 0:
            return "off"
        else:
            if self._job == None or self._job == "none":
                return "idle"
            else:
                return "printing"

class Fan():
    """Fan data."""
    def __init__(self,
                 on,
                 voltage):
        self._on = on
        self._voltage = voltage

    @property
    def on(self):
        return self._on

    @property
    def voltage(self):
        return self._voltage

class Temperature():
    """Temperature data."""
    def __init__(self,
                 error,
                 output,
                 tempread,
                 tempset):
        self._error = error
        self._output = output
        self._tempread = tempread
        self._tempset = tempset

    @property
    def error(self):
        return self._error

    @property
    def output(self):
        return self._output

    @property
    def tempread(self):
        return self._tempread

    @property
    def tempset(self):
        return self._tempset
