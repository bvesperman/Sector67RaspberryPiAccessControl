import unittest

class DoorTest(unittest.TestCase):
	"""tests that the lights work"""
	def setUp(self):
		self.fizz = 'fizz'
		self.foo = 'foo'
		self.bar = 'bar'
		self.foobar = [self.foo, self.bar]

	def test_something(self):
		self.assertTrue(True)


if __name__ == '__main__':
	unittest.main(exit=False)
