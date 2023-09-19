import os
import argparse
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

def upload_csv_to_bigquery():
    """Uploads a CSV file to a given BigQuery table."""
    # Load arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', help='Path to the CSV file')
    parser.add_argument('--project_id', help='Google Cloud project ID')
    parser.add_argument('--dataset_id', help='BigQuery dataset ID')
    parser.add_argument('--table_id', help='BigQuery table ID')
    parser.add_argument('--mode', help='append or overwrite', default='append')
    parser.add_argument('--auto_create_table', help='auto create table', default='True')    

    args = parser.parse_args()
    csv_file_path = args.csv_file
    project_id = args.project_id
    dataset_id = args.dataset_id
    table_id = args.table_id
    mode = args.mode
    auto_create_table = args.auto_create_table == 'True'

    # Create a BigQuery client
    client = bigquery.Client(project=project_id)

    # Check if the dataset exists
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)

    # Check if the table exists, create it if necessary
    table_ref = dataset.table(table_id)
    try:
        client.get_table(table_ref)
    except NotFound:
        table = bigquery.Table(table_ref)
        if auto_create_table:
            table = client.create_table(table)
        else:
            raise Exception('Table not found: {}.{}.{}'.format(project_id, dataset_id, table_id))

    # Load the CSV data into the table
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = True
    if mode == 'append':
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    elif mode == 'overwrite':
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    
    with open(csv_file_path, 'rb') as f:
        job = client.load_table_from_file(f, table_ref, job_config=job_config)
    job.result()

    print('CSV file uploaded to BigQuery successfully.')


if __name__ == '__main__':
    upload_csv_to_bigquery()
