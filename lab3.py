import string
import re
init_str = '''	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.

'''
modif_str = init_str.lower().replace(' iz ', ' is ')  # modify iz to is
end_of_sent = ' '.join(re.findall(r'\S*[.]', modif_str)).replace('. ', ' ') + ' '  # sentence from last words
cnt = 0
str_new_sent = []
for i in range(len(modif_str)):
    if modif_str[i] == '.':
        cnt += 1
    if cnt == 2:  # insert new sentence after 2 sentence
        str_new_sent = modif_str[:i + 2] + ' ' + end_of_sent + modif_str[i + 2:]
list_of_sent = str_new_sent.split('.')
sentence_with_capit = []
for sent_in_list in list_of_sent:   # every element in list with Capit letter
    k = 0
    while sent_in_list[k].isspace() and k < (len(sent_in_list) - 2):
        k += 1
    if k == (len(sent_in_list) - 1):
        sentence_with_capit.append(sent_in_list)
    else:
        sentence_with_capit.append(sent_in_list[:k] + sent_in_list[k:].capitalize())
str_total = ('.'.join(sentence_with_capit))  # new str without mistakes
print('new text:\n', str_total)
cnt_whitesp = 0  # calc count of whitespaces
for i in init_str:   # count of whitespaces
    if i in string.whitespace:
        cnt_whitesp += 1
print('Count of whitespaces: ', cnt_whitesp)
