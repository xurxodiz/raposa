import json

class Unit:

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


class Context:

    def __init__(self, ix, s, previous=None, next_=None):
        self.ix = ix
        # contexts are not touched by filters
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

    def __init__(self, unit, context):
        self.unit = unit
        self.context = context

    def __repr__(self):
        return "<%s [%s: %s] %s>\n<%s [%s: %s] %s>" % (
            self.unit.previous,
            self.unit.ix,
            self.unit.as_is,
            self.unit.next,
            self.context.previous,
            self.context.ix,
            self.context,
            self.context.next
        )

    @staticmethod
    def dump(results, path):
        js = [
            {
                "unit": dict(
                    index = result.unit.ix,
                    as_is = result.unit.as_is,
                    previous = result.unit.previous,
                    next = result.unit.next,
                    **result.unit.tags.copy()),
                "context": {
                    "index": result.context.ix,
                    "as_is": result.context.as_is,
                    "previous": result.context.previous,
                    "next": result.context.next
                }
            } for result in results
        ]
        with open(path, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(js, indent=4, ensure_ascii=False, default=str))
