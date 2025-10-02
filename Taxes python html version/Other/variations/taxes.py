from bs4 import BeautifulSoup
import json


def get_money_ammount(transaction_html):
    # find the span with the $ammount
    span = transaction_html.find("span", class_="ada-offscreen")
    try:
        formatted = span.string.strip()
        # removing USD from string
        formatted = formatted[formatted.find("USD") + len("USD"):]
        return float(formatted)
    except ValueError:
        print(span)
        raise ValueError("no bueno")


def get_location(transaction_html):
    span = transaction_html.find(
        "span", class_="y-regular-text y-ellipsis col-margin ios-ellipsis")
    return span.string


def get_date(transaction_html):
    span = transaction_html.find("span", class_="ada-hidden")
    return span.string


# def get_type(transaction_html): # _type = get_type(transaction) you can use type to add to the is_blank lists by category
#     span = transaction_html.find(
#         "span", class_="y-secondary-text ellipsis col-margin")
#     return span.string


def get_trans(file):
    with open(file) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        return soup.find_all("div", class_="transaction-inner-row")


def get_key(my_dict, val):
    for key, value in my_dict.items():
        if val == value:
            my_dict[key] = None
            return key
    return "key doesn't exist"


def add_keys(dict, lis, name):  # this could take a list of keys and use a loop to mearge more than 2
    if name.upper() in lis:
        raise Exception("name can not be in list")

    dict[name.upper()] = [sum([dict[i][0] for i in lis])]  # sum up and assign
    for i in lis:  
        dict[name.upper()].append(dict[i])
        del dict[i]
        

# def print_dict(dictionary):
#     # print total
#     print(f"Total: ${sum(dictionary.values())}  Number of items: {len(dictionary)}")


def write_files(dic, name, TXT=False, JSON=True):
    if JSON:
        i = 1
        while i <= 100:
            if i == 100:
                raise Exception("max files is 100")
            try:
                with open(f"Results/{name}({i}).json", "x") as f:
                    json.dump(dic, f, sort_keys=False)
                break
            except FileExistsError:
                i += 1
                continue

    if TXT:
        with open("Results/new1.txt", "w") as f:
            for value in sorted(dic.values()):  # print dict
                # get_key changes the vals of dic to none
                key = get_key(dic, value)
                f.write(f"{key} {value}\n")


categories = {
    "gas_stations": {'CASTLE ROCK CITG FRIEN - NA', 'BP 6XX5928J R E JANES - NA', 'BP 9XX8732CROSS SUN P - NA', 'LAKE GENEVA EXP LAKE - NA', 'CENEX', 'SHELL', 'BP 6XX5236ARROW MUKWO - NA', "LOVE'S", 'ND GAS LLC BELOI - NA', "BUCKY'S CONVENIENCE STORES", '7-ELEVEN', 'BP 1XX8096LIBER PORTA - NA', 'PILOT FLYING J', 'KWIK TRIP', 'HANDI MART INC LAKE - NA', 'MARATHON PETROLEUM', 'BP 8XX4218MILLP MADIS - NA', 'HOLIDAY STATIONSTORES', "CASEY'S GENERAL STORES", 'BP 6XX3693METROPOLIQPS METRO - NA', 'MOBIL', 'MBL ON MAIN DEERF - NA', 'EXXONMOBIL', 'THORNTONS', 'BP 6XX7943LYNDO LYNDO - NA', 'AMOCO', 'BP 8XX1960BLUEMKES QPS ROSEN - NA', 'BP 3XX3639LOEDE DEERF - NA', 'SPEEDWAY', 'BP 6XX3898I 90 COTTA - NA', 'CITGO'},
    "food": {"FESTIVAL FOODS", "DOMINO'S PIZZA", 'RODESIDE GRILL WINDS - NA', 'SUBWAY', 'RUSTIC ROADHAUS MANIT - NA', 'PANDA EXPRESS', 'ANDYS ON RYAN RD FRANK - NA', 'IHOP', 'OUTBACK STEAKHOUSE', 'THE JOINT EAST TOWNE MADIS - NA', 'HOOTERS'},
    "car_parts": {'WALMART', 'EBAY', 'NORTH CENTRAL UTILITY', 'EBAYCOMMERCE SAN J - NA', 'AUTO VALUE WAUNAKEE WAUNA - NA', 'MORRISON S AUTO            60888 - NA', 'AUTOZONE', 'ADVANCED WINDOW CORP CHICA - NA', 'MAGIC WASH', "O'REILLY AUTO PARTS", 'MORRISON S AUTO XX88 - NA', 'MORRISON S AUTO XX 8 - NA', 'AUTOMART NATIONWIDE', 'AMAZON', 'KALSCHEUR IMPLEMENT C CROSS - NA', 'ZIMBRICK EUROPEAN MADIS - NA'},
    "personals": {"BEST LOCKERS", "MARCUS PALACE CINE CON SUN P - NA", "MARCUS PALACE CINE BOX SUN P - NA", 'SIX FLAGS GREAT ADVENTURE', 'SIX FLAGS GREAT AMERICA', 'SIX FLAGS WHITE WATER', "APPLE", "IN ARELLANO AND PHEBU XX 8 - NA", "TRANSFER FROM EBAY", "FOUR LAKES DRIVER TRAI XX 2 - NA", "GREAT CLIPS", "RBT OUTBACK 4815           EASYS - NA", "ROBINHOOD", "THE BARBERSHOP"},
    "supplies": {'MNRD JANESVILLE JANE - NA', 'MNRD SUNPRAIRIE SUN - NA', 'MNRD WAUKESHA WAUK - NA', 'ABC SUPPLY', "ALSIDE SUPPLY 161 NEW B - NA", "ALSIDE SUPPLY 172 FITCH - NA", 'BALES LMB SUPPLY WESTM - NA', 'CLIMATE GUARD MP CHICA - NA', 'HOME LUMBER WHITE - NA', 'MENARDS', 'THE HOME DEPOT', 'TRUE VALUE', 'HARBOR FREIGHT TOOLS', 'FARM FLEET OF MADIS - NA', "ROGAN'S SHOES", 'TOTEM LMB MILLWORK SCHIL - NA'},
    "insurances": {'PAYMENT TO EMC INSURANCE COMPANIES', 'PAYMENT TO ERIE INSURANCE GROUP', 'PAYMENT TO AUTO OWNERS INSURANCE'},
    "utilities": {'PAYMENT TO GFL ENVIRONMENTAL INC.', 'PAYMENT TO NICOR GAS', 'PAYMENT TO SPECTRUM', 'PAYMENT TO VERIZON WIRELESS', 'SUN PRAIRIE WATER'}
}

path = "Transaction html/km windows taxe transactions/"
file = "all1"
file2 = "all2"
extension = ".html"
transactions = get_trans(path + file + extension) + get_trans(path + file2 + extension)
dic = {}

# making dictionary of transactions
for transaction in transactions:
    money_num = get_money_ammount(transaction)
    location = get_location(transaction).upper()
    date = get_date(transaction)
    
    if location not in dic:
        dic[location] = [money_num, date]
    else:
        dic[location] = [dic[location][0] + money_num]

# combine different locations into categories, ex: kwik trip + bp turns into fuel in the dict
for k,v in categories.items(): 
    add_keys(dic, v, k)

# rounding
for k in dic.keys(): 
    try:
        dic[k] = [round(dic[k][0], 2), dic[k][1]]
    except IndexError:
        dic[k] = [round(dic[k][0], 2)]

write_files(dic, JSON=True, name=f"{file.split('.')[0]}_taxes")
