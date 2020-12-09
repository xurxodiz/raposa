import re

import emoji


class TubeError(Exception):
    pass


class InputError(TubeError):

    def __init__(self, expression):
        self.expression = expression


class BasicTube:

    # tag keys must be of the following shape to avoid clashes:
    # t_FILTER_TAGNAME
    # with the following meanings
    # t : fixed prefix
    # FILTER : name of the filter
    # TAGNAME : name of the tag for this filter

    # t_FILTER_match is reserved
    # discard decision is saved there automatically

	def __init__(self, tag=False, discard=True, inverse=False, slug="base", **kwargs):
		self._discard = discard
		self.slug = slug
		self._inverse = inverse
		self._tag = tag

	def pipe(self, gen_unit):
		for unit in gen_unit:
			new_unit = self._process(unit)
			out_unit = new_unit or unit
			# if it shouldn't discard, allow through
			# otherwise, allow only if a new unit was produced
			# [other way around if inverse is enabled (^ = XOR)]
			if (not self._discard or (self._inverse ^ bool(new_unit))):
				if self._tag:
					out_unit["t_"+self.slug+"_match"] = bool(new_unit)
				yield out_unit

	def _process(self, unit):
		return None


class ValAdaptor(BasicTube):

	def __init__(self, slug="val", **kwargs):
		super().__init__(slug=slug, **kwargs)

	def _process(self, unit):
		return {"val": unit}


class LowercaseAdaptor(BasicTube):

	def __init__(self, slug="lower", **kwargs):
		super().__init__(slug=slug, **kwargs)

	def _process(self, unit):
		if type(unit) == str:
			return unit.lower()
		else:
			unit["val"] = unit["val"].lower()
			return unit


class UppercaseAdaptor(BasicTube):

	def __init__(self, slug="upper", **kwargs):
		super().__init__(slug=slug, **kwargs)

	def _process(self, unit):
		if type(unit) == str:
			return unit.upper()
		else:
			unit["val"] = unit["val"].upper()
			return unit


class RegexFilter(BasicTube):

	def __init__(self, regex, compiled=False, slug="regex", **kwargs):
		if compiled:
			self.regex = regex
		else:
			self.regex = re.compile(regex)
		super().__init__(slug=slug, **kwargs)

	def _process(self, unit):
		return None if self.regex.fullmatch(unit["val"]) else unit


class NumberFilter(RegexFilter):

	def __init__(self, slug="number", **kwargs):
		super().__init__(r'[0-9.,]+', slug=slug, **kwargs)


class HashtagFilter(RegexFilter):

	def __init__(self, slug="hashtag", **kwargs):
		super().__init__(r'#.*', slug=slug, **kwargs)


class MentionFilter(RegexFilter):

	def __init__(self, slug="mention", **kwargs):
		super().__init__(r'@.*', slug=slug, **kwargs)


class UrlFilter(RegexFilter):

	def __init__(self, slug="url", **kwargs):
		super().__init__(r'https?://\S+', slug=slug, **kwargs)


class EmojiFilter(RegexFilter):

	def __init__(self, slug="emoji", **kwargs):
		rx = emoji.get_emoji_regexp()
		super().__init__(rx, compiled=True, slug=slug, **kwargs)

	def _process(self, unit):
		return None if all([self.regex.fullmatch(c) for c in unit["val"]]) else unit


class PunctFilter(RegexFilter):

	def __init__(self, slug="punct", **kwargs):
		super().__init__(r'([^\w0-9\'/-]+|[\'_/-]+)', slug=slug, **kwargs)


class RegexRemoval(RegexFilter):

	def __init__(self, regex, slug="regexrem", **kwargs):
		super().__init__(regex, slug=slug, **kwargs)

	def _process(self, unit):
		before = unit if type(unit) == str else unit["val"]
		after = self.regex.sub('', before)
		if self._tag:
			unit["f_"+self.slug+"_before"] = before
			unit["f_"+self.slug+"_after"] = after
			unit["val"] = after
			# let unit through as long as something's left
			return None if after == "" else unit
		else:
			return None if after == "" else after


class EmojiRemoval(RegexRemoval):

	def __init__(self, slug="emojirem", **kwargs):
		rx = emoji.get_emoji_regexp()
		super().__init__(rx, compiled=True, slug=slug, **kwargs)


class NumberRemoval(RegexRemoval):

	def __init__(self, slug="numberrem", **kwargs):
		super().__init__(r'[0-9.,]+', slug=slug, **kwargs)


class HashtagRemoval(RegexRemoval):

	def __init__(self, slug="hashtag", **kwargs):
		super().__init__(r'#\S+', slug=slug, **kwargs)


class MentionRemoval(RegexRemoval):

	def __init__(self, slug="mention", **kwargs):
		super().__init__(r'@\S+', slug=slug, **kwargs)

class UrlRemoval(RegexRemoval):

	def __init__(self, slug="urlrem", **kwargs):
		super().__init__(r'https?://\S+', slug=slug, **kwargs)


class PunctRemoval(BasicTube):

	def __init__(self, slug="punctrem", **kwargs):
		super().__init__(slug=slug, **kwargs)
		self._f1 = RegexRemoval(r'[^\w0-9\'/-]+', slug=slug+"f1", **kwargs)
		self._f2 = RegexRemoval(r'^[\'/-]+', slug=slug+"f2", **kwargs)
		self._f3 = RegexRemoval(r'[\'/-]+$', slug=slug+"f3", **kwargs)


	def _process(self, unit):
		try:
			# wrap unit in list to convert to generator so it can be piped
			return next(self._f3.pipe(
						self._f2.pipe(
						self._f1.pipe(
							[unit]
						))))
		except StopIteration:
			return None


class DictFilter(BasicTube):

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

	def _process(self, unit):
		v = unit if type(unit) == str else unit["val"]
		if self._ignore_case:
			v = v.lower()
		return None if v in self._exclusion else unit
