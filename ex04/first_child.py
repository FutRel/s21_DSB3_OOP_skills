import os
import sys
from random import randint

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def file_reader(self, has_header=True):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError("Not found")
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            
            if len(lines) == 0:
                raise ValueError("Empty")
            
            result = []
            start_index = 1 if has_header else 0
            
            for i in range(start_index, len(lines)):
                line = lines[i].strip()
                if not line:
                    continue
                values = line.split(',')
                if len(values) != 2:
                    raise ValueError(f"Invalid format {i}")
                if values[0] not in ['0', '1'] or values[1] not in ['0', '1']:
                    raise ValueError(f"Invalid values {i}")
                if values[0] == values[1]:
                    raise ValueError(f"Both values {i}")
                
                result.append([int(values[0]), int(values[1])])
            
            return result

class Calculations:
    def __init__(self, data):
        self.data = data
    
    def counts(self):
        heads = sum(item[0] for item in self.data)
        tails = sum(item[1] for item in self.data)
        return heads, tails
    
    def fractions(self, heads, tails):
        total = heads + tails
        if total == 0:
            return 0, 0
        head_fraction = heads / total
        tail_fraction = tails / total
        return head_fraction, tail_fraction

class Analytics(Calculations):
    def predict_random(self, num_predictions):
        predictions = []
        for _ in range(num_predictions):
            if randint(0, 1) == 0:
                predictions.append([0, 1])
            else:
                predictions.append([1, 0])
        return predictions
    
    def predict_last(self):
        return self.data[-1] if self.data else None

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        sys.exit(1)
    
    try:
        research = Research(sys.argv[1])
        data = research.file_reader()
        print(data)
        
        analytics = Analytics(data)
        
        heads, tails = analytics.counts()
        print(f"{heads} {tails}")
        
        head_frac, tail_frac = analytics.fractions(heads, tails)
        print(f"{head_frac:.4f} {tail_frac:.4f}")
        
        predictions = analytics.predict_random(3)
        print(predictions)
        
        last_prediction = analytics.predict_last()
        print(last_prediction)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)