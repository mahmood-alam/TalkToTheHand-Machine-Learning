
import myo
from myo.utils import TimeInterval

class Listener(myo.DeviceListener):

  def __init__(self):
    self.interval = TimeInterval(None, 0.05)
    self.orientation = None
    self.pose = myo.Pose.rest
    self.emg_enabled = False
    self.locked = False
    self.rssi = None
    self.emg = None

  def on_connected(self, event):
    print("Hello, '{}'! Double tap to exit.".format(event.device_name))
    event.device.vibrate(myo.VibrationType.short)
    event.device.request_battery_level()

  def on_battery_level(self, event):
    print("Your battery level is:", event.battery_level)

  def on_pose(self, event):
    if event.pose == myo.Pose.double_tap:
      return False


if __name__ == '__main__':
  myo.init(sdk_path="C:\Program Files (x86)\Thalmic Labs\myo-sdk-win-0.9.0")
  hub = myo.Hub()
  listener = Listener()
  while hub.run(listener.on_event, 500):
    pass
  print('Bye, bye!')
