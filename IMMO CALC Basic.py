#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ImmoCalc Tool

"""

import os
import plotly

if __name__ == "__main__":
    print("Wilkommen im Immobilienkalkulationstool.")
    #preis
    preis = float(input("Geben Sie zuerst den Preis der Immobilie ein:"))
    #Kreditzins
    zins = float(input("Geben Sie nun den Kreditzins ein (in Dezimal):"))
    #miete
    miete = float(input("Welche monatlichen Mieteinnahmen können erwartet werden?"))
    #anzahlung
    anzahlung = float(input("Anzahlung:"))
    #eigenanteil
    eigenanteil = float(input("Mit wie viel Geld werden Sie neben der Miete monatlich verwenden, um den Kredit abzubezahlen?"))
    #Jahresmiete
    miete_jahr = miete * 12
    #Kredit
    kredit_uebrig = preis-anzahlung
    #Tilgung pro Jahr
    tilgung = miete_jahr + eigenanteil*12
    #Gesamtkosten
    kosten_ges = preis #TODO
    
    #plotted -10% / -5% / 0% / 2% / 5% / 10%
    gewinn = 0 #d.h. Geld
    vermoegen_bei_immobilie_stabil = preis - kredit_uebrig
    kredithoehe = kredit_uebrig
    
    
    plot_years = int(input("Über wie viele Jahre möchten sie die Entwicklung berechnen?"))
    
    for i in range(1, plot_years):
        if kredit_uebrig > tilgung: #Es ist mehr als eine Tilgung notwendig.
            kredit_uebrig -= tilgung 
            temp = kredit_uebrig
            kredit_uebrig *= (1+zins)
            temp = kredit_uebrig - temp
            kosten_ges += temp
            
            #append
            kredithoehe.append(kredit_uebrig)
            gewinn.append(0)
        elif kredit_uebrig > 0:
            kosten_ges += kredit_uebrig
            gewinn.append(tilgung - kredit_uebrig)
            
            kredit_uebrig = 0
            kredithoehe.append(0)
            
        elif kredit_uebrig<0: #ERROR NEGATIVER KREDIT
            print("Error: negativer Kreditwert")
        
        else:
            gewinn.append(gewinn[i-1]+miete_jahr)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        