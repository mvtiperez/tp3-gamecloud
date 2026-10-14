import json
import boto3
import os

ENDPOINT_URL = os.environ.get('AWS_ENDPOINT_URL', 'http://localhost:4566')
sqs = boto3.client('sqs', endpoint_url=ENDPOINT_URL, region_name='us-east-1')
QUEUE_URL = os.environ.get('QUEUE_URL', 'http://localhost:4566/000000000000/puntajes')

def handler(event, context):
    try:
        body = event.get('body', '{}')
        if isinstance(body, str):
            data = json.loads(body)
        else:
            data = body

        juego = data.get('juego')
        jugador = data.get('jugador')
        puntaje = data.get('puntaje')

        if not juego or not jugador or puntaje is None:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Faltan campos obligatorios: juego, jugador, puntaje'})
            }

        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({'juego': juego, 'jugador': jugador, 'puntaje': int(puntaje)})
        )

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'mensaje': 'Puntaje recibido y encolado correctamente'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
