import csv


def chase_parser(stuff: str):
    stri = '*\/#'
    remove = ["SUN", "PRAIRIE", 'WISCONSIN', 'BERRIEN', 'BELVIDERE', 'NEW BUFFALO', 'FITCHBURG', 'MARSHALL', 'DE FOREST', 'MADISON', ' OF ',
              'STOUGHTON', 'VERONA', ' TO ', 'EAST', '- ', '.COM', 'NO ', '_', 'PU ', ' E ', ' T-'] + [i for i in stri]

    stuff = stuff.replace('POS DEBIT', '')
    stuff = stuff.replace('TST*', '')
    stuff = stuff.replace('SQ *', '')
    stuff = stuff.upper()

    for word in remove:
        try:
            stuff = stuff[:stuff.index(word)]  # .replace(word, "")
        except ValueError:
            pass

    for j in range(10):
        stuff = stuff.replace(str(j), '')

    return stuff.strip()


def make_chase_dic(transaction_path):
    dic = {}
    with open(transaction_path, "r") as f:
        for transaction in csv.DictReader(f):
            place = chase_parser(transaction['Description'])
            # print(transaction['Description'] + ' | ' + place)
            amount = float(transaction["Amount"])
            # year = int(transaction['Posting Date'].split('/')[2])
            # dic = dic_dic[f'muro chase {year}']  # this is dumb cuz dicts in python dont assign its a refferance
            if place not in dic:
                dic[place] = amount
            else:
                dic[place] = dic[place] + amount
    return dic


def make_bmo_dic(transaction_path):
    dic = {}
    with open(transaction_path, "r") as f:
        for transaction in csv.DictReader(f):
            # print(transaction)
            place = transaction['Simple Description'].upper()
            place = 'BP' if place.strip()[:3] == 'BP ' else place.replace(
                ' - NA', '').strip()

            amount = float(transaction['Amount'].replace(',', ''))

            # combining transactions in the dict by place
            if place not in dic:
                dic[place] = amount
            else:
                dic[place] += amount

    return dic


# making the dictionary of bank account names to their transaction dicts
'''
this is very useful if you want to write multiple files and work with multiple accounts
you're just looping over the top level dictionary
'''
dic_dic = {}  # {f'muro chase {i}': {} for i in range(2022, 2023)}
resultsDickDick = {}

results_folder_path = r'Bis2022'
categoriesPath = r'categories.txt'

dic_dic['bis2022TP'] = make_bmo_dic(r'Bis2022\transactions.csv')

for name, dic in dic_dic.items():  # combining places by industry & wrinting result file
    with open(categoriesPath, 'r') as f:  # combining
        for category in f.read().split('\n\n'):
            sum = 0
            key_del_list = []
            categoryName, categorieMembers = category.split(':')
            resultsDickDick[categoryName] = {}

            for sellerName, dollarAmmount in dic.items():
                if sellerName in categorieMembers:

                    if sellerName not in resultsDickDick[categoryName]:
                        resultsDickDick[categoryName][sellerName] = dollarAmmount
                    else:
                        resultsDickDick[categoryName][sellerName] += dollarAmmount

                    sum += dollarAmmount
                    if sellerName != 'Supplies and Equiptment': #special exception
                        key_del_list.append(sellerName)

            for i in key_del_list: # deleting combined transactions
                del dic[i]
            dic[categoryName] = sum # adding the sum as a transaction

    dic = {k: round(v, 2) for k, v in dic.items()}  # rounding
    dic = dict(sorted(dic.items(), key=lambda item: item[1])) # sorting
    # with open(f'{results_folder_path}\{name}.txt', 'w') as f:  # writing the file
    #     for k, v in dic.items():
    #         f.write(f'{k} | {v}\n')

print(resultsDickDick.__repr__())