The [OpenFIDO platform](https://app.openfido.org) allows you to configure and run data processing pipelines. 

The following is a list of known pipeline libraries that are compatible with OpenFIDO

| Pipeline name        | Pipeline repo | Entry point | Docker image | Publisher | Description
| -------------------- | ------------- | ----------- | ------------ | --------- | -----------
| CYME MDB Extract     | https://github.com/openfido/cyme-extract | `openfido.sh` | `ubuntu:20.04` | SLAC National Accelerator Laboratory | Extract CYME databases to network graphs and GridLAB-D models
| GRIP Absorption      | https://github.com/PresencePG/grip-absorption-pipeline | `openfido.sh` | `slacgrip/master:200527` | SLAC National Accelerator Laboratory | GRIP absorption analysis
| GRIP Anticipation    | https://github.com/PresencePG/grip-anticipation-pipeline | `openfido.sh` | `slacgrip/master:200527` | SLAC National Accelerator Laboratory | GRIP absorption analysis
| GRIP Recovery        | https://github.com/PresencePG/grip-recovery-pipeline | `openfido.sh` | `slacgrip/master:200527` | SLAC National Accelerator Laboratory | GRIP absorption analysis
| HiPAS Converters     | https://github.com/openfido/hipas-converters | `openfido.sh` | `ubuntu:20.04` | SLAC National Accelerator Laboratory | HiPAS GridLAB-D converters
| Load Composition     | https://github.com/slacgismo/load_composition_analysis | `openfido.sh` | `python:3` | SLAC National Accelerator Laboratory | NERC composite load model data analysis
