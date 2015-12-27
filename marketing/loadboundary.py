import os
from django.contrib.gis.utils import LayerMapping
from marketing.models import Boundaries

# Auto-generated `LayerMapping` dictionary for administration model
boundaries_mapping = {
    'id' : 'Id',
    'geom' : 'MULTILINESTRING',
}


boundary_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/registration_blockboundary.shp'))

def run(verbose=True):
    lm = LayerMapping(Boundaries, boundary_shp, boundaries_mapping,transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)