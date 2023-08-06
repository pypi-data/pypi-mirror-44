Docker Jobber
==============================
> *Twas buildy in the softly woves did gen and gitter in the web...*

Docker Jobber (`jobber`) is a command line interface (CLI) application for managing machine learning workflows using Docker.

![workflow](./docs/images/workflow.png)

### Contents
* [Introduction](#Introduction)
* [Installation](#Installation)
* [Usage](#Usage)
* [Command Line Arguments](#CommandLineArguments)
* [Configuration Files](#ConfigurationFiles)
    * [Directory Search](#ConfigurationDirectorySearch)
    * [Credentials](#ConfigurationCredentials)
    * [Named Configurations](#NamedConfigurations)


# Introduction
Docker Jobber leverages Docker to manage the machine learning (ML) / deep learning (DL) development lifecycle.

* Use with any machine learning framework
* Gain all the advantages of Docker (portability, runtime environment isolation, efficiency, etc.)
* Write custom Dockerfiles incorporating your code along with all dependencies
* Run jobs locally or in the cloud
* Fast development cycle (no need to commit or check in everything before each experiment)
* Design complex data pipelines; Docker images are used for both code and data
* Capture everything (the entire file system is saved after each run)

Once configured, using Docker Jobber can be as easy as

```bash
$ jobber build
$ jobber run
```

## We're all Scientists now
A neural network is like a black box - we don't know how it works, but we can adjust the inputs and observe the outputs.
So a DL developer essentially acts as an experimental scientist applying the scientific method:

1. Form a hypothesis
2. Design an experiment to test the hypothesis
3. Parameterize and conduct the experiment
4. Analyze the results, then return to step 1

And just like for a scientist, reproducibility and data tracking are the keys to making progress.

> Any serious attempt to apply deep learning must confront the challenges of data and configuration management. 


# Model
The unifying technology behind Docker Jobber is the Docker *image*.
A Docker image represents a snapshot of the Linux file system running in a virtual machine.
Docker images are stored in Docker *registries* using an efficient layered approach that reduces both total storage size as well as transfer times when pushing or pulling images (in the Docker vernacular, images stored in a registry are known as *repositories*).

In Docker Jobber, both code and data reside in Docker images.
Code and data may be stored together in a single image for simple cases, but separate *data images* may be used to support versioning or more complex data generation scenarios.
Data images specified as *inputs* are automatically mounted as Docker volumes when a code image is executed.
Any number of input data images may be provided, but each must be associated with a unique mount point (`/data` by default). 
After the job completes (either successfully or unsuccessfully), a snapshot of the filesystem is saved to a *result image* (with a tag formed from the base name of the image with `latest-run` appended).
A log file of the job's execution is also written to the image.
The log file can be useful when trying to determine what went wrong with a job (especially for remote jobs).
Additional meta data in the form of Docker LABELS are written linking the result image to the code and data images from which it was created.
This provides the complete provenance for each job enabling reproducible results.

# Installation
You'll need [Docker](www.docker.com/get-started) of course, then install the `jobber` command using pip (Docker Jobber requires Python3):

```
pip install docker-jobber
```


# Usage
Using Docker Jobber is very similar to just using Docker by itself:
* You write instructions for constructing Docker images using Dockerfiles
* You build Docker images with the build command (e.g. `jobber build`)
* You execute jobs with the run command (e.g. `jobber run`)
  
> Note: `docker run` starts a container that will continue to exist on the Docker host even after the container exits, 
`jobber run` instead snapshots the file system and then deletes the container at exit. 
The file system snapshot is saved as the *result image* for the run.
The result image may be mounted as an input volume during a succeeding run.
Arbitrarily complex data dependency chains may be built up in this way.

## Running Docker Jobber

### <a name="CommandLineArguments"></a> Command Line Arguments

```sh
jobber [GLOBAL-OPTIONS] [build|run] [COMMAND-OPTIONS] [ARG]
```
#### <a name="GlobalOptions"></a> Global Options 
|option|multiple|description|
|------|:------:|-----------|
|--version || Print version and exit
|-v, --verbose || Print extra information during execution of the command |
|-H, --host *host* || Docker host to connect to |
|-r, --reg *registry* || Default registry specification. Images are automatically pushed. |
|-c, --config *config* |Y| Apply a named config (see the [Configuration](#ConfigurationFiles) section).

The 'default' configuration from the config file (if found) is used if none are specified on the command line.

Images without a repository path (i.e. registry url and/or namespace spec.) are automatically pulled from or pushed to the default registry.

#### Build Command
```
jobber build [OPTIONS]
```

|option|multiple|description|
|------|:------:|-----------|
|-t, --tag *image-name:tag* |Y| Set the image name and optional tag (see below) |
|-f, --file *Dockerfile* || Name of the Dockerfile (default `Dockerfile`)

Build a Docker image from a Dockerfile.
The current directory name will be used as the image name if no tags are specified.
Tags consist of an *image-name* optionally followed by a colon (:) and a *tag-name*.
`jobber` will add two default tags to the image name if a tag name isn't specified: 'latest', and a UTC timestamp with format 'YYYYMMDD_HHMMSS'. Meta-data in the form of Docker LABELS are also written to the image:

| label | description |
|--|--|
|jobber.version| The version of Docker Jobber that created the image |
|jobber.build-tags| List of tags set for the image |

#### Run Command
```
jobber run [OPTIONS] [IMAGE[:TAG]] [CMD] [ARGS...]
```

|option|multiple|description|
|------|:------:|-----------|
|--runtime [runc \| nvidia] || Docker runtime environment
|-i, --in *in-spec* |Y| Input data image (mounted read-only)
|-o, --out *src-dir* || Default src data directory 
|-ri, --result-image [none \| success \| always] || Whether to create a result image on exit
|-Xd, -XDocker *docker-args* |Y| Pass *docker-args* to the docker command

Run a docker image and create a result image from a snapshot of the filesystem at exit.
The current directory name will be used as the name of the image to run if not specified.
Any additional arguments appearing after the image name are passed as the docker CMD.
`jobber` adds two tags to the result image name: 'latest-run', and a UTC timestamp with format 'YYYYMMDD_HHMMSS'.
Meta-data in the form of Docker LABELS are also written to the result image as listed in the following table:

| label | description |
|--|--|
|jobber.version| The version of Docker Jobber that created the image |
|jobber.parent| The sha256 id of the image that was executed |
|jobber.out| The default *src* directory for when the image is used as an input (see the `-o` option below)
|jobber.inputs| Comma separated list of input image vol-specs. A vol-spec is a string with format: "*image-id*:*src-directory*:ro".

The out (`-o`) option specifies the default *src* directory when the result image is used as an input image on a later run (default is `/data`).

The in (`-i`) option specifies one or more input images to use as data sources for the current run.
Source directories from the input data images are copied (as needed) to scratch docker volumes and mounted in the running image's file system at their corresponding destination directories.

*in-spec* has the following format:
```
IMAGE[,src=SRC-PATH][,dest=DEST-PATH]
```

Both the src and dest portions are optional.
The *out* directory from the input image will be used as the SRC-PATH if not specified (defaults to `/data`).
The DEST-PATH also defaults to `/data`.
You will need to specify a unique dest directory for each input image if multiple input images are used.
A Docker volume is created if one doesn't already exist for a given input image.
This may lead to excessive disk usage if many variants of input images are built.
Use the various `docker volume` commands to view and clean up unused volumes.

#### Example:
```
jobber run -i mnist-data,src=/data,dest=/digits -o /digit-images mnist
```
This example runs the `mnist` code image with `mnist-data` mounted as an input image.
The `/data` directory from `mnist-data` is mounted as `/digits` during the run.
The result image (`mnist:latest-run`) created after the run specifies `/digit-images` as the default mount point for when the result image is used as input to some other run.


# <a name="ConfigurationFiles"></a> Configuration Files
Docker Jobber is configured using a flexible architecture based on yml files with the name `jobber-config.yml` (see [example](#example) below).

## <a name="ConfigurationSettings"></a> Settings
Settings from configuration files define default values for unspecified command line options and internal settings.

|name|value|description|
|--|--|--|
|verbose| [True or False] | Sets the `-v` flag
|host| *host URL*| Docker host to connect to 
|default-registry| *registry URL*| Default registry
|credentials| *credential specs.* | Login credentials (see [below](#Credentials))
|runtime|[runc \| nvidia] | Docker runtime environment
|inputs| list of *in-spec*| Input data images (mounted read-only)
|out| *src-dir* | Default src data directory
|timeout| *secs* | Terminate run if it takes more than *secs* seconds
|result-image| [none \| success \| always] | Whether to create a result image on exit
|cmd| [none \| *docker-cmd*]| Pass *docker-cmd* as the CMD when running an image 
|Xdocker|*docker-args*| Pass *docker-args* to the docker command
|configs| list of *configuration names*| Define named configurations (see [below](#NamedConfigurations))

## <a name="ConfigurationDirectorySearch"></a> Directory Search
Configuration settings are read from the `~/.config/jobber/jobber-config.yml` if it exists.
Additionally, the entire path up to the root is searched starting from the current directory for additional `jobber-config.yml` files when a jobber command is executed.
Settings found in more deeply nested config files override those from higher up in the search path (except for `credentials`, which are concatenated).

## <a name="ConfigurationCredentials"></a> Credentials
A list of credentials for remote Docker registries may be specified under the `credentials` setting.
Credentials are automatically provided before `push` or `pull` operations with remote registries.
Support for the following credentialing mechanisms are currently supported (more to come):

| type | description |
| -- | -- |
| login | Docker registry login using user name and password

> Note: Google Cloud Platform provides for login authentication using a [json file](https://cloud.google.com/container-registry/docs/advanced-authentication#json_key_file).
Use the `password-file` key as described next.


Docker login requires a user name and password.

| key | description |
| -- | -- |
| registry | Url of remote registry
| user | user name
| password | password (stored in the clear)
| password-file| The name of a file containing the password

#### Example:
```YML
credentials:
  - registry: "localhost:5000"
    user: me
    password: in-the-clear
  - registry: gcr.io
    user: _json_key
    password-file: ~/certs/gcr_key.json
  ```

## <a name="NamedConfigurations"></a> Named Configurations

A *named configuration* is a key/value pair in which the key is a configuration name and the value is a list of other configuration names, or a dictionary of setting-name/value pairs.
Named configurations are defined under the `configs` key in the yml file.
Configuration names are activated on the command line using the `-c` [option](#GlobalOptions), or using the configuration named `default` (if it exists).

Settings defined under a named configuration override values that are not part of a configuration (i.e. outside of the `configs` key).
Also, `Xdocker` and `inputs` values are concatenated in addition to `credentials` when processing named configurations.

A named configuration may be defined in terms of other named configurations. 
Encountering a list of configuration names as as part of a definition activates those configurations as if they had been provided on the command line.
This results in a surprisingly flexible and easy to use system making it simple to switch between different development and runtime tasks.

#### Example:

The following is representative of a complex real-world software project incorporating machine learning.

As the lead ML engineer on the project, you are responsible for developing, testing, and deploying ML as a critical component of the product.
Your duties include quantifying and reporting on ML progress, as well as performing regression analysis when problems arise in the field with previously deployed versions.
You alternate between algorithm development and analysis and product integration and deployment.
You also must manage and track work performed by contract ML developers and researchers working remotely.
Docker Jobber makes it possible to succeed in this type of environment.

We'll take a look at how you might configure Docker Jobber for use during development of ML unit tests.
Assume that the project has the following directory structure:
```
myproject/
  jobber-config.yml
  ...
  tests/
    jobber-config.yml
    DockerFile
    tests.py
    ...
```


In your home directory, define a set named configurations for common tasks using a jobber config file `/home/user/.config/jobber/jobber-config.yml`:
``` YML
credentials:
  - registry: "localhost:5000"
    user: me
    password: in-the-clear
configs:
  tensorboard:
    Xdocker: -p 6006:6006
  develop:
    # Xdocker: -v /home/user/myproject/<dir>:/work
    result-image: none
    cmd: bash
  debug:
    result-image: success
  release:
    result-image: always
```

You make use of [Tensorboard](https://github.com/tensorflow/tensorboard) to track the learning progress during training (the `tensorboard` configuration exposes port 6006).

The `develop` configuration is intended for use while you are writing code.
It disables creation of result images (no need to clutter the registry with hundreds of failed runs), and overrides the Docker CMD to open a bash prompt.
The intent is to map your source code from the host machine into the Docker container so you may use an external editor without having to repeatedly rebuild code images (an example of how you would do that from a subdirectory is shown in the commented line).
You can modify, debug, and execute code multiple times from inside the container.
Once you're happy with the results, just type `^D` to exit back to the host where you can then build and run in `debug` or `release` mode.
We'll see this in action shortly.

The config file in the project root (`myproject/jobber-config.yml`) provides credentials for the project repository on Google Cloud Platform.
It also activates the `develop` and `tensorboard` configurations by default:
```YML
credentials:
  - registry: gcr.io/myproject
    user: _json_key
    password-file: ~/certs/myproject_gcr_key.json
configs:
  default:
     - develop
     - tensorboard
```


Here's the config file in the unit testing directory
`myproject/tests/jobber-config.yml`:

```YML
inputs:
  - test-data
configs:
  develop:
    Xdocker: -v /home/user/myproject/tests:/work 
  debug:
    cmd: python -m unittest
  release:
    cmd: echo "Unit tests disabled in release mode"
```

You've provided the source directory mapping for the `develop` configuration as outlined above.
An input data image is also mapped (using its default src directory).
The data image will be available in all configurations.
Building the image is simple:
```
$ cd tests
$ jobber build
```

Use `develop` mode to work on the code:
```
$ jobber run
root@c552bc46c03c:/work# python -m unittest 
F
======================================================================
FAIL: test_learning_rate (tests.MyTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests.py", line 5, in test_learning_rate
    self.assertEqual(1, 0)
AssertionError: 1 != 0

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
root@c552bc46c03c:/work#
```
Notice that it wasn't necessary to specify `-c develop` on the command line since the `develop` configuration is active by default in the project level config file.
Continue to edit and run the code until happy.
No result images are produced during the development process (`result-image: none`).
Finally, exit and run in debug mode

```
root@c552bc46c03c:/work# exit
$ jobber build
$ jobber run -c debug
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```
This will produce a result image if no errors occurred (`result-image: success`).

The combination of named configurations and nested configuration files provides an unobtrusive and productive development environment while still retaining strict reproducibility and data provenance.


