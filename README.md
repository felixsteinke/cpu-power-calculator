# CPU Power Calculator

FastAPI for the Green Coding Berlin - XGBoost PowerModel.

## Table of Content

* [Dockerfile](Dockerfile)
* [main.py (FastAPI)](main.py)
* [requirements.txt (Dependencies)](requirements.txt)

## Installation

Tested on __Python 3.10.3__:

```shell
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
python main.py
```

## Usage

Endpoint is available at: `POST http://localhost:8080/api/calc-power` (e.g. [test_main.http](test_main.http))

### Request Body Parameters

| Parameter      | Datatype | Unit | Expected Values  | Description                              |
|----------------|----------|------|------------------|------------------------------------------|
| cpu_freq       | integer  | MHz  | 3500             | CPU frequency                            |
| cpu_threads    | integer  | #    | 128              | Number of CPU threads                    |
| cpu_cores      | integer  | #    | 64               | Number of CPU cores                      |
| tdp            | integer  | Watt | 240              | TDP of the CPU                           |
| release_year   | integer  | Year | 2023             | Release year of the CPU                  |
| ram**          | integer  | GB   | 16               | Amount of DRAM for the bare metal system |
| architecture** | string   |      | `haswell`        | The architecture of the CPU. lowercase!  |
| cpu_make**     | string   | Enum | `intel` or `amd` | The make of the CPU (intel or amd)       |

** optional

### Response Body

Power Model including an array of power data that describes the watt consumption at different utilization levels.

The utilization values in the array are between `0` and `100` with the step range 5.

```json
{
  "powerModel": "GC XGBoost",
  "sourceUrl": "https://github.com/green-coding-berlin/spec-power-model",
  "powerData": [
    {
      "utilization": 0,
      "watt": 34.603267669677734
    }
  ]
}
```

## Container Image

```shell
docker build -t cpu-power-api .
docker run -p 8080:8080 cpu-power-api
```
