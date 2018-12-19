$(() => {
	$("#SlicerSettingsParser_analyze").click(() => {
		console.log("SlicerSettingsParser analyze_all");
		$.ajax({
		    url: "/api/plugin/SlicerSettingsParser",
		    type: "POST",
			data:  JSON.stringify({ command: "analyze_all" }),
			contentType: "application/json",
		})
	})
})
