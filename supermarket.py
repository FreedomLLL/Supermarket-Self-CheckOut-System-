"""simulates a supermarket cashier system (also known as POS system). The module allows a self-checkout customer to list the products on stock, add products from the stock to a shopping basket or remove products from it, list all the items in the basket, and produce a bill of the basket (applying two types of promotions)"""import csv # read a csv filefrom prettytable import PrettyTable #print a dictionaryfrom decimal import Decimalimport copy# Task 0def correctForm(dic):    """    convert a dictionary to correct form as described in Task 0    """    for keys,values in dic.items():        values["price"] = float(values["price"])        if values["promotion"] == "None":            values["promotion"] = None                #correct "group" form        if values["group"] == "None":            values["group"] = None        if values["promotion"] == "get4pay3":            values["group"] = int(values["group"])                #correct "amount" form        if values["unit"] == "pieces":            values["amount"] = int(values["amount"])        if values["unit"] == "kg":            values["amount"] = float(values["amount"])    return dic# Task 1def addProduct(Collection,Newkey,Newvalue):    """    add a new dictionary item Newkey:Newvalue to Collection    return new Collection    """    newitem = {Newkey : Newvalue}    Collection.update(newitem)         return Collectiondef isFloat(x):    """    if the type of x is Float, return Ture and false otherwise     """    try:        float(x)        return True    except:        return False    def isInt(x):    """    if the type of x is Int, return Ture and false otherwise     """    try:        int(x)        return True    except:        return Falsedef isCorrupted(l):    """    value type as following        name : string    price : float    unit : either string "pieces" or "kg""    promotion : None or a string get2pay1 or get4pay3    group : either None or integer (the latter only when promotion is get4pay3 )    amount : either integer (in case unit takes the value pieces ) or float(in case unit takes the value kg )        if the values in the sub-dictionaries representing each product have the correct type,    return True and otherwise False    """    if isFloat(l[2]):        if (l[3] == "pieces" and isInt(l[6])) or (l[3] == "kg" and isFloat(l[6])):                if (l[4] == "None" or l[4] == "get2pay1") and l[5] == "None":                    return False                                    if l[4] == "get4pay3" and isInt(l[5]):                    return False    return True def loadStockFromFile(filename="stock.csv"):    """     reads the products from a file and returns the dictionary stock    """        names = ["name","price","unit","promotion","group","amount"]    #store product information    product = {}    stock = {}        #temporarily store each line     temp = ()    #TODO: load the stock items from file    with open(filename,mode = "rt", encoding = "utf8") as f:         for line in f:            temp = line.rstrip('\n').split("|")            #if the line is in incorrect type, ignore it             if isCorrupted(temp):                continue                        #if the format of line is correct, read it              for i in range(len(names)):                #If the key doesn’t exist, it will be added and will point to that value.                 #If the key exists, the current value it points to will be overwritten.                product[names[i]] = temp[i+1]                        #add a new product into stock            addProduct(stock,temp[0],product)            #initialize product             product={}    #convert this dictionary to correct form    correctForm(stock)                return stock# Task 2def listItems(dct):    """    input a dictionary dct      returns a string corresponding to a nicely formatted table.    """        #convert the form of price and amount values to string form     for keys,values in dct.items():        values["price"] = str(values["price"])        values["amount"] = str(values["amount"])    # the following 2 lines follow a similar code on    # http://zetcode.com/python/prettytable/ as retrieved on 4/12/2020    x = PrettyTable()    x.field_names = ["Ident", "Product", "Price", "Amount"]        #add each line into table    for keys,values in dct.items():                #The kg amounts are displayed with one decimal place        if values["unit"] == "kg":            values["amount"] = Decimal(values["amount"]).quantize(Decimal("0.0"))            values["amount"] = str(values["amount"])                #The prices need to be displayed with two decimal places        values["price"] = Decimal(values["price"]).quantize(Decimal("0.00"))        values["price"] = str(values["price"])                x.add_row([keys,values["name"],values["price"]+" "+"£",values["amount"]+" "+values["unit"]])              #The prices and amount are right-aligned    #The Ident and product are left-aligned    x.align["Ident"] = "l"    x.align["Product"] = "l"    x.align["Price"] = "r"    x.align["Amount"] = "r"           #The products are sorted by increasing ident identifier    x.sortby = "Ident"        #convert a dictionary to correct form as described in Task 0    correctForm(dct)        #returns a string corresponding to a nicely formatted table    return x.get_string()# Task 3def stringMatch(fullstring,substring):    """   input a fullstring and a substring   make it all lower case.   if fullstring contains a substring, return True   otherwise False    """    #convert all to lower case    fullstring = fullstring.lower()    substring = substring.lower()        # the following 1 lines follow a similar code on    # https://stackabuse.com/python-check-if-string-contains-substring/ as retrieved on 4/12/2020    if substring in fullstring:        return True    else:        return Falsedef searchStock(stock, s):    """    input a dictionary and a string    returns a dictionary substock of the same form as stock ,     but containing only those products whose name contains the string s as a substring.     The search should be case-insensitive    """    substock={}    for keys,values in stock.items():        #if the name of products contains the string s as a substring        if stringMatch(values["name"],s):                    #add this product into substock                    addProduct(substock,keys,values)                           return substock# Task 4def addToBasket(stock,basket,ident,amount):    """    adds amount units of the product with identifier ident from the stock to the basket.     The function should return a message msg , which can either be None or a string:        msg = None        msg = 'Cannot add this many {unit} to the basket, only added {amount} {unit}.'        msg = 'Cannot remove this many {unit} from the basket,only removed {amount} {unit}.'    """    msg = ""        #used as medium when applying deep copy    temp = {}    #amount > 0 means the product will be taken out from stock and added to the basket    if amount > 0:        for keys,values in stock.items():                        #find the correct ident so that we can match the product             if keys == ident:                                #there are sufficiently many units of the product on stock                if values["amount"] >= amount:                    #modify the amount of this product in stock                     stock[keys]["amount"] = values["amount"] - amount                                        if keys in basket:                        basket[keys]["amount"] = basket[keys]["amount"] + amount                                            else:                        #deep copy this product to temp                        addProduct(temp,keys,values)                        # # the following 1 lines follow a similar code on                        # https://www.runoob.com/w3cnote/python-understanding-dict-copy-shallow-or-deep.html                        #as retrieved on 4/12/2020                        temp = copy.deepcopy(temp)                                                #modify the correct amount of product in basket                         temp[keys]["amount"] = amount                        addProduct(basket,keys,temp[keys])                                            #mark msg  as None                     msg = None                    return msg                                  #there are less units of the product on stock                if values["amount"] < amount:                                        if keys in basket:                        basket[keys]["amount"] = basket[keys]["amount"] + values["amount"]                                        else:                        #deep copy this product to temp                        addProduct(temp,keys,values)                                    temp = copy.deepcopy(temp)                                                                        #this many units will be added to the basket                        temp[keys]["amount"] = stock[keys]["amount"]                        addProduct(basket,keys,temp[keys])                                        msg = "Cannot add this many "+str(amount)+" to the basket, only added "+str(values["amount"])+" "+values["unit"]                    #leaving 0 units of the product on stock                    stock[keys]["amount"] = 0                    return msg                    #amount < 0 means the product will be taken out from basket and added back to the stock    elif amount < 0:        for keys,values in basket.items():            if keys == ident:                                #there are sufficiently many units of the product in the basket                if values["amount"] >= abs(amount):                    #modify the correct amount of product on stock                     stock[keys]["amount"] = stock[keys]["amount"] + abs(amount)                                        #modify the amount of this product in basket                     basket[keys]["amount"] = values["amount"] - abs(amount)                                            #mark msg  as None                     msg = None                    return msg                                 #there are less units of the product in the basket                if values["amount"] < abs(amount):                                        #modify the amount of this product on stock                     stock[keys]["amount"] = values["amount"] + stock[keys]["amount"]                                        #the product will be removed from the basket                    del basket[keys]                                        msg = "Cannot remove this many "+str(amount)+" from the basket, only added "+str(values["amount"])+" "+str(values["unit"])                    return msg# Task 5def prepareCheckout(basket):    """    loops through each item in the basket     and adds a key amountPayable taking the same value as the corresponding amount value    """    for keys,values in basket.items():        values["amountPayable"] = values["amount"]            return None    # Task 6def getBill(basket):    """    input a dictionarty    return a string, which is a nicely formatted bill for the basket    """    priceSum = 0.0        #convert the form of price and amount values to string form     for keys,values in basket.items():        values["price"] = str(values["price"])        values["amount"] = str(values["amount"])        values["amountPayable"] = str(values["amountPayable"])    x = PrettyTable()    #header    x.field_names = ["Product", "Price", "Amount", "Payable"]        #add each line into table    for keys,values in basket.items():                #save Payable        currentPayable = float(values["price"]) * float(values["amountPayable"])        priceSum = priceSum + currentPayable                if values["amount"] != values["amountPayable"]:            promotionPayable = -(float(values["price"]) * float(values["amount"]) - currentPayable)                        currentPayable = float(values["price"]) * float(values["amount"])                        promotionAmount = int(values["amount"]) - int(values["amountPayable"])                                    #The promotionPayable need to be displayed with two decimal places            promotionPayable = Decimal(promotionPayable).quantize(Decimal("0.00"))             promotionPayable = str(promotionPayable)                        promotionAmount = str(promotionAmount)                #The kg amounts are displayed with one decimal place        if values["unit"] == "kg":            values["amount"] = Decimal(values["amount"]).quantize(Decimal("0.0"))            values["amount"] = str(values["amount"])                #The prices need to be displayed with two decimal places        values["price"] = Decimal(values["price"]).quantize(Decimal("0.00"))        values["price"] = str(values["price"])                #The Payable need to be displayed with two decimal places        priceSum = Decimal(priceSum).quantize(Decimal("0.00"))        priceSum = str(priceSum)                #The currentPayable need to be displayed with two decimal places        currentPayable = Decimal(currentPayable).quantize(Decimal("0.00"))         currentPayable = str(currentPayable)                x.add_row([values["name"],values["price"]+" "+"£",values["amount"]+" "+values["unit"],currentPayable+" "+"£"])            if values["amount"] != values["amountPayable"]:            firstColumn ="      "+"Promotion"+" "+values["promotion"]            x.add_row([firstColumn,"-"+values["price"]+" "+"£",promotionAmount+" "+values["unit"],promotionPayable+" "+"£"])            promotionAmount = int(promotionAmount)            promotionPayable = float(promotionPayable)                    #recover to float         currentPayable = float(currentPayable)        priceSum = float(priceSum)            #The priceSum need to be displayed with two decimal places    priceSum = Decimal(priceSum).quantize(Decimal("0.00"))    priceSum = str(priceSum)    #the last line     x.add_row(["TOTAL:"," "," ",priceSum+" "+"£"])        #The payable, prices and amount are right-aligned    #The product are left-aligned    x.align["Product"] = "l"    x.align["Price"] = "r"    x.align["Amount"] = "r"    x.align["Payable"] = "r"           #convert a dictionary to correct form as described in Task 0    correctForm(basket)        #returns a string corresponding to a nicely formatted table    return x.get_string()# Task 8def applyPromotions(basket):        #save the amount of free product for 4 promotion groups    promotionCount=[0,0,0,0]    #save the promotion product for each group     tempDict = [{},{},{},{}]        for keys,values in basket.items():        if values["promotion"] == "get2pay1":            #modify amountPayable for get2pay1            values["amountPayable"] = values["amount"]//2 + values["amount"]%2        elif values["promotion"] == "get4pay3":            for i in range(4):                if values["group"] == i+1:                                        #save the total number of promotion product for each group for get4pay3                     promotionCount[i] += values["amount"]                    #save the promotion product for each group for get4pay3                    addProduct(tempDict[i], keys, values)    #calculate the amount of free product for each group    for i in range(4):        promotionCount[i] = promotionCount[i]//4        min = 99999    for i in range(4):        #find the cheapest product        for keys,values in tempDict[i].items():            if values["price"] < min:                min = values["price"]                #modify amountPayable for get4pay3        for keys,values in tempDict[i].items():            if values["price"] == min:                values["amountPayable"] = values["amountPayable"] - promotionCount[i]    # Task 7def main():    """     mimic a self-checkout system which allows the customer to list the products on stock,    add (remove) products from the stock to their shopping basket,     list the items in the basket, and display a bill for the basket    """    stock = loadStockFromFile('stock.csv')    basket = {}    substock = {}            print("*"*75)    print("*"*15+" "*10+"WELCOME TO STEFAN EXPRESS"+" "*10+"*"*15)    print("*"*75,"\n")        while True:        s = input("Input product-Ident, search string, 0 to display basket, 1 to check out: ")                if s == "0":            if basket == {}:                print("Your current shopping basket is empty!")            else:                print("Your current shopping basket: ")                print(listItems(basket))                        elif s == "1":            prepareCheckout(basket)            applyPromotions(basket)            print()            print("Here is your shopping bill: ")            print()            print(getBill(basket))            print()            print("***** THANK YOU FOR SHOPPING AT STEFAN EXPRESS! ******")            break                elif s in stock:            nr = input("How many units ("+stock[s]["unit"]+") do you want to add to your basket? ")            while stock[s]["unit"] == "kg" and not isFloat(nr):                nr = input("Please input a corrected number: ")                                    while stock[s]["unit"] == "pieces" and not isInt(nr):                nr = input("Please input a corrected number: ")                                if stock[s]["unit"] == "pieces":                nr = int(nr)                                        if stock[s]["unit"] == "kg":                nr = float(nr)                msg = addToBasket(stock, basket,s, nr)            if msg != None:                print(msg)                        else:                        for keys,values in stock.items():                substock = searchStock(stock, s)                     print("There were "+str(len(substock))+" search results for "+"'"+s+"'")            print(listItems(substock))if __name__ == '__main__':    main()  