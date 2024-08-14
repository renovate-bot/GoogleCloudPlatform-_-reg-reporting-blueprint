# Copyright 2023 The Reg Reporting Blueprint Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Composer DAG to excute the Flashing Detection workflow

import datetime

from airflow.models import Variable

from dag_utils.tools import DBTComposerPodOperator, ComposerPodOperator
from airflow.models import Param
from airflow.decorators import dag


# Project and region for the repository
PROJECT_ID = Variable.get("PROJECT_ID")
REGION = Variable.get("REGION")

# GCS Ingest Bucket
GCS_INGEST_BUCKET = Variable.get("INGEST_BUCKET")

# BigQuery location
BQ_LOCATION = Variable.get("BQ_LOCATION")

# Tag to run (default is latest if not set)
TAG = Variable.get("tag", default_var="latest")

# Repository
REPO = Variable.get("REPO")


# Define the DAG
@dag(
    schedule_interval="0 3 * * *",
    catchup=False,
    start_date=datetime.datetime(2022, 1, 1),
    default_args={
        "retries": 2
    },
    params={
        'tag': Param(
            default=TAG,
            type='string',
        ),
        'repo': Param(
            default=REPO,
            type='string',
        ),
    },
)
def flashing_detection():

    generate_data_job = ComposerPodOperator(
        task_id='flashing-detection-generate-data',
        name='flashing-detection-generate-data',
        image='{{ params.repo }}/flashing-detection-data-generator:{{ params.tag }}',
        arguments=[
            # The project where the data will be ingested
            '--project_id', PROJECT_ID,
            # The BQ dataset where the data will be ingested
            '--bq_dataset', 'regrep_source',
            # The date to generate
            '--date', '{{ dag_run.logical_date | ds }}',
        ],
        env_vars={
            'PROJECT_ID': PROJECT_ID,
        },
    )

    run_flashing_report = DBTComposerPodOperator(
        task_id='transform-data',
        name='transform-data',
        image='{{ params.repo }}/flashing-detection-dbt:{{ params.tag }}',
        cmds=[
            '/bin/bash',
            '-xc',
            '&&'.join([
                'dbt run',
                'dbt docs generate --static',
            ]),
        ],
        env_vars={
            'PROJECT_ID': PROJECT_ID,
            'BQ_LOCATION': BQ_LOCATION,
            'REGION': REGION,
            'GCS_INGEST_BUCKET': GCS_INGEST_BUCKET,
        },
    )

    test_flashing_report = DBTComposerPodOperator(
        task_id='data-quality-test',
        name='data-quality-test',
        image='{{ params.repo }}/flashing-detection-dbt:{{ params.tag }}',
        cmds=[
            '/bin/bash',
            '-xc',
            '&&'.join([
                'dbt --no-use-colors test',
                'dbt docs generate --static',
            ]),
        ],
        env_vars={
            'PROJECT_ID': PROJECT_ID,
            'BQ_LOCATION': BQ_LOCATION,
            'REGION': REGION,
            'GCS_INGEST_BUCKET': GCS_INGEST_BUCKET,
        },
    )

    generate_data_job >> run_flashing_report >> test_flashing_report


flashing_detection()
