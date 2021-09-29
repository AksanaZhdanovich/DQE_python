import random


def lst_of_dic(num_dic):
    global lst
    lst = []
    for _ in range(num_dic):
        num_key = random.randint(2, 26)  # 26 - count of letters in English alphabet
        dic = {}
        list_of_keys = [i for i in range(97, 123)]  # ANSII_codes of low letters
        for _ in range(num_key):
            key_new = chr(random.choice(list_of_keys))
            list_of_keys.remove(ord(key_new))
            value_new = random.randint(0, 100)
            dic[key_new] = value_new
        lst.append(dic)
    return lst


def uniq_keys(x):  # set of all generated keys
    global all_keys
    all_keys = []
    for diction in x:
        for key in diction.keys():
            all_keys.append(key)
    all_keys = sorted(all_keys)
    return all_keys


def result_of_dict(x):
    global result_dict
    result_dict = {}
    for i in x:
        max_val = 0
        key_ind = 0
        update_type = 0
        for dict1 in range(len(lst)):
            for k, v in lst[dict1].items():
                if k == i:
                    update_type += 1
                    if v >= max_val:
                        key_ind = dict1 + 1
                        max_val = v
        if update_type == 1:
            result_dict.update({str(i): max_val})
        else:
            result_dict.update({str(i) + '_' + str(key_ind): max_val})
    return result_dict


lst_of_dic(random.randint(2, 10))  # number of dictionaries
uniq_keys(lst)
print(result_of_dict(all_keys))
