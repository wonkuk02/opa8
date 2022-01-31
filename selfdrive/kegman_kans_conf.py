import json
import os

class kegman_kans_conf():
  def __init__(self, CP=None):
    self.conf = self.read_config()
    if CP is not None:
      self.init_config(CP)

  def init_config(self, CP):
    write_conf = False
    if self.conf['tuneGernby'] != "1":
      self.conf['tuneGernby'] = str(1)
      write_conf = True

    # only fetch Kp, Ki, Kf sR and sRC from interface.py if it's a PID controlled car
    if CP.lateralTuning.which() == 'pid':
      if self.conf['Kp'] == "-1":
        self.conf['Kp'] = str(round(CP.lateralTuning.pid.kpV[0],3))
        write_conf = True
      if self.conf['Ki'] == "-1":
        self.conf['Ki'] = str(round(CP.lateralTuning.pid.kiV[0],3))
        write_conf = True
      if self.conf['Kd'] == "-1":
        self.conf['Kd'] = str(round(CP.lateralTuning.pid.kdV[0],3))
        write_conf = True
      if self.conf['Kf'] == "-1":
        self.conf['Kf'] = str('{:f}'.format(CP.lateralTuning.pid.kf))
        write_conf = True

    if write_conf:
      self.write_config(self.config)

  def read_config(self):
    self.element_updated = False

    if os.path.isfile('/data/kegman_kans.json'):
      with open('/data/kegman_kans.json', 'r') as f:
        self.config = json.load(f)

      if "battPercOff" not in self.config:
        self.config.update({"battPercOff":"80"})
        self.config.update({"carVoltageMinEonShutdown":"12000"})
        self.config.update({"brakeStoppingTarget":"0.65"})
        self.element_updated = True

      if "tuneGernby" not in self.config:
        self.config.update({"tuneGernby":"1"})
        self.config.update({"Kp":"0.25"})
        self.config.update({"Ki":"0.12"})
        self.config.update({"Kd":"0.00017"})
        self.element_updated = True

      if "liveParams" not in self.config:
        self.config.update({"liveParams":"1"})
        self.element_updated = True

      if "ONE_BAR_DISTANCE" not in self.config:
        self.config.update({"ONE_BAR_DISTANCE":"1.0"})
        self.config.update({"TWO_BAR_DISTANCE":"1.8"})
        self.config.update({"THREE_BAR_DISTANCE":"2.7"})
        self.config.update({"STOPPING_DISTANCE":"2.0"})
        self.element_updated = True

      if "deadzone" not in self.config:
        self.config.update({"deadzone":"0.15"})
        self.element_updated = True

      if "1barBP0" not in self.config:
        self.config.update({"1barBP0":"-0.3"})
        self.config.update({"1barBP1":"1.85"})
        self.config.update({"2barBP0":"-0.2"})
        self.config.update({"2barBP1":"2.25"})
        self.config.update({"3barBP0":"-0.1"})
        self.config.update({"3barBP1":"3.2"})
        self.element_updated = True

      if "1barMax" not in self.config:
        self.config.update({"1barMax":"1.6"})
        self.config.update({"2barMax":"2.0"})
        self.config.update({"3barMax":"2.95"})
        self.element_updated = True

      if "1barHwy" not in self.config:
        self.config.update({"1barHwy":"0.4"})
        self.config.update({"2barHwy":"0.3"})
        self.config.update({"3barHwy":"0.2"})
        self.element_updated = True

# AutoHold
      if "AutoHold" not in self.config:
        self.config.update({"AutoHold":"1"})
        self.element_updated = True

      if "nTune" not in self.config:
        self.config.update({"nTune":"1"})
        self.element_updated = True

      if "steerLimitTimer" not in self.config:
        self.config.update({"steerLimitTimer":"5.0"})
        self.element_updated = True

      if "CruiseDelta" not in self.config:
        self.config.update({"CruiseDelta":"5"})
        self.element_updated = True

      if "CruiseEnableMin" not in self.config:
        self.config.update({"CruiseEnableMin":"10"})
        self.element_updated = True

      if "epsModded" not in self.config:
        self.config.update({"epsModded":"0"})
        self.element_updated = True

      if "CAMERA_SPEED_FACTOR" not in self.config:
        self.config.update({"CAMERA_SPEED_FACTOR":"0.98"})
        self.element_updated = True

      if self.element_updated:
        print("updated")
        self.write_config(self.config)

    else:
      self.config = {"battChargeMin":"60", "battChargeMax":"75", "wheelTouchSeconds":"18000", \
                     "battPercOff":"80", "carVoltageMinEonShutdown":"12000", \
                     "brakeStoppingTarget":"0.65", "tuneGernby":"1", "AutoHold":"1", "steerLimitTimer":"5.0", \
                     "Kp":"0.25", "Ki":"0.12", "Kd":"0.000017", "Kf":"0.00006", "liveParams":"1", "deadzone":"0.15", \
                     "1barBP0":"-0.3", "2barBP0":"-0.2", "3barBP0":"-0.1", \
                     "1barBP1":"1.85", "2barBP1":"2.25", "3barBP1":"3.2", \
                     "1barMax":"1.6", "2barMax":"2.0", "3barMax":"2.95", "STOPPING_DISTANCE":"2.0", \
                     "ONE_BAR_DISTANCE":"1.0", "TWO_BAR_DISTANCE":"1.8", "THREE_BAR_DISTANCE":"2.7", \
                     "1barHwy":"0.4", "2barHwy":"0.3", "3barHwy":"0.2", "CruiseDelta":"5", \
                     "CruiseEnableMin":"10", "epsModded": "0", "CAMERA_SPEED_FACTOR":"0.98"}


      self.write_config(self.config)
    return self.config

  def write_config(self, config):
    try:
      with open('/data/kegman_kans.json', 'w') as f:
        json.dump(self.config, f, indent=2, sort_keys=True)
        os.chmod("/data/kegman_kans.json", 0o764)
    except IOError:
      os.mkdir('/data')
      with open('/data/kegman_kans.json', 'w') as f:
        json.dump(self.config, f, indent=2, sort_keys=True)
        os.chmod("/data/kegman_kans.json", 0o764)