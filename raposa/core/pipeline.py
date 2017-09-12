import json

from nltk import word_tokenize, sent_tokenize


class Word:

    def __init__(self, ix, s, previous=None, next_=None):
        self.ix = ix
        self.as_is = s # unmutable copy of token as it's in text
        self.tags = {}
        # 'val' is a universal tag updatable by filters
        # it is the one that should be checked by filters by default
        # some filters may transform it (e.g. orthography changes)
        self.tags["val"] = self.as_is
        self.previous = previous
        self.next = next_


    def __str__(self):
        return self["val"]


    def __getitem__(self, name):
        return self.tags[name] if name in self.tags else None


    def __setitem__(self, name, value):
        self.tags[name] = value


    def __repr__(self):
        return "<%s [%s: %s] %s >> %s>" % (
            self.previous,
            self.ix,
            self.as_is,
            self.next,
            self.tags
        )


    def __eq__(self, other):
        if self.as_is != other.as_is \
          or self.ix != other.ix:
            return False
        for my_tag, my_tag in self.tags.items():
            if my_tag not in other.tags \
              and my_val != other.tags[my_tag]:
                return False
        return True


    def __ne__(self, other):
        return not self == other


    def __hash__(self):
        # arbitrary hash definition
        return str(self.ix) \
          + self.as_is \
          + "&".join(self.tags.keys()) \
          + "%".join(self.tags.values())


    def __lt__(self, other):
        return str(self) < str(other)


    def __le__(self, other):
        return str(self) <= str(other)


class Sentence:

    def __init__(self, ix, s, previous=None, next_=None):
        self.ix = ix
        # sentences are not touched by filters
        # but we save it as '_as_is' for sistematicity
        self.as_is = s.strip()
        self.previous = previous.strip() if previous is not None else None
        self.next = next_.strip() if next_ is not None else None


    def __str__(self):
        return self.as_is


    def __repr__(self):
        return "<%s [%s: %s] %s>" % (
            self.previous,
            self.ix,
            self.as_is,
            self.next
        )


    def __eq__(self, other):
        return self.as_is == other.as_is \
           and self.ix == other.ix \
           and self.previous == other.previous \
           and self.next == other.next


    def __ne__(self, other):
        return not self == other


    def __hash__(self):
        # arbitrary hash definition
        return "%s&%s&%s&%s" % (self.ix, self.as_is, self.previous, self.next)


    def __lt__(self, other):
        return str(self) < str(other)


    def __le__(self, other):
        return str(self) <= str(other)


class Result:

    def __init__(self, word, sentence):
        self.word = word
        self.previous_word = word.previous
        self.next_word = word.next
        self.sentence = sentence
        self.previous_sentence = sentence.previous
        self.next_sentence = sentence.next


    def __repr__(self):
        return "<%s [%s: %s] %s>\n<%s [%s: %s] %s>" % (
            self.previous_word,
            self.word.ix,
            self.word.as_is,
            self.next_word,
            self.previous_sentence,
            self.sentence.ix,
            self.sentence,
            self.next_sentence
        )


class SimplePipeline():

    def __init__(self, filters):
        self.filters = filters


    def evaluate(self, word):
        for f in self.filters:
            discarded = f.evaluate(word)
            if discarded:
                break
        return discarded


    @classmethod
    def into_sentences(cls, txt):
        return txt.splitlines()


    @classmethod
    def into_words(cls, sentence):
        return [{"val": w} for w in sentence.split()]


    def pipe(self, text):
        results = []
        for sentence in self.into_sentences(text):
            for word in self.into_words(sentence):
                discarded = self.evaluate(word)
                if not discarded:
                    r = self._pack(word, sentence)
                    results.append(r)
        return results

    @classmethod
    def _pack(cls, word, sentence):
        return (word["val"], sentence)


class AdvancedPipeline(SimplePipeline):

    def __init__(self, filters, **kwargs):
        super().__init__(filters, **kwargs)


    @classmethod
    def into_sentences(cls, txt):
        tokens = sent_tokenize(txt)
        for i, (p, c, n) in enumerate(cls._take_in_threes(tokens)):
            yield Sentence(i, c, previous=p, next_=n)


    @classmethod
    def into_words(cls, sentence):
        tokens = word_tokenize(sentence.as_is)
        for i, (p, c, n) in enumerate(cls._take_in_threes(tokens)):
            yield Word(i, c, previous=p, next_=n)


    @classmethod
    def _pack(cls, word, sentence):
        return Result(word, sentence)


    @staticmethod
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


class JSONDumper():

    def __init__(self):
        pass


    @staticmethod
    def dump(results, path):
        js = [
            {
                "word": dict(
                    index = result.word.ix,
                    as_is = result.word.as_is,
                    previous = result.word.previous,
                    next = result.word.next,
                    **result.word.tags.copy()),
                "sentence": {
                    "index": result.sentence.ix,
                    "as_is": result.sentence.as_is,
                    "previous": result.sentence.previous,
                    "next": result.sentence.next
                }
            } for result in results
        ]
        with open(path, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(js, indent=4, ensure_ascii=False, default=str))
