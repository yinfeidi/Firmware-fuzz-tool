# SIoTFuzzer
There are three components in this projject: Emulation, Spider and Fuzzer.
## Emulation
The Emulation component is based on Firmadyne and we futher add some modification in the linux kernel as well as the filesystem.
You can follow the ### setup.sh in this component to set up your emulation enviroment.

## Spider 
This component is used to capture the pcaps between the emulated devices and browsers.

## Fuzzer
This component fuzzes the pcaps captured in Spider.
