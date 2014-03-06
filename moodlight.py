from maya.utils import executeDeferred
import pymel.core as pm
import threading
import time


_active_mood_light = None
_running = False


class MoodLightThread(threading.Thread):

	def __init__(self, speed):
		self.speed = speed
		super(MoodLightThread, self).__init__()

	def run(self):
		while _running:
			time.sleep(0.05)
			color = pm.dt.Color()
			hue = time.time() * self.speed % 1 * 360
			color.set('HSV', hue, 1, 0.3)
			executeDeferred(
				pm.mel.displayRGBColor,
				'backgroundBottom',
				color.r,
				color.g,
				color.b
			)
			color.set('HSV', hue, 0.3, 1)
			executeDeferred(
				pm.mel.displayRGBColor,
				'backgroundTop',
				color.r,
				color.g,
				color.b
			)


def is_running():
	global _active_mood_light, _running
	return _active_mood_light is not None and _running


def start(speed=0.05):
	global _active_mood_light, _running
	stop()
	_running = True
	_active_mood_light = MoodLightThread(speed)
	_active_mood_light.start()


def stop():
	global _active_mood_light, _running
	if is_running():
		_running = False
		_active_mood_light.join()
		_active_mood_light = None