import re

import emoji

class FilterError(Exception):
    pass


class InputError(FilterError):

    def __init__(self, expression):
        self.expression = expression


class BaseFilter:

    # tag keys must be of the following shape to avoid clashes:
    # t_FILTER_TAGNAME
    # with the following meanings
    # t : fixed prefix
    # FILTER : name of the filter
    # TAGNAME : name of the tag for this filter

    # t_FILTER_match is reserved
    # discard decision is saved there automatically

	def __init__(self, discard=True, inverse=False, slug="base", **kwargs):
		self._discard = discard
		self.slug = slug
		self._inverse = inverse


	def evaluate(self, s):
		discards = self._process(s)
		s["t_"+self.slug+"_match"] = discards
		# if not _discard, then always False (allow through)
		# ^ = XOR
		# basically uses _inverse as NOT flag for discards
		return self._discard and (self._inverse ^ discards)


	def _process(self, s):
		return False


	def matches(self, s):
		# s must be a string
		# simpler method for occasional use
		# throws away much of the info
		return self.evaluate({"val": s})


class ComboFilter(BaseFilter):

	def __init__(self, lst_filters, slug="combo", **kwargs):
		self.lst_filters = lst_filters
		super().__init__(self, slug=slug, **kwargs)


	def _process(self, s):
		return any([f.evaluate(s) for f in self])


	def __iter__(self):
		for f in self.lst_filters:
			yield f


class RegexFilter(BaseFilter):

	def __init__(self, regex, compiled=False, slug="regex", **kwargs):
		if compiled:
			self.regex = regex
		else:
			self.regex = re.compile(regex)
		super().__init__(slug=slug, **kwargs)


	def _process(self, word):
		return (self.regex.fullmatch(word["val"]) is not None)


class NumberFilter(RegexFilter):

	def __init__(self, slug="number", **kwargs):
		super().__init__("[0-9]+", slug=slug, **kwargs)


class EmojiFilter(RegexFilter):

	def __init__(self, slug="emoji", **kwargs):
		rx = emoji.get_emoji_regexp()
		super().__init__(rx, compiled=True, slug=slug, **kwargs)


class PunctFilter(RegexFilter):

	def __init__(self, slug="punct", **kwargs):
		super().__init__("[^\w0-9'-]+", slug=slug, **kwargs)


class PunctRemoval(PunctFilter):

	# same regex as PunctFilter
	# but this one replaces punctuation in the word
	# and does not filter

	def __init__(self, slug="punctrem", **kwargs):
		super().__init__(slug=slug, **kwargs)


	def _process(self, word):
		before = word["val"]
		after = self.regex.sub('', before)
		word["f_punctrem_before"] = before
		word["f_punctrem_after"] = after
		word["val"] = after
		return (after == "") # discard only if nothing left


class DictFilter(BaseFilter):

	def __init__(self, exclusion=None, file=None, ignore_case=True, slug="dict", **kwargs):

		self._ignore_case = ignore_case

		if file is not None:
			with open(file) as f:
				if ignore_case:
					self._exclusion = set(l.strip().lower() for l in f if l.strip())
				else:
					self._exclusion = set(l.strip() for l in f if l.strip())

		elif exclusion is not None:
			if ignore_case:
				self._exclusion = set(e.lower() for e in exclusion)
			else:
				self._exclusion = set(exclusion)

		else:
			raise InputError("Either a exclusion list/set or a file are needed")

		super().__init__(slug=slug, **kwargs)


	def _process(self, s):
		w = s["val"]
		if self._ignore_case:
			w = w.lower()
		return (w in self._exclusion)

