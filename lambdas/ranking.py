import json
import boto3
import os
from decimal import Decimal

ENDPOINT_URL = os.environ.get('AWS_ENDPOINT_URL', 'http://localhost:4566')
dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL, region_name='us-east-1')
table = dynamodb.Table('Puntajes')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def handler(event, context):
    try:
        params = event.get('queryStringParameters') or {}
        juego_filter = params.get('juego') if isinstance(params, dict) else None

        response = table.scan()
        items = response.get('Items', [])

        if juego_filter:
            items = [item for item in items if item.get('juego') == juego_filter]

        items.sort(key=lambda x: x.get('puntaje', 0), reverse=True)

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(items, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
