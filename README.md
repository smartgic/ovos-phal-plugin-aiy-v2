# PHAL plugin - Google AIY Voice Kit V2

A plugin to handle the button and LED from the famous Google AIY Voice Kit V2

[![Video](https://img.youtube.com/vi/o8ih1P3NI60/maxresdefault.jpg)](https://www.youtube.com/watch?v=o8ih1P3NI60)

## About

This PHAL plugin interacts with the button and the LED connected to AIY Voice Bonnet.

- When a wake word is detected the LED turns on and when the audio output is over the LED turns off.
- When the button is pressed, the default behaviour is to make the assistant listen and turn on the LED.

It also possible to configure the plugin to only turn the LED on and off during the listening (not the audio output).

## Installation

```shell
pip install ovos-phal-plugin-aiy-v2
```

## Configuration

The plugin configuration file is `~/.config/OpenVoiceOS/ovos-phal-plugin-aiy-v2.json`.

| Option          | Value                | Description                                                   |
| --------------- | -------------------- | ------------------------------------------------------------- |
| `color`         | `green`              | Define the color of the LED                                   |
| `wakeword_only` | `false`              | Turn on the LED only during the wakeword detection            |
| `pulse`         | `true`               | Make the LED pulse                                            |
| `button_event`  | `mycroft.mic.listen` | Which event to send to message bus when the button is pressed |

### Example

Configuration sample of `~/.config/OpenVoiceOS/ovos-phal-plugin-aiy-v2.json`.

```json
{
  "color": "green",
  "wakeword_only": false,
  "pulse": true,
  "button_event": "mycroft.mic.listen"
}
```

## Credits

- [Smart'Gic](https://smartgic.io/)
