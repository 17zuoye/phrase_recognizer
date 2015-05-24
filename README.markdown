Phrase Recognizer
======================
[![Build Status](https://img.shields.io/travis/17zuoye/phrase_recognizer/master.svg?style=flat)](https://travis-ci.org/17zuoye/phrase_recognizer)
[![Coverage Status](https://coveralls.io/repos/17zuoye/phrase_recognizer/badge.svg)](https://coveralls.io/r/17zuoye/phrase_recognizer)
[![Health](https://landscape.io/github/17zuoye/phrase_recognizer/master/landscape.svg?style=flat)](https://landscape.io/github/17zuoye/phrase_recognizer/master)
[![Download](https://img.shields.io/pypi/dm/phrase_recognizer.svg?style=flat)](https://pypi.python.org/pypi/phrase_recognizer)
[![License](https://img.shields.io/pypi/l/phrase_recognizer.svg?style=flat)](https://pypi.python.org/pypi/phrase_recognizer)



Example
------------------------
```python
>>> from phrase_recognizer import PhrasalRecognizer
>>> recognizer = PhrasalRecognizer([ u"a lot of", u"tie...to...", u"or...or...a...a"])
>>> recognizer
[first_strs_dict] {u'a': True, u'tie': True, u'or': True}


[tree] {u'a': {u'lot': {u'of': {u'a lot of': True}}}, u'tie': {u'...': {u'to': {u'...': {u'tie...to...': True}}}}, u'or': {u'...': {u'or': {u'...': {u'a': {u'...': {u'a': {u'or...or...a...a': True}}}}}}}}
>>> recognizer.process(u"There are a lot of signs the grass.", replace=True)
[u'There are signs the grass.', [u'a lot of']]
>>> recognizer.process(u"To fasten or secure with or as if with a cord, rope, or strap: tied the kite to a post; tie up a bundle.")
[u'To fasten or secure with or as if with a cord, rope, or strap: tied the kite to a post; tie up a bundle.', [u'or...or...a...a', u'tie...to...']]
```


License
------------------------
MIT. David Chen @ 17zuoye.
