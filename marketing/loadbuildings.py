import os
from django.contrib.gis.utils import LayerMapping
from marketing.models import Buildings

# Auto-generated `LayerMapping` dictionary for administration model
buildings_mapping = {
    'objectid' : 'OBJECTID',
    'shape_leng' : 'SHAPE_Leng',
    'shape_area' : 'SHAPE_Area',
    'building_n' : 'Building_N',
    'geom' : 'MULTIPOLYGON',
}

building_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/Buildings.shp'))

def run(verbose=True):
    lm = LayerMapping(Buildings, building_shp, buildings_mapping,transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)