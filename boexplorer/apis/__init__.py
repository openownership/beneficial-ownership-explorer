from boexplorer.apis.bulgaria_cr import BulgarianCR
from boexplorer.apis.gleif import GLEIF
from boexplorer.apis.uk_psc import UKPSC
from boexplorer.apis.nigeria_cac import NigerianCAC
from boexplorer.apis.slovakia_orsr import SlovakiaORSR
from boexplorer.apis.denmark_cvr import DenmarkCVR
from boexplorer.apis.latvia_ur import LatviaUR
from boexplorer.apis.poland_krs import PolandKRS
from boexplorer.apis.estonia_rik import EstoniaRIK
from boexplorer.apis.france_inpi import FranceINPI
from boexplorer.apis.czech_cr import CzechCR
from boexplorer.data.data import load_data

scheme_data = load_data()

search_companies_apis = [GLEIF(scheme_data=scheme_data),
               BulgarianCR(),
               UKPSC(),
               NigerianCAC(),
               SlovakiaORSR(),
               DenmarkCVR(),
               LatviaUR(),
               PolandKRS(),
               EstoniaRIK(),
               #FranceINPI(),
               CzechCR()]

search_persons_apis = [BulgarianCR(),
		       NigerianCAC(),
                       DenmarkCVR(),
               ]
