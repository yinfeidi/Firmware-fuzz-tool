from boofuzz import *
from boofuzz.constants import DEFAULT_WEB_UI_PORT
import os


class New_target(Target):
    def __init__(self, connection, monitors=None, monitor_alive=None, max_recv_bytes=10000, repeater=None, firmware_log=None, interval = 0.4, **kwargs):
        super(New_target, self).__init__(connection)
        self.firmware_log = firmware_log
        self.XSS_payloads = []
        self.BO_payloads = []
        self.CI_payloads = []
        self.interval = interval


class IOT_mutate(primitives.base_primitive.BasePrimitive):
    def __init__(self, value, fuzzable=True, max_len=0, name=None, exploit_dir="./", attack_mode=0, encoding="ascii",):
        super(IOT_mutate, self).__init__()
        left = None
        self._original_value = value
        self._value = bytes(value, encoding="ascii")
        self._fuzzable = fuzzable
        self._name = name
        self._fuzz_library = [bytes("", encoding="ascii"), self._value]
        if "=" in self._original_value:
            left = self._original_value.split("=")[0]
            right = self._original_value.split("=")[0]
        for item in ["ci.txt", "xss.txt", "overflow.txt"]:
            path = os.path.join(exploit_dir, item)
            with open(path, "rb") as _file_handle:
                content = list(filter(None, _file_handle.read().splitlines()))
                for s in content:
                    self._fuzz_library.append(s)
                    self._fuzz_library.append(self._value + s)
                    if left:
                        self._fuzz_library.append(bytes(left + "=", encoding="ascii") + s)
                        self._fuzz_library.append(bytes(left + "=" + right, encoding="ascii") + s)
    @property
    def name(self):
        return self._name    

def s_attack(value, encoding="ascii", fuzzable=True, max_len=0, name=None, exploit_dir="./", attack_mode=0):
    s = IOT_mutate(value, fuzzable, max_len, name, exploit_dir, attack_mode)
    blocks.CURRENT.push(s)