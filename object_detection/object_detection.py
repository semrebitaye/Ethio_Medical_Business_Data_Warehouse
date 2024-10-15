import os
import logging
import yaml
import cv2
import torch
import psycopg2

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/object_detection_db.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Load configuration
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

db_config = config['postgres']

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )
        logging.info('Connected to PostgreSQL database')
        return conn
    except Exception as e:
        logging.error(f'Error connecting to database: {str(e)}')
        return None

def create_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detection_data (
                    id SERIAL PRIMARY KEY,
                    image_path TEXT,
                    box_coordinates TEXT,
                    confidence_score FLOAT,
                    class_label TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            logging.info('Table detection_data is ready')
    except Exception as e:
        logging.error(f'Error creating table: {str(e)}')

def detect_objects_in_images(image_paths):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Load YOLOv5s model
    results = []
    for image_path in image_paths:
        img = cv2.imread(image_path)  # Read image using OpenCV
        result = model(img)  # Perform object detection
        results.append((image_path, result))
    return results

def process_detection_results(results):
    processed_results = []
    for image_path, result in results:
        for *box, conf, cls in result.pred[0]:
            box_coords = ','.join(map(str, box))
            confidence_score = float(conf)
            class_label = int(cls)
            processed_results.append((image_path, box_coords, confidence_score, class_label))
    return processed_results

def store_detection_data_to_database(conn, detection_data):
    try:
        with conn.cursor() as cursor:
            insert_query = """
                INSERT INTO detection_data (image_path, box_coordinates, confidence_score, class_label)
                VALUES (%s, %s, %s, %s);
            """
            for data in detection_data:
                cursor.execute(insert_query, data)
            conn.commit()
            logging.info(f'Successfully inserted {len(detection_data)} records into database')
    except Exception as e:
        logging.error(f'Error storing data to database: {str(e)}')

if __name__ == '__main__':
    image_directory = 'images'
    image_paths = [os.path.join(image_directory, img) for img in os.listdir(image_directory) if img.endswith(('.jpg', '.jpeg', '.png'))]

    if image_paths:
        logging.info(f'Found {len(image_paths)} images in {image_directory}')

        results = detect_objects_in_images(image_paths)
        processed_results = process_detection_results(results)

        logging.info(f'Processed detection results for {len(processed_results)} images')

        conn = connect_to_db()
        if conn:
            create_table(conn)
            store_detection_data_to_database(conn, processed_results)
            conn.close()
        else:
            logging.error('Could not connect to database')
    else:
        logging.warning(f'No images found in {image_directory}')
