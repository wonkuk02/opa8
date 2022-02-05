from abc import abstractmethod, ABC

from common.realtime import DT_CTRL
from common.numpy_fast import clip
from selfdrive.kegman_kans_conf import kegman_kans_conf

MIN_STEER_SPEED = 0.3


class LatControl(ABC):
  def __init__(self, CP, CI):
    self.kegman_kans = kegman_kans_conf(CP)
    self.sat_count_rate = 1.0 * DT_CTRL
    self.sat_limit = CP.steerLimitTimer
    self.sat_count = 0.
    self.mpc_frame = 0

  def reset(self):
    self.sat_limit.reset()

  def live_tune(self, CP):
    self.mpc_frame += 1
    if self.mpc_frame % 300 == 0:
      # live tuning through /data/openpilot/tune.py overrides interface.py settings
      self.kegman_kans = kegman_kans_conf()
      if self.kegman_kans.conf['tuneGernby'] == "1":
        self.steerLimitTimer = float(self.kegman_kans.conf['steerLimitTimer'])
        self.sat_limit = self.steerLimitTimer

      self.mpc_frame = 0

  @abstractmethod
  def update(self, active, CS, CP, VM, params, last_actuators, desired_curvature, desired_curvature_rate):
    self.live_tune(CP)
    pass

  def reset(self):
    self.sat_count = 0.

  def _check_saturation(self, saturated, CS):
    if saturated and CS.vEgo > 10. and not CS.steeringRateLimited and not CS.steeringPressed:
      self.sat_count += self.sat_count_rate
    else:
      self.sat_count -= self.sat_count_rate
    self.sat_count = clip(self.sat_count, 0.0, self.sat_limit)
    return self.sat_count > (self.sat_limit - 1e-3)
