import os
import re
import requests
import pandas as pd
import datetime as date
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from zipfile import ZipFile
import pandas as pd
from urllib.request import urlopen
import datetime
import ephem
from pridobivanje_podatkov import *


#ANALIZA 1
# ANALIZA ŠTEVILA PROMETNIH NESREČ

def Stevilo_PN(leto):
    '''
    funkcija vrne število prometnih nesreč v podanem letu
    '''
    df = pd.read_csv(leto, sep=';', encoding='windows-1250')
    df = df.drop_duplicates(subset = ['UraPN', 'DatumPN', 'UpravnaEnotaStoritve', 
                                'KlasifikacijaNesrece','GeoKoordinataX', 'GeoKoordinataY', 'StanjePrometa'], ignore_index=True)
    stevilo = df.shape[0] - 1 #odštejemo prvo vrstico
    return stevilo

# print(Stevilo_PN(os.getcwd()+ "/podatki/pn2009.csv"))

def Stevilo_vseh_PN(mapa):
    '''
    poisce stevilo nesrec v vsakem letu. Vrne seznam parov (letnica, st nesreč)
    '''
    st_nesrec = []
    for leto in os.listdir(mapa):
        if not leto.startswith('.'):
            reg = r'[1-9][0-9]*'
            letnica = re.findall(reg,leto)[0]
            st_nesrec.append((int(letnica), Stevilo_PN(mapa + '/' +leto)))
    return sorted(st_nesrec)

def Graf_Stevila_PN(mapa):
    '''
    Narise graf s podatki o številu prometnih nesreč v odvisnosti od leta
    '''
    podatki = Stevilo_vseh_PN(mapa)
    unzipped = list(zip(*podatki))
    x = unzipped[0]
    y = unzipped[1]
    plt.xticks(x)
    plt.xlabel('Leto', fontsize = 12)
    plt.ylabel('Število prometnih nesreč', fontsize = 12)
    font = {'family': 'serif',
        'color':  'red',
        'weight': 'normal',
        'size': 16}
    plt.title('Število prometnih nesreč v obdobju {} - {}'.format(x[0], x[-1]), fontdict=font)

    plt.plot(x, y, marker ='o', markersize=10, color = 'red', markeredgecolor='red')
    plt.show()


# print(Graf_Stevila_PN(os.getcwd() + "/podatki"))


#ANALIZA 2
#ANALIZA NESREČ V ODVISNOSTI OD LETNIH ČASOV
def letni_cas(datum):
    ''' 
        Funkcija datumu pripiše ustrezen letni čas
    '''
    slovar = {}
    prehodni_datum_1 ='{}-03-21'.format(datum[0:4])
    prehodni_datum_2 ='{}-06-21'.format(datum[0:4])
    prehodni_datum_3 ='{}-09-23'.format(datum[0:4])
    prehodni_datum_4 ='{}-12-21'.format(datum[0:4])
    if prehodni_datum_1 <= datum < prehodni_datum_2:
        slovar[datum] = 'POMLAD'
    elif prehodni_datum_2 <= datum < prehodni_datum_3:
        slovar[datum] = 'POLETJE'
    elif prehodni_datum_3 <= datum < prehodni_datum_4:
        slovar[datum] = 'JESEN'
    elif prehodni_datum_4 <= datum or datum < prehodni_datum_1:
        slovar[datum] = 'ZIMA'
    return slovar[datum]
#print(letni_cas('2018-02-21'))

def letni_cas_nesrece_graf(leto):
    '''
    Funkcija vrne število nesreč v odvisnosti od letnih časov
    '''
    stari_format='%d.%m.%Y'
    novi_format='%Y-%m-%d'
    df = pd.read_csv(leto, sep=';', encoding='windows-1250')
    df = df.drop_duplicates(subset = ['UraPN', 'DatumPN', 'UpravnaEnotaStoritve', 
                            'KlasifikacijaNesrece','GeoKoordinataX', 'GeoKoordinataY', 'StanjePrometa'], ignore_index=True)
    df = df[['DatumPN']]
    df['DatumPN'] = pd.to_datetime(df['DatumPN'], format=stari_format).dt.strftime(novi_format)
    df['DatumPN'] = df['DatumPN'].map(letni_cas)
    df = df.pivot_table(index='DatumPN', aggfunc='size')
 
    # graf = df.plot.pie(rot = 0, edgecolor = 'black', color='red')
    barve = ['lightblue','lightsteelblue','silver', 'cyan']
    explode = (df == max(df)) * 0.1
    graf = df.plot.pie(autopct='%1.1f%%', colors = barve, shadow = True, explode = explode)
    plt.ylabel('')
    graf.set_title('ŠTEVILO PROMETNIH NESREČ V POSAMEZNIH LETNIH ČASIH') 
    plt.show()
    return df

# print(letni_cas_nesrece_graf(os.getcwd()+ "/podatki/pn2014.csv"))


#ANALIZA 3
#STEVILO SMRTNIH ŽRTEV
def StSmrtnihZrtev(leto):
    '''
    funkcija vrne stevilo smrtnih zrtev v podanem letu
    '''
    df = pd.read_csv(leto, sep=';', encoding='windows-1250')
    poskodbe = df['PoskodbaUdelezenca']
    st = poskodbe.loc[df['PoskodbaUdelezenca']=="SMRT"].count()
    return st

def SmrtneZrtve_VsaLeta(mapa):
    '''
    poisce stevilo smrtnih nesrec v vsakem letu. Vrne seznam parov (letnica, st smrti)
    '''
    st_smrti = []
    for leto in os.listdir(mapa):
        if not leto.startswith('.'):
            reg = r'[1-9][0-9]*'
            letnica = re.findall(reg,leto)[0]
            st_smrti.append((int(letnica), StSmrtnihZrtev(mapa + '/' +leto)))
    return sorted(st_smrti)

def GrafSmrtnihZrtev(mapa):
    '''
    Narise graf stevila smrtnih žrtev v odvisnosti od leta
    '''
    podatki = SmrtneZrtve_VsaLeta(mapa)
    unzipped = list(zip(*podatki))
    x = unzipped[0]
    y = unzipped[1]
    plt.xticks(x)
    plt.xlabel('Leto')
    plt.ylabel('Število smrtnih žrtev')
    font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 14}
    plt.title('Število smrtnih žrtev v obdobju {} - {}'.format(x[0], x[-1]), fontdict=font)

    plt.plot(x, y, marker ='.', markersize=8, markeredgecolor='red')
    plt.show()

#print(GrafSmrtnihZrtev(os.getcwd() + "/podatki"))

#ANALIZA 4
#VRSTA POŠKODBE V ODVISNOSTI OD UPORABE VARNOSTNEGA PASU

def uporaba_varnostnega_pasu(leto):
    '''
    Funkcija pogleda vrsto poškodbe v odvisnosti od uporabe varnostnega pasu.
    '''
    df = pd.read_csv(leto, sep=';', encoding='windows-1250')
    df = df[['UporabaVarnostnegaPasu','PoskodbaUdelezenca']]
    df['sestevek'] = 1
    #csv_loader.groupby('Valuegroup')['Value'].mean().plot()
    df = df.groupby(['UporabaVarnostnegaPasu','PoskodbaUdelezenca']).count()['sestevek']
    return df


def narisi_histogram(leto, varn_pas):
    '''Funckija nariše histogram in prikaže poškodbe v odvisnosti od uporabe varnostnega pasu.
    '''
    pripasani_udelezenci = varn_pas['DA']
    nepripasani_udelezenci = varn_pas['NE']
    vsi_DA = pripasani_udelezenci.sum()
    vsi_NE = nepripasani_udelezenci.sum()
    delez_pripasanih = round(pripasani_udelezenci/vsi_DA*100, 2)
    delez_nepripasanih = round(nepripasani_udelezenci/vsi_NE*100, 2)
    # varn_pas.plot.bar()
    indeks = delez_pripasanih.keys()
    for vzrok in delez_nepripasanih.keys():
        if vzrok not in indeks:
            indeks.append(vzrok)
    tabela_prip = [delez_pripasanih[x] for x in indeks]
    tabela_neprip = [delez_nepripasanih[x] for x in indeks]
    df = pd.DataFrame({'Pripasani udeleženci prometne nesreče': tabela_prip,
                        'Nepripasani udeleženci prometne nesreče': tabela_neprip}, index=indeks)

    graf = df.plot.bar(figsize =(14,5), rot = 0, color=['cyan', 'blue'], edgecolor = 'black')
    graf.set_ylabel('Delež pripasanih/nepripasanih udeležencev')
    graf.set_title('KLASIFIKACIJA POŠKODB V ODVISNOSTI OD UPORABE VARNOSTNEGA PASU') 
    graf.set_facecolor('gray') 
    plt.show()
    
#print(narisi_histogram(os.getcwd()+ "/podatki/pn2019.csv", uporaba_varnostnega_pasu(os.getcwd()+ "/podatki/pn2019.csv")))

#ANALIZA 5
#NAJPOGOSTEJŠI VZROKI NESREČE V POSAMEZNIH REGIJAH

def seznam_url_regij(url):
    '''
    funkcija poisce ustrezen url regije na spletni strani in mu pripiše ime regije
    vrne tabelo parov oblike (ime_regije, url_regije)
    '''
    html = requests.get(url)
    reg_iz = r'/obcine/sl/Region/Index/?[1-9][0-9]*">[a-zčšžA-ZČŠŽ\s\-]*</a>'
    tab_nizov = re.findall(reg_iz,html.text)
    tab_parov = []
    for i in tab_nizov:
        url_regij = i.split('">')[0]
        regija = i.split('">')[1][:-4].upper()
        tab_parov.append((regija, url_regij))
    return tab_parov


def obcine_v_regiji(url):
    '''
    funkcija poisce vse obcine v regiji (url regije) in vrne tabelo obcin v podani regiji
    '''
    html = requests.get(url)
    reg_iz = r'/obcine/sl/Municip/Index/?[1-9][0-9]*">[a-zčšžA-ZČŠŽ\s\-]*</a>'
    obcine = re.findall(reg_iz, html.text)
    sez_obcin = []
    for i in obcine:
        obcina = i.split('>')[1][:-3].upper()
        sez_obcin.append(obcina)
    return sez_obcin


def slovar_obcin_v_regijah(url):
    '''
    funkcija naredi tabelo, ki vsaki občini pripiše ustrezna statistično regijo
    '''
    df = pd.DataFrame()
    sez_vseh_obcin = []
    sez_vseh_regij = []
    seznam_regij = seznam_url_regij(url)
    for par in seznam_regij:
        sez_obcin = obcine_v_regiji('https://www.stat.si'+par[1])
        regija = par[0]
        sez_regij = [regija]*len(sez_obcin)
        sez_vseh_obcin.extend(sez_obcin)
        sez_vseh_regij.extend(sez_regij)


    df['Obcine'] = sez_vseh_obcin
    df['Statisticne regije'] = sez_vseh_regij
    # zaradi neujemanja imena obcine Sentjur, to obcino preimenujemo v nasi tabeli
    df['Obcine'] = df['Obcine'].str.replace('ŠENTJUR ','ŠENTJUR PRI CELJU')
    # naredimo tabelo, ki vsaki obcini pripise statisticno regijo
    df = df.pivot_table(index='Obcine', aggfunc=lambda x: x)
    return df

# print(slovar_obcin_v_regijah("https://www.stat.si/obcine"))


def DodajStatisticnoRegijo(leto):
    '''
    funkcija vsaki obcini iz tabele podatkov pripise ustrezno statisticno regijo in prešteje število posameznega vzroka nesrece.
    Vrne tabelo z občinami, vzroki nesrec in statisticnimi regijami.
    '''
    df = pd.read_csv(leto, sep=';', encoding='windows-1250')
    df = df[['UpravnaEnotaStoritve','VzrokNesrece']]

    stat_reg = slovar_obcin_v_regijah("https://www.stat.si/obcine")
    regije = stat_reg['Statisticne regije']
    # naredimo nov stolpec statisticnih regij, ki ustrezajo obcinam
    stolpec_regij = df['UpravnaEnotaStoritve'].map(regije.rename('StatisticneRegije'))
    df['StatisticneRegije'] = stolpec_regij
    # z funkcijo unstack(fill_value) dodamo tudi vzroke nesrec, ki jih v posamezni regiji sicer niso zaznali, vrednost le-teh pa nastavimo na 0
    st_vzrokov = df.pivot_table(index = ['StatisticneRegije','VzrokNesrece'], aggfunc ='size').unstack(fill_value=0).stack()
    # df.to_csv('pivot.csv', encoding='utf-8')
    # st_vzrokov = st_vzrokov.index.get_level_values(0)
    return st_vzrokov

# print(DodajStatisticnoRegijo(os.getcwd()+ "/podatki/pn2010.csv"))


def TortniDiagram_VzrokovNesrec(leto, ime_regije):
    '''
    Funkcija narise tortni diagram, ki prikazuje stevilo posameznega vroka nesrece, za podano regijo
    '''
    stat_reg = DodajStatisticnoRegijo(os.getcwd()+ "/podatki/pn2009.csv")
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 4), subplot_kw = dict(aspect='equal'))

    x = stat_reg[ime_regije]
    tab_vzrokov = stat_reg[ime_regije].keys()
    st_vzrokov = sum(x) 

    explode = (x == max(x)) * 0.1
    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'silver', 'pink', 'brown', 'gold', 'cyan']
    vzroki, tekst= ax.pie(x, colors=colors, explode=explode, shadow=True)
    plt.legend(vzroki, tab_vzrokov, title='Vzroki nesreče', loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)
    ax.set_title("Število posameznega vzroka nesreče v statistični regiji {}".format(ime_regije))
    plt.show()

# print(TortniDiagram_VzrokovNesrec(os.getcwd()+ "/podatki/pn2009.csv", 'SAVINJSKA'))



#PREDSTAVITEV TORTNIH DIAGRAMOV NA ZEMLJEVIDU

def Podatki_KartaSlovenije(url):
    '''
    funkcija naloži mapo z datotekami, ki vsebujejo podatke o karti Slovenije.
    In jih shrani v trenutni direktorij.
    '''
    # pridobimo shapefile slovenije iz spletne strani https://www.diva-gis.org/datadown
    # (zaenkrat zakomentirano zaradi hitrosti izpisa)
    # prenos_datotek(url, '/karta_slovenije') 
    slika_slo = 'karta_slovenije/SVN_adm1.shp'
    karta_slo = gpd.read_file(slika_slo)
    # popravimo imena statističnih regij v tabeli
    karta_slo['NAME_1'] = karta_slo['NAME_1'].str.upper()
    karta_slo['NAME_1'] = karta_slo['NAME_1'].str.replace('NOTRANJSKO-KRAŠKA', 'PRIMORSKO-NOTRANJSKA')
    karta_slo['NAME_1'] = karta_slo['NAME_1'].str.replace('SPODNJEPOSAVSKA', 'POSAVSKA')
    return karta_slo


def TortniDiagrami_StatisticneRegije(leto):
    '''
    funkcija glede na podano leto izrise tortne diagrame na zemljevidu
    po statisticnih regijah Slovenije
    '''
    karta_slo = Podatki_KartaSlovenije('http://biogeo.ucdavis.edu/data/diva/adm/SVN_adm.zip')

    # narisemo graf slovenije
    fig, ax = plt.subplots(figsize=[12,8])
    graf = karta_slo.plot(ax = ax, color='green', edgecolor = 'black')
    graf.set_title('Delež vzrokov nesreč po regijah Slovenije', fontsize=22)

    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'silver', 'pink', 'brown', 'gold', 'cyan']
    stat_reg = DodajStatisticnoRegijo(leto)
    # zabelezimo vse mozne vzorke nesrec
    df = pd.read_csv(leto, sep=';', encoding='windows-1250')
    tab_vzrokov = df.pivot_table(index = ['VzrokNesrece'], aggfunc ='size').keys()
    # narišemo vseh 12 tortnih diagramov na karto slovenije
    for ind, row in karta_slo.iterrows():
        ax_sub = inset_axes(ax, width=0.8, 
                                height=0.8, 
                                loc=10, 
                                bbox_to_anchor=(karta_slo.centroid.x[ind], karta_slo.centroid.y[ind]), # določimo koordinate (center vsake regije)
                                bbox_transform=ax.transData)
        podatki = stat_reg[row['NAME_1']]
        explode = (podatki == max(podatki)) * 0.2 # najvecji delez izrazimo 
        barve, tekst = ax_sub.pie(podatki, shadow=True, colors=colors, explode=explode)
    # naredimo skupno legendo za tortne diagrame
    ax_sub.legend(barve, tab_vzrokov, title='Vzroki nesreč',  loc=10, bbox_to_anchor=[4.5, -1.8], fontsize=8)

    plt.show()
# print(Podatki_KartaSlovenije("http://biogeo.ucdavis.edu/data/diva/adm/SVN_adm.zip"))
# print(TortniDiagrami_StatisticneRegije(os.getcwd()+ "/podatki/pn2009.csv"))


#ANALIZA 6
#ANALIZA POVZROČITELJEV NESREČE GLEDE NA STAROST

def starostne_skupine(letnica):
    ''' 
        Funkcija datumu pripiše ustrezen letni čas
    '''
    slovar_starosti = {}
    if int(letnica) <= 25:
        slovar_starosti[letnica] = '25 ali manj'
    elif 26 <= int(letnica) <= 35:
        slovar_starosti[letnica] = 'Med 26 in 35'
    elif 36 <= int(letnica) <= 45:
        slovar_starosti[letnica] = 'Med 36 in 45'
    elif 26 <= int(letnica) <= 35:
        slovar_starosti[letnica] = 'Med 26 in 35'
    elif 36 <= int(letnica) <= 45:
        slovar_starosti[letnica] = 'Med 36 in 45'
    elif 46 <= int(letnica) <= 55:
        slovar_starosti[letnica] = 'Med 46 in 55'
    elif 56 <= int(letnica) <= 65:
        slovar_starosti[letnica] = 'Med 56 in 65'
    elif int(letnica) > 65:
        slovar_starosti[letnica] = 'Več od 65'
    return slovar_starosti[letnica]
#print(starostne_skupine(89))

def povzrocitelji_PN_hist(leto):
    '''
    Funkcija nariše histogram, ki ponazarja delež povzročiteljev prometnih nesreč 
    razvrščenih v ustrezne starostne skupine
    '''
    df = pd.read_csv(leto, sep=';', encoding='windows-1250')
    #izmed vseh izločimo povzročitelje prometne nesreče (udeleženci nas ne zanimajo)
    df = df.loc[(df["Povzrocitelj"] == 'POVZROČITELJ') & (df["Starost"] > 0)]
    stevilo_vseh_povzrociteljev = df.count()['Povzrocitelj']
    #Povzročiteljem dodelimo ustrezno starostno skupino
    df['Starost'] = df['Starost'].map(starostne_skupine)
    delez = (df.pivot_table(index='Starost', aggfunc='size').sort_values(ascending=False) / stevilo_vseh_povzrociteljev)*100
    #podatke grafično predstavimo
    plt.figure(tight_layout = True, figsize = (8, 5))
    plt.style.use('ggplot')
    hist = delez.plot(kind="bar",color='yellow', edgecolor = 'black')
    hist.set_xlabel('Starostne skupine')
    hist.set_ylabel('Delež povzročiteljev')
    plt.xticks(rotation=45)
    hist.set_title('Povzročitelji prometne neseče razdeljeni v starostne skupine', fontsize = 14) 
    hist.set_facecolor('lightblue') 

    plt.show()

#print(povzrocitelji_PN_hist(os.getcwd()+ "/podatki/pn2019.csv"))



#ANALIZA 7
#ANALIZA VPLIVA POLNE LUNE NA ŠTEVILO PROMETNIH NESREČ

def polna_luna(leto):
    '''
    funkcija zgenerira seznam datumov polnih lun za podano leto.
    '''
    zacetni_datum = ephem.Date(datetime.date(leto-1, 12, 31))
    koncni_datum = ephem.Date(datetime.date(leto+1, 1, 1))
    polne_lune = []
    while zacetni_datum <= koncni_datum:
        # poiscemo datum naslednje polne lune
        zacetni_datum = ephem.next_full_moon(zacetni_datum)
        # datum nastavimo nazaj na nas zapis datuma 
        lokalni_datum = ephem.localtime(zacetni_datum)
        if lokalni_datum.year == leto:
            prejsni = lokalni_datum - date.timedelta(days=1)
            polne_lune.append(prejsni.strftime("%Y-%m-%d"))
            # dodamo se datum pred datumom polne lune 
            polne_lune.append(lokalni_datum.strftime("%Y-%m-%d"))

    return polne_lune

# print(polna_luna(2018))

def obdobje_polneLune(datum, tab_polnih_lun):
    '''
    funkcija podanemu datumu pripise vrednost bodisi DA bodisi NE.
    Datumu je pripisana vrednost DA, ce sovpada z datumom polne lune.
    '''
    sl = {}
    if datum in tab_polnih_lun:
        sl[datum] = 'DA'
    else:
        sl[datum] = 'NE'
    return sl[datum]

def stNesrec_polnaLuna(leto):
    '''
    funkcija vrne tabelo, ki primerja povprecno stevilo nesrec na dan v obdobju polne lune, 
    s povprecnim stevilom nesrec na dan izven obdobja polne lune.
    '''
    stari_format='%d.%m.%Y'
    novi_format='%Y-%m-%d'
    df = pd.read_csv(leto, sep=';', encoding='windows-1250')
    # V osnovni tabeli podatkov so nekatere nesrece ponovljene zaradi vecjega stevila udelezencev. 
    # Teh vrstic v nasi analizi ne potrebujemo, zato jih odstranimo
    df = df.drop_duplicates(subset = ['UraPN', 'DatumPN', 'UpravnaEnotaStoritve', 
                            'KlasifikacijaNesrece','GeoKoordinataX', 'GeoKoordinataY', 'StanjePrometa'], ignore_index=True)
    df = df[['DatumPN']]
    # V stolpcu z datumi spremenimo zapis datuma ('%d.%m.%Y' --> '%Y-%m-%d'), zaradi lazjega branja programa
    df['DatumPN'] = pd.to_datetime(df['DatumPN'], format=stari_format).dt.strftime(novi_format)

    df = df.sort_values(by='DatumPN', ignore_index = True)
    tr_leto = int(df['DatumPN'][0][:4])
    tab_polnih_lun = polna_luna(tr_leto)
    df['PolnaLuna'] = df['DatumPN'].apply(obdobje_polneLune, args=(tab_polnih_lun,))
    # df.to_csv('polne_lune')
    df = df.pivot_table(index='PolnaLuna', aggfunc='size')
    # predpostavljamo, da se je zgodila vsaj ena prometna nesreca na dan
    # zanemarimo vpliv prestopnega leta!!!
    df['DA'] = df['DA']/(len(tab_polnih_lun)) # stevilo nesrec delimo s stevilom polnih lun v letu
    df['NE'] = df['NE']/(365-(len(tab_polnih_lun)))
    return df

# print(stNesrec_polnaLuna(os.getcwd()+ "/podatki/pn2018.csv"))

def histagramPolnaLuna(mapa):
    '''
    funkcija narise histogram, ki primerja povprecno stevilo nesrec na dan v obdobju polne lune,
    s povprecnim stevilom nesrec na dan izven obdobja polne lune za vsa leta. 
    '''
    tab_letnic = []
    tab_polna = []
    tab_niPolna = []
    for leto in os.listdir(mapa):
        if not leto.startswith('.'):
            reg = r'[1-9][0-9]*'
            letnica = re.findall(reg,leto)[0] # v mapi poiscemo vse letnice
            tab_letnic.append(int(letnica))
            tab_polna.append(stNesrec_polnaLuna(mapa + '/' +leto)['DA'])
            tab_niPolna.append(stNesrec_polnaLuna(mapa + '/' +leto)['NE'])

    df = pd.DataFrame({'POLNA LUNA': tab_polna, 'NI POLNA LUNA': tab_niPolna}, index=tab_letnic)
    df = df.sort_index()

    graf = df.plot.bar(figsize =(14,5), rot = 0, color=['cyan', 'blue'], edgecolor = 'black')
    graf.set_ylabel('Povprečno število nesreč na dan')
    graf.set_title('VPLIV POLNE LUNE NA ŠTEVILO PROMETNIH NESREČ') 
    graf.set_facecolor('gray') 
    plt.show()    

# print(histagramPolnaLuna(os.getcwd()+'/podatki'))

#ANALIZA 8
#ANALIZA POGOSTOSTI PROMETNIH NESREČ V STATISTIČNIH REGIJAH
def Gostota_PrometnihNesrec(leto):
    '''
    funkcija prikaže pogostost prometnih nesrec v odvisnosti od statisticne regije
    '''
    # pridobimo karto slovenije
    karta_slo = Podatki_KartaSlovenije('http://biogeo.ucdavis.edu/data/diva/adm/SVN_adm.zip')
    # pridobimo podatke o nesrecih in odstranimo ponovljene nesrece
    df = pd.read_csv(leto, sep=';', encoding='windows-1250')
    df = df.drop_duplicates(subset = ['UraPN', 'DatumPN', 'UpravnaEnotaStoritve', 
                            'KlasifikacijaNesrece','GeoKoordinataX', 'GeoKoordinataY', 'StanjePrometa'], ignore_index=True)

    stat_reg = slovar_obcin_v_regijah("https://www.stat.si/obcine")
    regije = stat_reg['Statisticne regije']
    # naredimo nov stolpec statisticnih regij, ki ustrezajo obcinam
    stolpec_regij = df['UpravnaEnotaStoritve'].map(regije.rename('StatisticneRegije'))
    df['StatisticneRegije'] = stolpec_regij
    df = df[['StatisticneRegije']]
    df['SteviloPrometnihNesrec'] = 1
    df = df.pivot_table(index = ['StatisticneRegije'], aggfunc='size')
    # vsaki statisticni regiji pripisemo ustrezno stevilo prometnih nesrec
    karta_slo['SteviloPrometnihNesrec'] = karta_slo['NAME_1'].apply(lambda x: df[x])
    # narisemo graf
    fig, ax = plt.subplots(1, 1)
    karta_slo.plot(column='SteviloPrometnihNesrec', ax=ax, cmap='Reds', legend=True, legend_kwds={'label': 'Število prometnih nesreč v letu {}'.format(leto[-8:-4]), 'orientation': "horizontal"})
    plt.title('Gostota prometnih nesreč v Sloveniji leta {}'.format(leto[-8:-4]))

    plt.show()

#print(Gostota_PrometnihNesrec(os.getcwd()+ "/podatki/pn2019.csv"))

#ANALIZA 9
#ANALIZA UDELEŽENCEV POZITIVNIH NA ALKOTEST
def StNesrec_pozitivenAlkotest(leto):
    '''
    funkcija nam vrne podatke o stevilu nesrec, za posamezno upravno enoto,
    pri katerih je bil alkotest pozitiven
    '''
    df = pd.read_csv(leto, sep=';', encoding='windows-1250')
    new_df = df
    new_df['VrednostAlkotesta'] = new_df['VrednostAlkotesta'].str.replace(',', '.')
    new_df['VrednostAlkotesta'] = new_df['VrednostAlkotesta'].astype(float)
    gp = new_df[new_df['VrednostAlkotesta'] > 0].groupby('UpravnaEnotaStoritve') # grupiramo podatke o alkotestu po Upravnih enotah in pri tem izpustimo tiste, pri katerih je alkotest negativen 
    new_df = gp['VrednostAlkotesta'].count().sort_values(ascending=False) # prestejemo vse pozitivne alkoteste za posamezno Upravno enoto 

    return new_df

def HistogramStNesrec_pozitivenAlkotest(df):
    '''
    funkcija narise histogram, padajoc po stevilu nesrec, za prvih 10 upravnih enot
    '''

    plt.figure(tight_layout = True)
    hist = df[0:14].plot(kind="bar",color='red', edgecolor = 'black')
    hist.set_xlabel('Upravna Enota')
    hist.set_ylabel('Delež')
    hist.set_title('DELEŽ UDELEŽENCEV POZITIVNIH NA ALKOTEST') 
    hist.set_facecolor('darkgray') 
    plt.show()

def Razmerje_PozitivenAlkotest_VseNesrece(leto):
    '''
    Funkcija nam vrne podatke o kvocientu stevila nesrec, pri katerih je bil alkotest pozitiven z stevilom vseh nesrec,
    za posamezno Uporavno enoto
    '''
    df = pd.read_csv(leto, sep=';', encoding='windows-1250')
    # podatke v stolpcu 'VrednostAlkotesta' preoblikujemo v obliko float
    df['VrednostAlkotesta'] = df['VrednostAlkotesta'].str.replace(',', '.')
    df['VrednostAlkotesta'] = df['VrednostAlkotesta'].astype(float)

    # tabela podatkov pozitivnih alkotestov
    poz_alk = df[df['VrednostAlkotesta'] > 0][['UpravnaEnotaStoritve', 'VrednostAlkotesta']]
    poz_alk = poz_alk.groupby('UpravnaEnotaStoritve').count().sort_values('VrednostAlkotesta', ascending=False)
    poz_alk.columns = ['SteviloPozitivnihAlkotestov']
    # tabela podatkov vseh nesrec
    vse_nesr = df[['UpravnaEnotaStoritve', 'VrednostAlkotesta']]
    vse_nesr = vse_nesr.groupby('UpravnaEnotaStoritve').count().sort_values('VrednostAlkotesta', ascending=False)
    vse_nesr.columns = ['SteviloVsehAlkotestov']
    # tabela podatkov kvocienta pozitivnih alkotestov in vseh alkotestov podanih v procentih
    zdr_df = pd.concat([poz_alk, vse_nesr], axis=1)
    zdr_df['Razmerje'] = round(zdr_df['SteviloPozitivnihAlkotestov'] / zdr_df['SteviloVsehAlkotestov'] * 100, 2)
    zdr_df = zdr_df['Razmerje']
    zdr_df = zdr_df.sort_values(ascending=False)

    return zdr_df

# print(StNesrec_pozitivenAlkotest(os.getcwd()+ "/podatki/pn2009.csv"))
# print(graf_alkotst(StNesrec_pozitivenAlkotest(os.getcwd()+ "/podatki/pn2009.csv")))
#print(HistogramStNesrec_pozitivenAlkotest(Razmerje_PozitivenAlkotest_VseNesrece(os.getcwd()+ "/podatki/pn2017.csv")))
