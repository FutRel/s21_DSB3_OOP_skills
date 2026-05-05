import sys
import os

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
        @staticmethod
        def counts(data):
            heads = sum(item[0] for item in data)
            tails = sum(item[1] for item in data)
            return heads, tails
        
        @staticmethod
        def fractions(heads, tails):
            total = heads + tails
            if total == 0:
                return 0, 0
            head_fraction = heads / total
            tail_fraction = tails / total
            return head_fraction, tail_fraction

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    
    try:
        research = Research(sys.argv[1])
        data = research.file_reader()
        print(data)
        
        calc = research.Calculations()
        heads, tails = calc.counts(data)
        print(f"{heads} {tails}")
        
        head_frac, tail_frac = calc.fractions(heads, tails)
        print(f"{head_frac:.4f} {tail_frac:.4f}")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)