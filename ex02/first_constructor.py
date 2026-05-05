import sys
import os

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def file_reader(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError("Not found")
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            
            if len(lines) == 0:
                raise ValueError("Empty")
            
            header = lines[0].strip().split(',')
            if len(header) != 2:
                raise ValueError("Invalid format")
            
            for i in range(1, len(lines)):
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
        
        with open(self.file_path, 'r') as file:
            return file.read()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    
    try:
        research = Research(sys.argv[1])
        print(research.file_reader().strip())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
