import os

from ...core.tubes import BasicTube, DictFilter
from .stemmer import GLSimpleStemmer


PATH_TO_ESTRAVIZ = "data/estraviz_09_2017.dat"
PATH_TO_XIADA = "data/xiada_2.6.dat"
PATH_TO_CORGA = "data/corga_1.7.dat"
PATH_TO_TOPONYMS = "data/toponimia_2013.dat"
PATH_TO_WIKIPEDIA = "data/wikipedia_08_2017.dat"


def _pth(datfile):
	local_dir = os.path.dirname(os.path.realpath(__file__))
	return os.path.join(local_dir, datfile)


# filters below bubble up the kwargs
# for things like e.g. discard

class GLEstravizFilter(DictFilter):

	def __init__(self, slug="gl_estraviz", **kwargs):
		super().__init__(file=_pth(PATH_TO_ESTRAVIZ), slug=slug, **kwargs)


class GLXiadaFilter(DictFilter):

	def __init__(self, slug="gl_xiada", **kwargs):
		super().__init__(file=_pth(PATH_TO_XIADA), slug=slug, **kwargs)


class GLCorgaFilter(DictFilter):

	def __init__(self, slug="gl_corga", **kwargs):
		super().__init__(file=_pth(PATH_TO_CORGA), slug=slug, **kwargs)


class GLToponymFilter(DictFilter):

	def __init__(self, slug="gl_toponym", **kwargs):
		super().__init__(file=_pth(PATH_TO_TOPONYMS), slug=slug, **kwargs)


class GLWikipediaFilter(DictFilter):

	def __init__(self, slug="gl_wikipedia", **kwargs):
		super().__init__(file=_pth(PATH_TO_WIKIPEDIA), slug=slug, **kwargs)


class GLStemmerFilter(BasicTube):

	def __init__(self, slug="gl_stemmer", discard=False, replace=False, **kwargs):
		self._stemmer = GLSimpleStemmer()
		self._replace = replace
		super().__init__(slug=slug, discard=discard, **kwargs)


	def _process(self, unit):
		v = unit if type(unit) == str else unit["val"]
		chain = self._stemmer.stem(v)
		if self._tag:
			unit["t_"+self.slug+"_val"] = chain
		if self._replace:
			if type(unit) == str:
				return chain[0]
			else:
				unit["val"] = chain[0]
				return unit
		else:
			return unit
