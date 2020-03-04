# Getting Setup to run the OpenFIDO web platform

## Creating the env - ensure you are running the anaconda `4.5.x +`
```bash
conda env create -f openfido-environment.yml
```

## Updating the env after adding new packages
```bash
conda env update -f openfido-environment.yml
```

## Starting the env
```bash
conda activate venv_openfido
```

## Install pip packages after starting the env:
```bash
pip install -r requirements.txt
```

## Stopping the env
```bash
conda deactivate
```

## Running the platform - TBD


## Executing tests locally - TBD
