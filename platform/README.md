# Getting Setup to run the OpenFIDO web platform

## The Conda Way:
```bash
conda env create -f openfido-environment.yml
# if you need to update
conda env update -f openfido-environment.yml
# then
conda activate venv_openfido
# to stop
conda deactivate
```

## The Docker Way
```bash
docker build -t openfido-platform .
docker run openfido-platform
```
