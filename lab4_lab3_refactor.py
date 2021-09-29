import string
import re


def iz_to_is(str_init):
    global modif_str
    modif_str = str_init.lower().replace(' iz ', ' is ')  # modify iz to is
    return modif_str


def new_sentence(str_mod):
    global end_of_sent
    end_of_sent = ' '.join(re.findall(r'\S*[.]', str_mod)).replace('. ', ' ') + ' '  # sentence from last words
    return end_of_sent


def insert_new_sent(snt_end):
    cnt = 0
    str_new_sent = []
    global list_of_sent
    for i in range(len(modif_str)):
        if modif_str[i] == '.':
            cnt += 1
        if cnt == 2:  # insert new sentence after 2 sentence
            str_new_sent = modif_str[:i + 2] + ' ' + snt_end + modif_str[i + 2:]
    list_of_sent = str_new_sent.split('.')
    return list_of_sent


def final_snt(mod_sent):
    sentence_with_capit = []
    for sent_in_list in mod_sent:  # every element in list with Capit letter
        k = 0
        while sent_in_list[k].isspace() and k < (len(sent_in_list) - 2):
            k += 1
        if k == (len(sent_in_list) - 1):
            sentence_with_capit.append(sent_in_list)
        else:
            sentence_with_capit.append(sent_in_list[:k] + sent_in_list[k:].capitalize())
    str_total = ('.'.join(sentence_with_capit))  # new str without mistakes
    return str_total


def cnt_whitespaces(str):
    cnt_whitesp = 0  # calc count of whitespaces
    for i in str:  # count of whitespaces
        if i in string.whitespace:
            cnt_whitesp += 1
    return cnt_whitesp


init_str = '''	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.

'''

iz_to_is(init_str)
new_sentence(modif_str)
insert_new_sent(end_of_sent)
print('new text:\n', final_snt(list_of_sent))
print('Count of whitespaces: ', cnt_whitespaces(init_str))
