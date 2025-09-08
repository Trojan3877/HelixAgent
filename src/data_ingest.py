# src/data_ingest.py

"""
Data Ingestion Pipeline for HelixAgent
--------------------------------------
Handles dataset loading, preprocessing, and splitting.
Supports CSV files and can be extended for JSON, APIs, etc.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from utils.logger import setup_logger

log = setup_logger()


class DataIngestor:
    def __init__(self, file_path: str, test_size: float = 0.2, val_size: float = 0.1, random_state: int = 42):
        """
        Initialize data ingestion pipeline.

        Args:
            file_path (str): Path to dataset file (CSV).
            test_size (float): Fraction of data to reserve for test split.
            val_size (float): Fraction of data to reserve for validation.
            random_state (int): Random seed for reproducibility.
        """
        self.file_path = file_path
        self.test_size = test_size
        self.val_size = val_size
        self.random_state = random_state
        self.df = None

    def load_data(self):
        """Load dataset from CSV"""
        try:
            self.df = pd.read_csv(self.file_path)
            log.info(f"Loaded dataset: {self.file_path} | Shape: {self.df.shape}")
            return self.df
        except Exception as e:
            log.error(f"Failed to load dataset: {e}")
            raise

    def preprocess(self):
        """
        Example preprocessing:
        - Drop null values
        - Normalize column names
        Extend with NLP/text cleaning for real use.
        """
        if self.df is None:
            raise ValueError("No dataset loaded. Run load_data() first.")

        self.df = self.df.dropna()
        self.df.columns = [col.strip().lower() for col in self.df.columns]
        log.info("Preprocessed dataset (removed nulls, normalized headers).")
        return self.df

    def split_data(self):
        """Split dataset into train, validation, and test sets"""
        if self.df is None:
            raise ValueError("No dataset loaded. Run load_data() first.")

        train_df, test_df = train_test_split(self.df, test_size=self.test_size, random_state=self.random_state)
        train_df, val_df = train_test_split(train_df, test_size=self.val_size, random_state=self.random_state)

        log.info(
            f"Split data -> Train: {train_df.shape}, Validation: {val_df.shape}, Test: {test_df.shape}"
        )
        return train_df, val_df, test_df
        

# Example usage:
# ingestor = DataIngestor("data/sample_dataset.csv")
# df = ingestor.load_data()
# df = ingestor.preprocess()
# train, val, test = ingestor.split_data()
