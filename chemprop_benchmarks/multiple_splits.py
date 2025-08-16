import json
import random
import sys
import os

def parse_range(rng):
    """Convert "0-525" to [0,1,2,...,525]"""
    start, end = map(int, rng.split('-'))
    return list(range(start, end + 1))

def create_multiple_splits(input_file, num_splits=5, seed=42):
    # Set random seed for reproducibility
    random.seed(seed)
    
    # Generate output file path
    input_dir = os.path.dirname(input_file)
    output_file = os.path.join(input_dir, 'multiple_splits.json')
    
    # Load original split
    with open(input_file, 'r') as f:
        splits = json.load(f)
    
    base_split = splits[0]
    test_indices = parse_range(base_split['test'])
    train_indices = parse_range(base_split['train'])
    val_indices = parse_range(base_split['val'])
    
    # Combine train+val for shuffling (all non-test indices)
    non_test_indices = train_indices + val_indices
    n_train = len(train_indices)
    n_val = len(val_indices)
    
    multiple_splits = []
    
    # First split: keep original split exactly the same (in range format)
    original_split = {
        "test": base_split['test'],
        "train": base_split['train'],
        "val": base_split['val']
    }
    multiple_splits.append(original_split)
    
    # Remaining splits: shuffle train+val (as index lists)
    for i in range(num_splits - 1):
        # Shuffle the non-test indices
        shuffled = non_test_indices[:]
        random.shuffle(shuffled)
        
        # Split back maintaining original counts
        new_train = shuffled[:n_train]
        new_val = shuffled[n_train:]
        
        split = {
            "test": test_indices,     # Keep test as list of indices
            "train": new_train,       # New train indices
            "val": new_val           # New val indices
        }
        multiple_splits.append(split)
    
    # Save
    with open(output_file, 'w') as f:
        json.dump(multiple_splits, f, indent=2)
    
    print(f"Created {num_splits} splits and saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python multiple_splits.py /path/to/splits.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    create_multiple_splits(input_file)
