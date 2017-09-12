#! /usr/bin/env python3

from raposa.core.pipeline import AdvancedPipeline, JSONDumper
from raposa.filters.basic import ComboFilter
from raposa.langs.gl.stemming import GLSimpleStemmer
from raposa.langs.gl.filters import GLXiadaFilter, GLEstravizFilter, GLStemmerFilter, GLToponymFilter
from raposa.langs.es.filters import ESFirstNamesFilter


## this is the main pipeline use

# first instantiate the desired filters

xiada = GLXiadaFilter() # check if they're in XIADA
names = ESFirstNamesFilter() # check if they're a name
toponyms = GLToponymFilter() # check if they're a village
stemmer = GLStemmerFilter() # try to split into morpheme

# define pipeline through which to pass each word
pipe = AdvancedPipeline([
	xiada,
	names,
	toponyms,
	stemmer,
])

text = """
Os parruleiros fuxiron a Coirós a cas Antonia

"""

# now pipe and get results
results = pipe.pipe(text)

for res in results:
	# print the word as in the source text
	# print the product of the stemmer
	print(
		res.word.as_is,
		res.word["t_gl_stemmer_val"]
	)


# alternatively, dump it to a json file
j = JSONDumper()
j.dump(results, "test.json")

print("###")


# filters can also be called directly

estraviz = GLEstravizFilter()

s = "queque"
x = xiada.matches(s)
e = estraviz.matches(s)
print(s, x, e)

# even combined

combo = ComboFilter([xiada, estraviz])
c = combo.matches(s)
print(s, c)


print("##")


# same as the stemmer

glss = GLSimpleStemmer()
s = "cantásemos"
x = glss.stem(s)
print(s, x)
