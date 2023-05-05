from fastapi import FastAPI
from pydantic import BaseModel

from spec_power_model.xgb import *


class ArgumentInputModel(BaseModel):
    cpu_freq: int
    cpu_threads: int
    cpu_cores: int
    tdp: int
    release_year: int
    ram: int
    architecture: str
    cpu_make: str


class PowerConsumptionData(BaseModel):
    utilization: int
    watt: float


class PowerOutputModel(BaseModel):
    powerModel = "GC XGBoost"
    sourceUrl = "https://github.com/green-coding-berlin/spec-power-model"
    powerData = []


app = FastAPI()


@app.post('/api/calc-power', response_model=PowerOutputModel)
async def calculate(argsModel: ArgumentInputModel):
    data_frame = pd.DataFrame.from_dict({
        'HW_CPUFreq': [argsModel.cpu_freq],
        'CPUThreads': [argsModel.cpu_threads],
        'CPUCores': [argsModel.cpu_cores],
        'TDP': [argsModel.tdp],
        'Hardware_Availability_Year': [argsModel.release_year],
        'HW_MemAmountGB': [argsModel.ram],
        'Architecture': [argsModel.architecture],
        'CPUMake': [argsModel.cpu_make],
        'utilization': [0.0]
    })

    data_frame = pd.get_dummies(data_frame, columns=['CPUMake', 'Architecture'])
    data_frame = data_frame.dropna(axis=1)
    ml_model = train_model(cpu_chips=1, Z=data_frame)

    print('Sending following dataframe to model:\n', data_frame)

    predictions_inferred = infer_predictions(ml_model, data_frame)
    predictions_interpolated = interpolate_predictions(predictions_inferred)

    response = PowerOutputModel()
    for utilization in range(0, 91, 5):
        response.powerData.append(
            PowerConsumptionData(utilization=utilization, watt=predictions_interpolated[utilization]))
    # adjustment for similar values at 95 and 100
    response.powerData.append(
        PowerConsumptionData(utilization=95, watt=predictions_interpolated[94]))
    response.powerData.append(
        PowerConsumptionData(utilization=100, watt=predictions_interpolated[99]))
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
