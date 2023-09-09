# csv2bq

python package for uploading local csv files to google bigquery

## Installation

```bash
$ pip install csv2bq
```

## Prerequisites

Place your service account key file in `~/.config/gcloud/application_default_credentials.json`

## Usage

```bash
$ csv2bq sample.csv --project_id=sample --dataset_id=sample --table_id=sample
```

## Options

project_id: project id (default: current project id)
dataset_id: dataset id (required)
table_id: table id (required)
mode: append or overwrite (default: append)
auto_create_table: auto create table (default: True)
