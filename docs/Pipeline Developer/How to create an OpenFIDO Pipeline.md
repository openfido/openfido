# How to create an OpenFIDO Pipeline

1. Start with a new repository on GitHub.

2. Create an `openfido.sh` script to be used as an entry point for starting a run.

3. Include all necessary files and scripts to be run by the workflow service into the OpenFIDO pipeline repository that you have just created.

4. Reference any input files uploaded from the OpenFIDO client, using the `OPENFIDO_INPUT` as the base directory. If you need all of them, simply `cp -r $OPENFIDO_INPUT/* .` to your working directory.

5. If possible, create a `tmp` directory where you can store your artifacts and outputs from your processes.

6. Call your processes from the `openfido.sh` script.

7. After your processes have completed, move any artifacts from the `tmp` folder to the location referenced by `OPENFIDO_OUTPUT`.

Here is a quick `.sh` template to get you started:

**openfido.sh**

```
#!/bin/bash

# nounset: undefined variable outputs error message, and forces an exit
set -u
# errexit: abort script at first error
set -e
# print command to stdout before executing it:
set -x

echo "OPENFIDO_INPUT = $OPENFIDO_INPUT"
echo "OPENFIDO_OUTPUT = $OPENFIDO_OUTPUT"

if ! ls -1 $OPENFIDO_INPUT/<YOUR_INPUT_FILE>; then
  echo "Input <YOUR_INPUT_FILE> file not found"
  exit 1
fi

path_to_tmp_dir=tmp

echo "Creating tmp directory"
mkdir -p $path_to_tmp_dir

echo "Copying input files to working directory"
cp -r $OPENFIDO_INPUT/* .

<YOUR_PROCESSES_GO_HERE>

mv $path_to_tmp_dir/* $OPENFIDO_OUTPUT  # or some but not all
mv *.csv $OPENFIDO_OUTPUT               # example
```
