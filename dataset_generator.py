# dataset_generator.py - Generate test datasets similar to find_match_average.dat

import csv
import random
from pathlib import Path


class DatasetGenerator:
    """Generate CSV datasets similar to find_match_average.dat used in testing"""

    def __init__(self):
        self.columns = ['a', 'b', 'c', 'd', 'e', 'value']

    def generate_dataset(self, num_rows=100_000, output_file="test_dataset.dat"):
        """
        Args:
            num_rows: Number of data rows to generate (default: 100K rows ≈ 4MB)
            output_file: Output filename
        """
        print(f"Generating dataset with {num_rows:,} rows...")

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)

            # header
            writer.writerow(self.columns)

            # rows
            for i in range(num_rows):
                row = [
                    random.randint(1, 999999),  # column a
                    random.randint(1, 999999),  # column b
                    random.randint(1, 999999),  # column c
                    random.randint(1, 999999),  # column d
                    random.randint(1, 999999),  # column e
                    random.randint(100000, 999999)  # value column
                ]
                writer.writerow(row)

                if (i + 1) % 100000 == 0:
                    print(f"  Generated {i + 1:,} rows...")

        file_size_mb = Path(output_file).stat().st_size / (1024 * 1024)
        print(f"✅ Generated {output_file} ({file_size_mb:.1f} MB)")
        return output_file


if __name__ == "__main__":
    generator = DatasetGenerator()

    print(" \nDataset Generator\n")
    n = input("How many records do you want to generate? (default: 100k rows ≈ 4MB): ")
    if n == '':
        n = '100000'
    generator.generate_dataset(int(n), output_file="dataset.csv")

