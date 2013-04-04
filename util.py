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

par = ['''    Well, here's a story for you: Sarah Perry was a veterinary nurse who had been working daily at an old zoo in a deserted district of the territory, so she was very happy to start a new job at a superb private practice in North Square near the Duke Street Tower. That area was much nearer for her and more to her liking. Even so, on her first morning, she felt stressed. She ate a bowl of porridge, checked herself in the mirror and washed her face in a hurry. Then she put on a plain yellow dress and a fleece jacket, picked up her kit and headed for work.''', 
        '''    When she got there, there was a woman with a goose waiting for her. The woman gave Sarah an official letter from the vet. The letter implied that the animal could be suffering from a rare form of foot and mouth disease, which was surprising, because normally you would only expect to see it in a dog or a goat. Sarah was sentimental, so this made her feel sorry for the beautiful bird.''',
        '''    Before long, that itchy goose began to strut around the office like a lunatic, which made an unsanitary mess. The goose's owner, Mary Harrison, kept calling, "Comma, Comma," which Sarah thought was an odd choice for a name. Comma was strong and huge, so it would take some force to trap her, but Sarah had a different idea. First she tried gently stroking the goose's lower back with her palm, then singing a tune to her. Finally, she administered ether. Her efforts were not futile. In no time, the goose began to tire, so Sarah was able to hold onto Comma and give her a relaxing bath.''',
        '''    Once Sarah had managed to bathe the goose, she wiped her off with a cloth and laid her on her right side. Then Sarah confirmed the vet's diagnosis. Almost immediately, she remembered an effective treatment that required her to measure out a lot of medicine. Sarah warned that this course of treatment might be expensive - either five or six times the cost of penicillin. I can't imagine paying so much, but Mrs. Harrison - a millionaire lawyer - thought it was a fair price for a cure.''']
