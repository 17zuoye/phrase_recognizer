# -*- coding: utf-8 -*-

import os, sys
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

import unittest

from phrase_recognizer import PhrasalRecognizer

class TestPhrasalRecognizer(unittest.TestCase):

    def test_split(self):
        result1 = PhrasalRecognizer.split(u"I/We/They… always/usually/often/sometimes…")
        self.assertEqual(result1[0], "I ... always ...")
        self.assertEqual(result1[7], "We ... sometimes ...")

        result2 = PhrasalRecognizer.split(u"My name's...=My name is...")
        self.assertEqual(result2[1], u"My name be ...")

        result3 = PhrasalRecognizer.split(u"Usually /Sometimes…I go…")
        self.assertEqual(result3[0], u"Usually ... I go ...")


    def test_basic_process(self):
        recognizer = PhrasalRecognizer([
                   u"ruby python",
                   u"have lunch",
                   u"a lot of",

                   u"Don't",
                   u"Don't have to",
                ])
        recognizer.inspect = True
        print recognizer; print

        data = {
            u"ruby python which one"                                               : [u"which one", [u"ruby python"]],
            u"It’s 12:00 now. Let’s have lunch together."                          : [u"It’s 12:00 now. Let’s together.", [u"have lunch"]],
            u"There are a lot of signs                 the grass."                 : [u"There are signs                 the grass.", [u"a lot of"]],
            u"Don't    "                                                           : [u"", [u"Don't"]],
            # dont replace twice
            u"Don't have to        Don't have to    "                              : [u"Don't have to", [u"Don't have to", u"Don't"]],
            #u"Don't talk in class, Don't read in bed, Don't spill the sugar on the table" : [u"Don't talk in class, Don't read in bed,", [u"Don't"]],
        }

        for content in reversed(sorted(data.keys())):
            result = recognizer.process(content, inspect=True, replace=True)
            print "[result]", result
            #if 'talk' in result[0]: import pdb; pdb.set_trace() # TODO some extract bugs?
            self.assertEqual(result, data[content])

    def test_three_dots_process(self):
        print "\n"*50
        phrases = [
           u"tie...to...",
           u"used to...",
           u"wash...face",
           u"...weeks old",
           u"I/He/She... was(not) going to…",
           u"or...or...a...a",
        ]

        recognizer = PhrasalRecognizer(phrases)
        recognizer.inspect = True
        print recognizer; print

        data = {
            u"To fasten or secure with or as if with a cord, rope, or strap: tied the kite to a post; tie up a bundle." : phrases[0:1] + phrases[5:6],
            u"I am used to hitchhiking" : phrases[1:2],
            u"There are specific things to keep in mind when washing your face" : phrases[2:3],
            u"The Best Foods for 6 Week Old Puppies | Dog Care - The Daily" : phrases[3:4],
            u"He was(not) going to say hello." : phrases[4:5],
            u"To fasten or secure with or as if with a cord a cake" : phrases[5:6],
        }

        for content in reversed(sorted(data.keys())):
            result = recognizer.process(content)
            print "[result]", result
            self.assertEqual(result[1], data[content])

if __name__ == '__main__': unittest.main()
