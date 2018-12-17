# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.filemanager
import shlex
from subprocess import Popen, PIPE


class SlicerSettingsParserPlugin(
	octoprint.plugin.StartupPlugin,
	octoprint.plugin.EventHandlerPlugin,
):
	def __init__(self):
		self._storage_interface = self._file_manager._storage("local")

	def on_after_startup(self):
		self._logger.info("SlicerSettingsParser active")

	def on_event(self, event, payload):
		if event != "Upload" or payload["target"] != "local":
			return

		self._analyze_file(payload["path"])

	def _analyze_file(self, path):
		command = "sed '/^; .* = .*$/!d ; s/^; \\(.*\\) = \\(.*\\)/\\1=\\2/' %s" % self._storage_interface.path_on_disk(path)

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
__plugin_implementation__ = SlicerSettingsParserPlugin()

