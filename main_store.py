from Product import Product

def printOperations():
    print("Operazioni consentite (digita numero per eseguire operazione):")
    print("(1) Aggiungi un prodotto al magazzino")
    print("(2) Elenca i prodotto in magazzino")
    print("(3) Registra una vendita effettuata")
    print("(4) Mostra i profitti totali")
    print("(0) Esci dal programma")

prod_dict = {"nome_prodotto": 0, "quantita": 0, "prezzo_acquisto": 0.0, "prezzo_vendita": 0.0}
prod = Product(prod_dict)

cmd = None

while (cmd != 0):
    
    printOperations()
    cmd = int(input("Inserisci numero operazione: "))

    if cmd == 1:       
        prod.aggiungi()
    elif cmd == 2:       
        prod.elenca()
    elif cmd == 3:       
        prod.vendita()
    elif cmd == 4:       
        prod.profitto()
    elif cmd == 0:
        print("BYE BYE")
    else:
        print("Valore inserito non valido. Inserisci valore corretto")

        