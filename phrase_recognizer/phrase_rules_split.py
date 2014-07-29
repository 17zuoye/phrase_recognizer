# -*- coding: utf-8 -*-

from split_block import SplitBlockGroup

z = SplitBlockGroup.z # make a short alias

from etl_utils import Unicode, ld
import re

def phrase_rules_split(sentence):
    """
    Split complex phrase rules, include equal symbol and slash symbol.

    e.g. u"My name's...=My name is..."
    """
    assert isinstance(sentence, unicode)

    # 转换全角为半角
    sentence = Unicode.stringQ2B(sentence)

    # 替换 "..." 为 " ... "
    sentence = re.sub("\.\.\.", " ... ", sentence).strip()

    # 移除所有 "?|!"
    sentence = re.sub("\?|\!", "", sentence)

    # 排除中文字符
    sentence = u''.join([uchar for uchar in list(sentence) if not Unicode.is_chinese(uchar)])

    # 修复 / 前后的多余空格
    sentence = re.sub("\ *\/\ *", "/", sentence)

    # 再排除纯括号
    sentence = re.sub(u"()", "", sentence)

    # lemmatize
    sentence = lemmatize_sentence(sentence)

    # split all
    result = []
    [result.extend(sub_split(phrase1)) for phrase1 in sentence.split("=")]
    return result


def check_slash(first_sb, first_sb_idx, current_skiped_idxes):
    """ look forward slashes, and store them into current_skiped_idxes. """
    current_sb_idx = first_sb_idx
    while(first_sb):
        if z(first_sb.n_sb) and first_sb.n_sb.is_other and (first_sb.n_sb.string == '/') and z(first_sb.n_sb.n_sb) and first_sb.n_sb.n_sb.is_letter:
            current_skiped_idxes.extend([current_sb_idx+1,current_sb_idx+2])
            first_sb = first_sb.n_sb.n_sb
            current_sb_idx += 2
        else:
            first_sb = None

def sub_split(phrase1):
    """ split u"I/We/They… always/usually/often/sometimes…" into sub strs, e.g. "I... always...". """
    old_sbg = SplitBlockGroup.extract(phrase1)
    new_sbg_list=[SplitBlockGroup()]

    current_skiped_idxes = []
    for idx1, sb1 in enumerate(old_sbg):
        if idx1 in current_skiped_idxes: continue

        current_skiped_idxes = [idx1]

        check_slash(sb1, idx1, current_skiped_idxes)

        new_sbg_list_dup = []
        is_split = len(current_skiped_idxes) > 1
        for sbg1 in new_sbg_list:
            for skip_idx1 in current_skiped_idxes:
                current_sbg1 = SplitBlockGroup(sbg1) # make a dup
                sb2 = old_sbg[skip_idx1]
                if is_split and (not sb2.is_letter): continue
                current_sbg1.append(sb2)
                # strip blank into 1
                for sb1 in current_sbg1:
                    if z(sb1) and sb1.is_blank and (len(sb1) > 1): sb1.string = u' '
                new_sbg_list_dup.append(current_sbg1.concat_items())
        if len(new_sbg_list_dup): new_sbg_list = new_sbg_list_dup

    return new_sbg_list

def lemmatize_sentence(sentence):
    sbg = SplitBlockGroup.extract(sentence)
    for sb1 in sbg:
        if sb1.is_letter:
            sb1.string = ld.lemmatize(sb1.string)
    return sbg.concat_items()
