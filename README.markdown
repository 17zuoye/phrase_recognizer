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
>>> recognizer = PhrasalRecognizer([ u"a lot of", ])
>>> content = u"There are a lot of signs the grass."
>>> recognizer.process(content, replace=True)
[u'There are signs the grass.', [u'a lot of']]
```


License
------------------------
MIT. David Chen @ 17zuoye.
