from teknopoetx import *
from txt_formt import *
import json

mn_vocb = '/users/jason/teknopoetx/j_son/main_vocb.json'
syl_cnt = '/users/jason/teknopoetx/j_son/syl_count.json'
rv_gram = '/users/jason/teknopoetx/j_son/mrev_gram.json'
mn_gram = '/users/jason/teknopoetx/j_son/main_gram.json'
str_dct = '/users/jason/teknopoetx/j_son/strs_dict.json'
prn_dct = '/users/jason/teknopoetx/j_son/pron_dict.json'

anlz = Anlyz()
sett = Settings()


def gen_words(vocab, group_id):
    word_dict = {}
    for word in vocab:
        word_dict[word] = Word(word)
    f_id = 'j_son/' + group_id + 'w_dict.json'
    json.dump(word_dict, open(f_id, 'w'))


def gen_gram_strc():
    gen_frms = json.load(open('j_son/gram_strc/pdl_sentlines.json'))
    grm_lins = json.load(open('j_son/gram_strc/pdl_gramlines.json'))
    gram_strc = {}
    for i in range(len(gen_frms)):
        gram_strc[int(i)] = (gen_frms[i], grm_lins[i])
        print(grm_lins[i])
    json.dump(gram_strc, open('j_son/gram_strc/' + sett.file_idn + '_grmstrc.json', 'w'))
    return gram_strc


def combine_dict(dict1, dict2, f_id):
    combine_d = {}
    comb_dict = {}
    comb_keys = list(set(list(dict1.keys()) + list(dict2.keys())))
    for key in comb_keys:
        comb_dict.setdefault(key, [])
    for key1 in dict1.keys():
        comb_dict[key1] += dict1[key1]
    for key2 in dict2.keys():
        comb_dict[key2] += dict2[key2]
    for key in comb_keys:
        combine_d[key] = list(set(comb_dict[key]))
    file_id = 'j_son/rev_gram/' + f_id + '_combd.json'
    with open(file_id, 'w') as f_objid:
        json.dump(combine_d, f_objid)
    return combine_d


def word_list(textfile):
    file = open(textfile)
    text_string = file.read()
    all_words = wordpunct_tokenize(text_string)
    return all_words


def gen_rhym_dict(vocab):
    rhym_dict = {}
    for word in vocab:
        print(word)
        rhym_dict[word] = anlz.last_syl(word)
    json.dump(rhym_dict, open('j_son/rhym_dict.json', 'w'))


def gen_freq_pron():
    cmu_pdict = sett.cmu_pdict
    pron_vocab = [w.lower() for w in cmu_pdict.keys()]
    cmu_phon_clus = [(w, anlz.phon_clus(w), cmu_pdict[w][0]) for w in pron_vocab]
    cm_pc_std = [(x, y, z) for x, y, z in cmu_phon_clus if len(y) == len(z)]
    cm_fin = [(x, y, z) for x, y, z in cm_pc_std if anlz.sim_phon(y, z)]
    clus_list = [cm_fin[i][1] for i in range(len(cm_fin))]
    clus_fn = []
    for l in clus_list:
        for clus in l:
            clus_fn.append(clus)
    clus_fin = list(set(clus_fn))
    high_freq = {}
    for clus in clus_fin:
        high_freq.setdefault(clus, [])
    for x, y, z in cm_fin:
        for i in range(len(y)):
            high_freq[y[i]].append(z[i])
    keys = list(high_freq.keys())
    for k in keys:
        if not k.isalpha():
            high_freq.pop(k)
    with open('j_son/pron_freq2.json', 'w') as f_objpf:
        json.dump(high_freq, f_objpf)
    freq_pron = {}
    for clus in high_freq.keys():
        freq_pron.setdefault(clus, [])
    for key, value in high_freq.items():
        val = list(set(value))
        for phon in val:
            phon_perc = value.count(phon) / len(value)
            if phon_perc > .15:
                freq_pron[key].append(phon)
    json.dump(freq_pron, open('j_son/freq_pron.json', 'w'))
    return freq_pron


def gen_text_log(sent, sent_source):
    fname = 'logs/js_poems/log-' + sent_source
    file = open(fname, 'a')
    file.write(sent + '\n')
    file.close()


def fix_strs_dict(vocab, strs_dict=sett.strs_dict):
    strs_pat = ''
    for word in vocab:
        if word in sett.cmu_pdict.keys():
            strs_pat = strs_dict[word]
            strs_pat = strs_pat.replace('2', '1')
            strs_dict[word] = strs_pat
    fix_strs = [w for w in vocab if w not in sett.cmu_pdict.keys() and strs_dict[w]]
    for wrd in fix_strs:
        if wrd in strs_dict.keys():
            strs_pat = strs_dict[wrd]
        else:
            pron = anlz.gen_pron(wrd)
            for i in range(len(pron)):
                if pron[i][-1].isdigit():
                    strs_pat += pron[i][-1]
        strs_pat = strs_pat.replace('2', '1')
        if strs_pat[0] == '0':
            for i in range(len(strs_pat)):
                strsl = list(strs_pat)
                strsl[i] = str(i % 2)
                strs_pat = ''.join(strsl)
        else:
            for i in range(len(strs_pat)):
                strsl = list(strs_pat)
                strsl[i] = str((i + 1) % 2)
                strs_pat = ''.join(strsl)
        strs_dict[wrd] = strs_pat

    with open(str_dct, 'w') as fob5:
        json.dump(strs_dict, fob5)


def update_main_vocab(vocab):
    main_vocb = sett.main_vocb
    new_words = [w for w in vocab if w not in main_vocb]
    for w in new_words:
        main_vocb.append(w)
        print(w)
    with open(mn_vocb, 'w') as fobj1:
        json.dump(main_vocb, fobj1)
    print('vocab update finished')


def update_main_gram(vocab):
    main_gram = sett.main_gram
    mrev_gram = sett.mrev_gram
    new_gram = [w for w in vocab if w not in main_gram.keys()]
    count = 0
    for word in new_gram:
        if word in sett.brwn_dict.keys():
            pos = sett.brwn_dict[word]
        else:
            pos = pos_tag([word])[0][1]
        main_gram[word] = pos
        if pos in mrev_gram.keys():
            mrev_gram[pos].append(word)
        else:
            mrev_gram[pos] = [word]
        count += 1
        print(str(count) + '/' + str(len(new_gram)) + ': ' + word)
    with open(mn_gram, 'w') as fobj4:
        json.dump(main_gram, fobj4)
    with open(rv_gram, 'w') as fobj3:
        json.dump(mrev_gram, fobj3)
    print('main grammar dictionary update finished')


def update_pron_dict(vocab):
    pron_dict = sett.pron_dict
    new_pron = [w for w in vocab if w not in pron_dict.keys()]
    print(len(new_pron))
    anlz.gen_pron(new_pron[:100])
    print('pronunciation dictionary update finished')


def update_strs_dict(vocab):
    strs_dict = sett.strs_dict
    new_strs = [w for w in vocab if w not in strs_dict.keys()]
    for word in new_strs:
        strs_dict[word] = anlz.strs_pattrn(word)
    fix_strs_dict(new_strs)
    with open(str_dct, 'w') as fobj5: json.dump(strs_dict, fobj5)
    print('stress dictionary update finished')


def update_syl_dict(vocab):
    syl_count = sett.syl_count
    new_syl = [w for w in vocab if w not in syl_count.keys()]
    for w in new_syl:
        syl_count[w] = anlz.count_syl(w)
    with open(syl_cnt, 'w') as fobj2: json.dump(syl_count, fobj2)
    print('syllable count dictionary update finished')


def update_rhym_dict(vocab):
    rhym_dict = sett.rhym_dict
    new_words = [w for w in vocab if w not in rhym_dict.keys()]
    for word in new_words:
        print(word)
        rhym_dict[word] = anlz.last_syl(word)
    json.dump(rhym_dict, open('j_son/rhym_dict.json', 'w'))
    print('rhyme dictionary update finished')


def update_all(vocab):
    update_main_vocab(vocab)
    update_main_gram(vocab)
    update_pron_dict(vocab)
    update_strs_dict(vocab)
    update_syl_dict(vocab)
    update_rhym_dict(vocab)


def gen_main_dict(vocab, file_id=''):
    update_all(vocab)
    txt_dict = {}
    for word in vocab:
        txt_dict[word] = dict(pos=sett.main_gram[word.lower()], strs=sett.strs_dict[word.lower()],
                              pron=sett.pron_dict[word.lower()], numsyl=sett.syl_count[word.lower()])
    filename = '/users/jason/teknopoetx/j_son/' + file_id + 'txt_dict.json'
    with open(filename, 'w') as maind: json.dump(txt_dict, maind)

'''
def process_text(file_id, frm='', *files):
    total_vocab = []
    for file in files:
        format_text(file, file_id, sett, frm)
        nfile = 'process/procd/' + file_id + '_procd.txt'
        file_voc = gen_vocab(nfile, file_id)
        total_vocab += file_voc
    total_vocab = sorted(list(set(total_vocab)))
    with open('/users/jason/teknopoetx/j_son/vocab/' + file_id + '_vocab.json', 'w') as fvoc:
        json.dump(total_vocab, fvoc)
    update_all(total_vocab, sett)
    gen_rev_gram(total_vocab, sett, file_id)
'''


if __name__ == '__main__':
    nov_voc = json.load(open('j_son/vocab/nov_vocb.json'))
    update_pron_dict(nov_voc)

    '''
    test_words = json.load(open('j_son/sonnetsw_dict.json'))
    word = test_words['word']
    o_r = test_words['or']
    print(o_r < word)


    #novels = 'process/novels.txt'
    novel_words = formt.lower_case(formt.remove_punct(word_list(novels)))
    #print(novel_words[:30])
    novel_str = ' '.join(novel_words)
    fdist = FreqDist(novel_words)
    vocb = list(fdist.items())
    json.dump(vocb, open('nov_fdist.json', 'w'))
    '''

