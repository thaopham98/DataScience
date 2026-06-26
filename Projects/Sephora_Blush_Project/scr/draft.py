from pathlib import Path

## Looking for the path
print(f"Path Parent[0]: {Path(__file__).resolve().parents[0]}") # current parent
print(f"Path Parent[1]: {Path(__file__).resolve().parents[1]}") # grandparent
print(f"Path Parent[2]: {Path(__file__).resolve().parents[2]}") # grea-grandparent