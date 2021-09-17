import random
lst = []
num_dic = random.randint(2, 10)   # number of dictionaries
for _ in range(1, num_dic + 1):
    num_key = random.randint(2, 26)   # 26 - count of letters in English alphabet
    dic = {}
    list_of_keys = [i for i in range(97, 123)]   # ANSII_codes of low letters
    for _ in range(1, num_key + 1):
        key1 = chr(random.choice(list_of_keys))
        list_of_keys.remove(ord(key1))
        value1 = random.randint(0, 100)
        dic[key1] = value1
    lst.append(dic)
all_keys = sorted(set().union(*(k.keys() for k in lst)))  # all unique keys from all dictionaries
result_dict = {}
for i in all_keys:
    max_val = 0
    key_ind = 0
    update_type = 0
    for dict1 in range(0, len(lst)):
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
print(result_dict)