# TP3 - GameCloud: Arquitectura Serverless ☁️🎮

Este repositorio contiene el código fuente, las políticas IAM y los scripts de despliegue para la resolución del Trabajo Práctico 3 de Computación en la Nube. La solución implementa un backend orientado a eventos y un frontend estático para registrar y consultar puntajes de videojuegos.

## 🏗️ Arquitectura y Servicios Utilizados
El proyecto fue desplegado y testeado localmente utilizando **MiniStack / LocalStack** sobre **WSL 2 (Ubuntu)**. 
- **Amazon S3 & CloudFront:** Hosting del frontend estático (`index.html`).
- **Amazon API Gateway:** Exposición de endpoints REST (`/puntajes` y `/ranking`).
- **AWS Lambda:** Cómputo serverless para procesamiento e ingesta de datos.
- **Amazon SQS & DLQ:** Encolamiento de puntajes para tolerancia a fallos y nivelación de carga.
- **Amazon DynamoDB:** Persistencia NoSQL de los rankings (PAY_PER_REQUEST).
- **AWS IAM:** Políticas de mínimo privilegio para la ejecución de Lambdas.

## 🚀 Instrucciones para reproducir la práctica

### 1. Requisitos previos
- Docker y Docker Compose instalados.
- AWS CLI v2 instalado y configurado con credenciales de prueba.
- MiniStack o LocalStack corriendo en el puerto `4566`.

### 2. Despliegue de la infraestructura
El repositorio contiene las carpetas con el código y configuraciones necesarias. Para recrear el entorno, ejecutar secuencialmente los comandos de AWS CLI apuntando al endpoint local (`--endpoint-url http://localhost:4566`):

1. **S3:** Crear el bucket `gamecloud-web` y subir el archivo ubicado en `/web/index.html`.
2. **DynamoDB:** Crear la tabla `Puntajes` con `juego` (HASH) y `jugador` (RANGE).
3. **SQS:** Crear las colas `puntajes-dlq` y `puntajes` (vinculando la DLQ mediante la RedrivePolicy).
4. **IAM:** Crear el rol de ejecución aplicando los documentos JSON ubicados en la carpeta `/iam`.
5. **Lambda:** Desplegar las funciones comprimidas en `.zip` y configurar el `event-source-mapping` para que SQS dispare la función de procesamiento.
6. **API Gateway:** Crear los recursos, métodos e integraciones proxy, y desplegar en el stage `prod`.

### 3. Prueba del Frontend
Una vez desplegado el API Gateway, se debe actualizar la constante `API` en el archivo `web/index.html` con el nuevo `API_ID` generado, y volver a subir el archivo al bucket S3. Luego, acceder al frontend a través del navegador para visualizar las tablas e insertar puntajes.

*Nota: Puede ser necesario habilitar una extensión de CORS en el navegador para pruebas locales.*
