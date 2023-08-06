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
Docker images are stored in Docker *registries* using an efficient layered approach that reduces both total storage size as well as transfer times when pushing or pulling images (in the Docker vernacular, images stored in a registry are called *repositories*).

In Docker Jobber, both code and data reside in Docker images.
Code and data may be stored together in a single image for simple cases, but separate *data images* may be used to support versioning or more complex data generation scenarios.
Data images specified as input are automatically mounted as Docker volumes when a code image is executed.
Any number of input data images may be provided, but each must specify a unique mount point (`/data` by default). 
After the job completes (either successfully or unsuccessfully), a snapshot of the filesystem is saved to a *result image* (by default using a tag with '`latest-run`' appended).
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
|-r, --reg *registry* || Default registry. Images are automatically pushed. |
|-c, --config *config* |Y| Apply a named config (see the [Configuration](#ConfigurationFiles) section).

The 'default' configuration from the config file (if found) is used if none are specified on the command line.

Images are automatically pulled from or pushed to the default registry.

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
Meta-data in the form of Docker LABELS are also written to the result image:

| label | description |
|--|--|
|jobber.version| The version of Docker Jobber that created the image |
|jobber.parent| The sha256 id of the image that was run |
|jobber.out| The default *src* directory for when image is used as an input (see the `-o` option below)
|jobber.inputs| Comma separated list of input image vol-specs. A vol-spec is a string with format: "*image-id*:*src-directory*:ro".

The out (`-o`) option specifies the default *src* directory when the result image is used as an input image on a later run (default is `/data`).

The in (`-i`) option specifies one or more input images to use as data sources for the current run.
Source directories from the input data images are copied (if needed) to scratch docker volumes and mounted on the running image's file system at corresponding destination directories.

*in-spec* has the following format:
```
IMAGE[,src=SRC-PATH][,dest=DEST-PATH]
```

Both the src and dest portions are optional.
The *out* directory from the input image will be used as the SRC-PATH if not specified (defaults to `/data`).
The DEST-PATH also defaults to `/data`.
You will need to specify a unique dest directory for each input image if multiple input images are used.
A Docker volume is created if one doesn't already exists for a given input image.
This may lead to excessive disk usage if many variants of input images are built.
Use the various `docker volume` commands to view and clean up unused volumes.


# <a name="ConfigurationFiles"></a> Configuration Files
Docker Jobber is configured using a flexible architecture based on yml files with the name `jobber-config.yml` (see [example](#example) below).

## Settings
Settings from configuration files define default values for unspecified command line options and internal settings.

|name|value|description|
|--|--|--|
|verbose| [True or False] | Sets the `-v` flag
|host| *host URL*| Docker host to connect to 
|registry| *registry URL*| Default registry
|runtime|[runc \| nvidia] | Docker runtime environment
|inputs| list of *in-spec*| Input data images (mounted read-only)
|out| *src-dir* | Default src data directory
|timeout| *secs* | Terminate run if it takes more than *secs* seconds
|result-image| [none \| success \| always] | Whether to create a result image on exit
|cmd| [none \| *docker-cmd*]| Pass *docker-cmd* as the CMD when running an image 
|Xdocker|*docker-args*| Pass *docker-args* to the docker command
|configs| list of *configuration names*| Define named configurations (see [below](#NamedConfigurations))

## Directory Search
Configuration settings are read from `~/.config/jobber/jobber-config.yml` if it exists.
Additionally, the current directory and all parent directories are searched for a `jobber-config.yml` file when executing a jobber command. Settings read from the file (if found) override those from `~/.config/jobber/jobber-config.yml` except for the `Xdocker` and `inputs` settings which are appended.


## <a name="NamedConfigurations"></a> Named Configurations

A *named configuration* is a key/value pair in which the key is a configuration name and the value is a list of other configuration names, or a dictionary of setting-name/value pairs.
Named configurations are defined under the `configs` key in the yml file.
Configuration names are activated on the command line using the `-c` [option](#GlobalOptions).
The configuration named "default" is used (if it exists) if the user doesn't specify any configurations.

A named configuration may be defined in terms of other named configurations. 
Encountering a configuration name as part of a definition activates that configuration as if it had also occurred on the command line.
This results in a surprisingly flexible and easy to use system making it easy to switch between different development and runtime environments.

#### Example:
```YML
inputs:
  - mnist-data
configs:
  default:
    - develop
    - tensorboard
  tensorboard:
    Xdocker: -p 6006:6006
  develop:
    result-image: none
    cmd: bash
    Xdocker: -v /home/user/mnist:/work
  debug:
    result-image: success
  release:
    result-image: always
```
This settings file defaults to 'develop' mode with the tensorboard port mapped, so simply typing:

```sh
jobber run
```

starts Docker interactively and launches a bash shell.
The user's source directory on the host is mapped as `/work` in the container so file edits are reflected immediately.
The code may be modified, debugged, and executed multiple times during the run.
No result image is produced (`result-image: none`).
Once satisfied with the state of the code, the user just types `^D` to exit back to the host and then builds and runs in "debug" mode:

```sh
jobber build
jobber -c debug run
``` 

This will produce a result image if no errors occurred (`result-image: success`).

The combination of named configurations and nested configuration files provides an unobtrusive and productive development environment while still retaining strict reproducibility and data provenance.
