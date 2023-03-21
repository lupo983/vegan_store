import csv
import json

class Product:

    PATH_DB = "db/"
    PATH_RESOURCES = "resources/"
    DATABASE = "database.csv"
    SALES = "sales.csv"
    NOVEGANFOOD = "noveganfood.txt"

    """
    Class that handles vegan warehouse
    """

    def __init__(self, prod):  
        
        """
        Constructor about Product class
        
        prod (dict): parameter about prod information
        """

        self._prod = prod

    def add_products(self):

        """
        Insert or update a new product in the warehouse 
        """

        try:
            '''check if product is new or not: 1 new 0 otherwise'''
            flg_new = 1
            listProducts = list()
            amount = 0
            product_name = input("Nome del prodotto: ")
            assert(type(product_name) == str), "This is not a str value"
            
            if self.is_vegan_food(product_name) == 0:
                return print(f"{product_name}?!?! Questo è un negozio vegano. Prova a cercare su internet il significato di negozio vegano\n")

            with open(self.PATH_DB+self.DATABASE, encoding="utf-8") as products_csv:
    
                ''' DictReader object skip row header '''
                products = csv.DictReader(products_csv, delimiter=";")

                for product in products:
                    if product_name.lower().__eq__(product["product_name"].lower()):
                        flg_new = 0
                        option = int(input("Prodotto già presente nel database. Se vuoi aggiornare solo il quantitativo digita 1. In caso vuoi aggiornare anche Prezzo di acquisto: e di vendita digita 2: "))
                        while option != 1 and option != 2:
                            option = int(input("Input non valido. Se vuoi aggiornare solo il quantitativo digita 1. In caso vuoi aggiornare anche Prezzo di acquisto: e di vendita digita 2: "))

                        if option == 1:
                            amount = int(input("Quantità: "))
                            assert(type(amount) == int), "This is not an int value"
                            while amount < 0:
                                print("Valore negativo non consentito. Inserire valore maggiore o uguale a 0")
                                amount = int(input("Quantità: "))
                                assert(type(amount) == int), "This is not an int value"
                                if  amount == 0:
                                    return print("Nessun quantitativo inserito\n")

                            self._prod["product_name"] = product_name
                            self._prod["amount"] = int(product["amount"]) + amount
                            self._prod["purchase_price"] = product["purchase_price"]
                            self._prod["sale_price"] = product["sale_price"]

                        if option == 2:
                            amount = int(input("Quantità: "))
                            assert(type(amount) == int), "This is not an int value"
                            while amount < 0:
                                print("Valore negativo non consentito. Inserire valore maggiore o uguale a 0")
                                amount = int(input("Quantità: "))
                                assert(type(amount) == int), "This is not an int value"
                                if  amount == 0:
                                    return print("Nessun quantitativo inserito\n")

                            self._prod["product_name"] = product_name
                            self._prod["amount"] = amount
                            self._prod["purchase_price"] = round(float(input("Prezzo di acquisto: ")), 2)
                            self._prod["sale_price"] = round(float(input("Prezzo di vendita: ")), 2)

                        listProducts.append(self._prod.copy())
                    else:
                        self._prod["product_name"] = product["product_name"]
                        self._prod["amount"] = product["amount"]
                        self._prod["purchase_price"] = product["purchase_price"]
                        self._prod["sale_price"] = product["sale_price"]

                        listProducts.append(self._prod.copy())

            if flg_new:
                amount = int(input("Quantità: "))
                assert(type(amount) == int), "This is not an int value"
                while amount < 0:
                    print("Valore negativo non consentito. Inserire valore maggiore o uguale a 0")
                    amount = int(input("Quantità: "))
                    assert(type(amount) == int), "This is not an int value"
                    if  amount == 0:
                        return print("Nessun quantitativo inserito\n")

                purchase_price = round(float(input("Prezzo di acquisto: ")), 2)
                while purchase_price <= 0:
                    print("Valore inserito non valido. Inserire valore maggiore di 0")
                    purchase_price = round(float(input("Prezzo di acquisto: ")), 2)

                sale_price = round(float(input("Prezzo di vendita: ")), 2)
                while purchase_price <= 0:
                    print("Valore inserito non valido. Inserire valore maggiore di 0")
                    purchase_price = round(float(input("Prezzo di acquisto: ")), 2)                    
                
                self._prod["product_name"] = product_name
                self._prod["amount"] = amount
                self._prod["purchase_price"] = purchase_price
                self._prod["sale_price"] = sale_price

                while self._prod["sale_price"] <= self._prod["purchase_price"]:
                    print("Dovremmo provare a guadagnare qualcosa. Non possiamo vivere per la gloria")
                    print("Inserisci Prezzo di vendita: superiore al Prezzo di acquisto:")
                    self._prod["sale_price"] = round(float(input("Prezzo di vendita: ")), 2)

                listProducts.append(self._prod.copy())

            self.insert_db_value(self.DATABASE, ["product_name", "amount", "purchase_price", "sale_price"], listProducts)

            return print(f"AGGIUNTO: {amount} X {product_name}\n")

        except AssertionError as e:
            print(e)
        except ValueError as ve:
            print(ve)


    def list_products(self):
        
        """
        List of products in the warehouse
        """
        print("PRODOTTO QUANTITA' PREZZO")
        with open(self.PATH_DB+self.DATABASE, encoding="utf-8") as products_csv:
            products = csv.DictReader(products_csv, delimiter=";")
            for product in products:
                print(f"{product['product_name']} {product['amount']} €{product['sale_price']}")
        
        return None

    def sale_products(self):
        
        """
        Register products sale
        """
        list_sales = list()
        with open(self.PATH_DB+self.SALES, encoding="utf-8") as sales_csv:
            sales = csv.DictReader(sales_csv, delimiter=";")
            for sale in sales:
                list_sales.append(sale.copy())

        list_sale_act = list()

        cmd = None
        while cmd != "" and cmd != "N" and cmd != "n":
            '''this var handles sale product: 1 register the sale 0 otherwise'''
            flg_sale = 0
            '''check if product is into warehouse: 1 exists 0 otherwise'''
            flg_prod = 0
            max_amount = 0
            sale_price = 0.0
            purchase_price = 0.0
            with open(self.PATH_DB+self.DATABASE, encoding="utf-8") as products_csv:
                products = csv.DictReader(products_csv, delimiter=";")                
                prod = input("Nome del prodotto: ")
                for product in products:
                    if prod.lower().__eq__(product["product_name"].lower()):
                        flg_prod = 1
                        max_amount = int(product["amount"])
                        sale_price = round(float(product['sale_price']), 2)
                        purchase_price = round(float(product['purchase_price']), 2)
            if flg_prod:
                amount = int(input("Quantità: "))
                while amount > max_amount:
                    print("Quantità non disponibile in magazzino. Reinserire valore")
                    amount = int(input("Quantità: "))

                if amount == 0:
                    print("Vendita non effettuata\n")
                else:
                    flg_sale = 1
                    gross = round(amount * sale_price, 2)
                    net = round(amount * (sale_price - purchase_price), 2)
                    dict_sale = {"product_name": prod, "amount": amount, "gross": gross, "net": net}                   
                    list_sales.append(dict_sale.copy())
                    dict_sale_act = {"product_name": prod, "amount": amount, "vendita": gross, "sale_price": sale_price}
                    list_sale_act.append(dict_sale_act.copy())
                    fieldnames = ["product_name", "amount", "gross", "net"]
                    self.insert_db_value(self.SALES, fieldnames, list_sales)                        
            else:
                print("Prodotto non presente in magazzino\n")
                
            cmd = input("Aggiungere un altro prodotto (s/N)? ")
        
        totale = 0
        if flg_sale:
            print("VENDITA REGISTRATA")
            for sale in list_sale_act:
                print(f"{sale['amount']} X {sale['product_name']}: €{sale['sale_price']}")
                totale += round(float(sale['vendita']), 2)
            print(f"Totale: € {totale}\n")

    def gain_products(self):
        """
        Display information about gain
        """
        gross = 0.0
        net = 0.0
        print("PROFITTO")
        with open(self.PATH_DB+self.SALES, encoding="utf-8") as sales_csv:
            sales = csv.DictReader(sales_csv, delimiter=";")
            for sale in sales:
                gross += round(float(sale['gross']), 2)
                net += round(float(sale['net']), 2)
        return print(f"LORDO: €{gross}\nNETTO: €{net}\n")

    def is_vegan_food(self, product_name):
        """
        Check if the product is vegan or not
        """
        with open(self.PATH_RESOURCES+self.NOVEGANFOOD) as novegans:
            for novegan in novegans.readlines():
                if product_name.lower().__eq__(novegan[:-1]):
                    return 0
            
        return 1

    def insert_db_value(self, file_name, field_names, dict_data):
        """
        Method that insert information into csv files

        file_name: insert data into this file
        field_names: header file
        dict_data: values to insert in the file
        """
        with open(self.PATH_DB+file_name, "w", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=field_names)
            writer.writeheader()
            writer.writerows(dict_data)
    
