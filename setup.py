from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()

setup(
    name="csv2bq",
    description="upload local csv file to bigquery",
    long_description=readme,
    long_description_content_type="text/markdown",
    version="0.1.2",
    author="Hiroyuki Kuromiya",
    author_email="15026387+kromiii@users.noreply.github.com",
    packages=["csv2bq"],
    install_requires=["google-cloud-bigquery"],
    entry_points={
        "console_scripts": [
            "csv2bq = csv2bq.csv2bq:upload_csv_to_bigquery",
        ]
    },
)
