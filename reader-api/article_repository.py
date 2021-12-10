from datetime import datetime

import boto3
import logging

log = logging.getLogger()
dynamodb_client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE = "blog-article"


def get_article_by_id(article_id):
    log.info("Retrieving article for id  {}".format(article_id))
    table = dynamodb.Table(DYNAMODB_TABLE)
    response = table.get_item(Key={'id': article_id})
    log.info("get_article_by_id response {}".format(response))
    return response['Item']


def get_all_articles():
    log.info("Retrieving all articles")
    table = dynamodb.Table(DYNAMODB_TABLE)
    response = table.scan(ProjectionExpression="id, title, createdBy")
    return response['Items']
