# -*- coding: utf-8 -*-

# TODO
"""
1. 处理be为[am,is,are,were,was,be,been,being]
2. PE=physical education
3. ping-pong table
4. "put on"和"put on (your coat)"统一为后者
[5]. that's=that is
6. wash (one's) face这样为 中间可以替换的
7. 忽略结尾的["!", "."]
8. My/his…nose/arms...hurt(s)
9. It's...(o'clock). 其中...在这里一定是数字时间, 比如It's nine (o'clock).
10. 抽取 What's...plus...? 中的 ...
11. 也许 two-week-old 替换-为空格
12. 提示 I/you/he/he/she...had a dream/some fun… 前面一个在/后出现的...只是代表she后面还有同等的名词


# 规则修改建议
1. [平级的短语] 自己括号起来，并用 / 分割。比如 had (a dream)/(some fun)
2. [...] 只表示 这部分是省略的，可填补为除了符号的任何一个或多个单词。不能表示[平级的短语]里省略的。

兼容 What would you like to be (in the future/in two years later…)? 双括号

# TODO May I speak to…,(please)? 可能性
# 优化 I/He/She... go(goes) to Beijing/Shanghai...by bus/train… 和 What sport(s)...?
# `cat etl/common/files/primary_school_english_knowledge_dict/en_new_sentence.txt`.split("\n").map {|line| line.count("(") }.uniq => [0, 1] 只有一个()的

# OPTIMIZE 目前只是为了考虑 像 I/He/She... go(goes) to Beijing/Shanghai...by bus/train…的空格
# if len(sb_list) and n_sb.is_other and (not n_sb.string in ["'"]): break

# 优化 ... [key1_next] weeks 比如全文没有weeks就不为 这种 ... 开始的而查找了
"""

from split_block import SplitBlockGroup

from .phrase_rules_split import phrase_rules_split, z, ld

dots = "..."


class Phrase(unicode):
    def __init__(self, s1=u''):
        super(Phrase, self).__init__(s1)

    """
    # comment below to let tests passed.
    def __repr__(self):
        # Don't show phrase in the PhrasalRecognizer#tree,
        # to focus on the structure of the phrase tree.
        return "<Phrase>"

    def __eq__(self, s1):
        return unicode(self) == s1
    """


class PhrasalRecognizer():
    """
    目前处理情况
    1. u'how many'
    2. u"don't", u'P.E.'
    2. u'How old ... ?', u'learn ... from ...'

    目前不处理情况
    1. u'pass sth to sb'

    NOTICE
    1. input and output are all unicode.
    2. 词组之间相互包含的情况，比如假设存在 have one 和 have one of 两个词组，直接用长的替换小的。如果相等，就以前面一个为准。
    3. 全部转化为小写来比较

    Features
    1. Find all phrasal collocation, and extract them. Maybe some have intersection with others.
    2. Case-insensitive.

    Performance compare, 1,307 phrasal collocation, 129,509 sentences。
    1. [combine 1,307 Regexpes into a Regexp]      processed in 1 minutes 1 seconds.
    2. [PhrasalRecognizer]                         processed in 1 minutes 40 seconds.
    3. [1,307 Regexpes]                            processed in 2.5 hours.
    """

    @classmethod
    def split(cls, sentence):
        return phrase_rules_split(sentence)

    def __init__(self, phrasal_collocation_s):
        # generate self.first_strs_dict and self.tree these two data structure
        phrase_to_strs_list = dict()
        for phrasal_collocation1 in phrasal_collocation_s:
            assert isinstance(phrasal_collocation1, unicode)
            phrasal_collocation2 = Phrase(phrasal_collocation1)
            for pc2 in PhrasalRecognizer.split(phrasal_collocation1):
                split_block_group = SplitBlockGroup.extract(str(pc2).lower())
                # strip both words and spaces
                strs_list = [sb1.utf8low() for sb1 in split_block_group if sb1.pos_begin is not None]  # skip fake sb1
                if phrasal_collocation2 not in phrase_to_strs_list:
                    phrase_to_strs_list[phrasal_collocation2] = []
                phrase_to_strs_list[phrasal_collocation2].append(strs_list)

        self.first_strs_dict = {i2[0]: True for i1 in phrase_to_strs_list.values() for i2 in i1}

        self.tree = dict()
        for phrase1 in phrase_to_strs_list:
            for strs1 in phrase_to_strs_list[phrase1]:
                current_dict = self.tree
                for idx2, s2 in enumerate(strs1):
                    if not s2:
                        continue  # ignore spaces, and will ignore at search by the way.
                    # always a dict
                    if s2 not in current_dict:
                        current_dict[s2] = dict()
                    current_dict = current_dict[s2]
                    # mark a ender
                    if idx2 == (len(strs1) - 1):
                        current_dict[phrase1] = True

        self.inspect = False

    def process(self, sentence, inspect=False, replace=False):
        self.sentence = sentence  # TODO remove me

        inspect = self.inspect or inspect
        if self.inspect:
            print "#|" * 80
            print "processing \"%s\"" % self.sentence

        split_block_group = SplitBlockGroup.extract(self.sentence)
        candidate_split_block_s = []

        # generate candidate_split_block_s
        for letter1 in split_block_group.letters():
            # First string must be chars
            if ld.lemmatize(letter1.utf8low()) in self.first_strs_dict:
                candidate_split_block_s.append(letter1)

        if dots in self.tree:
            candidate_split_block_s.append(dots)  # TODO

        # generate letter1_sb_list
        matched_strs__to__phrase = dict()
        for letter1 in candidate_split_block_s:  # iterate each matched letter1
            sb1_list_current = SplitBlockGroup([letter1])  # actually we append it before the current loop here.

            if letter1 == dots:
                key1_current = dots
                sb1_current = split_block_group[0]
            else:
                key1_current = ld.lemmatize(letter1.utf8low())
                sb1_current = letter1

            key1_dict_current = self.tree[key1_current]

            for key1_next in key1_dict_current:
                self.recursive_match(matched_strs__to__phrase, sb1_current, sb1_list_current, key1_dict_current, key1_current, key1_next)

        letter1_sb_list = sorted(matched_strs__to__phrase.values(), key=lambda i1: -len(i1))
        if inspect:
            print
            print "[letter1_sb_list]", letter1_sb_list

        if replace:
            self.sentence = self.generate_replaced_sentence(letter1_sb_list, split_block_group)

        return [self.sentence, matched_strs__to__phrase.keys()]

    def recursive_match(self, matched_strs__to__phrase, sb1_current, sb1_list_current, key1_dict_current, key1_current, key1_next=None):
        if self.inspect:
            print "#" * 30, "[key1_current]", key1_current, "[key1_next]", key1_next
        key1_dict_next = None if key1_next is None else key1_dict_current[key1_next]
        phrase_current = ([p1 for p1 in key1_dict_current if isinstance(p1, Phrase)] or [None])[0]  # every level has only one phrase.

        def params_with(k1):
            """ encapsulate parameters in the current scope. """
            return [key1_dict_next, key1_next, "placeholder", matched_strs__to__phrase] + \
                   [k1] + \
                   [SplitBlockGroup(sb1_list_current), key1_dict_current, key1_current]

        if key1_next == dots:
            self.recursive_match_sub(*params_with(sb1_current))

        while sb1_current.n_sb:
            sb1_current     = sb1_current.n_sb  # direct to next, cause current is appended to `sb1_list_current`
            # sb1_current_str = sb1_current.utf8low()
            sb1_list_current.append(sb1_current)
            if self.inspect:
                print "[sb1_current]", "\"%s\"" % sb1_current
            if self.inspect:
                print "len [sb1_list_current]", len(sb1_list_current)

            if phrase_current:
                is_ender = ((sb1_current.is_other and (sb1_current.utf8low() not in ["'"])) or (sb1_current.n_sb is None))
                if ((key1_current == dots) and is_ender) or \
                   (key1_current != dots):
                        matched_strs__to__phrase[phrase_current] = SplitBlockGroup(sb1_list_current)  # make a copy
                        if self.inspect:
                            print
                            print "[end candidate_split_block_s loop : sb1_list_current]", sb1_list_current
                            print
                        if key1_next is None:
                            break

            if key1_current == dots:
                if not z(sb1_current.n_sb):
                    break
                if key1_next:
                    if key1_next == ld.lemmatize(sb1_current.n_sb.utf8low()):
                        self.recursive_match_sub(*params_with(sb1_current))
                        break
                    else:
                        continue
            else:
                if key1_next:
                    if key1_next == ld.lemmatize(sb1_current.utf8low()):
                        self.recursive_match_sub(*params_with(sb1_current))
                    continue
                else:
                    break

    def recursive_match_sub(self, key1_dict_next, key1_next, _, matched_strs__to__phrase, sb1_current, sb1_list_current, key1_dict_current, key1_current):
        if self.inspect:
            print "." * 50, "recursive_match_sub"
        key1_dict_next_keys = [i1 for i1 in key1_dict_current[key1_next] if not isinstance(i1, Phrase)]
        key1_dict_next_keys = key1_dict_next_keys or [None]
        for key1_next_next in key1_dict_next_keys:
            self.recursive_match(matched_strs__to__phrase, sb1_current, sb1_list_current, key1_dict_current[key1_next], key1_next, key1_next_next)

    def generate_replaced_sentence(self, letter1_sb_list, split_block_group):
        for sb_list in letter1_sb_list:
            sb_first = sb_list[0]
            idx_first = split_block_group.index(sb_first)

            if idx_first is None:
                # it means that other sb_list had already processed it.
                continue

            idx_last  = idx_first + len(sb_list)
            is_break = False
            for idx1 in range(idx_first, idx_last):
                if split_block_group[idx1] is None:
                    is_break = True
                    break
                split_block_group[idx1] = None
            if is_break:
                continue

            # remove duplicated blank
            if (idx_first > 0) and (idx_last < len(split_block_group)):
                # it means that letter1_sb_list has common parts.
                if (split_block_group[idx_first - 1] is None) or (split_block_group[idx_last] is None):
                    continue
                else:
                    if split_block_group[idx_first - 1].is_blank and split_block_group[idx_last].is_blank:
                        split_block_group[idx_first - 1] = None
        return split_block_group.concat_items().strip().decode("UTF-8")

    def __repr__(self):
        return str("\n".join(["[first_strs_dict] %s" % self.first_strs_dict,
                              "\n",
                              "[tree] %s" % self.tree]))
