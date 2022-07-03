import requests
import json
import time
import pprint

pp = pprint.PrettyPrinter(indent=4).pprint


class RDUtilities:
    def __init__(self, api_key=None):
        self.auth_key = api_key
        self.protocol = "https://"
        self.base = "api.real-debrid.com"
        self.api = "/rest/1.0"
        self.host = f"{self.protocol}{self.base}{self.api}"

    def get_magnet_hash(self, magnet_link):
        """
        Extracts and returns the SHA1 hash of a magnet link.

        This function simply extracts the hash from the magnet link using list comprehension and returns it.

        Parameters
        ----------
        magnet_link : str
            The magnet link to extract the hash from.

        Returns
        -------
        str
            The SHA1 hash of the magnet link.

        See Also
        --------
        get_magnet_link(magnet_hash) : Generates magnet links from hashes (NOT IMPLEMENTED).

        Examples
        --------
        >>> get_magnet_link("magnet:?xt=urn:btih:8DBB673D4F0AB8BFF6079E0A05C39E85320D4A2A&dn=The.Old.Man.S01E03.WEB.x264-PHOENiX")

        8DBB673D4F0AB8BFF6079E0A05C39E85320D4A2A
        """

        # print(f"magnet_link: {magnet_link}")
        result = magnet_link.split('?')[1]
        result_list = result.split('&')

        for item in result_list:
            if item.startswith('xt='):
                hash = item.split('=')[1]
                hash = hash.split(':')[-1]
                return hash
        return None

    def query_rd_by_hash(self, hash):
        print(f"AUTH: {self.auth_key}")
        get_str = f"{self.host}/torrents/instantAvailability/{hash}?auth_token={self.auth_key}"
        result = list(requests.get(get_str).json().values())[0]
        if len(result) == 0:
            return False, []
        else:
            print(f"RESULT: {result}")
            return True, result

    def delete_download(self, download_id):
        delete_str = f"{self.host}/downloads/delete/{download_id}?auth_token={self.auth_key}"
        # get_str = f"{self.host}/torrents/instantAvailability/{hash}?auth_token={self.auth_key}"
        result = requests.delete(delete_str)
        # result = list(requests.get(get_str).json().values())[0]
        # if len(result) == 0:
        #     return False, []
        # else:
        print(f"RESULT: {result}")
        return result

    def check_link(self, link):
        if link.startswith("magnet:"):
            hash = self.get_magnet_hash(link)
            print(f"HASH: {hash}")
        else:
            print(f"HASH: {link}")
            hash = link
        if hash is not None:
            status, result = self.query_rd_by_hash(hash)
            if not status or len(result) == 0:
                print(f"Link is not cached!")
                return False, None
            print(f"Link is cached!")
            return True, result

    def add_magnet(self, magnet):
        # HTML request header
        headers = {"Authorization": "Bearer " + self.auth_key}

        # Add magnet to Real-Debrid and process response
        data = {"magnet": magnet, "host": "real-debrid.com"}
        result = requests.post(
            "https://api.real-debrid.com/rest/1.0/torrents/addMagnet", headers=headers, data=data)
        if result.status_code != 201:
            if result.status_code == 401:
                print(
                    "Failed adding magnet to RD: Invalid token, to enter authentication token, use --token <value>.")
            elif result.status_code == 402:
                print("Failed adding magnet to RD: User not premium.")
            elif result.status_code == 503:
                print("Failed adding magnet to RD: Service not available.")
            else:
                print("Failed adding magnet to RD.")
            return False

        # Try to select file in magnet on Real-Debrid
        try:
            id = result.json()["id"]
            print(f"FILE ID: {id}")
            select_data = {"files": "all"}
            select_url = "https://api.real-debrid.com/rest/1.0/torrents/selectFiles/" + id
            requests.post(select_url, headers=headers, data=select_data)
        except Exception as e:
            print("{}".format(e))
            print("Magnet couldn't be activated on Real-Debrid (requires manual activation).")
        print("Added magnet to Real-Debrid.")
        return True

    def get_downloads(self, all=False, page=1, limit=100, offset=0):
        if not all:
            get_str = f"{self.host}/downloads/?auth_token={self.auth_key}&limit={limit}&offset={offset}&page={page}"
            result = requests.get(get_str).json()
            return True, result
        else:
            # Get number of results
            # Get limit and ignore offset
            # pages = (number of results / limit ) + 1
            # If the result is empty, you have reached the end of the list
            initial_get_str = f"{self.host}/downloads/?auth_token={self.auth_key}&limit={limit}&page={page}"
            initial_result = requests.get(initial_get_str)
            headers = initial_result.headers
            print(f"HEADERS: {headers}")
            x_count = int(headers["X-Total-Count"])
            pp(f"TOTAL ITEMS: {x_count}")
            pages = (x_count // limit) + 1
            print(f"PAGES: {pages}")

            # Get all pages
            results = []
            print("Getting all pages...")
            for i in range(1, pages + 1):
                print(f"Getting page {i}...")
                get_str = f"{self.host}/downloads/?auth_token={self.auth_key}&limit={limit}&page={i}"
                result = requests.get(get_str).json()
                if result:
                    results.append(result)
                else:
                    break
            # pp(f"\n------------------------------------------------\nRESULTS: {results}")
            with open('downloads.txt', 'w') as filehandle:
                json.dump(results, filehandle)
            return True, results

    def get_detailed_info(self, download_id):
        get_str = f"{self.host}/streaming/mediaInfos/{download_id}?auth_token={self.auth_key}"
        result = requests.get(get_str).json()
        return result

    def get_available_formats(self, download_id):
        get_str = f"{self.host}/streaming/transcode/{download_id}?auth_token={self.auth_key}"
        result = requests.get(get_str).json()
        return result

    def process_dl_file(self, filename):
        with open(filename, 'r') as filehandle:
            data = json.load(filehandle)
        return data
