from random import choice
from nltk import *
import json
from pystring import S

class Settings:

    def __init__(self):
        # Set file paths for texts used in techno_poet.gen_text
        self.txt_name = 'process/procd/shks2_procd.txt'
        self.rvg_name = 'js3_rg'
        self.file_idn = 'js_shks'
        self.log_fldr = 'sonnets'
        self.txt_frmt = 'poem'              # Set format to 'poem' to capitalize beginning of lines
        self.iter_num = 1                   # Set number of output texts to generate
        self.sylc     = True
        self.strs     = True
        self.rhym     = True
        self.alit     = False

        # Set main file path
        self.file_pth = '/users/jason/teknopoetx/'
        self.tmp_file = self.file_pth + 'tmp/tmp_file.txt'
        self.srce_txt = self.file_pth + self.txt_name
        self.log_file = self.file_pth + 'logs/' + self.log_fldr + '/' + self.file_idn

        self.grm_strc = json.load(open(self.file_pth + 'j_son/gram_strc/pdl_grmstrc.json'))
        self.frev_grm = json.load(open(self.file_pth + 'j_son/rev_gram/' + self.rvg_name + '.json'))

        # Open main dictionaries used in programs
        self.main_vocb = json.load(open(self.file_pth + 'j_son/main_vocb.json'))
        self.cmu_vocab = json.load(open(self.file_pth + 'j_son/cmu_vocab.json'))
        self.brwn_vocb = json.load(open(self.file_pth + 'j_son/brwn_vocb.json'))
        self.stnd_vocb = json.load(open(self.file_pth + 'j_son/stnd_vocb.json'))
        self.pron_dict = json.load(open(self.file_pth + 'j_son/pron_dict.json'))
        self.freq_pron = json.load(open(self.file_pth + 'j_son/freq_pron.json'))
        self.rhym_dict = json.load(open(self.file_pth + 'j_son/rhym_dict.json'))
        self.strs_dict = json.load(open(self.file_pth + 'j_son/strs_dict.json'))
        self.syl_count = json.load(open(self.file_pth + 'j_son/syl_count.json'))
        self.main_gram = json.load(open(self.file_pth + 'j_son/main_gram.json'))
        self.mrev_gram = json.load(open(self.file_pth + 'j_son/mrev_gram.json'))
        self.brwn_dict = json.load(open(self.file_pth + 'j_son/brwn_dict.json'))
        self.cmu_pdict = json.load(open(self.file_pth + 'j_son/cmu_pdict.json'))
        self.eng_words = json.load(open(self.file_pth + 'j_son/eng_words.json'))
        self.stp_words = json.load(open(self.file_pth + 'j_son/stp_words.json'))

        self.main_file = self.main_gram
        self.vocb_file = self.main_vocb
        self.rgrm_file = self.mrev_gram
        self.mgrm_file = self.main_gram
        self.pron_file = self.pron_dict
        self.strs_file = self.strs_dict
        self.sylc_file = self.syl_count
        self.rhym_file = self.rhym_dict


class Anlyz:
    def __init__(self):
        self.sett = Settings()
        self.vows = ['A', 'E', 'I', 'O', 'U', 'Y', 'a', 'e', 'i', 'o', 'u', 'y']
        self.cnst = 'bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ'
        self.cnsl = 'bcdfghjklmnpqrstvwxz'
        self.cnsu = 'BCDFGHJKLMNPQRSTVWXZ'
        self.prnv = ['A', 'E', 'I', 'O', 'U']
        self.prnc = list(self.cnsu)
        self.cncl = ['sh', 'ch', 'th', 'ph', 'ng']

    @staticmethod
    def time_elapse(start, end):
        t1 = start.split()[3].split(':')
        t2 = end.split()[3].split(':')
        hours   = int(t2[0]) - int(t1[0])
        minutes = int(t2[1]) - int(t1[1])
        seconds = int(t2[2]) - int(t1[2])
        if seconds < 0:
            seconds += 60
            minutes -= 1
        if minutes < 0:
            minutes += 60
            hours -= 1
        if hours < 10: hours = '0' + str(hours)
        else: hours = str(hours)
        if minutes < 10: minutes = '0' + str(minutes)
        else: minutes = str(minutes)
        if seconds < 10: seconds = '0' + str(seconds)
        else: seconds = str(seconds)
        print('\nTotal time = ' + hours + ':' + minutes + ':' + seconds + '\n')


    @staticmethod
    def list_inter(list1, list2):
        in_both = []
        for elem in list1:
            if elem in list2:
                in_both.append(elem)
        return in_both


    @staticmethod
    def clusters(let_list):
        count = 0
        end = []
        while count < len(let_list):
            p = [let_list[count]]
            while (count < (len(let_list) - 1)) and let_list[count] + 1 == let_list[count + 1]:
                p.append(let_list[count + 1])
                if count == len(let_list)-1:
                    break
                else: count += 1
            count += 1
            end.append(p)
        return end


    def vowel_index(self, word):
        vow_ind = []
        for i in range(len(word)):
            if word[i] in self.vows:
                vow_ind.append(i)
        return vow_ind


    def cons_index(self, word):
        cons_ind = []
        for i in range(len(word)):
            if word[i] not in self.vows:
                cons_ind.append(i)
        return cons_ind


    def pron_v_ind(self, word):
        pron_dict = self.sett.pron_dict
        pron = pron_dict[word]
        pron_vow_ind = []
        for i in range(len(pron)):
            if pron[i][0] in self.prnv:
                pron_vow_ind.append(i)
        return pron_vow_ind


    def pron_c_ind(self, word):
        pron = self.sett.pron_dict[word]
        pron_con_ind = []
        for i in range(len(pron[0])):
            if pron[0][i][0] in self.prnc:
                pron_con_ind.append(i)
        return pron_con_ind


    def clus_v_ind(self, word):
        phon = self.phon_clus(word)
        phon_clus_ind = []
        for i in range(len(phon)):
            if phon[i][0] in self.vows:
                phon_clus_ind.append(i)
        return phon_clus_ind


    def v_clus(self, word):
        v_ind = self.vowel_index(word)
        v_ind_clus = self.clusters(v_ind)
        v_clusters = []
        for v in v_ind_clus:
            first = v[0]
            length = len(v)
            seg = word[first: first + length]
            v_clusters.append(seg)
        return v_clusters


    def c_clus(self, word):
        c_ind = self.cons_index(word)
        c_ind_clus = self.clusters(c_ind)
        c_clusters = []
        for c in c_ind_clus:
            first = c[0]
            length = len(c)
            seg = word[first: first + length]
            c_clusters.append(seg)
        return c_clusters


    def phon_clus(self, word):
        phones = []
        v_cl = self.v_clus(word)
        c_cl = self.c_clus(word)
        if 0 in self.cons_index(word):
            phon_cl = c_cl[:]
            for n in range(len(v_cl)):
                phon_cl.insert(1 + (2 * n), v_cl[n])
        else:
            phon_cl = v_cl[:]
            for n in range(len(c_cl)):
                phon_cl.insert(1 + (2 * n), c_cl[n])
        for cl in phon_cl:
            if (cl[0] in self.cnst) and (cl not in self.cncl) \
                    and (len(set(list(cl))) > 1):
                phones += list(cl)
            else: phones.append(cl)
        if phones[-1] == 'e' or phones[-1] == 'E':
            phones.pop()
        return phones


    @staticmethod
    def slices(word):
        w_slices = [word[:i+1] for i in range(len(word))] + [word[i:] for i in range(len(word))]
        return w_slices


    def sim_words(self, word):
        s_words = []
        for i in range(len(word)):
            sim = [w for w in self.sett.eng_words if (word[:i] == w[:i]) and (word[i+1:] == w[i+1:])]
            s_words += sim
        return s_words


    def sim_phon(self, phon_cls, word_phon):
        sim = True
        for i in range(len(word_phon)):
            if word_phon[i] in self.cnsu:
                if word_phon[i] == 'K' and phon_cls[i] == 'c':
                    sim = True
                elif word_phon[i].lower() != phon_cls[i]:
                    sim = False
        return sim


    def most_freq(self, clus):
        phon = self.sett.freq_pron[clus]
        freq = list(set([p for p in phon if phon.count(p) == max([phon.count(c) for c in list(set(phon))])]))
        return freq


    def last_vowel(self, word):
        pron_dict = self.sett.pron_dict
        last_vows = []
        if word.lower() in list(pron_dict.keys()):
            pron = pron_dict[word.lower()]
        else:
            pron = self.gen_pron(word.lower())
        index = -1
        while -len(pron) <= index < 0:
            if pron[index][0] in self.vows:
                last_vows.append(pron[index])
                index = 0
            else: index -= 1
        return last_vows


    def last_syl(self, word):
        pron_dict = self.sett.pron_dict
        last_syls = []
        if word in list(pron_dict.keys()):
            pron = pron_dict[word]
        else:
            pron = self.gen_pron([word])
        index = -1
        while -len(pron) <= index < 0:
            if pron[index][0] in self.vows:
                vow = pron[index][:2]
                pron[index] = vow
                last_syls = pron[index:]
                index = 0
            else: index -= 1
        return last_syls


    def rhyme_test(self, word1, word2):
        try:
            if self.list_inter(self.last_syl(word1), self.last_syl(word2)):
                return True
            else: return False
        except:
            return False


    def strs_pattrn(self, word):
        pron_dict = self.sett.pron_dict
        strs_dict = self.sett.strs_dict
        strs_pat = ''
        if word.isalpha():
            if word in pron_dict.keys():
                pron = pron_dict[word]
            else:
                print('gen_pron:', word)
                pron = self.gen_pron([word])[0]
            for i in range(len(pron)):
                if pron[i][-1].isdigit():
                    strs_pat += pron[i][-1]
            strs_pat = strs_pat.split()
            strs_pat = ''.join(strs_pat)
            strs_dict[word] = strs_pat
        return strs_pat


    def count_syl(self, word):
        strs_dict = self.sett.strs_dict
        num_syls = 0
        if word.isalpha():
            if word in strs_dict.keys():
                num_syls = len(strs_dict[word])
            else:
                num_syls = len(self.strs_pattrn(word))
        else: print(word)
        return num_syls


    def gen_pron(self, word_list):
        prondict  = self.sett.cmu_pdict
        pron_dict = self.sett.pron_dict
        freq_pron = self.sett.freq_pron
        prons = []
        for word in word_list:
            if word not in prondict.keys():
                print(word)
                word_pron = []
                phon_cl = self.phon_clus(word)
                for i in range(len(phon_cl)):
                    if phon_cl[i].lower() in freq_pron.keys():
                        phon = choice(freq_pron[phon_cl[i].lower()])
                    else:
                        phon = phon_cl[i].upper()
                    word_pron.append(phon)
                pron_dict[word] = word_pron
                prons += word_pron
        with open(self.sett.file_pth + 'j_son/pron_dict.json', 'w') as mpd: json.dump(pron_dict, mpd)
        return prons


    def gram_struc(self, wordlist):
        mrev_gram = self.sett.mrev_gram
        main_gram = self.sett.main_gram
        sent_pos = []
        for word in wordlist:
            if word in main_gram.keys():
                sent_pos.append(main_gram[word])
            else:
                pos = pos_tag([word])[0][1]
                sent_pos.append(pos)
                main_gram[word] = pos
                if pos in mrev_gram.keys():
                    mrev_gram[pos].append(word)
                else:
                    mrev_gram[pos] = [word]
        return sent_pos


class Text:

    def __init__(self, filename, file_id):
        self.filename = filename
        self.file_id  = file_id
        self.file_ext = '/users/jason/teknopoetx/'

    @property
    def vocab(self):
        from txt_admin import update_all, gen_vocab
        try:
            f_id = self.file_ext + 'j_son/vocab/' + self.file_id + '_vocab.json'
            with open(f_id) as file:
                text_voc = json.load(file)
            return text_voc
        except FileNotFoundError:
            update_all(gen_vocab(self.filename, self.file_id))

    @property
    def rev_gram(self):
        from txt_admin import gen_rev_gram
        try:
            f_id = self.file_ext + 'j_son/rev_gram/' + self.file_id + '_rev_gram.json'
            with open(f_id) as f_obj_rv:
                revgrm = json.load(f_obj_rv)
                return revgrm
        except FileNotFoundError:
            gen_rev_gram(self.vocab, self.file_id)

    def formatted(self, filename, file_id, sett):
        from txt_formt import format_text
        format_text(self, filename, file_id, sett)


class Word(S):

    def __init__(self, word):
        super(S, self).__init__()
        self.word = word
        self.sett = Settings()
        self.anlz = Anlyz()

        # Associates word with part of speech, stress pattern, number of syllables, and phonetic description
        self.pstg = self.get_pstg()
        self.strs = self.get_strs()
        self.nsyl = self.get_nsyl()
        self.pron = self.get_pron()

    # Functions for generating above properties
    def genpron(self):    return self.anlz.gen_pron([self.word])

    def strspattrn(self): return self.anlz.strs_pattrn(self.word)

    def countsyl(self):   return self.anlz.count_syl(self.word)

    def get_pstg(self):
        try: return self.sett.main_gram[self.word]
        except: return self.anlz.gram_struc([self.word])[0]

    def get_pron(self):
        try: return self.sett.pron_dict[self.word]
        except: return self.anlz.gen_pron([self.word])[0]

    def get_strs(self):
        try: return self.sett.strs_dict[self.word]
        except: return self.anlz.strs_pattrn(self.word)

    def get_nsyl(self):
        try: return self.sett.syl_count[self.word]
        except: return self.anlz.count_syl(self.word)

    def __add__(self, other):
        return Word(self.word + other)

    # Breaks words into parts useful for determining the above properties
    def vin(self):    return self.anlz.vowel_index(self.word)
    def cin(self):    return self.anlz.cons_index(self.word)
    def pvin(self):   return self.anlz.pron_v_ind(self.word)
    def vclin(self):  return self.anlz.clus_v_ind(self.word)
    def vcls(self):   return self.anlz.v_clus(self.word)
    def ccls(self):   return self.anlz.c_clus(self.word)
    def phcls(self):  return self.anlz.phon_clus(self.word)
    def slcs(self):   return self.anlz.slices(self.word)
    def simw(self):   return self.anlz.sim_words(self.word)
    def lstv(self):   return self.anlz.last_vowel(self.word)
    def lstsyl(self): return self.anlz.last_syl(self.word)








if __name__ == '__main__':


    """
    paradise_lost = 'texts/milton-paradise_lost.txt'
    to_the_lhouse = 'texts/to_the_lighthouse_raw.txt'
    mrs_dalloway  = 'texts/mrs_dalloway_raw.txt'
    the_waves     = 'texts/the_waves.txt'
    plath_poems   = 'process/plath-poems.txt'
    colled_poems  = 'texts/poems_raw.txt'
    harry_potter  = 'texts/harry_potter_sorc_stone.txt'
    leavesofgrass = 'process/whitman-leaves.txt'
    js2_rg        = 'j_son/rev_gram/js2_rg.json'
    vwempl_rg     = 'j_son/rev_gram/vwempl_combd.json'
    plath_rev_grm = 'j_son/rev_gram/plath_rev_gram.json'
    yeats_rev_grm = 'j_son/rev_gram/yeats_rev_gram.json'
    js_hp_grm     = 'j_son/rev_gram/jshp_rg.json'
    pl_yt_grm     = 'j_son/rev_gram/pl_yt_rvgm_combd.json'

    """