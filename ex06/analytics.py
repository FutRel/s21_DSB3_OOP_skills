import os
import logging
import requests
import config
import json
from random import randint

# Configure logging
logging.basicConfig(
    filename='analytics.log',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Research:
    def __init__(self, file_path):
        logging.debug(f"Initializing: {file_path}")
        self.file_path = file_path
    
    def file_reader(self, has_header=True):
        logging.debug(f"File: {self.file_path}, has_header: {has_header}")
        if not os.path.exists(self.file_path):
            error_msg = f"Not found: {self.file_path}"
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            
            if len(lines) == 0:
                error_msg = "Empty"
                logging.error(error_msg)
                raise ValueError(error_msg)
            
            result = []
            start_index = 1 if has_header else 0
            
            for i in range(start_index, len(lines)):
                line = lines[i].strip()
                if not line:
                    continue
                values = line.split(',')
                if len(values) != 2:
                    error_msg = f"Invalid format {i}"
                    logging.error(error_msg)
                    raise ValueError(error_msg)
                if values[0] not in ['0', '1'] or values[1] not in ['0', '1']:
                    error_msg = f"Invalid values {i}"
                    logging.error(error_msg)
                    raise ValueError(error_msg)
                if values[0] == values[1]:
                    error_msg = f"Both values {i}"
                    logging.error(error_msg)
                    raise ValueError(error_msg)
                
                result.append([int(values[0]), int(values[1])])
            
            logging.debug(f"Read {len(result)} records")
            return result
    
    def send_to_telegram(self, message):
        logging.debug(f"Send: {message}")
        try:
            payload = {
                'chat_id': config.TELEGRAM_CHAT_ID,
                'text': message
            }
            response = requests.post(config.TELEGRAM_WEBHOOK_URL, data=payload)
            if response.status_code != 200:
                logging.error(f"Failed to send: {response.text}")
            else:
                logging.debug("Success")
            logging.info(f"Message: {message}")
        except Exception as e:
            logging.error(f"Error: {e}")

class Calculations:
    def __init__(self, data):
        logging.debug(f"{len(data)} records")
        self.data = data
    
    def counts(self):
        logging.debug("Calculating heads and tails")
        heads = sum(item[0] for item in self.data)
        tails = sum(item[1] for item in self.data)
        logging.debug(f"heads={heads}, tails={tails}")
        return heads, tails
    
    def fractions(self, heads, tails):
        logging.debug(f"Calculating fractions heads={heads}, tails={tails}")
        total = heads + tails
        if total == 0:
            logging.warning("Total count zero")
            return 0, 0
        head_fraction = heads / total * 100
        tail_fraction = tails / total * 100
        logging.debug(f"Fractions calculated: head_fraction={head_fraction:.2f}%, tail_fraction={tail_fraction:.2f}%")
        return head_fraction, tail_fraction

class Analytics(Calculations):
    def predict_random(self, num_predictions):
        logging.debug(f"Generating {num_predictions}")
        predictions = []
        for _ in range(num_predictions):
            if randint(0, 1) == 0:
                predictions.append([0, 1])
            else:
                predictions.append([1, 0])
        logging.debug(f"Generated {len(predictions)}")
        return predictions
    
    def predict_last(self):
        logging.debug("Getting last prediction")
        result = self.data[-1] if self.data else None
        logging.debug(f"Last prediction: {result}")
        return result
    
    def save_file(self, data, filename, extension):
        logging.debug(f"Saving: {filename}.{extension}")
        full_filename = f"{filename}.{extension}"
        try:
            with open(full_filename, 'w') as file:
                file.write(data)
            logging.info(f"Success: {full_filename}")
            return True
        except Exception as e:
            logging.error(f"Error{full_filename}: {e}")
            return False