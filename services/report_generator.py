"""Report generation engine mock data providers."""

import os
import random

import pandas as pd


def generate_sales_dataframe(total_records: int) -> pd.DataFrame:
    """
    Builds a Pandas DataFrame populated with mock sales transactions.
    """

    data = {
        "Transaction_ID": [
            f"TRX-{random.randint(100000, 999999)}" for _ in range(total_records)
        ],
        "Product": [
            random.choice(["Laptop", "Smartphone", "Monitor", "Keyboard", "Mouse"])
            for _ in range(total_records)
        ],
        "Amount": [
            round(random.uniform(20.0, 2500.0), 2) for _ in range(total_records)
        ],
        "Status": [
            random.choice(["COMPLETED", "PENDING", "CANCELLED"])
            for _ in range(total_records)
        ],
    }
    return pd.DataFrame(data)


def export_dataframe_to_csv(
    df: pd.DataFrame, filename: str, output_dir: str = "downloads"
) -> str:
    """
    Persists a DataFrame into a universal UTF-8 CSV file.
    """

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)
    df.to_csv(file_path, index=False, encoding="utf-8")
    return file_path
