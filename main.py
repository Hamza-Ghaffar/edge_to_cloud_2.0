from fastapi import Request, FastAPI
from fastapi.staticfiles import StaticFiles
import mariadb
from collections import defaultdict
import logging
import json
from pydantic import BaseModel

# Database connection details
db_connection = {
    'host': 'maria_db_2.0',  # Service name in docker-compose
    'port': 3306,            # Default MariaDB port
    'user': 'FHKaerntenMSCE23',  # User defined in MariaDB
    'password': 'RHMA-FHKaerntenMSCE23',  # Password defined in .env or init.sql
    'database': 'cloud_data_2.0'  # Database name
}

api_tags = [
    {
        'name': 'Get All Cameras Data',
        'description': 'Gets all the data for all cameras'
    },
    {
        'name': 'Post Cameras Data',
        'description': 'Saves the received data'
    },
    {
        'name': 'Post Cameras Data Static',
        'description': 'Saves the received data using Base Model'
    }
]

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI(
    title='Camera Dashboard API',
    version='0.1',
    description='API to get the camera data for dashboard',
    openapi_tags=api_tags
)
app.mount("/static", StaticFiles(directory="static"), name="static")


class Camera(BaseModel):
    cam1: int
    cam2: int
    cam3: int
    cam4: int
    cam5: int


@app.get('/getAll', tags=['Get All Cameras Data'])
async def get_all_data():
    connection = None
    cursor = None
    try:
        connection = mariadb.connect(**db_connection)
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT CameraId, DetectionTime, Detections FROM camera ORDER BY CameraId, DetectionTime;')
        result = cursor.fetchall()
        
        dataDict = defaultdict(list)
        for row in result:
            cameraId = row['CameraId']
            dataDict[cameraId].append({
                "detectionTime": row['DetectionTime'].strftime("%Y-%m-%d %H:%M:%S"),
                "detections": row['Detections']
            })
        
        json_data = [{"camId": cameraId, "data": data} for cameraId, data in dataDict.items()]
        return json_data

    except mariadb.Error as e:
        logger.error(f"Error fetching data from MariaDB: {e}")
        return {"error": f"Database error: {e}"}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.post('/pushDetections', tags=['Post Cameras Data'])
async def push_detections(request: Request):
    data = await request.json()
    connection = None
    cursor = None
    try:
        connection = mariadb.connect(**db_connection)
        cursor = connection.cursor()

        for key, value in data.items():
            logger.debug(f"Inserting data for CameraId: {key}, Detections: {value}")
            cursor.execute('INSERT INTO camera (CameraId, Detections) VALUES (?, ?)', (key, value))

        connection.commit()
        return {'message': 'success'}

    except mariadb.Error as e:
        logger.error(f"Error inserting data into MariaDB: {e}")
        return {"error": f"Database error: {e}"}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.post('/pushDetectionsStatic', tags=['Post Cameras Data Static'])
async def push_detections_static(camera: Camera):
    connection = None
    cursor = None
    try:
        connection = mariadb.connect(**db_connection)
        cursor = connection.cursor()

        cursor.execute('INSERT INTO camera (CameraId, Detections) VALUES (?, ?)', ('cam1', camera.cam1))
        cursor.execute('INSERT INTO camera (CameraId, Detections) VALUES (?, ?)', ('cam2', camera.cam2))
        cursor.execute('INSERT INTO camera (CameraId, Detections) VALUES (?, ?)', ('cam3', camera.cam3))
        cursor.execute('INSERT INTO camera (CameraId, Detections) VALUES (?, ?)', ('cam4', camera.cam4))
        cursor.execute('INSERT INTO camera (CameraId, Detections) VALUES (?, ?)', ('cam5', camera.cam5))

        connection.commit()
        return {'message': 'success'}

    except mariadb.Error as e:
        logger.error(f"Error inserting data into MariaDB: {e}")
        return {"error": f"Database error: {e}"}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.post('/pushDetections2')
async def push_detections2(request: Request):
    data = await request.json()
    connection = None
    cursor = None
    try:
        connection = mariadb.connect(**db_connection)
        cursor = connection.cursor()

        if isinstance(data, dict):
            dataItems = data
        else:
            dataItems = json.loads(data)

        for key, value in dataItems.items():
            cursor.execute('INSERT INTO camera (CameraId, Detections) VALUES (?, ?)', (key, value))

        connection.commit()
        return {'message': 'success'}

    except mariadb.Error as e:
        logger.error(f"Error inserting data into MariaDB: {e}")
        return {"error": f"Database error: {e}"}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
