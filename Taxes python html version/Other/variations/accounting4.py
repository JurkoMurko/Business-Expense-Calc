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
            print(transaction)
            place = transaction['Simple Description'].upper()
            place = 'BP' if place.strip()[:3] == 'BP ' else place.replace(' - NA', '').strip()

            amount = float(transaction['Amount'].replace(',', ''))

            # combining transactions in the dict by place
            if place not in dic:
                dic[place] = amount
            else:
                dic[place] += amount

    return dic


# making the dictionary of bank account names to their transaction dicts
dic_dic = {}  # {f'muro chase {i}': {} for i in range(2022, 2023)}

results_folder_path = r'Results\2022 tax trial'
categoriesPath = r'Categories\categories.txt'

# muro_transactions_path = r"Transaction html\muro chase oct 12\muro_chase_2022.CSV"
# filip_transactions_path = r'Transaction html\muro chase oct 12\filipChase 2022.CSV'
# bmo_bis_transactions_path = r"Transaction html\km windows taxe transactions\Jan 2022 - Oct 17 BMO Business.csv"
# bmo_personal_transactions_path = r'Transaction html\km windows taxe transactions\Bmo personal 2022.csv'
business2022trial_transactions_path = r'Transaction html\bis2022trial\Business Transactions - 2022 Jan-Dec28.csv.csv'

# dic_dic['muro chase 2022'] = make_chase_dic(muro_transactions_path)
# dic_dic['filip chase 2022'] = make_chase_dic(filip_transactions_path)
# dic_dic['bmo bis 2022'] = make_bmo_dic(bmo_bis_transactions_path)
# dic_dic['bmo personal 2022'] = make_bmo_dic(bmo_personal_transactions_path)
dic_dic['business2022trial'] = make_bmo_dic(business2022trial_transactions_path)


for name, dic in dic_dic.items(): # combining places by industry & wrinting result file
    with open(categoriesPath, 'r') as f: # combining
        for industry in f.read().split('\n\n'):
            sum = 0
            key_del_list = []
            category, places = industry.split(':')
            for key, value in dic.items():
                if key in places:
                    sum += value
                    key_del_list.append(key)

            for i in key_del_list:
                del dic[i]
            dic[category] = sum

    dic = {k: round(v, 2) for k, v in dic.items()}  # rounding
    dic = dict(sorted(dic.items(), key=lambda item: item[1]))   # sorting the dictionary

    with open(f'{results_folder_path}\{name}.txt', 'w') as f: # writing the file
        for k, v in dic.items():
            f.write(f'{k} | {v}\n')
