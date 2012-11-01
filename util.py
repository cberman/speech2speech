from nltk.corpus import cmudict

pron_dict = cmudict.dict()

char2word = {'0':'zero', '1':'one', '2':'two', 
        '3':'three', '4':'four', '5':'five', 
        '6':'six', '7':'seven', '8':'eight', 
        '9':'nine', '$':'dollars', '%':'percent',
        '^':'to the power of', '@':'at',
        '#':'number', '&':'and', '*':'times',
        '-':'minus', '+':'plus', '=':'equals',
        '/':'slash', '|':'piped into', '\\':'wack',
        '~':'tilda'}

doubledigit = {'1':'ten', '10':'ten', '11':'eleven',
        '12':'twelve', '13':'thirteen',
        '14':'fourteen', '15':'fifteen',
        '16':'sixteen', '17':'seventeen',
        '18':'eighteen', '19':'nineteen',
        '2':'twenty', '3':'thirty', '4':'forty',
        '5':'fifty', '6':'sixty', '7':'seventy',
        '8':'eighty', '9':'ninety'}

power10 = {1:'ten', 2:'hundred', 3:'thousand', 
        6:'million', 9:'billion', 12:'trillion'}
