import json
from datetime import datetime, date
import traceback

import article_repository as repo
import logging
log = logging.getLogger()
GET_ALL_ARTICLES = "/admin/article/all"
GET_ARTICLE = "/admin/article/"
CREATE_ARTICLE = "/admin/article"
UPDATE_ARTICLE = "/admin/article"
DELETE_ARTICLE = "/admin/article/"


def get_article_by_id(article_id):
    log.info("Retrieving article for id {}".format(article_id))
    if article_id:
        return repo.get_article_by_id(article_id)


def get_all_articles():
    log.info("Retrieving all articles")
    return repo.get_all_articles()


# TODO: Get user
def create_article(article):
    log.info("Creating article for title {}".format(article['title']))
    return repo.create_article(article, "admin")


def update_article(article):
    log.info("Updating article for title {}".format(article['title']))
    return repo.update_article(article, "admin")


def delete_article_by_id(article_id):
    log.info("Retrieving article for id {}".format(article_id))
    if article_id:
        return repo.delete_article(article_id)


def handle_get(event):
    path = event['path']
    try:
        if GET_ALL_ARTICLES == path:
            articles =  get_all_articles()
            return get_response(articles, "200")
        elif path.startswith(GET_ARTICLE):
            path_variables = event['pathParameters']
            article_id = path_variables['article-id']
            article = get_article_by_id(article_id)
            return get_response(article, "200")
    except Exception as ex:
        log.error(ex)
        log.error("Error {} occurred while handling POST request {} ".format(str(ex), path))
        traceback.print_exc()
        return get_response(str(ex), "422")


def handle_post(event):
    path = event['path']
    try:
        if CREATE_ARTICLE == path:
            article = json.loads(event['body'])
            article = create_article(article)
            return get_response(article, "201")
    except Exception as ex:
        log.error(ex)
        log.error("Error {} occurred while handling GET request {} ".format(str(ex), path))
        traceback.print_exc()
        return get_response(str(ex), "422")


def handle_put(event):
    path = event['path']
    try:
        if UPDATE_ARTICLE == path:
            article = json.loads(event['body'])
            article = update_article(article)
            return get_response(article, "200")
    except Exception as ex:
        log.error(ex)
        log.error("Error {} occurred while handling PUT request {} ".format(str(ex), path))
        traceback.print_exc()
        return get_response(str(ex), "422")


def handle_delete(event):
    path = event['path']
    try:
        if path.startswith(DELETE_ARTICLE):
            path_variables = event['pathParameters']
            article_id = path_variables['article-id']
            article_id = delete_article_by_id(article_id)
            return get_response(article_id, "200")
    except Exception as ex:
        log.error(ex)
        log.error("Error {} occurred while handling DELETE request {} ".format(str(ex), path))
        traceback.print_exc()
        return get_response(str(ex), "422")


method_handler_map = {"GET": handle_get, "POST": handle_post, "PUT": handle_put, "DELETE": handle_delete}


def handle_request(event):
    http_method = event['httpMethod']
    return method_handler_map[http_method](event)


def get_response(response, status):
    return {
        "statusCode": status,
        "body": json.dumps(response, default=json_serial),
    }


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
