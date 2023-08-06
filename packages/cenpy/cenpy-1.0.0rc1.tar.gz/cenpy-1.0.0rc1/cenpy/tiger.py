from six import iteritems as diter
import requests as r
import pandas as pd
from geopandas import GeoDataFrame
import copy

from . import geoparser as gpsr

# all queries to a map server, mounted at
# tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/
# are mounted by adding <name>/<MapServer> if they're mapservers

# none of the types at that url?f=json are not Mapservers.

_baseurl = "http://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb"
_pcs = "https://developers.arcgis.com/javascript/jshelp/pcs.html"
_bcs = "https://developers.arcgis.com/javascript/jshelp/bcs.html"

_basequery = {'where': '',  # sql query component
              'text': '',  # raw text search
              'objectIds': '',  # only grab these objects
              'time': '',  # time instant/time extend to query
              'geometry': '',  # spatial filter to apply to query
              'geometryType': 'esriGeometryEnvelope',  # spatial support
              'inSR': '',  # spatial ref of input geometry
              'spatialRel': '',  # what to do in a DE9IM spatial query
              'relationParam': '',  # used if arbitrary spatialRel is applied
              'outFields': '*',  # fields to pass from the header out
              'returnGeometry': True,  # bool describing whether to pass geometry out
              'maxAllowableOffset': '',  # set a spatial offset
              'geometryPrecision': '',
              'outSR': '',  # spatial reference of returned geometry
              'returnIdsOnly': False,  # bool stating to only return ObjectIDs
              'returnCountOnly': False,  # not documented, probably for the sql query
              'orderByFields': '',  # again not documented, probably for the sql
              'groupByFieldsForStatistics': '',  # not documented, probably for sql
              'outStatistics': '',  # no clue
              'returnZ': False,  # whether to return z components of shp-z
              'returnM': False,  # whether to return m components of shp-m
              'gdbVersion': '',  # geodatabase version name
              'returnDistinctValues': ''}  # no clue


def _jget(st):
    return r.get(st + '?f=json')


def available(verbose=False):
    """
    Query the TIGERweb geoAPI for available MapServices

    Parameters
    -----------
    verbose :   int
                int/bool describing verbosity level. Accepts levels -1, 0, 1, and
                greater.

    Returns
    -------
    list or dict of available MapServers through TIGERweb
    """
    q = _jget(_baseurl).json()
    for d in q['services']:
        d['name'] = d['name'].split('/')[-1]
    if verbose == -1:
        return [d['name'] for d in q['services']]
    if not verbose:
        return q['services']
    else:
        print('verbose may take a bit...')
        nexturls = ['/'.join([_baseurl, d['name'], d['type']])
                    for d in q['services']]
        for i, d in enumerate(q['services']):
            d['description'] = _jget(nexturls[i]).json()['description']
        if verbose == True:
            return q['services']
        else:
            return q


class ESRILayer(object):
    def __init__(self, baseurl, **kwargs):
        self.__dict__.update({'_'+k: v for k, v in diter(kwargs)})
        if hasattr(self, '_fields'):
            self.variables = pd.DataFrame(self._fields)
        self._baseurl = baseurl + '/' + str(self._id)

    def __repr__(self):
        try:
            return '(ESRILayer) ' + self._name
        except:
            return ''

    def query(self, raw=False, strict=False, **kwargs):
        """
        A query function to extract data out of MapServer layers. I've exposed
        every option here 

        Parameters
        ==========
        where: str, required
                    sql query string. 
        out_fields: list or str, (default: '*') 
                    fields to pass from the header out
        return_geometry: bool, (default: True)
                    bool describing whether to return geometry or just the
                    dataframe
        geometry_precision: str, (default: None)
                    a number of significant digits to which the output of the
                    query should be truncated
        out_sr: int or str, (default: None)
                    ESRI WKID spatial reference into which to reproject 
                    the geodata
        return_ids_only: bool, (default: False)
                    bool stating to only return ObjectIDs
        return_z: bool, (default: False)
                     whether to return z components of shp-z
        return_m: bool, (default: False)
                     whether to return m components of shp-m
        strict  :   bool (default: True)
                    whether to throw an error if invalid polygons are provided from the API (True)
                    or just warn that at least one polygon is invalid (False)
        raw : bool (default: False)
              whether to provide the raw geometries from the API
        Returns
        =======
        Dataframe or GeoDataFrame containing entries from the geodatabase

        Notes
        =====
        Most of the time, this should be used leaning on the SQL "where"
        argument: 

        cxn.query(where='GEOID LIKE "06*"')

        In most cases, you'll be querying against layers, not MapServices
        overall. 
        """
    # parse args
        kwargs = {''.join(k.split('_')): v for k, v in diter(kwargs)}

    # construct query string
        self._basequery = copy.deepcopy(_basequery)
        for k, v in diter(kwargs):
            try:
                self._basequery[k] = v
            except KeyError:
                raise KeyError("Option '{k}' not recognized, check parameters")
        qstring = '&'.join(['{}={}'.format(k, v)
                            for k, v in diter(self._basequery)])
        self._last_query = self._baseurl + '/query?' + qstring
    # run query
        resp = r.get(self._last_query + '&f=json')
        resp.raise_for_status()
        datadict = resp.json()
        if raw:
            return datadict
        if kwargs.get('returnGeometry', True) is False:
            return pd.DataFrame.from_records([x['attributes'] for x in datadict['features']])
    # convert to output format
        try:
            features = datadict['features']
        except KeyError:
            code, msg = datadict['error']['code'], datadict['error']['message']
            details = datadict['error']['details']
            if details is []:
                details = 'Mapserver provided no detailed error'
            raise KeyError(('Response from API is malformed. You may have '
                            'submitted too many queries, or experienced '
                            'significant network connectivity issues.\n'
                            '(API ERROR {}:{}({}))'.format(code, msg, details)))
        todf = []
        for i, feature in enumerate(features):
            locfeat = gpsr.__dict__[datadict['geometryType']](feature)
            todf.append(locfeat['properties'])
            todf[i].update({'geometry': locfeat['geometry']})
        df = pd.DataFrame(todf)
        outdf = gpsr.convert_geometries(df, strict=strict)
        outdf = GeoDataFrame(outdf)
        crs = datadict.pop('spatialReference', None)
        if crs is not None:
            crs = crs.get('latestWkid', crs.get('wkid'))
            crs = dict(init='epsg:{}'.format(crs))
        outdf.crs = crs
        return outdf


class TigerConnection(object):
    """
    a tiger connection
    """

    def __init__(self, name=None):
        if name not in available(verbose=-1):
            raise KeyError(
                'Dataset {n} not found. Please check cenpy.tiger.available()'.format(n=name))
        else:
            self._baseurl = '/'.join([_baseurl, name, 'MapServer'])
            resp = _jget(self._baseurl).json()
            self._key = name
            self.title = resp.pop('mapName', name)
            self.layers = self._get_layers()
            self.copyright = resp['copyrightText']
            self.projection = resp['spatialReference']['latestWkid']

    def _get_layers(self):
        resp = _jget(self._baseurl + '/layers').json()
        return [ESRILayer(self._baseurl, **d) for d in resp['layers']]

    def query(self, **kwargs):
        layer_idx = kwargs.pop('layer', None)
        if layer_idx is None:
            raise Exception('No layer selected.')
        return self.layers[layer_idx].query(**kwargs)
