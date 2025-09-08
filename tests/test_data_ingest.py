# tests/test_data_ingest.py

"""
Unit tests for HelixAgent Data Ingestion
----------------------------------------
Tests loading, preprocessing, and splitting dataset functionality.
"""

import os
import pandas as pd
import pytest
from src.data_ingest import DataIngestor


# Create a temporary sample dataset for testing
@pytest.fixture
def sample_csv(tmp_path):
    data = {
        "Text": [
            "The movie was great!",
            "The food was awful.",
            "Loved the service.",
            "Never going back.",
            "What a fantastic product!"
        ],
        "Label": [1, 0, 1, 0, 1]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "sample_dataset.csv"
    df.to_csv(file_path, index=False)
    return str(file_path)


def test_load_data(sample_csv):
    ingestor = DataIngestor(sample_csv)
    df = ingestor.load_data()
    assert not df.empty
    assert df.shape[0] == 5
    assert "Text" in df.columns


def test_preprocess(sample_csv):
    ingestor = DataIngestor(sample_csv)
    df = ingestor.load_data()
    df = ingestor.preprocess()
    assert "text" in df.columns  # lowercase normalization
    assert df.isnull().sum().sum() == 0


def test_split_data(sample_csv):
    ingestor = DataIngestor(sample_csv, test_size=0.2, val_size=0.25)
    df = ingestor.load_data()
    df = ingestor.preprocess()
    train, val, test = ingestor.split_data()

    assert len(train) > 0
    assert len(val) > 0
    assert len(test) > 0
    total = len(train) + len(val) + len(test)
    assert total == df.shape[0]
