import json
import boto3
import os

ENDPOINT_URL = os.environ.get('AWS_ENDPOINT_URL', 'http://localhost:4566')
dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL, region_name='us-east-1')
table = dynamodb.Table('Puntajes')

def handler(event, context):
    records = event.get('Records', [])
    for record in records:
        try:
            body = json.loads(record['body'])
            juego = body['juego']
            jugador = body['jugador']
            puntaje = int(body['puntaje'])

            table.put_item(
                Item={
                    'juego': juego,
                    'jugador': jugador,
                    'puntaje': puntaje
                }
            )
            print(f"Puntaje guardado: {jugador} - {juego}: {puntaje}")
        except Exception as e:
            print(f"Error procesando registro: {str(e)}")
            raise e

    return {'status': 'ok', 'processed': len(records)}
