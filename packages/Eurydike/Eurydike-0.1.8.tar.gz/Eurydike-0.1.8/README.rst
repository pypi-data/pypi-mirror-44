Εὐρυδίκη/Eurydike
[`wiki <https://de.wikipedia.org/wiki/Eurydike_(Tochter_des_Pelops)>`__]
is a simple event detection. Reacts to above-threshold, below-threshold,
and outside value-band.

.. figure:: img/Microservice%20Overview.png
   :alt: Pelops Overview

   Pelops Overview

``Eurydike`` is part of the collection of mqtt based microservices
`pelops <https://gitlab.com/pelops>`__. An overview on the microservice
architecture and examples can be found at
(http://gitlab.com/pelops/pelops).

For Users
=========

Installation Core-Functionality
-------------------------------

Prerequisites for the core functionality are:

::

    sudo apt install python3 python3-pip
    sudo pip3 install paho-mqtt pyyaml pelops

Install via pip:

::

    sudo pip3 install eurydike

To update to the latest version add ``--upgrade`` as prefix to the
``pip3`` line above.

Install via gitlab (might need additional packages):

::

    git clone git@gitlab.com:pelops/eurydike.git
    cd eurydike
    sudo python3 setup.py install

This will install the following shell scripts: \* ``eurydike``

The script cli arguments are: \* '-c'/'--config' - config file
(mandatory) \* '-v' - verbose output (optional) \* '--version' - show
the version number and exit

YAML-Config
-----------

A yaml [1]_ file must contain four root blocks: \* mqtt - mqtt-address,
mqtt-port, and path to credentials file credentials-file (a file
consisting of two entries: mqtt-user, mqtt-password) \* logger - which
log level and which file to be used \* eventdetectors - parameters for
the controller and the embedded pid

::

    mqtt:
        mqtt-address: localhost
        mqtt-port: 1883
        credentials-file: ~/credentials.yaml
        log-level: INFO

    logger:
        log-level: DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        log-file: test_eurydike.log

    eventdetectors:
        - name: above  # unqiue name for event detector
          type: onthreshold  # detector type identifier
          comparator: gt  # GREATERTHAN/GT/>, LOWERTHAN/LT/<, EQUALTO/==
          threshold: 7  # threshold in combintation with comparator and value from topic-sub
          topic-sub: /test/value
          topic-pub: /test/above
          responses:  # leave value empty or remove line for no response
    #          on-violation: event_detected  # on detection of a threshold violation send this value to topic-pub
              on-restoration: event_ended  # on the event of returning to valid values send this value to topic-pub
          active: False  # entry ignored if set to False

        - name: below  # unqiue name for event detector
          type: onthreshold  # detector type identifier
          comparator: lowerthan  # GREATERTHAN/GT/>, LOWERTHAN/LT/<, EQUALTO/==
          threshold: 7  # threshold in combintation with comparator and value from topic-sub
          topic-sub: /test/value
          topic-pub: /test/below
          responses:  # leave value empty or remove line for no response
              on-violation: event_detected  # on detection of a threshold violation send this value to topic-pub
              on-restoration: event_ended  # on the event of returning to valid values send this value to topic-pub
          active: True  # entry ignored if set to False

        - name: equal  # unqiue name for event detector
          type: onthreshold  # detector type identifier
          comparator: ==  # GREATERTHAN/GT/>, LOWERTHAN/LT/<, EQUALTO/==
          threshold: 7  # threshold in combintation with comparator and value from topic-sub
          topic-sub: /test/value
          topic-pub: /test/equal
          responses:  # leave value empty or remove line for no response
              on-violation: event_detected  # on detection of a threshold violation send this value to topic-pub
              on-restoration:  # on the event of returning to valid values send this value to topic-pub
          active: False  # entry ignored if set to False

        - name: outside  # unqiue name for event detector
          type: onband  # detector type identifier
          upper-threshold: 8  # upper threshold for on band detection
          lower-threshold: 7  # lower threshold for on band detection
          topic-sub: /test/value
          topic-pub: /test/band
          responses:  # leave value empty or remove line for no response
              on-violation: event_detected  # on detection of a threshold violation send this value to topic-pub
              on-restoration: event_ended  # on the event of returning to valid values send this value to topic-pub
          active: True  # entry ignored if set to False

systemd
-------

-  add systemd example.

For Developers
==============

Getting Started
---------------

The project consists of two main modules:

-  ``eventdetectionmanager`` - manages all configured event detectors
-  ``abstracteventdetector`` - base class for all event detectors

Todos
-----

-  ... ?

Misc
----

The code is written for ``python3`` (and tested with python 3.5 on an
Raspberry Pi Zero with Raspbian Stretch).

`Merge requests <https://gitlab.com/pelops/eurydike/merge_requests>`__ /
`bug reports <https://gitlab.com/pelops/eurydike/issues>`__ are always
welcome.

.. [1]
   Currently, pyyaml is yaml 1.1 compliant. In pyyaml On/Off and Yes/No
   are automatically converted to True/False. This is an unwanted
   behavior and deprecated in yaml 1.2. In copreus this autoconversion
   is removed. Thus, On/Off and Yes/No are read from the yaml file as
   strings (see module baseclasses.myconfigtools).

