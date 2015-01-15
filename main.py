# -*- coding: utf-8 -*-
from bottle import run, debug
import controllers
DEBUG = True
debug(DEBUG)
run(host='localhost', port=8080, reloader=DEBUG)


# class MainClass:

# 	def __init__(self):
# 		self.say_hello()

# 	def say_hello(self):
# 		print("Hello, World!")


# if(__name__ == "__main__"):
# 	MainClass()