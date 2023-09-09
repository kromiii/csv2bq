import os
import argparse
from google.cloud import bigquery

def upload_csv_to_bigquery(csv_file_path, project_id, dataset_id, table_id):
    # Create a BigQuery client
    client = bigquery.Client(project=project_id)

    # Check if the dataset exists, create it if necessary
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    if not client.get_dataset(dataset_ref):
        dataset = client.create_dataset(dataset)

    # # Create a BigQuery table
    table_ref = dataset.table(table_id)
    table = bigquery.Table(table_ref)
    table = client.create_table(table)

    # Load the CSV data into the table
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = True
    with open(csv_file_path, 'rb') as f:
        job = client.load_table_from_file(f, table_ref, job_config=job_config)
    job.result()

    print('CSV file uploaded to BigQuery successfully.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', help='Path to the CSV file')
    parser.add_argument('--project_id', help='Google Cloud project ID')
    parser.add_argument('--dataset_id', help='BigQuery dataset ID')
    parser.add_argument('--table_id', help='BigQuery table ID')
    args = parser.parse_args()

    upload_csv_to_bigquery(args.csv_file, args.project_id, args.dataset_id, args.table_id)
