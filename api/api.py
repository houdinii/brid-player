import pprint

import flask
from flask_cors import CORS
from flask_restful import Api, Resource
from py1337x import py1337x

from rdutilities.rdutilities import RDUtilities
from tools.tools import Settings

pp = pprint.PrettyPrinter(indent=4).pprint
app = flask.Flask(__name__)
CORS(app)
api = Api(app)
torrents = py1337x()
settings = Settings("private/settings.json")
rd = RDUtilities(api_key=settings.config.real_debrid.api_key)


class TorrentList(Resource):
    """Query the 1337x API for a list of torrents from query."""
    @staticmethod
    def get(query, max_pages=10):
        """Get a list of torrents matching a query from 1337x

        :param query: Search query
        :param max_pages: Maximum number of pages to search
        :return: List of torrents
        """
        raw_results = torrents.search(query)
        results = {'items': raw_results['items']}

        print(results)
        pages = int(raw_results['pageCount'])
        pages = min(pages, max_pages)
        if pages > 1:
            print("Multiple pages found.")
            for i in range(1, pages + 1):
                print("Page {}".format(i))
                next_page = torrents.search(query, page=i)
                print(next_page)
                for item in next_page['items']:
                    results['items'].append(item)
        return results, 200
        # skipcq: PYL-W0511
        # TODO In the future we should do this:
        # skipcq: PYL-W0511
        # TODO if torrents.search is successful, return
        # skipcq: PYL-W0511
        # TODO torrents.search(query), 200
        # skipcq: PYL-W0511
        # TODO else return
        # skipcq: PYL-W0511
        # TODO {}, 404


class TorrentAdd(Resource):
    """Add a torrent to Real-Debrid."""
    @staticmethod
    def get(torrent_id):
        """Add a torrent to Real-Debrid

        :param torrent_id: ID of the torrent to add
        :return: (result, 200) if successful, (response, 404) if not
        """
        info = torrents.info(torrentId=torrent_id)
        magnet = info['magnetLink']
        result = rd.add_magnet(magnet)

        if result:
            return result, 200
        response = flask.jsonify({"error": "There was an error!"})
        return response, 404


class CheckCache(Resource):
    """Check if a torrent is cached on Real-Debrid."""
    # noinspection PyUnusedLocal
    @staticmethod
    def get(link, *args):
        """Check if a link is cached in Real-Debrid

        :param link: Link to check
        :return: (result, 200) if successful, (response, 404) if not
        """
        print(f"link: {link}")
        magnet_list = list(flask.request.args.to_dict().items())
        magnet = "magnet:?"
        for item in magnet_list:
            magnet += f"{item[0]}={item[1]}&"
        magnet = magnet[:-1]
        result, data = rd.check_link(magnet)
        print(f"Result: {result}")
        print(f"Data: {data}")

        return (result, data), 200


class TorrentDetails(Resource):
    """Get details about a torrent from Real-Debrid."""
    @staticmethod
    def get(torrent_id):
        """Get details about a torrent from 1337x

        :param torrent_id: ID of the torrent to get details about
        :return: (result, 200) if successful, (response, 404) if not
        """
        info = torrents.info(torrentId=torrent_id)

        if info:
            return info, 200
        response = flask.jsonify({"error": "There was an error!"})
        return response, 404


class PopularTVWeek(Resource):
    """Get a list of popular TV shows this week"""
    @staticmethod
    def get():
        """Get a list of popular TV shows this week from 1337x

        TODO: Error Handling

        :return: (results, 200)
        """
        results = torrents.popular(category='tv', week=True)
        print(results)
        return results, 200


class PopularTV(Resource):
    """Get a list of popular TV shows today"""
    @staticmethod
    def get():
        """Get a list of popular TV shows today from 1337x

        TODO: Error Handling

        :return: (results, 200)
        """
        results = torrents.popular(category='tv', week=False)
        print(results)
        return results, 200


class PopularMovieWeek(Resource):
    """Get a list of popular movies this week"""
    @staticmethod
    def get():
        """Get a list of popular Movies this week from 1337x

        TODO: Error Handling

        :return: (results, 200)
        """
        results = torrents.popular(category='movies', week=True)
        print(results)
        return results, 200


class PopularMovie(Resource):
    """Get a list of popular Movies today"""
    @staticmethod
    def get():
        """Get a list of popular Movies today from 1337x

        TODO: Error Handling

        :return: (results, 200)
        """
        results = torrents.popular(category='movies', week=False)
        print(results)
        return results, 200


class TrendingTVWeek(Resource):
    """Get a list of trending TV shows this week"""
    @staticmethod
    def get():
        """Get a list of trending TV shows this week from 1337x

        TODO: Error Handling

        :return: (results, 200)
        """
        results = torrents.trending(category='tv', week=True)
        print(results)
        return results, 200


class TrendingTV(Resource):
    """Get a list of trending TV shows today"""
    @staticmethod
    def get():
        """Get a list of trending TV shows today from 1337x

        TODO: Error Handling

        :return: (results, 200)
        """
        results = torrents.trending(category='tv', week=False)
        print(results)
        return results, 200


class TrendingMovieWeek(Resource):
    """Get a list of trending movies this week"""
    @staticmethod
    def get():
        """Get a list of trending movies this week from 1337x

        TODO: Error Handling

        :return: (results, 200)
        """
        results = torrents.trending(category='movies', week=True)
        print(results)
        return results, 200


class TrendingMovie(Resource):
    """Get a list of trending movies today"""
    @staticmethod
    def get():
        """Get a list of trending movies today from 1337x

        TODO: Error Handling

        :return: (results, 200)
        """
        results = torrents.trending(category='movies', week=False)
        print(results)
        return results, 200


class Top100Movie(Resource):
    """Get a list of top 100 movies"""
    @staticmethod
    def get():
        """Get a list of top 100 movies from 1337x

        TODO: Error Handling

        :return: (results, 200)
        """
        results = torrents.top(category='movies')
        print(results)
        return results, 200


class Top100TV(Resource):
    @staticmethod
    def get():
        """Get a list of top 100 TV shows from 1337x

        TODO: Error Handling

        :return: (results, 200)
        """
        results = torrents.top(category='tv')
        print(results)
        return results, 200


class CheckMagnetFromId(Resource):
    """Check if a magnet is cached in Real-Debrid, which should actually be in RDUtilities"""
    @staticmethod
    def get(torrent_id):
        """Check if a magnet is cached in Real-Debrid

        :param torrent_id: ID of the torrent to check
        :return: (result, 200) if successful, (response, 500) if not
        """
        print(f"Torrent ID: {torrent_id}")
        info = torrents.info(torrentId=torrent_id)
        pp(info)
        magnet = info['magnetLink']
        result = None
        if magnet is None:
            result = False
        if magnet is not None:
            result = rd.check_link(magnet)
        return result, 200


api.add_resource(TorrentList, '/get/<string:query>')
api.add_resource(TorrentAdd, '/add/<string:torrent_id>')
api.add_resource(TorrentDetails, '/details/<string:torrent_id>')
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
api.add_resource(CheckMagnetFromId, '/CheckMagnetFromId/<string:torrent_id>')
