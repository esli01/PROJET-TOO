import random

class Utilisateur:
    def __init__(self, nom, adresse, telephone, cnic, identifiant, mot_de_passe):
        self.nom = nom
        self.adresse = adresse
        self.telephone = telephone
        self.cnic = cnic
        self.identifiant = identifiant
        self.mot_de_passe = mot_de_passe

class ClientUtilisateur(Utilisateur):
    def __init__(self, nom, adresse, telephone, cnic, identifiant, mot_de_passe, limite_retrait):
        super().__init__(nom, adresse, telephone, cnic, identifiant, mot_de_passe)
        self.numero_carte = str(random.randint(1000000000000000, 9999999999999999))
        self.code_PIN = random.randint(1000, 9999)
        self.solde = 0
        self.limite_retrait = limite_retrait
        self.erreurs_PIN = 0
        self.bloqué = False

    def authentifier(self, identifiant, mot_de_passe):
        return self.identifiant == identifiant and self.mot_de_passe == mot_de_passe

    def déposerArgent(self, montant):
        self.solde += montant
        self.enregistrer_transaction("Dépôt", montant)
        print(f"Dépôt de {montant} FCFA effectué. Nouveau solde : {self.solde} FCFA.")

    def retirerArgent(self, montant, pin):
        if self.bloqué:
            print("Compte bloqué en raison de tentatives frauduleuses.")
            return
        
        if pin != self.code_PIN:
            self.erreurs_PIN += 1
            if self.erreurs_PIN >= 3:
                self.bloqué = True
                print("Compte bloqué après 3 erreurs de PIN.")
            else:
                print(f"PIN incorrect. Tentative restante : {3 - self.erreurs_PIN}")
            return
        
        if montant > self.solde:
            print("Solde insuffisant.")
        elif montant > self.limite_retrait:
            print(f"Échec : Vous ne pouvez pas retirer plus de {self.limite_retrait} FCFA/jour.")
        else:
            self.solde -= montant
            self.enregistrer_transaction("Retrait", montant)
            print(f"Retrait de {montant} FCFA effectué. Solde restant : {self.solde} FCFA.")

    def enregistrer_transaction(self, type_transaction, montant, destinataire_id=None):
        with open("transactions.txt", "a") as file:
            if destinataire_id:
                file.write(f"{self.identifiant}, {montant}, {type_transaction}, {destinataire_id}\n")
            else:
                file.write(f"{self.identifiant}, {montant}, {type_transaction}\n")

    def afficher_historique_transactions(self):
        print("\n📜 Historique des transactions :")
        try:
            with open("transactions.txt", "r") as file:
                transactions = file.readlines()
                for transaction in transactions:
                    if self.identifiant in transaction:
                        print(transaction.strip())
        except FileNotFoundError:
            print("Aucune transaction enregistrée.")

# Création d'un client utilisateur
client1 = ClientUtilisateur("Aryel", "Cocody, Abidjan", "0123456789", "35202183648363", "aryel123", "pass456", 500000)
print(f"Carte générée : {client1.numero_carte}, PIN : {client1.code_PIN}")

client1.déposerArgent(500000)
client1.retirerArgent(200000, 2846)  # PIN incorrect ➝ Tentative échouée
client1.retirerArgent(200000, client1.code_PIN)  # Succès

client1.afficher_historique_transactions()

