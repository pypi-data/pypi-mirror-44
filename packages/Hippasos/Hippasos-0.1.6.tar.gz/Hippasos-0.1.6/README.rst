Πηααος [1]_ (Hippasos) plays preconfigured sound files upon reception of
predefined mqtt messages.

.. figure:: img/Microservice%20Overview.png
   :alt: Pelops Overview

   Pelops Overview

``Hippasos`` is part of the collection of mqtt based microservices
`pelops <https://gitlab.com/pelops>`__. An overview on the microservice
architecture and examples can be found at
(http://gitlab.com/pelops/pelops).

For Users
=========

Installation Core-Functionality
-------------------------------

Prerequisites for the core functionality are:

::

    sudo apt install python3 python3-pip python3-pygame
    sudo pip3 install paho-mqtt pyyaml pygame pelops

Install via pip:

::

    sudo pip3 install epidaurus

To update to the latest version add ``--upgrade`` as prefix to the
``pip3`` line above.

Install via gitlab (might need additional packages):

::

    git clone git@gitlab.com:pelops/hippasos.git
    cd hippasos
    sudo python3 setup.py install

This will install the following shell scripts: \* ``hippasoss``

The script cli arguments are: \* '-c'/'--config' - config file
(mandatory) \* '-v' - verbose output (optional) \* '--version' - show
the version number and exit

YAML-Config
-----------

| A yaml [2]_ file must contain four root blocks: \* mqtt -
  mqtt-address, mqtt-port, and path to credentials file credentials-file
  (a file consisting of two entries: mqtt-user, mqtt-password) \* logger
  - which log level and which file to be used
| \* sound-mappings - list of sound events

::

    mqtt:
        mqtt-address: localhost
        mqtt-port: 1883
        credentials-file: ~/credentials.yaml
        log-level: WARNING

    logger:
        log-level: DEBUG
        log-file: hippasos.log

    sound-mappings:
        - name: bell_building  # unique name for sound event
          sound-file: ../resources/church_bell.ogg  # uri to sound file. must be ogg or wav.
          topic-sub: /test/button1  # react to published values on this channel
          message-value: PRESSED  # react to this message content
          volume: 0.1  # 0..1 - volume relative to system volume
          active: True  # entry ignored if set to False

systemd
-------

-  add systemd example.

For Developers
==============

Getting Started
---------------

The project consists of two main modules: \* ``soundservice`` - Creates,
starts and stops sound events. \* ``soundevent`` - Subscribes to a topic
and plays a sound file upon reception of a specific message.

Todos
-----

-  Make maximum number of parallel playable sound configurable.
-  ...

Misc
----

The code is written for ``python3`` (and tested with python 3.5 on an
Raspberry Pi Zero with Raspbian Stretch).

`Merge requests <https://gitlab.com/pelops/hippasos/merge_requests>`__ /
`bug reports <https://gitlab.com/pelops/hippasos/issues>`__ are always
welcome.

.. [1]
   The icon used for this project is not Hippasos, son of pelops but it
   depicts Hippasus of Metapontum.

.. [2]
   Currently, pyyaml is yaml 1.1 compliant. In pyyaml On/Off and Yes/No
   are automatically converted to True/False. This is an unwanted
   behavior and deprecated in yaml 1.2. In copreus this autoconversion
   is removed. Thus, On/Off and Yes/No are read from the yaml file as
   strings (see module baseclasses.myconfigtools).

