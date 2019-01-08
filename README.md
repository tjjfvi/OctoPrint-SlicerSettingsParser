# OctoPrint-SlicerSettingsParser

**NOTE: Only supports Slic3r, Simplify3D, and Cura currently; suggest more in issues; contributions welcome!**

Analyses gcode for slicer settings comments and adds additional metadata of such settings. Useless without plugin(s) to use the metadata. 

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/tjjfvi/OctoPrint-SlicerSettingsParser/archive/master.zip

You will most likely want to install another plugin to use the metadata. Such plugins of mine are:
 - [OctoPrint-SlicerSettingsTab](https://github.com/tjjfvi/OctoPrint-SlicerSettingsTab)
 
### Cura

Cura doesn't natively support injecting the slicer settings into the gcode, so you must add [this](https://gist.github.com/tjjfvi/75210b2ed20ed194d6eab48bf70c4f12) to your start/end gcode.

## Configuration

### Python regexes (Advanced)

This plugin uses python regexes to parse the gcode.
Syntax can be easily found on the web.
There should be two named capturing groups, `key` and `val`.
Multiple regexes should be listed on seperate lines, ordered by precedence.
Any chars are allowed in the groups; `\n` will be replaced by newlines.

See the [wiki](https://github.com/tjjfvi/OctoPrint-SlicerSettingsParser/wiki/Python-regexes) for examples.
