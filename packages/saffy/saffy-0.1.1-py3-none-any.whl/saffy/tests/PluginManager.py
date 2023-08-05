import unittest

from .. import PluginManager


class TestPluginManager(unittest.TestCase):
	@staticmethod
	def smoke_test():
		PluginManager()
		assert 1 == 1

	def custom_plugin_test(self):
		class TestPlugin(PluginManager):
			def __init__(self):
				super().__init__()

		self.assertTrue(TestPlugin in PluginManager.__subclasses__(), 'TestPlugin should be a subclass of the PluginManager')


if __name__ == '__main__':
	unittest.main()
