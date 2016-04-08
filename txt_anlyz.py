from random import choice
from nltk import *
from teknopoetx import Settings

sett = Settings()

vowels = ['A', 'E', 'I', 'O', 'U', 'Y', 'a', 'e', 'i', 'o', 'u', 'y']
consonants = 'bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ'
consonants_low = 'bcdfghjklmnpqrstvwxz'
consonants_up = 'BCDFGHJKLMNPQRSTVWXZ'
pron_vows = ['A', 'E', 'I', 'O', 'U']
pron_cons = list(consonants_up)
cons_clusters = ['sh', 'ch', 'th', 'ph', 'ng']

file1 = 'j_son/pron_dict.json'

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


def list_inter(list1, list2):
    in_both = []
    for elem in list1:
        if elem in list2:
            in_both.append(elem)
    return in_both


def vowel_index(word):
    vow_ind = []
    for i in range(len(word)):
        if word[i] in vowels:
            vow_ind.append(i)
    return vow_ind


def cons_index(word):
    cons_ind = []
    for i in range(len(word)):
        if word[i] not in vowels:
            cons_ind.append(i)
    return cons_ind


def pron_v_ind(word):
    pron_dict = sett.pron_dict
    pron = pron_dict[word]
    pron_vow_ind = []
    for i in range(len(pron)):
        if pron[i][0] in pron_vows:
            pron_vow_ind.append(i)
    return pron_vow_ind


def pron_c_ind(word):
    pron = sett.pron_dict[word]
    pron_con_ind = []
    for i in range(len(pron[0])):
        if pron[0][i][0] in pron_cons:
            pron_con_ind.append(i)
    return pron_con_ind


def clus_v_ind(word):
    phon = phon_clus(word)
    phon_clus_ind = []
    for i in range(len(phon)):
        if phon[i][0] in vowels:
            phon_clus_ind.append(i)
    return phon_clus_ind


def v_clus(word):
    v_ind = vowel_index(word)
    v_ind_clus = clusters(v_ind)
    v_clusters = []
    for v in v_ind_clus:
        first = v[0]
        length = len(v)
        seg = word[first: first + length]
        v_clusters.append(seg)
    return v_clusters


def c_clus(word):
    c_ind = cons_index(word)
    c_ind_clus = clusters(c_ind)
    c_clusters = []
    for c in c_ind_clus:
        first = c[0]
        length = len(c)
        seg = word[first: first + length]
        c_clusters.append(seg)
    return c_clusters


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


def phon_clus(word):
    phones = []
    v_cl = v_clus(word)
    c_cl = c_clus(word)
    if 0 in cons_index(word):
        phon_cl = c_cl[:]
        for n in range(len(v_cl)):
            phon_cl.insert(1 + (2 * n), v_cl[n])
    else:
        phon_cl = v_cl[:]
        for n in range(len(c_cl)):
            phon_cl.insert(1 + (2 * n), c_cl[n])
    for cl in phon_cl:
        if (cl[0] in consonants) and (cl not in cons_clusters) \
                and (len(set(list(cl))) > 1):
            phones += list(cl)
        else: phones.append(cl)
    if phones[-1] == 'e' or phones[-1] == 'E':
        phones.pop()
    return phones


def slices(word):
    w_slices = [word[:i+1] for i in range(len(word))] + [word[i:] for i in range(len(word))]
    return w_slices


def sim_words(word):
    s_words = []
    for i in range(len(word)):
        sim = [w for w in sett.eng_words if (word[:i] == w[:i]) and (word[i+1:] == w[i+1:])]
        s_words += sim
    return s_words


def sim_phon(phon_cls, word_phon):
    sim = True
    for i in range(len(word_phon)):
        if word_phon[i] in consonants_up:
            if word_phon[i] == 'K' and phon_cls[i] == 'c':
                sim = True
            elif word_phon[i].lower() != phon_cls[i]:
                sim = False
    return sim


def most_freq(clus):
    phon = sett.freq_pron[clus]
    freq = list(set([p for p in phon if phon.count(p) == max([phon.count(c) for c in list(set(phon))])]))
    return freq


def last_vowel(word):
    pron_dict = sett.pron_dict
    last_vows = []
    if word.lower() in list(pron_dict.keys()):
        pron = pron_dict[word.lower()]
    else:
        pron = gen_pron(word.lower())
    index = -1
    while -len(pron) <= index < 0:
        if pron[index][0] in vowels:
            last_vows.append(pron[index])
            index = 0
        else: index -= 1
    return last_vows


def last_syl(word):
    pron_dict = sett.pron_dict
    last_syls = []
    if word in list(pron_dict.keys()):
        pron = pron_dict[word]
    else:
        pron = gen_pron([word])
    index = -1
    while -len(pron) <= index < 0:
        if pron[index][0] in vowels:
            vow = pron[index][:2]
            pron[index] = vow
            last_syls = pron[index:]
            index = 0
        else: index -= 1
    return last_syls


def rhyme_test(word1, word2):
    try:
        if list_inter(last_syl(word1), last_syl(word2)):
            return True
        else: return False
    except:
        return False


def strs_pattrn(word):
    pron_dict = sett.pron_dict
    strs_dict = sett.strs_dict
    strs_pat = ''
    if word.isalpha():
        if word in pron_dict.keys():
            pron = pron_dict[word]
        else:
            print('gen_pron:', word)
            pron = gen_pron([word])[0]
        for i in range(len(pron)):
            if pron[i][-1].isdigit():
                strs_pat += pron[i][-1]
        strs_pat = strs_pat.split()
        strs_pat = ''.join(strs_pat)
        strs_dict[word] = strs_pat
    return strs_pat


def count_syl(word):
    strs_dict = sett.strs_dict
    num_syls = 0
    if word.isalpha():
        if word in strs_dict.keys():
            num_syls = len(strs_dict[word])
        else:
            num_syls = len(strs_pattrn(word))
    else: print(word)
    return num_syls


def gen_pron(wordlist):
    import json
    prondict  = sett.cmu_pdict
    pron_dict = sett.pron_dict
    freq_pron = sett.freq_pron
    prons = []
    count = 0
    for word in wordlist:
        count += 1
        if word not in prondict.keys():
            word_pron = []
            phon_cl = phon_clus(word)
            for i in range(len(phon_cl)):
                if phon_cl[i].lower() in freq_pron.keys():
                    phon = choice(freq_pron[phon_cl[i].lower()])
                else:
                    phon = phon_cl[i].upper()
                word_pron.append(phon)
            pron_dict[word] = word_pron
            prons += word_pron
    with open(file1, 'w') as mpd: json.dump(pron_dict, mpd)
    return prons


def gram_struc(wordlist):
    mrev_gram = sett.mrev_gram
    main_gram = sett.main_gram
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



#if __name__ == '__main__':


