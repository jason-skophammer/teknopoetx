import txt_admin as admin
import txt_formt as formt
import re
import json
import abc
from nltk import pos_tag
from teknopoetx import Settings
from teknopoetx import Anlyz

sett = Settings()
anlz = Anlyz()


class File:

    __metaclass__ = abc.ABCMeta

    def __init__(self, f_id='', addl=None):
        self.f_id = f_id + '.json'
        self.addl = addl
        self.fnct = (lambda x: x == x)
        self.updt = sett.main_file
        self.fltr = self.updt.keys()
        self.m_ex = sett.file_pth + 'j_son/' + self.f_id
        self.f_ex = sett.file_pth + 'j_son/' + self.f_id

    def generate(self, data):
        gen = self.process(data)
        self.save_data(gen, self.f_ex)
        return gen

    def update(self):
        main_file = self.updt
        new = [w for w in self.addl if w not in self.fltr]
        self.enter(main_file, new)
        self.save_data(main_file, self.m_ex)
        print('update complete')

    def process(self, data):
        words = list(set(formt.remove_punct(data)))
        new_dict = {}
        self.enter(new_dict, words)
        return new_dict

    def enter(self, main_file, data):
        for x in data:
            if x in self.fltr:
                main_file[x] = self.updt[x]
            else:
                main_file[x] = self.fnct(x)

    @staticmethod
    def save_data(data, ext):
        json.dump(data, open(ext, 'w'))


class Vocab(File):

    def __init__(self, f_id='', addl=None):
        super(Vocab, self).__init__(f_id='', addl=None)
        self.addl = addl
        self.updt = sett.vocb_file
        self.fltr = sett.vocb_file
        self.f_id = f_id + '_vocb.json'
        self.m_ex = sett.file_pth + 'j_son/' + self.f_id
        self.f_ex = sett.file_pth + 'j_son/vocab/' + self.f_id

    def process(self, file):
        words = admin.word_list(file)
        voc = list(set(formt.remove_punct(words)))
        vocab = list(set([w for w in voc if w.isalpha()]))
        vocab += formt.lower_case(vocab)
        vocab = list(set(vocab))
        for x in [w for w in vocab if re.findall(r'^[ivxlcIVXLC]+$', w)
        and w not in ['I', 'i', 'Ill', 'ill', 'civil', 'Civil']]:
            vocab.remove(x)
        return vocab

    def enter(self, main_file, word_list):
        for word in word_list:
            main_file.append(word)
        return main_file


class MainGram(File):

    def __init__(self, f_id='', addl=None):
        super(MainGram, self).__init__(f_id='', addl=None)
        self.addl = addl
        self.f_id = f_id + '_mg.json'
        self.updt = sett.mgrm_file
        self.m_ex = sett.file_pth + 'j_son/' + self.f_id
        self.f_ex = sett.file_pth + 'j_son/main_grm/' + self.f_id

    def enter(self, main_file, word_list):
        for word in word_list:
            if word in sett.brwn_dict.keys():
                pos = sett.brwn_dict[word]
            else: pos = pos_tag([word])[0][1]
            main_file[word] = pos
        return main_file


class RevGram(File):

    def __init__(self, f_id='', addl=None):
        super(RevGram, self).__init__(f_id='', addl=None)
        self.addl = addl
        self.f_id = f_id + '_rg.json'
        self.updt = sett.rgrm_file
        self.fltr = sett.mgrm_file.keys()
        self.m_ex = sett.file_pth + 'j_son/' + self.f_id
        self.f_ex = sett.file_pth + 'j_son/rev_gram/' + self.f_id

    def process(self, word_list):
        words = list(set(formt.remove_punct(word_list)))
        old_words = [w for w in words if w in sett.main_gram.keys()]
        new_words = [w for w in words if w not in old_words]
        rev_gram = {}
        for pos in sett.main_gram.values():
            rev_gram.setdefault(pos, [])
        pairs = pos_tag(new_words)
        gram_list = list(set([y for x, y in pairs]))
        for pos in gram_list:
            rev_gram[pos] = list(set([pairs[i][0] for i in range(len(new_words)) if pairs[i][1] == pos]))
        for word in old_words:
            rev_gram[sett.main_gram[word]].append(word)
        return rev_gram

    def enter(self, main_file, word_list):
        for word in word_list:
            if word in sett.brwn_dict.keys():
                pos = sett.brwn_dict[word]
            else: pos = pos_tag([word])[0][1]
            if pos in main_file.keys():
                main_file[pos].append(word)
            else: main_file[pos] = [word]
        return main_file


class StrsDict(File):

    def __init__(self, f_id='', addl=None):
        super(StrsDict, self).__init__(f_id='', addl=None)
        self.addl = addl
        self.f_id = f_id + '_strs.json'
        self.updt = sett.strs_file
        self.m_ex = sett.file_pth + 'j_son/' + self.f_id
        self.f_ex = sett.file_pth + 'j_son/strs_dct/' + self.f_id

    def enter(self, main_file, word_list):
        for word in word_list:
            main_file[word] = anlz.strs_pattrn(word)
        admin.fix_strs_dict(word_list, main_file)
        return main_file


class PronDict(File):

    def __init__(self, f_id='', addl=None):
        super(PronDict, self).__init__(f_id='', addl=None)
        self.addl = addl
        self.f_id = f_id + '_prndct.json'
        self.updt = sett.pron_file
        self.fltr = self.updt.keys()
        self.fnct = (lambda x: anlz.gen_pron([x]))
        self.m_ex = sett.file_pth + 'j_son/pron_dict.json'
        self.f_ex = sett.file_pth + 'j_son/pron_dct/' + self.f_id


class SylDict(File):

    def __init__(self, f_id='', addl=None):
        super(SylDict, self).__init__(f_id='', addl=None)
        self.addl = addl
        self.f_id = f_id + '_sylc.json'
        self.updt = sett.sylc_file
        self.fnct = (lambda x: anlz.count_syl(x))
        self.m_ex = sett.file_pth + 'j_son/' + self.f_id
        self.f_ex = sett.file_pth + 'j_son/syl_cnt/' + self.f_id


class RhymDict(File):

    def __init__(self, f_id='', addl=None):
        super(RhymDict, self).__init__(f_id='', addl=None)
        self.addl = addl
        self.f_id = f_id + '_rhym.json'
        self.updt = sett.rhym_file
        self.fnct = (lambda x: anlz.last_syl(x))
        self.m_ex = sett.file_pth + 'j_son/' + self.f_id
        self.f_ex = sett.file_pth + 'j_son/rhym/' + self.f_id


if __name__ == '__main__':
    #print('idly' in sett.pron_dict.keys())
    #print(sett.pron_dict['idly'])

    nov_voc = json.load(open('j_son/vocab/nov_vocb.json'))
    PronDict('pron_dict', nov_voc[:100]).update()
