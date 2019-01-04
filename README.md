# OctoPrint-SlicerSettingsParser

**NOTE: Only supports Slic3r currently; suggest more in issues; contributions welcome!**

Analyses gcode for slicer settings comments and adds additional metadata of such settings. Useless without plugin(s) to use the metadata. 

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/tjjfvi/OctoPrint-SlicerSettingsParser/archive/master.zip

You will most likely want to install another plugin to use the metadata. Such plugins of mine are:
 - [OctoPrint-SlicerSettingsTab](https://github.com/tjjfvi/OctoPrint-SlicerSettingsTab)

## Configuration

### Sed command (Advanced)

This plugin uses `sed` to parse the gcode. Sed command syntax can be easily found on the web [(help)](http://lmgtfy.com/?q=sed+command+syntax). The output should be of the format:
```
key=value
key2=value
key lalalalala=value=haha
with_newlines=abc\ndef
```
will be parsed as (JSON):
```json
{
    "key": "value",
    "key2": "value",
    "key lalalalala": "value=haha",
    "with_newlines": "abc\ndef"
}
```
