### A convenient pose wrapper

#### Requirements

You need steamVR running to use it.

#### Usage

Simple sampling example, return dictionnary poses values converted to different useful formats.
```
"""Example script using pose_openvr_wrapper."""
import pose_openvr_wrapper

pyopenvr_wrapper = pose_openvr_wrapper.OpenvrWrapper('cfg/config.json')
print(pyopenvr_wrapper.devices)

samples = pyopenvr_wrapper.sample('tracker_0', samples_count=10)
print(samples)
```
 it's also possible to get relative poses, from choosen reference device to target device.

```
relative_samples = pyopenvr_wrapper.sample(
       ref_device_key='tracking_reference_1',
       target_device_key='tracker_0', samples_count=10)

print(relative_samples)
```


#### Example config file :
 It require a config file to always keep same tracker/lighthouses names.
```
{
    "devices":[
        {
          "name": "tracking_reference_0",
          "type": "tracking_reference",
          "serial":"LHB-02F97E98"
        },
        {
          "name": "tracking_reference_1",
          "type": "tracking_reference",
          "serial":"LHB-431A55FD"
        },
        {
          "name": "tracker_0",
          "type": "tracker",
          "serial":"LHR-3CD1A9DA"
        },
        {
          "name": "tracker_1",
          "type": "tracker",
          "serial":"LHR-25865D81"
        },
        {
          "name": "tracker_2",
          "type": "tracker",
          "serial":"LHR-4359D2B6"
        }
    ]
}
```
