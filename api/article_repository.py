from datetime import datetime

import boto3
import logging
log = logging.getLogger()
dynamodb_client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE = "blog-article"


def create_article(article, user_id):
    time_now = datetime.now(tz=None)
    table = dynamodb.Table(DYNAMODB_TABLE)
    article['id'] = time_now.strftime('%Y%m%d%H%M%S')
    article['createdBy'] = user_id
    article['createdTimestamp'] = time_now.isoformat()
    response = table.put_item(Item=article)
    log.info("Article created with id {}".format(article['id']))
    return article


def get_article_by_id(article_id):
    log.info("Retrieving article for id  {}".format(article_id))
    table = dynamodb.Table(DYNAMODB_TABLE)
    response = table.get_item(Key={'id': article_id})
    log.info("get_article_by_id response {}".format(response))
    return response['Item']


def delete_article(article_id):
    log.info("Deleting article for id  {}".format(article_id))
    table = dynamodb.Table(DYNAMODB_TABLE)
    response = table.delete_item(Key={'id': article_id})
    log.info("delete_article response {}".format(response))
    return article_id


def update_article(article, user_id):
    article['updatedBy'] = user_id
    article['updatedTimestamp'] = datetime.now().isoformat()
    a, v = get_update_params(article)
    table = dynamodb.Table(DYNAMODB_TABLE)
    response = table.update_item(Key={'id': article['id']}, UpdateExpression=a, ExpressionAttributeValues=dict(v))
    return article


def get_all_articles():
    log.info("Retrieving all articles")
    table = dynamodb.Table(DYNAMODB_TABLE)
    response = table.scan(ProjectionExpression="id, title, createdBy")
    return response['Items']


def get_update_params(body):
    """Given a dictionary we generate an update expression and a dict of values
    to update a dynamodb table.

    Params:
        body (dict): Parameters to use for formatting.

    Returns:
        update expression, dict of values.
    """
    update_expression = ["set "]
    update_values = dict()

    for key, val in body.items():
        if key != 'id':
            update_expression.append(f" {key} = :{key},")
            update_values[f":{key}"] = val

    return "".join(update_expression)[:-1], update_values
