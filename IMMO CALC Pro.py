#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
ImmoCalc Tool Pro
"""
import os
import plotly.express as px
import pandas as pd

if __name__ == "__main__":
    print("Wilkommen im Immobilienkalkulationstool. Dies ist die Pro Version.")
    print("Wenn Sie ihre Eingaben nicht kennen, bitte Basic Version benutzen.")
    inp = input("Alle Eingaben nur mit einem Leerzeichen trennen.")
    inp = inp.split(" ")
    #string to float??
    for i, val in enumerate(inp):
        inp[i] = float(val)
    #preis
    preis = inp[0]
    #Kreditzins
    zins = inp[1]
    #miete
    miete = inp[2]
    #anzahlung
    anzahlung = inp[3]
    #eigenanteil
    eigenanteil = inp[4]
    #Jahresmiete
    miete_jahr = miete * 12
    #Kredit
    kredit_uebrig = preis-anzahlung
    #Tilgung pro Jahr
    tilgung = miete_jahr + eigenanteil*12
    #Gesamtkosten
    kosten_ges = preis #TODO
    
    #plotted -5% / 0% / 2% / 5% / 10%
    gewinn = [0] #d.h. Geld
    v0 = preis - kredit_uebrig #Vermögen bei Immobilienkauf
    preis_immo = [preis, preis, preis, preis, preis]
    vermoegen_bei_x = [[v0], [v0], [v0], [v0], [v0]]
    preisentwicklung_str = ["-5%", "0", "+2%", "+5%", "+10%"]
    preisentwicklung_fl = [0.95, 1, 1.02, 1.05, 1.1]
    kredithoehe = [kredit_uebrig]
    
    
    jahre_plot = int(input("Über wie viele Jahre möchten sie die Entwicklung berechnen?"))
    for i in range(1, jahre_plot):
        if kredit_uebrig > tilgung:
            kredit_uebrig -= tilgung
            temp = kredit_uebrig
            kredit_uebrig *= (1+zins)
            temp = kredit_uebrig - temp
            kosten_ges += temp
            
            #append
            kredithoehe.append(kredit_uebrig)
            gewinn.append(0)
            for x in range(0, len(vermoegen_bei_x)):#iterieren über preisentwicklung
                temp2 = preis_immo[x]
                preis_immo[x] *= preisentwicklung_fl[x]
                before = vermoegen_bei_x[x][i-1]
                before  += preis_immo[x]-temp2
                before += tilgung
                vermoegen_bei_x[x].append(before)
                
        elif kredit_uebrig > 0:
            kosten_ges += kredit_uebrig
            gewinn.append(tilgung - kredit_uebrig)
            for x in range(0, len(vermoegen_bei_x)):#iterieren über preisentwicklung
                temp2 = preis_immo[x]
                preis_immo[x] *= preisentwicklung_fl[x]
                before = vermoegen_bei_x[x][i-1]
                before  += preis_immo[x]-temp2
                before += tilgung
                vermoegen_bei_x[x].append(before)
            
            kredit_uebrig = 0
            kredithoehe.append(0)
            
        elif kredit_uebrig<0: #ERROR NEGATIVER KREDIT
            print("Error: negativer Kreditwert")
        
        else: #KREDIT-FREI
            gewinn.append(gewinn[i-1]+miete_jahr)
            kredithoehe.append(0)
            for x in range(0, len(vermoegen_bei_x)):#iterieren über preisentwicklung
                temp2 = preis_immo[x]
                preis_immo[x] *= preisentwicklung_fl[x]
                before = vermoegen_bei_x[x][i-1]
                before  += preis_immo[x]-temp2
                before += tilgung
                vermoegen_bei_x[x].append(before)
                

##########
#DEBUG INPUT DATA
##########
    #print("gewinn")
    #print(gewinn)
    #print("kredit_uebrig")
    #print(kredit_uebrig)
    #print("kredithoehe")
    #print(kredithoehe)
    #print("vermoegen_bei_x")
    #print(vermoegen_bei_x)
   # print(preis_immo[0])
   
   
   
##########   
#CREATE DATA FRAMES
##########
    years_arr = []
    for y in range(jahre_plot):
        years_arr.append(y)
    df_gewinn = pd.DataFrame(dict(year = years_arr, profit = gewinn))
    df_kredithoehe = pd.DataFrame(dict(a=years_arr, b = kredithoehe))
   
   
   
   
##########
#PLOT
##########
    
    fig_gewinn = px.line(df_gewinn, x="year", y="profit", title='Profits from the immo:')
    fig_gewinn.write_html("/Users/a2/Desktop/gewinn.html")
    fig_kredithoehe = px.line(df_kredithoehe, x="year", y="kredithoehe", title="Kredithöhe")
    fig_kredithoehe.write_html("/Users/a2/Desktop/kredit.html")
    urls=["file://Users/a2/Desktop/gewinn.html", "file://Users/a2/Desktop/kredit.html"]
    for url in urls:
        os.system(f"start {url}")



#DEBUG INOUT CONTROL PLOTLY