from collections.abc import Iterable

from .tokenizers import BasicTokenizer

class BasicPipeline():

    def __init__(self, tubes=[], tokenizer=BasicTokenizer(), reads_from_gen=True):
        self.tubes = tubes
        self.tokenizer = tokenizer
        self._reads_from_gen = reads_from_gen

    def pipe(self, g):
        gen_text = g if self._reads_from_gen else [g]
        for text in gen_text:
            for token in self._into_tokens(text):
                for t in self._process(token):
                    yield self._pack(t, None)

    def _process(self, token):
        tokens = (t for t in [token])
        for t in self.tubes:
            tokens = t.pipe(tokens)
        yield from tokens

    def _into_tokens(self, text):
        return self.tokenizer.split(text)

    def _pack(self, token, context):
        return token
