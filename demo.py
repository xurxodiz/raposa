#!/usr/bin/env python3

#
# This file is very similar to the one used every year
# for the #NeoloxismoDoAno neology selection process
# As such, it's a perfect example of use for the library
# We hope it helps understand how it's used
#

from raposa.core.pipeline import BasicPipeline
from raposa.core.tokenizers import RegexTokenizer
from raposa.core.tubes import LowercaseAdaptor, UrlRemoval, MentionRemoval, HashtagRemoval, EmojiRemoval, RegexRemoval, PunctRemoval, NumberRemoval 
from raposa.langs.gl.tubes import GLXiadaFilter, GLEstravizFilter, GLToponymFilter, GLWikipediaFilter
from raposa.langs.es.tubes import ESFirstNamesFilter, ESLastNamesFilter


pipe = BasicPipeline([
	# preprocessing
	BasicPipeline([
		LowercaseAdaptor(),
		UrlRemoval(),
		MentionRemoval(),
		HashtagRemoval(),
		EmojiRemoval()
	]),
	# word massaging & filtering
	BasicPipeline(
		tokenizer=RegexTokenizer(r'[.,;:_\s\'\"]+'),
		tubes=[
			RegexRemoval(r'[ºª]+'),
			NumberRemoval(),
			PunctRemoval(),
			GLXiadaFilter(),
			GLEstravizFilter(),
			GLToponymFilter(),
			GLWikipediaFilter(),
			ESFirstNamesFilter(),
			ESLastNamesFilter()
		]
	)
], reads_from_gen=False)

with open("input.txt") as in_file, \
	 open("output.txt", mode='w') as out_file:
	for line in in_file:
		for word in pipe.pipe(line):
			out_file.write(word + "\n")
