import os
from django.contrib.gis.utils import LayerMapping
from marketing.models import Parcels

# Auto-generated `LayerMapping` dictionary for administration model
parcels_mapping = {
    'objectid' : 'OBJECTID',
    'shape_leng' : 'SHAPE_Leng',
    'shape_area' : 'SHAPE_Area',
    'designated' : 'Designated',
    'geom' : 'MULTIPOLYGON',
}

parcels_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/LandParcels.shp'))

def run(verbose=True):
    lm = LayerMapping(Parcels, parcels_shp, parcels_mapping,transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)