from Product import Product

def helper():
    print("I comandi disponibili sono i seguenti\n")
    print("aggiungi: aggiungi un prodotto al magazzino")
    print("elenca: elenca i prodotto in magazzino")
    print("vendita: registra una vendita effettuata")
    print("profitti: mostra i profitti totali")
    print("aiuto: mostra i possibili comandi")
    print("chiudi: esci dal programma")
    print("\n")

prod_dict = {"product_name": 0, "amount": 0, "purchase_price": 0.0, "sale_price": 0.0}

prod = Product(prod_dict)

cmd = None

while (cmd != "chiudi"):
    
    cmd = input("Inserisci un comando: ")

    if cmd == "vendita":
        prod.sale_products()
    elif cmd == "profitti":
        prod.gain_products()
    elif cmd == "aggiungi":       
        prod.add_products()
    elif cmd == "elenca":       
        prod.list_products()
    elif cmd == "aiuto":       
        helper()
    elif cmd == "chiudi":       
        print("Bye bye")
    else:
        print("Comando non valido")
        helper()