$(() => {
	function SlicerSettingsParserViewModel([ settingsViewModel ]){
		let self = this;

		self.startupComplete = ko.observable(false);

		self.analyzeAll = () => {
			console.log("SlicerSettingsParser analyze_all");
			$.ajax({
			    url: "api/plugin/SlicerSettingsParser",
			    type: "POST",
				data:  JSON.stringify({ command: "analyze_all" }),
				contentType: "application/json",
			})
		};

		self.joinedRegexes = ko.computed({
			read: () => self.startupComplete() && self.settings.regexes().join("\n"),
			write: rs => self.startupComplete() && self.settings.regexes(rs.split("\n")),
		});

		self.onStartupComplete = () => {
			console.log("hi!");
			self.settings = settingsViewModel.settings.plugins.SlicerSettingsParser;
			self.startupComplete(true);
			// console.log(self.settings.events(), self.events());
		}
	}

    OCTOPRINT_VIEWMODELS.push({
        construct: SlicerSettingsParserViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#settings_plugin_SlicerSettingsParser"],
    });
})
