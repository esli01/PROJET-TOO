import tkinter as tk
from tkinter import messagebox
import random
import os

SCORES_FILE = "scores.txt"

class Morpion:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Jeu du Morpion")
        
        self.grille = [[" "]*3 for _ in range(3)]
        self.joueur = "X"
        self.ia_active = False
        
        self.boutons = [[tk.Button(self.fenetre, text=" ", font=('Arial', 20), width=5, height=2,
                                   command=lambda x=i, y=j: self.jouer(x, y))
                          for j in range(3)] for i in range(3)]
        
        for i in range(3):
            for j in range(3):
                self.boutons[i][j].grid(row=i, column=j)
        
        self.label = tk.Label(self.fenetre, text="Tour du joueur: X", font=('Arial', 14))
        self.label.grid(row=3, column=0, columnspan=3)
        
        self.bouton_rejouer = tk.Button(self.fenetre, text="Rejouer", command=self.reinitialiser)
        self.bouton_rejouer.grid(row=4, column=0, columnspan=3)
        
        self.bouton_ia = tk.Button(self.fenetre, text="Jouer contre l'IA", command=self.activer_ia)
        self.bouton_ia.grid(row=5, column=0, columnspan=3)
        
        self.fenetre.mainloop()
    
    def jouer(self, x, y):
        if self.grille[x][y] == " ":
            self.grille[x][y] = self.joueur
            self.boutons[x][y].config(text=self.joueur)
            
            if self.verifier_victoire(self.joueur):
                messagebox.showinfo("Victoire", f"Le joueur {self.joueur} a gagné !")
                self.sauvegarder_score(self.joueur)
                self.reinitialiser()
                return
            
            if self.grille_pleine():
                messagebox.showinfo("Match nul", "La partie se termine sur un match nul !")
                self.reinitialiser()
                return
            
            self.joueur = "O" if self.joueur == "X" else "X"
            self.label.config(text=f"Tour du joueur: {self.joueur}")
            
            if self.ia_active and self.joueur == "O":
                self.jouer_ia()
    
    def jouer_ia(self):
        cases_vides = [(i, j) for i in range(3) for j in range(3) if self.grille[i][j] == " "]
        if cases_vides:
            x, y = random.choice(cases_vides)
            self.jouer(x, y)
    
    def verifier_victoire(self, symbole):
        for ligne in self.grille:
            if all(cell == symbole for cell in ligne):
                return True
        
        for col in range(3):
            if all(self.grille[row][col] == symbole for row in range(3)):
                return True
        
        if all(self.grille[i][i] == symbole for i in range(3)) or all(self.grille[i][2-i] == symbole for i in range(3)):
            return True
        
        return False
    
    def grille_pleine(self):
        return all(cell != " " for row in self.grille for cell in row)
    
    def reinitialiser(self):
        self.grille = [[" "]*3 for _ in range(3)]
        self.joueur = "X"
        self.label.config(text="Tour du joueur: X")
        for i in range(3):
            for j in range(3):
                self.boutons[i][j].config(text=" ")
    
    def activer_ia(self):
        self.ia_active = not self.ia_active
        if self.ia_active:
            self.bouton_ia.config(text="Désactiver l'IA")
        else:
            self.bouton_ia.config(text="Jouer contre l'IA")
    
    def sauvegarder_score(self, gagnant):
        scores = self.charger_scores()
        scores[gagnant] = scores.get(gagnant, 0) + 1
        
        with open(SCORES_FILE, "w") as f:
            for joueur, score in scores.items():
                f.write(f"{joueur}:{score}\n")
    
    def charger_scores(self):
        scores = {}
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, "r") as f:
                for ligne in f:
                    joueur, score = ligne.strip().split(":")
                    scores[joueur] = int(score)
        return scores

if __name__ == "__main__":
    Morpion()
