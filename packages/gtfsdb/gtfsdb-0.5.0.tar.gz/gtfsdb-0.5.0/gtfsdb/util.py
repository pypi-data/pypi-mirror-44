import os
import sys
import datetime
import tempfile

import logging
log = logging.getLogger(__name__)


def get_all_subclasses(cls):
    """
    :see https://stackoverflow.com/questions/3862310/how-to-find-all-the-subclasses-of-a-class-given-its-name
    """
    ret_val = set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in get_all_subclasses(c)]
    )
    return ret_val


def make_temp_sqlite_db_uri(name=None):
    """
    will return a FILE URI to a temp file, ala /tmp/bLaHh111 for the path of a new sqlite file db
    NOTE: name is optional ... if provided, the file will be named as such (good for testing and refreshing sqlite db)
    """
    if name:
        db_file = os.path.join(tempfile.gettempdir(), name)
    else:
        db_file = tempfile.mkstemp()[1]
    url = 'sqlite:///{0}'.format(db_file)
    log.debug("DATABASE TMP FILE: {0}".format(db_file))
    return url


def safe_get(obj, key, def_val=None):
    """
    try to return the key'd value from either a class or a dict
    (or return the raw value if we were handed a native type)
    """
    ret_val = def_val
    try:
        ret_val = getattr(obj, key)
    except:
        try:
            ret_val = obj[key]
        except:
            if isinstance(obj, (int, long, str)):
                ret_val = obj
    return ret_val


def safe_get_any(obj, keys, def_val=None):
    """
    :return object element value matching the first key to have an associated value
    """
    ret_val = def_val
    for k in keys:
        v = safe_get(obj, k)
        if v and len(v) > 0:
            ret_val = v
            break
    return ret_val


def check_date(in_date, fmt_list=['%Y-%m-%d', '%m/%d/%Y', '%m-%d-%Y'], def_val=None):
    """
    utility function to parse a request object for something that looks like a date object...
    """
    if def_val is None:
        def_val = datetime.date.today()

    if in_date is None:
        ret_val = def_val
    elif isinstance(in_date, datetime.date) or isinstance(in_date, datetime.datetime):
        ret_val = in_date
    else:
        ret_val = def_val
        for fmt in fmt_list:
            try:
                d = datetime.datetime.strptime(in_date, fmt).date()
                if d is not None:
                    ret_val = d
                    break
            except Exception as e:
                log.debug(e)
    return ret_val


class Point(object):
    is_valid = False

    def __init__(self, **kwargs):
        self.srid = kwargs.get('srid', None)
        try:
            self.lat = float(kwargs.get('lat'))
            self.lon = float(kwargs.get('lon'))
            self.is_valid = True
        except:
            self.lat = self.lon = None

    def get_point(self):
        return self.lon, self.lat

    def to_geojson(self):
        point = self.make_geo(self.lon, self.lat, self.srid)
        return point

    @classmethod
    def make_geo(cls, lon, lat, srid=None):
        geo = 'POINT({0} {1})'.format(lon, lat)
        if geo:
            geo = 'SRID={0};{1}'.format(srid, geo)
        return geo


class BBox(object):
    is_valid = False

    def __init__(self, **kwargs):
        self.srid = kwargs.get('srid', None)
        try:
            self.min_lat = float(kwargs.get('min_lat'))
            self.min_lon = float(kwargs.get('min_lon'))
            self.max_lat = float(kwargs.get('max_lat'))
            self.max_lon = float(kwargs.get('max_lon'))
            self.is_valid = True
        except:
            self.min_lat = self.min_lon = self.max_lat = self.max_lon = None

    def get_bbox(self):
        return self.min_lon, self.min_lat, self.max_lon, self.max_lat

    def to_geojson(self):
        poly = self.make_geo(self.min_lon, self.max_lon, self.min_lat, self.max_lat, self.srid)
        return poly

    @classmethod
    def make_geo(cls, left_lon, right_lon, bot_lat, top_lat, srid=None):
        """
        see: https://gis.stackexchange.com/questions/25797/select-bounding-box-using-postgis
        note: 5-pt POLY top-left, top-right, bot-right, bot-left,         ulx uly
                        llon/tlat, rlon/tlat, rlon/blat, min-lon/max-lat, min-lon/max-lat
        """
        geo = 'POLYGON(({0} {3}, {1} {3}, {1} {2}, {0} {2}, {0} {3}))'.format(left_lon, right_lon, bot_lat, top_lat)
        if geo:
            geo = 'SRID={0};{1}'.format(srid, geo)
        return geo


class UTF8Recoder(object):
    """Iterator that reads an encoded stream and encodes the input to UTF-8"""
    def __init__(self, f, encoding):
        import codecs
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        if sys.version_info >= (3, 0):
            return next(self.reader)
        else:
            return self.reader.next().encode('utf-8')

    def __next__(self):
        return self.next()
