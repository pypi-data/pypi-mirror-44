#	usage:
#		cd src
#		python3 -m unittest

import unittest
import jobber as dj

class Test_parse_image_url(unittest.TestCase):
	def test_parse_image_url_hello(self):
		url = 'hello'
		reg, path, name, tag, digest = dj.parse_image_url(url)
		self.assertEqual(name, 'hello')
		self.assert_empty([reg, path, tag, digest])
		self.assertEqual(dj.make_image_url(reg, path, name, tag, digest), url)

	def test_parse_image_url_ubuntu(self):
		url = 'linux/ubuntu'
		reg, path, name, tag, digest = dj.parse_image_url(url)
		self.assertEqual(path, 'linux')
		self.assertEqual(name, 'ubuntu')
		self.assert_empty([reg, tag, digest])
		self.assertEqual(dj.make_image_url(reg, path, name, tag, digest), url)

	def test_parse_image_url_digest(self):
		url = 'ubuntu@sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2'
		reg, path, name, tag, digest = dj.parse_image_url(url)
		self.assertEqual(name, 'ubuntu')
		self.assertEqual(digest, 'sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2')
		self.assert_empty([reg, path, tag])
		self.assertEqual(dj.make_image_url(reg, path, name, tag, digest), url)

	def test_parse_image_url_and_digest(self):
		url = 'ubuntu:latest@sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2'
		reg, path, name, tag, digest = dj.parse_image_url(url)
		self.assertEqual(name, 'ubuntu')
		self.assertEqual(tag, 'latest')
		self.assertEqual(digest, 'sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2')
		self.assert_empty([reg, path])
		self.assertEqual(dj.make_image_url(reg, path, name, tag, digest), url)

	def test_parse_image_url_example(self):
		url = 'example.com:5000/mnist/data/numerals:latest'
		reg, path, name, tag, digest = dj.parse_image_url(url)
		self.assertEqual(reg, 'example.com:5000')
		self.assertEqual(path, 'mnist/data')
		self.assertEqual(name, 'numerals')
		self.assertEqual(tag, 'latest')
		self.assertEqual(digest, '')
		self.assertEqual(dj.make_image_url(reg, path, name, tag, digest), url)

	def test_parse_image_url_complex(self):
		url = 'example.com:5000/data/mnist-data:latest@sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2'
		reg, path, name, tag, digest = dj.parse_image_url(url)
		self.assertEqual(reg, 'example.com:5000')
		self.assertEqual(path, 'data')
		self.assertEqual(name, 'mnist-data')
		self.assertEqual(tag, 'latest')
		self.assertEqual(digest, 'sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2')
		self.assertEqual(dj.make_image_url(reg, path, name, tag, digest), url)

	def test_localhost(self):
		url = 'localhost/hello:latest'
		reg, path, name, tag, digest = dj.parse_image_url(url)
		self.assertEqual(reg, 'localhost')
		self.assertEqual(name, 'hello')
		self.assertEqual(tag, 'latest')
		self.assert_empty([path, digest])
		self.assertEqual(dj.make_image_url(reg, path, name, tag, digest), url)

	def assert_empty(self, strs):
		list(map(lambda x: self.assertEqual(x, ''), strs))
