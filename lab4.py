import random
import re
import string


def create_random_dict(num_dic):
    for _ in range(num_dic):
        num_key = random.randint(2, 26)  # 26 - count of letters in English alphabet
        dic = {}
        list_of_keys = [i for i in range(97, 123)]  # ANSII_codes of low letters
        for _ in range(num_key):
            key_new = chr(random.choice(list_of_keys))
            list_of_keys.remove(ord(key_new))
            value_new = random.randint(0, 100)
            dic[key_new] = value_new
        random_lst_of_dict.append(dic)
    return random_lst_of_dict


def all_keys_dict(list_of_rand):
    for diction in list_of_rand:
        for key in diction.keys():
            all_keys.append(key)
    return all_keys


def result_of_dict(set_of_keys):
    for i in set_of_keys:
        max_val = 0
        key_ind = 0
        update_type = 0
        for num_of_el in range(len(random_lst_of_dict)):
            for k, v in random_lst_of_dict[num_of_el].items():
                if k == i:
                    update_type += 1
                    if v >= max_val:
                        key_ind = num_of_el + 1
                        max_val = v
        if update_type == 1:
            result_dict.update({str(i): max_val})
        else:
            result_dict.update({str(i) + '_' + str(key_ind): max_val})
    return result_dict


def replace_sent_in_text(str_init, string_to_replace_lower_case, new_string_value_lower_case):
    return str_init.lower().replace(string_to_replace_lower_case, new_string_value_lower_case)


def new_sentence(str_mod):
    return ' '.join(re.findall(r'\S*[.]', str_mod)).replace('. ', ' ') + ' '  # sentence from last words


def insert_new_sent(snt_end, position_of_new_sent):
    cnt = 0
    str_new_sent = []
    for i in range(len(modif_str)):
        if modif_str[i] == '.':
            cnt += 1
        if cnt == position_of_new_sent:  # insert new sentence on position
            str_new_sent = modif_str[:i + 2] + ' ' + snt_end + modif_str[i + 2:]
    return str_new_sent.split('.')


def sentence_with_capit_letters(text_with_low_letters):
    sentence_with_capit = []
    for sentence_in_list in text_with_low_letters:  # every element in list with Capit letter
        k = 0
        while sentence_in_list[k].isspace() and k < (len(sentence_in_list) - 2):
            k += 1
        if k == (len(sentence_in_list) - 1):
            sentence_with_capit.append(sentence_in_list)
        else:
            sentence_with_capit.append(sentence_in_list[:k] + sentence_in_list[k:].capitalize())
    return '.'.join(sentence_with_capit)  # new text with Capit letters and full stop after each sentence


def cnt_whitespaces(str_for_count_whitespaces):
    cnt_whitesp = 0  # calc count of whitespaces
    for i in str_for_count_whitespaces:
        if i in string.whitespace:
            cnt_whitesp += 1
    return cnt_whitesp


random_lst_of_dict, all_keys, result_dict = [], [], {}
create_random_dict(random.randint(2, 10))   # create of random list of dict with random low letters of English alphabet
all_keys_dict(random_lst_of_dict)  # all keys of all dicts
print(result_of_dict(sorted(set(all_keys))))  # dict with unique keys and max value
init_str = '''	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.

'''
modif_str = replace_sent_in_text(init_str, ' iz ', ' is ')  # modify in init text(var init_str) iz to is in
new_sent_from_end_of_sent = new_sentence(modif_str)   # new str from  the last word of each sentence
list_of_sent = insert_new_sent(new_sent_from_end_of_sent, 2)  # insert new sentence on selected position
print('new text:\n', sentence_with_capit_letters(list_of_sent))   # text with capital letters in every sentence
print('Count of whitespaces: ', cnt_whitespaces(init_str))  # count of whitespaces in the text
