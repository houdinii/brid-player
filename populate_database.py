from rdutilities.rdutilities import RDUtilities
from tools.tools import Settings
from dbutilities.dbutilities import DBUtilities
import pprint

settings = Settings("private/settings.json")
rd = RDUtilities(api_key=settings.config.real_debrid.api_key)
db = DBUtilities()
pp = pprint.PrettyPrinter(indent=4).pprint

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # GET ALL DOWNLOADS FROM REALDB AND ADD TO DOWNLOADS.TXT FILE:
    # status, downloads = rd.get_downloads(all=True)
    # print(downloads)

    # LOAD DLS FROM FILE:
    # dls = rd.process_dl_file("downloads.txt")
    # ids = []
    # GET LIST OF DOWNLOAD ID'S (dls[x]['torrent_id'])
    # ADD DLS TO DOWNLOADS TABLE:

    db.connect("bpData.db")
    # Get all records from bp_Downloads table
    # Get all records from bp_detailed_info table if it exists based on download_id
    # Get all records from bp_available_formats table if it exists based on download_id
    # Display records one at a time

    downloads = db.get_all_download_records()
    for download in downloads:
        record = {
            'download_id': download['download_id'],
            'filename': download['filename'],
            'mimeType': download['mimeType'],
            'filesize': download['filesize'],
            'link': download['link'],
            'host': download['host'],
            'host_icon': download['host_icon'],
            'chunks': download['chunks'],
            'download': download['download'],
            'streamable': download['streamable'],
            'generated': download['generated']
        }

        formats = db.get_formats_for_download(download['download_id'])
        format_list = []
        for format in formats:
            f_record = {
                'label': format['label'],
                'extension': format['extension']
            }
            format_list.append(f_record)
        record['formats'] = format_list

        info = db.get_detailed_info(download['download_id'])
        info_list = []
        for line in info:
            i_record = {
                'download_id': line['download_id'],
                'filename': line['filename'],
                'hoster': line['hoster'],
                'link': line['link'],
                'type': line['type'],
                'season': line['season'],
                'episode': line['episode'],
                'year': line['year'],
                'duration': line['duration'],
                'bitrate': line['bitrate'],
                'size': line['size'],
                'poster_path': line['poster_path'],
                'backdrop_path': line['backdrop_path'],
                'baseUrl': line['baseUrl'],
                'modelUrl': line['modelUrl'],
                'host': line['host']
            }
            info_list.append(i_record)
        record['detailed_info'] = info_list

        pp(record)

    db.close()
