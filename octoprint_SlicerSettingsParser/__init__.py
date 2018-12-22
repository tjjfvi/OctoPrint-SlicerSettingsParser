# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.filemanager
import shlex
import flask
from subprocess import Popen, PIPE


class SlicerSettingsParserPlugin(
	octoprint.plugin.StartupPlugin,
	octoprint.plugin.EventHandlerPlugin,
	octoprint.plugin.SettingsPlugin,
	octoprint.plugin.TemplatePlugin,
	octoprint.plugin.AssetPlugin,
	octoprint.plugin.SimpleApiPlugin,
):
	# def initialize(self):

	def on_after_startup(self):
		self._storage_interface = self._file_manager._storage("local")
		self._logger.info("SlicerSettingsParser still active")

	def get_settings_defaults(self):
		return dict(
			sed_command="/^; .* = .*$/!d ; s/^; \\(.*\\) = \\(.*\\)/\\1=\\2/",
		)

	def get_template_configs(self):
	    return [
	        dict(type="settings", custom_bindings=False)
	    ]

	def get_assets(self):
		return dict(js=["js/SlicerSettingsParser.js"])

	def get_api_commands(self):
		self._logger.info("Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
		return dict(
			analyze_all=[]
		)

	def on_api_command(self, command, data):
		import flask
		self._logger.info("recieveed api command: %s" % command)
		if command == "analyze_all":
			self._analyze_all()

	def on_event(self, event, payload):
		if event != "Upload" or payload["target"] != "local":
			return

		self._analyze_file(payload["path"])

	def _analyze_all(self):
		process = Popen(["find"], cwd=self._storage_interface.path_on_disk(""), stdin=PIPE, stdout=PIPE, stderr=PIPE)
		(output, error) = process.communicate()

		if error != "":
			self._logger.error("find command errored: %s" % error)
			return

		files = list(filter(lambda f: ".gcode" in f, output.split("\n")))

		for file in files:
			self._analyze_file(file[2:])

	def _analyze_file(self, path):
		self._logger.info("Analyzing file: %s" % path)

		command = "sed '%s' %s" % (self._settings.get(["sed_command"]), self._storage_interface.path_on_disk(path))

		self._logger.info("Running command: %s" % command);

		process = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=PIPE)
		(output, error) = process.communicate()

		if error != "":
			self._logger.error("Command errored: %s" % error)
			return

		slicer_settings = dict()
		lines = output.split("\n")

		for line in lines:
			split_line = line.split("=")
			key = split_line[0]
			value = "=".join(split_line[1:])
			slicer_settings[key] = value

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

