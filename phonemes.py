from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize as tokenize
from util import *
from re import search

def take_input(string):
    return raw_input(string)

def normalize(text):
    #text = tokenize(text)
    text = text.split()
    text = [word.lower() for word in text]
    return text

def get_pronunciation(sent):
    prons = list()
    for word in sent:
        end = ''
        if word[-1] in ['.', ',', '!', '?']:
            end = word[-1]
            word = word[:-1]
        if not word[-1].isalnum():
            word = word[:-1]
        if search(r'^[0-9]+$', word):
            if int(word) < 3000 and int(word) > 1000:
                for num in year_pron(word).split():
                    prons.append(pron_dict[num][0])
            else:
                for num in number_pron(word).split():
                    prons.append(pron_dict[num][0])
        elif search(r'^-?[0-9]*.?[0-9]+$', word):
            for num in number_pron(word).split():
                prons.append(pron_dict[num][0])
        elif search(r'^\$[0-9]+', word):
            for num in money_pron(word).split():
                prons.append(pron_dict[num][0])
        elif search(r'^.+@.+\.(com|net|org|gov|info|biz)$', word):
            for part in email_pron(word).split():
                prons.append(pron_dict[part][0])
        elif search(r'.+\.(com|net|org|gov|info|biz)', word):
            for part in url_pron(word).split():
                prons.append(pron_dict[part][0])
        elif search(r'^((2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9][0-9]|[1-9]).)' + \
                r'{3}(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9][0-9]|[1-9])$', word):
            for part in ip_pron(word).split():
                prons.append(pron_dict[part][0])
        else:
            prons.append(pron_dict[word][0])
        if end:
            pass    # do something for prosody
    return prons

def number_pron(num):
    if num[0] == '-':
        return 'negative ' + number_pron(num[1:])
    if '.' in num:
        parts = str()
        if num[0] != '.':
            parts += number_pron(num[:num.index('.')])
        parts += ' point '
        for c in num[num.index('.')+1:]:
            parts += char2word[c] + ' '
        return parts
    num = str(int(num))
    if len(num) == 1:
        return char2word[num]
    elif len(num) == 2:
        if num[0] == '1':
            return doubledigit[num]
        else:
            if num[1] == '0':
                return doubledigit[num[0]]
            else:
                return doubledigit[num[0]]+' '+char2word[num[1]]
    elif len(num) == 3:
        if num[1:] == '00':
            return char2word[num[0]] +' '+ power10[2]
        return char2word[num[0]] +' '+ power10[2] +' '+ number_pron(num[1:])
    elif len(num) < 16:
        place = (len(num) - 1) / 3 * 3
        head = num[:(len(num) - 1) % 3 + 1]
        tail = num[(len(num) - 1) % 3 + 1:]
        return number_pron(head) +' '+ power10[place] +' '+ number_pron(tail)
    
def money_pron(money):
    if search(r'^\$[0-9]+\.[0-9][0-9]$', money):
        index = money.index('.')
        return number_pron(money[1:index])+' dollars and '+\
                number_pron(money[index+1:])+' cents'
    elif search(r'^\$[0-9]+$', money):
        return number_pron(money[1:])+' dollars'

def year_pron(year):
    if year[2] == '0':
        return number_pron(year[:2])+' ought '+number_pron(year[3])
    return number_pron(year[:2])+' '+number_pron(year[2:])

def url_pron(url):
    ssl = False
    if url[:7] == 'http://':
        url = url[7:]
    elif url[:8] == 'https://':
        ssl = True
        url = url[8:]
    toReturn = str()
    if url[:4] == 'www.':
        toReturn = 'w w w dot '
        url = url[4:]
    parts = url.split('.')
    for part in parts[:-1]:
        toReturn += part+' dot '
    if ssl:
        return toReturn + parts[-1] + ' over s s l'
    return toReturn + parts[-1]

def email_pron(email):
    index = email.index('@')
    return email[:index]+' at '+url_pron(email[index+1:])

def ip_pron(ip):
    parts = str()
    for octet in ip.split('.'):
        for num in str(octet):
            if num == '0':
                parts += 'oh'
            else:
                parts += char2word[num]
            parts += ' '
        parts += 'dot '
    return parts[:-4]  # get rid of trailing dot

def main():
    running = True
    while running:
        try:
            sent = normalize(take_input('gogogo: '))
            pron = get_pronunciation(sent)
            print pron
        except (EOFError, KeyboardInterrupt):
            running = False
    print

if __name__ == '__main__': main()
