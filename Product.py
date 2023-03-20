import csv
import json

class Product:

    PATH = "db/"
    DATABASE = "database.csv"
    SALES = "sales.csv"

    """
    Classe che registra un nuovo prodotto
    """

    def __init__(self, prod):  
        
        """
        Costruttore classe Prodotto
        
        prod (dict): informazioni del prodotto
        """

        self._prod = prod

    def aggiungi(self):

        """
        Inserisci nuovo prodotto in magazzino oppure aggiorna quantita
        """

        try:
            flg_new = 1
            listProducts = list()
            quantita = 0
            nome_prodotto = input("Nome del prodotto ")
            assert(type(nome_prodotto) == str), "Non è stata inserita una stringa"
            
            if self.isVeganFood(nome_prodotto) == 0:
                return print(f"{nome_prodotto}?!?! Questo è un negozio vegano. Prova a cercare su internet il significato di negozio vegano\n")

            with open(self.PATH+self.DATABASE, encoding="utf-8") as products_csv:
    
                # quando si utilizza l'oggetto DictReader la riga header viene scartata
                products = csv.DictReader(products_csv, delimiter=";")

                for product in products:
                    if nome_prodotto.lower().__eq__(product["nome_prodotto"].lower()):
                        flg_new = 0
                        scelta = int(input("Prodotto già presente nel database. Se vuoi aggiornare solo il quantitativo digita 1. In caso vuoi aggiornare anche prezzo di acquisto e di vendita digita 2: "))
                        while scelta != 1 and scelta != 2:
                            scelta = int(input("Input non valido. Se vuoi aggiornare solo il quantitativo digita 1. In caso vuoi aggiornare anche prezzo di acquisto e di vendita digita 2: "))

                        if scelta == 1:
                            quantita = int(input("Quantità "))
                            if  quantita == 0:
                                return print("Nessun quantitativo inserito\n")

                            self._prod["nome_prodotto"] = nome_prodotto
                            self._prod["quantita"] = int(product["quantita"]) + quantita
                            self._prod["prezzo_acquisto"] = product["prezzo_acquisto"]
                            self._prod["prezzo_vendita"] = product["prezzo_vendita"]

                        if scelta == 2:
                            quantita = int(input("Quantità "))
                            if  quantita == 0:
                                return print("Nessun quantitativo inserito\n")

                            self._prod["nome_prodotto"] = nome_prodotto
                            self._prod["quantita"] = quantita
                            self._prod["prezzo_acquisto"] = round(float(input("Prezzo di acquisto ")), 2)
                            self._prod["prezzo_vendita"] = round(float(input("Prezzo di vendita ")), 2)

                        listProducts.append(self._prod.copy())
                    else:
                        self._prod["nome_prodotto"] = product["nome_prodotto"]
                        self._prod["quantita"] = product["quantita"]
                        self._prod["prezzo_acquisto"] = product["prezzo_acquisto"]
                        self._prod["prezzo_vendita"] = product["prezzo_vendita"]

                        listProducts.append(self._prod.copy())

            if flg_new:
                quantita = int(input("Quantità "))
                if  quantita == 0:
                    return print("Nessun quantitativo inserito")

                self._prod["nome_prodotto"] = nome_prodotto
                self._prod["quantita"] = quantita
                self._prod["prezzo_acquisto"] = round(float(input("Prezzo di acquisto ")), 2)
                self._prod["prezzo_vendita"] = round(float(input("Prezzo di vendita ")), 2)

                while self._prod["prezzo_vendita"] <= self._prod["prezzo_acquisto"]:
                    print("Dovremmo provare a guadagnare qualcosa. Non possiamo vivere per la gloria")
                    print("Inserisci prezzo di vendita superiore al prezzo di acquisto")
                    self._prod["prezzo_vendita"] = round(float(input("Prezzo di vendita ")), 2)

                listProducts.append(self._prod.copy())

            self.insertDBValue(self.DATABASE, ["nome_prodotto", "quantita", "prezzo_acquisto", "prezzo_vendita"], listProducts)

            return print(f"AGGIUNTO {quantita} X di {nome_prodotto}\n")

        except AssertionError as e:
            print(e)
        except ValueError as ve:
            print(ve)


    def elenca(self):
        
        """
        Elenca i prodotti in magazzino
        """
        print("PRODOTTO - QUANTITA' - PREZZO")
        with open(self.PATH+self.DATABASE, encoding="utf-8") as products_csv:
            products = csv.DictReader(products_csv, delimiter=";")
            for product in products:
                print(f"{product['nome_prodotto']} - {product['quantita']} - {product['prezzo_vendita']}")
        
        return None

    def vendita(self):
        
        """
        Registra una vendita
        """
        list_sales = list()
        with open(self.PATH+self.SALES, encoding="utf-8") as sales_csv:
            sales = csv.DictReader(sales_csv, delimiter=";")
            for sale in sales:
                list_sales.append(sale.copy())

        list_sale_act = list()

        cmd = None
        while cmd != "" and cmd != "N" and cmd != "n":
            flg_sale = 0
            flg_prod = 0
            max_qty = 0
            prezzo_vendita = 0.0
            prezzo_acquisto = 0.0
            with open(self.PATH+self.DATABASE, encoding="utf-8") as products_csv:
                products = csv.DictReader(products_csv, delimiter=";")                
                prod = input("Nome del prodotto ")
                for product in products:
                    if prod.lower().__eq__(product["nome_prodotto"].lower()):
                        flg_prod = 1
                        max_qty = int(product["quantita"])
                        prezzo_vendita = round(float(product['prezzo_vendita']), 2)
                        prezzo_acquisto = round(float(product['prezzo_acquisto']), 2)
            if flg_prod:
                qty = int(input("Quantita "))
                while qty > max_qty:
                    print("Quantità non disponibile in magazzino. Reinserire valore")
                    qty = int(input("Quantita "))

                if qty == 0:
                    print("Vendita non effettuata\n")
                else:
                    flg_sale = 1
                    lordo = round(qty * prezzo_vendita, 2)
                    netto = round(qty * (prezzo_vendita - prezzo_acquisto), 2)
                    dict_sale = {"nome_prodotto": prod, "quantita": qty, "lordo": lordo, "netto": netto}                   
                    list_sales.append(dict_sale.copy())
                    dict_sale_act = {"nome_prodotto": prod, "quantita": qty, "vendita": lordo, "prezzo_vendita": prezzo_vendita}
                    list_sale_act.append(dict_sale_act.copy())
                    fieldnames = ["nome_prodotto", "quantita", "lordo", "netto"]
                    self.insertDBValue(self.SALES, fieldnames, list_sales)                        
            else:
                print("Prodotto non persente in magazzino\n")
                
            cmd = input("Aggiungere un altro prodotto (s/N)? ")
        
        totale = 0
        if flg_sale:
            print("VENDITA REGISTRATA")
            for sale in list_sale_act:
                print(f"{sale['quantita']} X {sale['nome_prodotto']}: € {sale['prezzo_vendita']}")
                totale += round(float(sale['vendita']), 2)
            print(f"Totale: € {totale}\n")

    def profitto(self):
        """
        Mostra i profitti lordo/netto dell'azienda
        """
        lordo = 0.0
        netto = 0.0
        print("PROFITTO")
        with open(self.PATH+self.SALES, encoding="utf-8") as sales_csv:
            sales = csv.DictReader(sales_csv, delimiter=";")
            for sale in sales:
                lordo += round(float(sale['lordo']), 2)
                netto += round(float(sale['netto']), 2)
        return print(f"LORDO: {lordo}\nNETTO: {netto}\n")

    def isVeganFood(self, nomeProdotto):
        """
        Verifica se il prodotto inserito è vegano oppure no
        """
        with open("resources/noveganfood.txt") as novegans:
            for novegan in novegans.readlines():
                if nomeProdotto.lower().__eq__(novegan[:-1]):
                    return 0
            
        return 1

    def insertDBValue(self, file_name, field_names, dict_data):
        """
        Metodo che inserisce i prodotti in un file csv

        file_name: nome del file in cui effettuare la scrittura
        field_names: nomi dei campi dell'header del file
        dict_data: valori da inserire nel file
        """
        with open(self.PATH+file_name, "w", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, delimiter=";", fieldnames=field_names)
            writer.writeheader()
            writer.writerows(dict_data)
    
