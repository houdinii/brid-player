from py1337x import py1337x
import flask
from flask import Response

from flask_restful import Api, Resource
from flask_cors import CORS
import pprint
import requests
import json
from rdutilities.rdutilities import RDUtilities
from tools.tools import Settings

pp = pprint.PrettyPrinter(indent=4).pprint
app = flask.Flask(__name__)
CORS(app)
api = Api(app)
torrents = py1337x()
settings = Settings("private/settings.json")
rd = RDUtilities(api_key=settings.config.real_debrid.api_key)

# utilities = Utilities()

# settings = utilities.get_settings()
# host = settings['SERVER']['HOST']
# port = int(settings['SERVER']['PORT'])
# auth_token = settings["REALDEBRID"]["AUTH_TOKEN"]
# max_pages = int(settings["1337X"]["MAX_PAGES"])


class TorrentList(Resource):
    def get(self, query, max_pages=10):
        raw_results = torrents.search(query)
        results = {'items': raw_results['items']}

        print(results)
        pages = int(raw_results['pageCount'])
        if pages > max_pages:
            pages = max_pages
        print(pages, max_pages)
        if pages > 1:
            print("Multiple pages found.")
            for i in range(1, pages + 1):
                print("Page {}".format(i))
                next_page = torrents.search(query, page=i)
                print(next_page)
                for item in next_page['items']:
                    results['items'].append(item)
        return results, 200
        # TODO In the future we should do this:
        # TODO if torrents.search is successful, return
        # TODO torrents.search(query), 200
        # TODO else return
        # TODO {}, 404


class TorrentAdd(Resource):
    def get(self, id):
        # This function is going to add the item to RD drive.

        info = torrents.info(torrentId=id)
        magnet = info['magnetLink']
        # result = utilities.add_magnet(magnet)
        result = rd.add_magnet(magnet)

        if result:
            return result, 200
        else:
            response = flask.jsonify({"error": "There was an error!"})
            return response, 404


class CheckCache(Resource):
    def get(self, link, *args):
        magnet_list = list(flask.request.args.to_dict().items())
        magnet = "magnet:?"
        for item in magnet_list:
            magnet += f"{item[0]}={item[1]}&"
        magnet = magnet[:-1]
        hash = rd.get_magnet_hash(magnet)
        result, data = rd.check_link(magnet)
        print(f"Result: {result}")
        print(f"Data: {data}")

        try:
            return (result, data), 200
        except Exception as e:
            message = json.dumps({"error": f"There was an error! {e}"})
            return Response(message, status=404, mimetype='application/json')


class TorrentDetails(Resource):
    def get(self, id):
        # This function is going to get the details of a torrent.

        info = torrents.info(torrentId=id)

        if info:
            return info, 200
        else:
            response = flask.jsonify({"error": "There was an error!"})
            return response, 404


class PopularTVWeek(Resource):
    def get(self):
        results = torrents.popular(category='tv', week=True)
        print(results)
        return results, 200


class PopularTV(Resource):
    def get(self):
        results = torrents.popular(category='tv', week=False)
        print(results)
        return results, 200


class PopularMovieWeek(Resource):
    def get(self):
        results = torrents.popular(category='movies', week=True)
        print(results)
        return results, 200


class PopularMovie(Resource):
    def get(self):
        results = torrents.popular(category='movies', week=False)
        print(results)
        return results, 200


class TrendingTVWeek(Resource):
    def get(self):
        results = torrents.trending(category='tv', week=True)
        print(results)
        return results, 200


class TrendingTV(Resource):
    def get(self):
        results = torrents.trending(category='tv', week=False)
        print(results)
        return results, 200


class TrendingMovieWeek(Resource):
    def get(self):
        results = torrents.trending(category='movies', week=True)
        print(results)
        return results, 200


class TrendingMovie(Resource):
    def get(self):
        results = torrents.trending(category='movies', week=False)
        print(results)
        return results, 200


class Top100Movie(Resource):
    def get(self):
        results = torrents.top(category='movies')
        print(results)
        return results, 200


class Top100TV(Resource):
    def get(self):
        results = torrents.top(category='tv')
        print(results)
        return results, 200


class CheckMagnetFromId(Resource):
    def get(self, id):
        print(f"Torrent ID: {id}")
        info = torrents.info(torrentId=id)
        pp(info)
        magnet = info['magnetLink']
        # hash = rd.get_magnet_hash(magnet)
        result = None
        if magnet is None:
            result = False
        if magnet is not None:
            result = rd.check_link(magnet)
        try:
            return result, 200
        except Exception as e:
            message = json.dumps({"error": "There was an error!"})
            return Response(message, status=500, mimetype='application/json')


api.add_resource(TorrentList, '/get/<string:query>')
api.add_resource(TorrentAdd, '/add/<string:id>')
api.add_resource(TorrentDetails, '/details/<string:id>')
api.add_resource(PopularTVWeek, '/PopularTVWeek/')
api.add_resource(PopularTV, '/PopularTV/')
api.add_resource(PopularMovieWeek, '/PopularMovieWeek/')
api.add_resource(PopularMovie, '/PopularMovie/')
api.add_resource(TrendingTVWeek, '/TrendingTVWeek/')
api.add_resource(TrendingTV, '/TrendingTV/')
api.add_resource(TrendingMovieWeek, '/TrendingMovieWeek/')
api.add_resource(TrendingMovie, '/TrendingMovie/')
api.add_resource(Top100Movie, '/Top100Movie/')
api.add_resource(Top100TV, '/Top100TV/')
api.add_resource(CheckCache, '/Check/<string:link>')
api.add_resource(CheckMagnetFromId, '/CheckMagnetFromId/<string:id>')


