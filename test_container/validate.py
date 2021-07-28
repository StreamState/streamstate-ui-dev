import sys

sys.path.append("/opt/spark/work-dir/")
from dev_app import create_json_objects_for_unit_testing
import json
from streamstate_utils.structs import (
    FileStruct,
    InputStruct,
    OutputStruct,
    TableStruct,
    KafkaStruct,
)
from typing import List
import requests
import yaml
import base64
import os


def _push_results_to_streamstate(
    organization: str,
    inputs: List[InputStruct],
    outputs: OutputStruct,
    assertions: List[dict],
    kafka: KafkaStruct,
    table: TableStruct,
    token: str,
    process_py_location: str = "process.py",
):
    url = f"https://{organization}.streamstate.org/api/deploy"
    with open(process_py_location, "r") as process:
        pythoncode = base64.b64encode(process.read())
    data = {
        "pythoncode": pythoncode,
        "inputs": [input.dict() for input in inputs],
        "outputs": outputs,
        "assertions": assertions,
        "kafka": kafka.dict(),
        "table": table.dict(),
    }
    headers = {"Authorization": f"Bearer {token}"}
    requests.post(url, data=data, headers=headers)


def _load_configuration(config_location: str):
    with open(config_location, "r") as config:
        conf = yaml.safe_load(config)
    kafka = conf.get("kafka")
    assert kafka is not None

    kafka["confluent_api_key"] = os.getenv(
        "CONFLUENT_API_KEY", kafka["confluent_api_key"]
    )
    kafka["confluent_secret"] = os.getenv("CONFLUENT_SECRET", kafka["confluent_secret"])

    outputs = conf.get("outputs")
    assert outputs is not None
    table = conf.get("table")
    assert table is not None
    app_name = conf.get("appname")
    return KafkaStruct(**kafka), OutputStruct(**outputs), TableStruct(**table), app_name


if __name__ == "__main__":
    [
        _,
        app_name,  #
        file_struct,
        input_struct,
    ] = sys.argv
    file_info = FileStruct(**json.loads(file_struct))
    input_info = [InputStruct(**v) for v in json.loads(input_struct)]
    results = create_json_objects_for_unit_testing(
        app_name,
        file_info.max_file_age,
        input_info,
    )
    print(results)
    token = os.getenv("TOKEN")
    organization = os.getenv("ORGANIZATION")

    if token is not None and organization is not None:
        kafka, outputs, table, app_name = _load_configuration("./config/config.yml")
        _push_results_to_streamstate(
            organization,
            results["inputs"],
            outputs,
            results["assertions"],
            kafka,
            table,
            token,
            "process.py",
        )
