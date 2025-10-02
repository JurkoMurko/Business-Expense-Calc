import csv, json


def parse(stuff):
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

dic_list = []
for i in range(2020, 2023):
    dic_list.append({})
remove_words = ["SUN PRAIRIE", " WI",'MADISON', ' MI', 'THE ', 'OF', 'POS DEBIT', 'TST*', 'SQ']
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

# parsing
with open(r"Transaction html\muro chase oct 12\muroChase.CSV", "r") as f:
    reedThing = csv.DictReader(f)
    for transaction in reedThing:
        print(transaction)
        place = parse(transaction['Description']).split()[0].upper()
        amount = float(transaction["Amount"])
        date = transaction['Posting Date']
        year = int(date.split('/')[2])
        # print(transaction['Description'] + ' | ' + place)

        # making the dictionary 
        current_year_dic = dic_list[year - 2020]
        if place not in current_year_dic:
            current_year_dic[place] = amount
        else:
            current_year_dic[place] = current_year_dic[place] + amount

for dic in dic_list:
    year = dic_list.index(dic) + 2020

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

    # sorting the dictionary
    sorted_dic = dict(sorted(dic.items(), key=lambda item: item[1]))

    # writing the file
    name = "fuuuuuck " + str(year)
    with open(name + '.txt', 'w') as fi:
        fi.write(f"Juro Chase Transactions & Accounting {year}\n\n")
        for k,v in sorted_dic.items():
            fi.write(f'{k} | {v}\n')
