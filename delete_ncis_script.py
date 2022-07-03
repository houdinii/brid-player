from ncis_ids import ncis_ids
from rdutilities.rdutilities import RDUtilities
from dbutilities.dbutilities import DBUtilities
from tools.tools import Settings
import pprint

settings = Settings("private/settings.json")
rd = RDUtilities(api_key=settings.config.real_debrid.api_key)
db = DBUtilities()
pp = pprint.PrettyPrinter(indent=4).pprint

if __name__ == '__main__':
    print(f"NUMBER OF NCIS DOWNLOADS: {len(ncis_ids)}")
    db.connect("bpData.db")
    for id in ncis_ids:
        db.delete_download_record(id)
    db.close()
