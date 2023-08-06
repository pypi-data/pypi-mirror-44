from pelops.abstractmicroservice import AbstractMicroservice
from eurydike.eventdetectors.eventdetectorfactory import EventDetectorFactory
import eurydike.schema as schema
from eurydike import version


class EventDetectionManager(AbstractMicroservice):
    """
    Creates, stores, starts, and stops all configured event detectors.

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
    """

    _version = version

    _event_detectors = None  # list of event detector instances

    def __init__(self, config, mqtt_client=None, logger=None, stdout_log_level=None, no_gui=None):
        """
        Constructor.

        :param config: config yaml structure
        :param mqtt_client: instance of an mymqttclient (optional)
        :param logger: instance of a logger (optional)
        :param no_gui: if False create and control a ui instance
        :param stdout_log_level: if set, a logging handler with target sys.stdout will be added
        """
        AbstractMicroservice.__init__(self, config, "eventdetectors", mqtt_client=mqtt_client, logger=logger,
                                      stdout_log_level=stdout_log_level, no_gui=no_gui)
        self._event_detectors = EventDetectorFactory.create_elements(self._config, self._mqtt_client, self._logger)

    @classmethod
    def _get_schema(cls):
        return schema.get_schema()

    @classmethod
    def _get_description(cls):
        return "Eurydike is a simple event detection. Reacts to above-threshold, below-thershold, "\
                "and outside value-band."

    def _start(self):
        """
        start all event detectors
        """

        for event in self._event_detectors:
            event.start()

    def _stop(self):
        """
        stop all event detectors
        """
        for event in self._event_detectors:
            event.stop()

    def runtime_information(self):
        return {}

    def config_information(self):
        return {}

    
def standalone():
    """Calls the static method DataPointManager.standalone()."""
    EventDetectionManager.standalone()


if __name__ == "__main__":
    EventDetectionManager.standalone()

