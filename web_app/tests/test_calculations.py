import pytest
from utils import compute_csv
import pandas as pd

def test_compute_csv():
    data = {
        'A': [1, 3, 5, 8],
        'O': ['+', '*', '-', '/'],
        'B': [2, 4, 6, 4]
    }
    df = pd.DataFrame(data)
    df.to_csv('test.csv', index=False)
    
    result = compute_csv('test.csv')
    assert result == 16.0
