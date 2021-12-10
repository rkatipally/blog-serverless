import json
import traceback
import article_repository as repo
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
GET_ALL_ARTICLES = "/reader/article/all"
GET_ARTICLE = "/reader/article/"


def get_article_by_id(article_id):
    log.info("Retrieving article for id {}".format(article_id))
    if article_id:
        return repo.get_article_by_id(article_id)


def get_all_articles():
    log.info("Retrieving all articles")
    return repo.get_all_articles()


def handle_get(event):
    path = event['path']
    try:
        if GET_ALL_ARTICLES == path:
            articles = get_all_articles()
            return get_response(articles, "200")
        elif path.startswith(GET_ARTICLE):
            path_variables = event['pathParameters']
            article_id = path_variables['article-id']
            article = get_article_by_id(article_id)
            return get_response(article, "200")
    except Exception as ex:
        log.error(ex)
        log.error("Error {} occurred while handling GET request {} ".format(str(ex), path))
        traceback.print_exc()
        return get_response(str(ex), "422")


method_handler_map = {"GET": handle_get}


def handle_reader_request(event):
    http_method = event['httpMethod']
    log.info("Handling {} method for reader".format(http_method))
    return method_handler_map[http_method](event)


def get_response(response, status):
    return {
        "statusCode": status,
        "body": json.dumps(response),
    }
