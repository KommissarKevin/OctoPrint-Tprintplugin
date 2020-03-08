# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
import RPi.GPIO as GPIO


class TPrintPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.TemplatePlugin, octoprint.plugin.SettingsPlugin, octoprint.plugin.EventHandlerPlugin):
	def on_after_startup(self):
		self._logger.info("TPrintPlugin started! (pinlight: " + self._settings.get(["pinlight"]) + "; pinfan: " + self._settings.get(["pinfan"]))

	def get_settings_defaults(self):
		return dict(pinlight="4", pinfan="17")

	def get_template_configs(self):
		return [
			dict(type="navbar", custom_bindings=False),
			dict(type="settings", custom_bindings=False)
		]

	def on_event(self, event, payload):
		if event == "Connected":
			# Lampe an
			GPIO.setmode(GPIO.BCM)  # GPIO Nummern statt Board Nummern
			relais_light_gpio = int(self._settings.get(["pinlight"]))
			GPIO.setup(relais_light_gpio, GPIO.OUT)  # GPIO Modus zuweisen
			GPIO.output(relais_light_gpio, GPIO.HIGH)  # an

		if event == "Disconnected":
			# Lampe aus
			GPIO.setmode(GPIO.BCM)  # GPIO Nummern statt Board Nummern
			relais_light_gpio = int(self._settings.get(["pinlight"]))
			GPIO.setup(relais_light_gpio, GPIO.OUT)  # GPIO Modus zuweisen
			GPIO.output(relais_light_gpio, GPIO.LOW)  # aus

		if event == "PrintStarted" or event == "PrintResumed":
			# Bei Start Lüfter
			GPIO.setmode(GPIO.BCM)  # GPIO Nummern statt Board Nummern
			relais_fan_gpio = int(self._settings.get(["pinfan"]))
			GPIO.setup(relais_fan_gpio, GPIO.OUT)  # GPIO Modus zuweisen
			GPIO.output(relais_fan_gpio, GPIO.HIGH)  # an

		if event == "PrintFailed" or event == "PrintCancelled" or event == "PrintPaused":
			# Lüfter aus
			GPIO.setmode(GPIO.BCM)  # GPIO Nummern statt Board Nummern
			relais_fan_gpio = int(self._settings.get(["pinfan"]))
			GPIO.setup(relais_fan_gpio, GPIO.OUT)  # GPIO Modus zuweisen
			GPIO.output(relais_fan_gpio, GPIO.LOW)  # aus


__plugin_name__ = "TPrintPlugin"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = TPrintPlugin()
