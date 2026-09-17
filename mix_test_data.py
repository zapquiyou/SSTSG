import shutil
import os

source_files = [
    'generate_data/test/generate_test_1000.txt',
    'generate_data/test/generate_test_1000.jsonl',
    'fix_data/test/fix_test_1000.txt',
    'fix_data/test/fix_test_1000.jsonl',
    'verify_data/test/verify_test_1000.txt',
    'verify_data/test/verify_test_1000.jsonl'
]

destination_dir = 'mix_data/test'

os.makedirs(destination_dir, exist_ok=True)

for file in source_files:
    shutil.copy(file, destination_dir)
    print(f"Copied {file} to {destination_dir}")
