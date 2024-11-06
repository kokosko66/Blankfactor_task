import pandas as pd

def compute_csv(file_path):
    df = pd.read_csv(file_path)
    total = 0

    for index, row in df.iterrows():
        a, op, b = row['A'], row['O'], row['B']
        if op == '+':
            total += a + b
        elif op == '-':
            total += a - b
        elif op == '*':
            total += a * b
        elif op == '/':
            total += a / b
        else:
            raise ValueError(f"Unsupported operator: {op}")

    return total
