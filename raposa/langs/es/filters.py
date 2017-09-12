import os

from ...filters.basic import DictFilter, ComboFilter


PATH_TO_DRAE = "data/drae_2011.dat"
PATH_TO_FIRST_NAMES = "data/nombres_2016.dat"
PATH_TO_LAST_NAMES = "data/apellidos_2016.dat"


def _pth(datfile):
	local_dir = os.path.dirname(os.path.realpath(__file__))
	return os.path.join(local_dir, datfile)


# filters below bubble up the kwargs
# for things like e.g. discard

class ESDraeFilter(DictFilter):

	def __init__(self, slug="drae", **kwargs):
		super().__init__(file=_pth(PATH_TO_DRAE), slug=slug, **kwargs)


class ESFirstNamesFilter(DictFilter):

	def __init__(self, slug="es_firstnames", **kwargs):
		super().__init__(file=_pth(PATH_TO_FIRST_NAMES), slug=slug, **kwargs)


class ESLastNamesFilter(DictFilter):

	def __init__(self, slug="es_lastnames", **kwargs):
		super().__init__(file=_pth(PATH_TO_LAST_NAMES), slug=slug, **kwargs)


class ESNamesFilter(ComboFilter):

	def __init__(self, slug="es_names", **kwargs):
		lst_filters = [
			ESFirstNamesFilter(),
			ESLastNamesFilter()
		]
		super().__init__(lst_filters, slug=slug, **kwargs)
