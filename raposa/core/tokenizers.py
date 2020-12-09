import itertools
import re

from nltk import word_tokenize, sent_tokenize


class BasicTokenizer():

	def __init__(self):
		pass

	def split(self, text):
		return self._process(text)

	def _process(self, text):
		return [text]

	# Unused for now, but may come in handy for some subclass
	@staticmethod
	def _flatten(arr):
		for i in arr:
			if isinstance(i, list):
				yield from BasicTokenizer._flatten(i)
			else:
				yield i


class WhitespaceTokenizer(BasicTokenizer):

	def _process(self, text):
		return ctxt.split()


class NewlineTokenizer(BasicTokenizer):

	def _process(self, text):
		return text.splitlines()


class NltkWordTokenizer(BasicTokenizer):

	def _process(self, text):
		return word_tokenize(text)


class NltkSentTokenizer(BasicTokenizer):

	def _process(self, text):
		return sent_tokenize(text)


class RegexTokenizer(BasicTokenizer):

	def __init__(self, regex, compiled=False):
		if compiled:
			self.regex = regex
		else:
			self.regex = re.compile(regex)

	def _process(self, ctxt):
		return [s for s in self.regex.split(ctxt) if s]
