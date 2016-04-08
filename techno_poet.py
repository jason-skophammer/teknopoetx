from time import ctime

start = ctime()
print('Start:', start)

from txt_admin import *

import teknopoetx as tpx
sett = tpx.Settings()
anlz = tpx.Anlyz()


class PoemGen:
    def __init__(self):
        self.sylc     = sett.sylc
        self.strs     = sett.strs
        self.rhym     = sett.rhym
        self.alit     = sett.alit
        self.grm_fnct = anlz.gram_struc
        self.rev_gram = sett.mrev_gram
        self.pos_file = sett.frev_grm
        self.syl_file = sett.syl_count
        self.str_file = sett.strs_dict
        self.rhy_file = sett.rhym_dict

    @staticmethod
    def same_posw(pos):
        return [w.lower() for w in sett.frev_grm[pos] if w.isalpha()]

    @staticmethod
    def same_sylw(word, word_list):
        return [w for w in word_list if (sett.syl_count[w] == sett.syl_count[word]) and w != word]

    @staticmethod
    def same_strw(word, word_list):
        return [w for w in word_list if sett.strs_dict[word] == sett.strs_dict[w]]

    @staticmethod
    def same_alit(word, word_list):
        return [w for w in word_list if w[0] == word[0]]

    @staticmethod
    def same_rhyw(word, word_list):
        return [w for w in word_list if sett.rhym_dict[word] == sett.rhym_dict[w]]

    def gen_text(self):
        sent_lines = sentlines(sett.txt_name)
        count = 0
        while count < sett.iter_num:
            f_num = file_num()
            log_text = ''
            for line in sent_lines:
                mad_sen = self.poem_gen(line)
                log_text += (mad_sen + '\n')
            with open(sett.log_file + f_num, 'w') as f:
                f.write(log_text)
            count += 1
        end = ctime()
        print(anlz.time_elapse(start, end))
        pass

    def gram_struc(self, line):
        grm_sent = self.grm_fnct(line)
        return grm_sent

    def filter(self):
        pass

    def choose_word(self, line):
        mad_sent = []
        for i in range(len(line)):
            gen_word = line[i].lower()
            rand_word = gen_word
            if self.sylc and self.strs and self.rhym and self.alit:
                word_list = [w for w in self.same_posw(self.grm_fnct(line)[i])
                             if self.syl_file[w] == self.syl_file[gen_word]
                             and self.str_file[w] == self.str_file[gen_word]
                             and self.rhy_file[w] == self.rhy_file[gen_word]
                             and w[0] == gen_word[0]]
                rand_word = choice(word_list)
            mad_sent.append(rand_word)
        return mad_sent

    def poem_gen(self, line):
        self.gram_struc(line)
        self.filter()
        mad_sent = self.choose_word(line)
        return mad_sent




def poem_gen(line):
    grm_sent = anlz.gram_struc(line)
    stp_wrds = sett.stp_words
    madlib = []
    print(sent_form(line, sett.txt_frmt))
    for i in range(len(line)):
        gen_word = line[i].lower()
        old_word = line[i]
        if gen_word in stp_wrds or not gen_word.isalpha():
            madlib.append(old_word)
        elif grm_sent[i] in sett.frev_grm.keys():
            same_pos = same_posw(grm_sent[i])
            same_syl = same_sylw(gen_word, same_pos)
            same_str = same_strw(gen_word, same_syl)
            same_rhy = same_rhyw(gen_word, same_str)
            if (gen_word == line[-1].lower()
                    or ((not line[-1].isalpha())
                        and (gen_word == line[-2].lower()))) \
                    and same_pos and same_syl and same_str and same_rhy:
                rand_word = choice(same_rhy)
            elif same_pos and same_syl and same_str:
                rand_word = choice(same_str)
            elif same_pos and same_syl:
                rand_word = choice(same_syl)
            elif same_pos:
                rand_word = choice(same_pos)
            else:
                rand_word = old_word
            if old_word[0].isupper():
                rand_word = rand_word.capitalize()
            madlib.append(rand_word)
        else: madlib.append(old_word)
    mad_sent = sent_form(madlib, sett.txt_frmt)
    return mad_sent


def poem_gen_2(line):
    madlib = []
    print(sent_form(line, sett.txt_frmt))
    for i in range(len(line)):
        word = line[i]
        if word in sett.stp_words or not word.isalpha():
            madlib.append(word)
        else:
            gen_word = word.lower()
            gen_pos = sett.main_gram[gen_word]
            if gen_pos in sett.frev_grm.keys():
                g_type = [w for w in sett.frev_grm[gen_pos] if w.isalpha()]
                if g_type:
                    same_syl = [w for w in g_type if
                                (sett.srce_dct[gen_word]['numsyl']
                                 == sett.fill_dct[w]['numsyl'])]
                    if same_syl:
                        same_str = [w for w in same_syl if sett.fill_dct[w]['strs']
                                    == sett.srce_dct[gen_word]['strs']]
                        if same_str:
                            rand_word = choice(same_str)
                        else:
                            rand_word = choice(same_syl)
                    else:
                        rand_word = choice(g_type)
                    if word[0].isupper():
                        rand_word = rand_word.capitalize()
                    madlib.append(rand_word)
                else: madlib.append(word)
            else: madlib.append(word)
    mad_sent = sent_form(madlib, sett.txt_frmt)
    return mad_sent


def poem_gen_3():
    f_num = file_num()
    log_text = ''
    for x in range(len(sett.grm_strc.keys())):
        madlib = []
        gen_sent = sett.grm_strc[str(x)][0]
        grm_sent = sett.grm_strc[str(x)][1]
        print(sent_form(gen_sent, sett.txt_frmt))
        for i in range(len(gen_sent)):
            gen_word = gen_sent[i].lower()
            if gen_word in sett.stp_words or not gen_word.isalpha():
                madlib.append(gen_sent[i])
            elif grm_sent[i] in sett.frev_grm.keys():
                same_pos = same_posw(grm_sent[i])
                same_syl = same_sylw(gen_word, same_pos)
                same_str = same_strw(gen_word, same_syl)
                if same_pos and same_syl and same_str:
                    rand_word = choice(same_str)
                elif same_pos and same_syl:
                    rand_word = choice(same_syl)
                elif same_pos:
                    rand_word = choice(same_pos)
                else: rand_word = gen_sent[i]
                if gen_sent[i][0].isupper():
                    rand_word = rand_word.capitalize()
                madlib.append(rand_word)
            else: madlib.append(gen_sent[i])
        mad_sent = sent_form(madlib, sett.txt_frmt)
        log_text += (mad_sent + '\n')
    with open(sett.log_file + f_num, 'w') as f: f.write(log_text)
    end = ctime()
    print(anlz.time_elapse(start, end))
    return log_text



if __name__ == '__main__':

    gen_text(True)

