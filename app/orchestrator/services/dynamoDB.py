import boto3
from boto3.dynamodb.conditions import Key
from typing import Union, Dict


def query_rrtk(flight):
    """Query RESIBER_RRTK table, contains info about passengers."""
    dynamodb = connectToDynamodb()
    table = dynamodb.Table("RESIBER_RRTK")
    response = table.query(
        KeyConditionExpression=Key("flightid").eq(str(flight)),
    )
    return response["Items"]


def connectToDynamodb(region: str = 'eu-west-1'):
    return boto3.resource('dynamodb', region_name=region)


def getItem(table_name: str, keys: Dict[str, Union[str, int]]) -> Dict:
    dynamodb = connectToDynamodb()
    table = dynamodb.Table(table_name)
    return table.get_item(Key=keys)


def queryTable(table_name: str, key_condition_expression, filter_expression) -> Dict:
    dynamodb = connectToDynamodb()
    table = dynamodb.Table(table_name)
    return table.query(KeyConditionExpression=key_condition_expression, FilterExpression=filter_expression)


def scanTable(table_name: str, filter_expression, **kwargs) -> Dict:
    dynamodb = connectToDynamodb()
    table = dynamodb.Table(table_name)
    return table.scan(FilterExpression=filter_expression, **kwargs)
