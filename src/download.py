import os
import requests

RAW_DATA_URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
DEFAULT_OUTPUT_PATH = os.path.join("data", "raw", "Telco-Customer-Churn.csv")


def download_raw_data(url: str = RAW_DATA_URL, output_path: str = DEFAULT_OUTPUT_PATH) -> str:
    """
    Downloads the raw IBM Telco Customer Churn CSV file from the given URL
    and saves it to the specified output path without modification.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


if __name__ == "__main__":
    path = download_raw_data()
    print(f"Downloaded raw dataset to {path}")
