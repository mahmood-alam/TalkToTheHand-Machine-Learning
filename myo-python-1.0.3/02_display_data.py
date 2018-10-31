# The MIT License (MIT)
#
# Copyright (c) 2017 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
"""
This example displays the orientation, pose and RSSI as well as EMG data
if it is enabled and whether the device is locked or unlocked in the
terminal.

Enable EMG streaming with double tap and disable it with finger spread.
"""

from __future__ import print_function
from myo.utils import TimeInterval
import myo
import sys
import time
import pandas as pd

class Listener(myo.DeviceListener):

  def __init__(self):
    self.interval = TimeInterval(None, 0.05)
    self.orientation = None
    self.pose = myo.Pose.rest
    self.emg_enabled = True
    self.locked = False
    self.rssi = None
    self.emg = None
    #self.output = ""
    self.csv = open("out.csv",'a')
    self.LABEL = 'j'

  def output(self):
    if not self.interval.check_and_reset() or not self.emg or not self.orientation:
      return

    parts = []
    for comp in self.orientation:
        parts.append('{:.4f}'.format( comp))
    #parts.append(str(self.pose).ljust(10))
    #parts.append('E' if self.emg_enabled else ' ')
    #parts.append('L' if self.locked else ' ')
    #parts.append(self.rssi or 'NORSSI')

    for comp in self.emg:
        parts.append(str(comp).strip())
    line = self.LABEL + ', {:.4f}, '.format(time.time()) + ''.join('{}, '.format(p) for p in parts) + '\n'
    self.csv.write(line)
    self.csv.flush()
    print(line, end='')
    sys.stdout.flush()

  def on_connected(self, event):
    event.device.request_rssi()
    #event.device.request_battery_level()

  def on_rssi(self, event):
    self.rssi = event.rssi
    #self.output()

  def on_pose(self, event):
    self.pose = event.pose
    event.device.stream_emg(True)
    self.output()
    """
    if self.pose == myo.Pose.double_tap:
      event.device.stream_emg(True)
      self.emg_enabled = True
    elif self.pose == myo.Pose.fingers_spread:
      event.device.stream_emg(False)
      self.emg_enabled = False
      self.emg = None
    self.output()
    """

  def on_orientation(self, event):
    self.orientation = event.orientation
    self.output()

  def on_emg(self, event):
    self.emg = event.emg
    self.output()

  def on_unlocked(self, event):
    #self.locked = False
    #self.output()
    pass

  def on_locked(self, event):
    #self.locked = True
    #self.output()
    pass

if __name__ == '__main__':
  #out = {'timestamp':" ", 'Quaternion': [], 'EMG': []}

  myo.init(sdk_path="C:\Program Files (x86)\Thalmic Labs\myo-sdk-win-0.9.0")
  hub = myo.Hub()
  listener = Listener()
  while hub.run(listener.on_event, 500):
    pass


  def prediction(inputdata):

    data = pd.read_csv('./output.csv',header=None)#,names = ['label','time','qa','qb','qc','qd','1','2','3','4','5','6','7','8'])
    data.drop(data.columns[[-1,]], axis=1, inplace=True)
    X = data.iloc[:,1:].values
    y = data.iloc[:,0].values


    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaler.fit(X_train)

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    from sklearn.neighbors import KNeighborsClassifier
    classifier = KNeighborsClassifier(n_neighbors=5)
    classifier.fit(X_train, y_train)

    classifier.predict(input)

