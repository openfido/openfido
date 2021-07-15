# Example Pipeline

[Sample Pipeline Worker](https://github.com/PresencePG/presence-pipeline-example)

This repository illustrates the structure expected of a git repository that is used in OpenFIDO to execute a Pipeline. See its README.md for more information and requirements of a pipeline repository.

[GRIP Anticipation Pipeline](https://github.com/PresencePG/grip-anticipation-pipeline)

The GRIP Anticipation Pipeline repository contains plugin files that are necessary for the OpenFIDO app and workflow services to create and run a pipeline of this nature via a workflow pipeline or as a standalone pipeline.

It includes an `openfido.sh` entry point as well as all the necessary files to run a GridLabD Anticipation simulation - apart from the input models and variable weather data.

The entry point has two environment variables in use: `OPENFIDO_INPUT` and `OPENFIDO_OUTPUT`.

Any input files needed to complete a pipeline run of GRIP Anticipation will be available at the `OPENFIDO_INPUT` path.

Additionally, the `openfido.sh` script places any and all resulting artifacts deemed necessary for a successful pipeline run into the `OPENFIDO_OUTPUT` directory. These files will be surfaced into the OpenFIDO client once the pipeline run completes.

---

##### Links to other similar pipeline repos

[GRIP Absorption Pipeline](https://github.com/PresencePG/grip-absorption-pipeline)

[GRIP Recovery Pipeline](https://github.com/PresencePG/grip-recovery-pipeline)
