# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.filemanager
import re
import flask

class SlicerSettingsParserPlugin(
	octoprint.plugin.StartupPlugin,
	octoprint.plugin.EventHandlerPlugin,
	octoprint.plugin.SettingsPlugin,
	octoprint.plugin.TemplatePlugin,
	octoprint.plugin.AssetPlugin,
	octoprint.plugin.SimpleApiPlugin,
):
	def on_after_startup(self):
		self._storage_interface = self._file_manager._storage("local")
		self._logger.info("SlicerSettingsParser still active")

	def get_settings_defaults(self):
		return dict(
			regexes=[
				"^; (?P<key>[^,]*?) = (?P<val>.*)",
				"^;   (?P<key>.*?),(?P<val>.*)",
			]
		)

	def get_template_configs(self):
	    return [
	        dict(type="settings", custom_bindings=True)
	    ]

	def get_assets(self):
		return dict(js=["js/SlicerSettingsParser.js"])

	def get_api_commands(self):
		return dict(
			analyze_all=[]
		)

	def on_api_command(self, command, data):
		import flask
		self._logger.info("received api command: %s" % command)
		if command == "analyze_all":
			self._analyze_all()

	def on_event(self, event, payload):
		if event != "Upload" or payload["target"] != "local":
			return

		self._analyze_file(payload["path"])

	def _analyze_all(self):
		def recurse(files):
			for key in files:
				file = files[key]

				if file["type"] == "folder":
					recurse(file["children"])
					continue

				if file["typePath"][-1] != "gcode": continue

				self._analyze_file(file["path"])



		recurse(self._storage_interface.list_files())

	def _analyze_file(self, path):
		self._logger.info("Analyzing file: %s" % path)

		file = open(self._storage_interface.path_on_disk(path))

		slicer_settings = dict()
		regexes = map(lambda x: re.compile(x), self._settings.get(["regexes"]))

		for line in file:
			for regex in regexes:
				match = re.search(regex, line)

				if not match: continue

				key, val = match.group("key", "val")
				slicer_settings[key] = val

				break

		self._storage_interface.set_additional_metadata(path, "slicer_settings", slicer_settings, overwrite=True)

		self._logger.info("Saved slicer settings metadata for file: %s" % path)

		# self._logger.info(self._storage_interface.get_metadata(path))

        def get_update_information(self):
                return dict(
                        SlicerSettingsParser=dict(
                                displayName="SlicerSettingsParser Plugin",
                                displayVersion=self._plugin_version,

                                # version check: github repository
                                type="github_release",
                                user="tjjfvi",
                                repo="OctoPrint-SlicerSettingsParser",
                                current=self._plugin_version,

                                # update method: pip
                                pip="https://github.com/tjjfvi/OctoPrint-SlicerSettingsParser/archive/{target_version}.zip"
                        )
                )

__plugin_name__ = "SlicerSettingsParser"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = SlicerSettingsParserPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
