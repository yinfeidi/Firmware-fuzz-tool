import os, re, json, sys, time, argparse
from configparser import ConfigParser




class myparser(ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr

