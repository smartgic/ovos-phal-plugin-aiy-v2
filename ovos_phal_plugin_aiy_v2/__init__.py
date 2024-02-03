"""AIY V2 entrypoint PHAL plugin
"""

from time import sleep
from json_database import JsonConfigXDG
from ovos_bus_client import Message
from ovos_plugin_manager.phal import PHALPlugin
from ovos_utils import create_daemon
from ovos_utils.log import LOG

from aiy.leds import Leds, Pattern, Color
from aiy.board import Board


class AiyV2Plugin(PHALPlugin):
    """This is the place where all the magic happens for the
    AIY V2 LED PHAL plugin.
    """

    def __init__(self, bus=None, config=None):
        super().__init__(bus=bus, name="ovos-phal-plugin-aiy-v2", config=config)

        # Retrieves settings from ~/.config/OpenVoiceOS/ovos-phal-plugin-aiy-v2.json
        self.settings = JsonConfigXDG(self.name, subfolder="OpenVoiceOS")
        self.wakeword_only = self.settings.get("wakeword_only", False)
        self.pulse = self.settings.get("pulse", True)
        self.color = self.settings.get("color", "green").upper()
        self.button_event = self.settings.get("button_event", "mycroft.mic.listen")

        # Initialize AIY classes
        self.leds = Leds()
        self.board = Board()

        # Handle bus events
        self.bus.on("recognizer_loop:record_begin", self._handle_led_on)
        self.bus.on("recognizer_loop:record_end", self._handle_led_off)
        self.bus.on("ovos.utterance.cancelled", self._handle_led_off)
        self.bus.on("recognizer_loop:audio_output_end", self._handle_led_off)

        def _press_button():
            """This function detects when the button is pressed. Once pressed
            the LED turns on.
            """
            while True:
                self.board.button.wait_for_press()
                LOG.debug("aiy button pressed")
                self._turn_on_led()
                self.bus.emit(Message(self.button_event))

        # Start a thread when plugin is loaded. This thread is responsible to detect
        # when the button is pressed.
        # create_daemon() method from ovos-utils
        create_daemon(_press_button)

    def _turn_on_led(self):
        """This function turns on the LED. Depending if pulse is enabled the function
        make the LED "breathe" or blink.
        """
        if self.pulse:
            self.leds.pattern = Pattern.breathe(500)
            self.leds.update(Leds.rgb_pattern(eval("Color.{}".format(self.color))))
            LOG.debug("aiy-v2 led pulsing")
        else:
            self.leds.update(Leds.rgb_on(eval("Color.{}".format(self.color))))
            LOG.debug("aiy-v2 led blinking")

    def _handle_led_on(self, _):
        """Handle the record_begin event detection and turn the LED on using the
        _turn_on_led() method.
        """
        self._turn_on_led()

    def _handle_led_off(self, message):
        """Handle the different events that will lead to turn the LED off."""
        # Retrieve message type from the message payload
        message_type = message.msg_type

        if message_type == "recognizer_loop:record_end":
            if self.wakeword_only:
                self.leds.update(Leds.rgb_off())

        self.leds.update(Leds.rgb_off())
