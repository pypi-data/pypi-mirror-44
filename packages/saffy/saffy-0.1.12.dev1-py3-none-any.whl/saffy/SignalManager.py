import numpy as np

import types

from obci_readmanager.signal_processing.read_manager import ReadManager

from saffy.plugins import *

plugins = PluginManager.__subclasses__()


class SignalManager(*plugins):
	def __init__(self, name='', *args, **kwargs):
		for plugin in SignalManager.__bases__:
			super(plugin, self).__init__(*args, **kwargs)

		self.name = name

		if 'filename' in kwargs:
			filename = kwargs['filename']

			mgr = ReadManager("%s.xml" % filename, "%s.raw" % filename, "%s.tag" % filename)

			self.fs = int(float(mgr.get_param("sampling_frequency")))

			self.num_channels = int(mgr.get_param("number_of_channels"))
			self.channel_names = mgr.get_param("channels_names")

			self.data = mgr.get_microvolt_samples()
			self.data = np.reshape(self.data, (1, *self.data.shape))

			self.t = np.arange(self.data.shape[1]) / self.fs

			self.epochs = 1
			self.tags = []

		if 'generator' in kwargs:
			generator = kwargs['generator']

			self.fs = generator['fs']

			self.num_channels = generator['num_channels']
			self.channel_names = generator['channel_names']

			self.data = generator['data']
			self.t = generator['t']

			self.epochs = generator['epochs']
			self.tags = generator['tags']

	def __getattribute__(self, attr):
		def call_history(method):
			def out(*args, **kwargs):
				_args = [arg.__repr__() for arg in args]
				_kwargs = [f"{key}={kwargs[key]}" for key in kwargs]
				self.history.append(f'{method.__name__}({",".join(_args)}, {",".join(_kwargs)})')
				return method(*args, **kwargs)

			return out

		method = object.__getattribute__(self, attr)

		if type(method) == types.MethodType:
			method = call_history(method)

		return method

	def set_tags_from_channel(self, channel_name):
		tag_channel = self.data[:, self.channel_names.index(channel_name)]

		tag_channel = tag_channel / np.max(tag_channel)

		self.tags = np.where(tag_channel > 0.9)[1]

		self.tags = self.tags[
			np.concatenate(([0], np.where(np.diff(self.tags) > 1)[0] + 1))
		]

	def set_epochs_from_tags(self, low, high):
		self.t = np.arange(low, high, 1 / self.fs)

		low = int(low * self.fs)
		high = int(high * self.fs)

		length = high - low
		data = np.zeros((len(self.tags), self.num_channels, length))

		self.epochs = len(self.tags)

		for idx, tag in enumerate(self.tags):
			data[idx] = self.data[:, :, tag + low: tag + high]

		self.data = data
		self.tags = []

	def remove_channel(self, channel_name):
		channel_id = self.channel_names.index(channel_name)

		self.data = np.delete(self.data, channel_id, 1)
		del self.channel_names[channel_id]
		self.num_channels -= 1

	def extract_channels(self, channel_names):
		channel_ids = [self.channel_names.index(channel_name) for channel_name in channel_names]

		self.data = self.data[:, channel_ids, :]
		self.num_channels = len(channel_ids)
		self.channel_names = list(filter(
			lambda x: self.channel_names.index(x) in channel_ids,
			self.channel_names
		))

	def extract_time_range(self, low, high):
		low_samp = low * self.fs
		high_samp = high * self.fs

		self.t = np.arange(low, high, 1 / self.fs)

		self.data = self.data[:, :, low_samp: high_samp]

	def copy(self, name=''):
		return SignalManager(name=name, generator={
			'fs': self.fs,
			'num_channels': self.num_channels,
			'channel_names': self.channel_names,
			'epochs': self.epochs,
			'data': self.data,
			't': self.t,
			'tags': self.tags
		})

	@classmethod
	def register_plugin(cls, plugin):
		cls.__bases__ = tuple(filter(lambda x: str(x) != str(plugin), cls.__bases__))
		cls.__bases__ = (*cls.__bases__, plugin)

	def __str__(self):
		return 'Signal Manager'

	def __repr__(self):
		return 'Signal Manager'


if __name__ == '__main__':
	SignalManager()
