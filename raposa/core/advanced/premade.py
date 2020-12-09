from ..tokenizers import WhitespaceTokenizer, NewlineTokenizer, NltkWordTokenizer, NltkSentTokenizer
from .elements import Context, Unit, Result

#
# OUTDATED
#
# Theis class does not work after the last refactor
# Its usefulness probably remains, but it needs a refactor
# 


class AdvancedPipeline(BasicPipeline):

    def __init__(self, filters, unit_tokenizer=NltkWordTokenizer(), ctxt_tokenizer=NltkSentTokenizer(), **kwargs):
        super().__init__(filters, unit_tokenizer=unit_tokenizer, ctxt_tokenizer=ctxt_tokenizer, **kwargs)

    def _into_contexts(self, text):
        tokens = self.ctxt_tokenizer.split(text)
        for i, (p, c, n) in enumerate(cls._take_in_threes(tokens)):
            yield Context(i, c, previous=p, next_=n)

    def _into_units(self, context):
        tokens = self.unit_tokenizer.split(context.as_is)
        for i, (p, c, n) in enumerate(cls._take_in_threes(tokens)):
            yield Unit(i, c, previous=p, next_=n)

    def _pack(cls, word, context):
        return Result(word, context)

    @classmethod
    def _take_in_threes(lst):
        if len(lst) == 0:
            return

        previous = None
        curr = lst[0]
        next_ = None

        if len(lst) == 1:
            yield previous, curr, next_

        else:
            for currtoken in lst[1:]:
                # we yield for the token before the current
                next_ = currtoken
                yield previous, curr, next_
                previous = curr
                curr = next_

            # last yield, with last element of list as current
            next_ = None
            yield previous, curr, next_
