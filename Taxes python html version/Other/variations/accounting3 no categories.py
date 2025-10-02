import csv

print('hi')
# takes the transaction discription string and returns a simple version
def chase_parser(stuff):
    for word in remove_words:
        stuff = stuff.replace(word, "")

    new = ''
    stuff = stuff.strip(''.join([str(i) for i in range(0, 10)] + [*r"\ /#*"]))
    for letter in stuff:
        if letter not in remove_letters:
            new += letter
        else:
            return new
    return new


def bmo_parser(str):
    str = str.strip().replace(' - NA', '')
    if str[:2] == 'BP':
        str = 'BP'
    return str

remove_words = ["SUN PRAIRIE", " WI", 'MADISON', ' MI', 'THE ', 'OF', 'POS DEBIT', 'TST*', 'SQ']
remove_letters = [str(i) for i in range(0, 10)] + [*r"\/#*"]
combine = {
    'GROCHERIES': 'ALDI HY-VEE WOODMANS PICK METRO JOHNNY',
    'WALMART': 'WAL-MART WALMART.COM WAL',
    'DADDY JEFF': 'AMAZON AMAZON.COM AMZN',
    'GAS': 'AMOCO BP KWIK RACENIMART SHELL SPEEDWAY ',
    'RANDOM STORE SHIT': 'WALMART TARGET FIVE WALGREENS HOME DOLLAR AM',
    'PARKING AND TICKET': 'CITY PARKING CERTUS',
    'GOT PAYED BACK': 'DISPLATE NOAH\'S SIX APPLE.COM',
    'FUN TIMES': 'MARCUS NON-CHASE SPENCER AMC BOWLAVARD PRINCETON',
    'WEIRD OTHER': 'NBX FUN WP UW UNIVERSITY MMCCHARGE.COM',
    'RESTAURANT': 'CHICK-FIL-A DOORDASH COSTCO PARTHENON PIZZA RED GUSS CULVER\'S CULVERS FAMOUS GUYS HOOTERS IANSPIZZA.COM IHOP MARCOS MCDONALD\'S MOD MOKA- OLIVE PANDA PANERA POKE POPEYES SONIC SUBWAY SUGAR SUMO TACO WENDY\'S'
}

dic_dic = {f'muro chase {i}': {} for i in range(2020, 2023)}

# making the chase dictionary
with open(r"Transaction html\muro chase oct 12\muroChase.CSV", "r") as f:
    for transaction in csv.DictReader(f):
        place = chase_parser(transaction['Description']).split()[0].upper()
        amount = float(transaction["Amount"])
        year = int(transaction['Posting Date'].split('/')[2])
        # print(transaction['Description'] + ' | ' + place)

        current_dic = dic_dic[f'muro chase {year}'] # this is dumb cuz dicts in python dont assign its a refferance
        if place not in current_dic:
            current_dic[place] = amount
        else:
            current_dic[place] = current_dic[place] + amount

# making bmo dictionary
bmo_dic = {}
bmo_path = "Transaction html\km windows taxe transactions\Jan 2022 - Oct 17 BMO Business.csv"
with open(bmo_path, "r") as f:
    for transaction in csv.DictReader(f):
        place = bmo_parser(transaction['Simple Description'])
        amount = float(transaction['Amount'].replace(',', ''))

        # combining things into small categories
        if place not in bmo_dic:
            bmo_dic[place] = amount
        else:
            bmo_dic[place] += amount

dic_dic['bmo 2022'] = bmo_dic

for name,dic in dic_dic.items():
    # combining things into categories
    for k, v in combine.items():
        sum = 0
        for place in v.split():
            try:
                sum += dic[place]
                del dic[place]
            except KeyError:
                pass
        dic[k] = sum

    # rounding
    dic = {k:round(v, 2) for k,v in dic.items()}

    # sorting the dictionary
    dic = dict(sorted(dic.items(), key=lambda item: item[1]))

    # writing the file
    folder_path = 'Results\muro chase oct 12 results'
    with open(f'{folder_path}\{name}.txt', 'w') as f:
        for k, v in dic.items():
            f.write(f'{k} | {v}\n')
