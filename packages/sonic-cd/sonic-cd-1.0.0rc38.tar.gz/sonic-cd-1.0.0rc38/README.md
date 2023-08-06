
# Sonic CD

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Build Status](https://travis-ci.org/WirelessCar/sonic.svg?branch=master)](https://travis-ci.org/WirelessCar/sonic)
[![PyPI version](https://badge.fury.io/py/sonic.svg)](https://badge.fury.io/py/sonic)

## What is Sonic CD?
Sonic is a portable, vendor independent continuous integration/delivery/deployment pipe runner.

## Why Sonic?
A key essence to Continuous Delivery is reproducibility of the entire process from source control to production environment. Yet, very few CI/CD solutions offer true portability.

Portability is not only important because it increases reproducibility but also because it improves development turnaround and decreases debug time.

At WirelessCar we developed Sonic to help increase portability and transparency in our build pipes through portability. The positive effect we have seen has been enormous. We have decreased the time it takes to implement build pipe changes as well as the time to debug failed builds by an astonishing amount.

## How does Sonic work?
You define pipes, sequences, tasks and steps in a .sonic.yml file. Sonic converts these files into a set of Docker Compose files that are then processed in order.

Individual Docker images can be used for each step. This allows for not only full customization of the pipe but also for packaging and sharing steps.

## Why not one of the similar commercial solutions?
Some of the commercial and community tools can't fully run locally. Sonic is truly portable and designed to run on any build environment. The same build pipe can run locally, on travis, on gitlabci, on codebuild, on jenkins or any other build
system. By being totally vendor independent, Sonic allows for full separation between build/release/reporting/deployment tools, build servers and the CI/CD process.

## For whom is Sonic?
We at WirelessCar are about 400 developers and we have a few hundred git repositories that we build and deploy to AWS using Sonic. We have used Sonic to help us define a shared responsibility model between the central Tools team and our
development teams.

The portability of Sonic makes it an ideal tool to use as an organization grows, matures and transforms. For the Startup it provides a simple way of running CI/CD without even having a build server. Then, as the organization grows, Sonic helps
you move between build systems as well as creating shared responsibility models between teams.

## Getting Started


### Prerequisites

To run Sonic you need
1. Python3 and Pip
2. Docker and Docker Compose


### Installing

Install

```
pip install sonic-cd
```

### Usage

Sonic is executed as a CLI.

#### Prerequisites

A .sonic.yml file is required in the directory where sonic is executed, or in the location defined by the -f flag.

#### Grammar
(Slightly out of date, but should follow [EBNF](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form))
```
<sonic_command> ::= sonic <executable list>
<executable list> ::= "" | <executable> [<executable list>]
<pipe> ::= <pipe_name> [<pipe_arg>]
<executable_name> ::= build | test | publish | deploy | ..
<pipe_arg> ::= -c key:value
```

#### Running
```
sonic [-h] [-f FILE] [-c CONTEXT] [-p] [-l] [-s] [-n] [-d] [-v] [-g] [-D] [sequence [sequence ...]]
```

## The .sonic.yml

A CI/CD pipe in Sonic is composed of the following constructs:

* A ***Pipe*** is composed of several tasks and is Sonic executable.
* A ***Task*** is part of a pipe and can consist of multiple steps that are executed in the defined order. A Task is Sonic executable.
* A **Step** is transformed into a Docker Compose file and executed.
* A ***Sequence*** links pipes together into a series of pipes. The sequence is a Sonic executable.

### File Structure

TODO

#### Context

TODO

#### Tasks & Steps

A Sonic task is composed of steps. A step in Sonic is translated into a Docker Compose file and the unit is executed by
Sonic. There are three ways of defining steps:

* Simplistic Format using a default Docker image (defined in the config.yml file). By default this is
[triha74/sonic-base-image](https://hub.docker.com/r/triha74/sonic-base-image)
* Simplistic Format using an explicit Docker image, with or without the registry included in the image name
(the registry defaults to
docker.io if not specified otherwise). This format takes the image  and the command, i.e. `${image} ${command}`
* The Docker Compose format used in the `services` section (see https://docs.docker.com/compose/compose-file/ for
reference)

When executing a task the execution stops if a step fails, with the exception of _Post Tasks_ that are always executed
regardless of the exit code of a task.


##### Examples

*Simplistic Format using a default docker image*
```
tasks:
  hello:
    - $ echo 'Hello World'
    - $ echo 'Hello Galaxy'
```

*Simplistic Format using an explicit image*
```
tasks:
  hello:
    - debian:stretch-slim echo 'Hello World'
    - alpine:latest echo 'Hello Galaxy'
```
*Docker Compose Format*
```
tasks:
  hello:
    main:
        image: docker.io/debian:stretch-slim
        command: echo 'Hello World'
        volumes:
            - ${workdir}:/workdir
        links:
            - galaxy
    galaxy:
        image: docker.io/alpine:latest
        command: echo 'Hello Galaxy'
        volumes:
            - ${workdir}:/workdir
```
Run these by executing
``
sonic hello
``

#### Pre and Post Tasks
By convention Sonic looks for (and executes) `pre-task-${task_name}` and `post-task-${task_name}`, if their definitions are found. _Pre_ and _Post_ tasks are tasks
composed of steps just like normal task with the exception that they are always executed. Default pre & post tasks can be created by just defining `pre-task` and `post-task`.

```
tasks:
  pre-task-hello:
    - $ echo 'Tap Tap Anyone home'
  hello:
    - debian:stretch-slim echo 'Hello World'
    - alpine:latest echo 'Hello Galaxy'
  post-task-hello:
    - $ echo 'Night all!'
```

Typically we recommend defining global pre/post tasks for collection of metrics, logs (etc) in the config.yml file and only the main tasks in the .sonic.yml.

#### Pipes

Pipes are series of tasks. The default Sonic pipe consists of `build` and `test`. To have a pipe that does something else it needs to be explicitly implemented in either the .sonic.yml or the config.yml (as described above).

##### Example:

*CI and CD pipes referencing the tasks defined under root `tasks`*
```
pipes:
  ci:
    tasks:
      - build
      - test
      - publish
  cd:
    tasks:
      - launch
      - verify
tasks:
  build:
    - $ mvn install
  test:
    - $ mvn verify
  publish:
    - $ mvn deploy
  launch:
    - $ aws cloudformation .....
  verify:
    - $ curl https://something.test
```
 All tasks in a pipe are treated as optional. This means that with a pipe defined globally in the config.yml file, a specific project can choose to implement only the tasks needed for that project in the .sonic.yml file without breaking anything.

 Pipes can also have Pre and Post Tasks on a pipe level. The Post Task on the pipe level is always executed.

 ##### Example:

 *CI and CD pipes referencing the tasks defined under root `tasks` and implementing a Pre and Post step that uses a slack image in a custom registry*

```
pipes:
  ci:
    pre:
      - my-docker-registry.io/slack "${component} now building"
    tasks:
      - build
      - test
      - publish
    post:
      - my-docker-registry.io/slack "${component} version ${version} finished with status ${status}"
  cd:
    tasks:
      - launch
      - verify
```


#### Sequences
A Sequence is a sequence of pipes executed in the defined order. It is possible to provide individual context variables for each of the pipe executions in a sequence.

##### Example:

*CI and CD pipes with task definitions and a deployment sequence going from qa to prod.*

*Execute `sonic auto-deploy`*

```
tasks:
  build:
    - $ mvn install
  test:
    - $ mvn verify
  publish:
    - $ mvn deploy
  launch:
    - $ aws cloudformation .....
  verify:
    - $ curl https://something.test

pipes:
  ci:
    tasks:
      - build
      - test
      - publish
  cd:
    tasks:
      - launch
      - verify

sequences:
  auto-deploy:
     - ci
     - cd:
        context:
          environment: qa
          account: 98765432101
     - cd:
        context:
          environment: prod
          account: 01234567890
```
##### Example:
*Reusing the pipe and deploy sequences across multiple applications by moving it to the config.yml while keeping the tasks in the .sonic.yml. This way the application can be built using any build tool and deployed using any deployment mechanism
but still having one CI/CD process that all applications follow*

*Executed with `sonic auto-deploy`*

.sonic.yml
```
tasks:
  build:
    - $ mvn install
  test:
    - $ mvn verify
  publish:
    - $ mvn deploy
  launch:
    - $ aws cloudformation .....
  verify:
    - $ curl https://something.test
```

~/.sonic/config.yml
```    
pipes:
  ci:
    tasks:
      - build
      - test
      - publish
  cd:
    tasks:
      - launch
      - verify

sequences:
  auto-deploy:
     - ci
     - cd:
        context:
          environment: qa
          account: 98765432101
     - cd:
        context:
          environment: prod
          account: 01234567890
```

## Development Setup
If you are using Sonic in your projects but also doing a bit of development of Sonic itself, you need to ensure that a broken development version of Sonic doesn't block you in your projects. To do this, setup a Virtual Environment and install Sonic into it. This way you can switch between the production version and the development version by activating/deactivating the virtual environment.

In this directory:

```
$ virtualenv venv
$ source venv/bin/activate
$ python setyp.py install
```

(Note: If your default Python interpreter is 2.x, pass `--python=/usr/bin/python3` to `virtualenv` when creating the environment)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/wirelesscar/sonic/tags).

## Authors

* **Tomas Riha** - *Initial work* - [triha-wcar](https://github.com/triha-wcar)
* **Mikael Carneholm** - *Initial work* - [carniz](https://github.com/carniz)
* **Lennart Coopmans** - *Initial work* - [LennartC](https://github.com/LennartC)

See also the list of [contributors](https://github.com/wirelesscar/sonic/contributors) who participated in this project.

## License

This project is licensed under the 3-Clause BSD License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* All of the Tools Team at WirelessCar
