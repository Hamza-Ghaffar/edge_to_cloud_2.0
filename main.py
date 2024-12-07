from fastapi import Request, FastAPI
from fastapi.staticfiles import StaticFiles
import mariadb  # Use the MariaDB connector instead of pymysql and mysql
from collections import defaultdict
import logging

# Database connection details directly in the code
db_connection = {
    'host': 'maria_db_2.0',  # Correctly using the service name in docker-compose
    'port': 3306,            # Default MariaDB port inside container
    'user': 'FHKaerntenMSCE23',  # The user created in MariaDB
    'password': 'RHMA-FHKaerntenMSCE23',  # The password defined in .env or init.sql
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
    }
]

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI(title='Camera Dashboard API', version='0.1', description='API to get the camera data for dashboard', openapi_tags=api_tags)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/getAll', tags=['Get All Cameras Data'])
async def get_all_data():
    cursor = None  # Initialize cursor to avoid UnboundLocalError
    connection = None  # Initialize connection to avoid UnboundLocalError
    try:
        # Connect to MariaDB using hardcoded details
        connection = mariadb.connect(**db_connection)
        cursor = connection.cursor(dictionary=True)  # Use dictionary for easier access
        cursor.execute('SELECT CameraId, DetectionTime, Detections FROM camera ORDER BY CameraId, DetectionTime;')
        result = cursor.fetchall()

        # Organize data by CameraId
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
        logger.error(f"Error connecting to MariaDB: {e}")
        return {"error": f"Database error: {e}"}

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.post('/pushDetections', tags=['Post Cameras Data'])
async def send_message(request: Request):
    data = await request.json()
    logger.debug(data)
    cursor = None  # Initialize cursor to avoid UnboundLocalError
    connection = None  # Initialize connection to avoid UnboundLocalError
    try:
        # Connect to MariaDB using hardcoded details
        connection = mariadb.connect(**db_connection)
        cursor = connection.cursor()

        # Insert each camera's detections into the database
        for key, value in data.items():
            logger.debug(f"Inserting data for CameraId: {key}, Detections: {value}")
            cursor.execute('INSERT INTO camera (CameraId, Detections) VALUES (%s, %s)', (key, value))

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
