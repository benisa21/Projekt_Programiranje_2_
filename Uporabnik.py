from funkcije import *

def pravilno_leto(leto, vrni=None):
    '''
    funkcija vrne True, ce je vneseno leto pravilno in False, ce ni
    '''
    mapa = os.getcwd() + '/podatki'
    letnice = []
    for dat in os.listdir(mapa):
        if not dat.startswith('.'):
            reg = r'[1-9][0-9]*'
            letnica = re.findall(reg, dat)[0] # v mapi poiscemo vse letnice
            letnice.append(letnica)   
    if leto in letnice:
        if vrni == None:
            return True
        else:
            return sorted(letnice)[-1]
    else:
        if vrni == None:
            return False     
        else:
            return sorted(letnice)[-1]


print('')
print('POZDRAVLJENI V PROGRAMU ANALIZE PROMETNIH NESREČ!\n')
print('Za uspešno delovanje programa, boste potrebovali naslednje knjižnice:')
print('- Matplotlib.pyplot')
print('- ephem')
print('- urllib.requests')
print('- zipfile')
print('- Numpy')
print('- Pandas')
print('- GeoPandas')

while True:
    zacetek = input('\nAli želite nadaljevati? (DA/NE): ')
    if zacetek == 'DA':
        print('\nNa voljo so:')
        print('1.) ANALIZA ŠTEVILA PROMETNIH NESREČ')
        print('2.) ANALIZA NESREČ V ODVISNOSTI OD LETNIH ČASOV')
        print('3.) ANALIZA ŠTEVILA SMRTNIH ŽRTEV')
        print('4.) ANALIZA VRSTE POŠKODBE V ODVISNOSTI OD UPORABE VARNOSTNEGA PASU')
        print('5.) ANALIZA NAJPOGOSTEJŠIH VZROKOV NESREČ V STATISTIČNIH REGIJAH')
        print('6.) ANALIZA POVZROČITELJEV NESREČE GLEDE NA STAROST')
        print('7.) ANALIZA VPLIVA POLNE LUNE NA ŠTEVILO PROMETNIH NESREČ')
        print('8.) ANALIZA POGOSTOSTI PROMETNIH NESREČ V STATISTIČNIH REGIJAH')
        print('9.) ANALIZA UDELEŽENCEV POZITIVNIH NA ALKOTEST\n')
        nadaljevanje = True
        while nadaljevanje:
            st_analize = input('Prosim, vnesite številko poljubne analize: ')
            print('')
            if st_analize == '1':
                while True:
                    Graf_Stevila_PN(os.getcwd() + "/podatki")
                    break
                nadaljevanje = False

            elif st_analize == '2':
                while True:
                    leto = input('Prosim vnesite letnico med 2009 do {}: '.format(pravilno_leto('2009', True)))
                    if pravilno_leto(leto):
                        letni_cas_nesrece_graf(os.getcwd()+ "/podatki/pn{}.csv".format(leto))
                        break
                    else:
                        print('\nVnesli ste napačno letnico!')
                        continue
                nadaljevanje = False
            #SMRTNE ŽRTVE 
            #VSA LETA
            elif st_analize == '3':
                while True:
                    GrafSmrtnihZrtev(os.getcwd() + "/podatki")
                    break
                nadaljevanje = False
                
            #VARNOSTNI PAS
            elif st_analize == '4':
                while True:
                    leto = input('Prosim vnesite letnico med 2009 do {}: '.format(pravilno_leto('2009', True)))
                    if pravilno_leto(leto):
                        narisi_histogram(os.getcwd()+ "/podatki/pn{}.csv".format(leto), uporaba_varnostnega_pasu(os.getcwd()+ "/podatki/pn{}.csv".format(leto)))
                        break
                    else:
                        print('\nVnesli ste napačno letnico!')
                        continue
                nadaljevanje = False
            #VZROKI NESREČE PO STATISTIČNIH REGIJAH
            elif st_analize == '5':
                nadaljevanje = False
                while True:
                    leto = input('Prosim vnesite letnico med 2009 do {}: '.format(pravilno_leto('2009', True)))
                    if pravilno_leto(leto):
                        TortniDiagrami_StatisticneRegije(os.getcwd()+ "/podatki/pn{}.csv".format(leto))
                        ali_regija = input('\nAli želite analizo za posamezno regijo? (DA/NE): ')
                        ponovitev = True
                        while ponovitev:
                            if ali_regija == 'DA':
                                print('\nIzbirate lahko med naslednjimi regijami:')
                                print('1.) OSREDNJESLOVENSKA')
                                print('2.) GORENJSKA')
                                print('3.) GORIŠKA')
                                print('4.) OBALNO-KRAŠKA')
                                print('5.) KOROŠKA')
                                print('6.) PODRAVSKA')
                                print('7.) POMURSKA')
                                print('8.) POSAVSKA')
                                print('9.) PRIMORSKO-NOTRANJSKA')
                                print('10.) SAVINJSKA')
                                print('11.) ZASAVSKA')
                                while True:
                                    regija = input('\nProsimo vnesite številko statistične regije: ')
                                    if regija == '1': regija = 'OSREDNJESLOVENSKA'
                                    elif regija == '2': regija = 'GORENJSKA'
                                    elif regija == '3': regija = 'GORENJSKA'
                                    elif regija == '4': regija = 'GORIŠKA'
                                    elif regija == '5': regija = 'OBALNO-KRAŠKA'
                                    elif regija == '6': regija = 'PODRAVSKA'
                                    elif regija == '7': regija = 'POMURSKA'
                                    elif regija == '8': regija = 'POSAVSKA'
                                    elif regija == '9': regija = 'PRIMORSKO-NOTRANJSKA'
                                    elif regija == '10': regija = 'SAVINJSKA'
                                    elif regija == '11': regija = 'ZASAVSKA'
                                    try:
                                        TortniDiagram_VzrokovNesrec(leto, regija)
                                        ponovitev = False
                                        break
                                    except:
                                        print('\nVnesli ste napačno številko regije!')
                                        continue

                            elif ali_regija == 'NE':
                                break
                            else:
                                print('\nVnesli ste napačen niz!')
                                continue   
                        break
                    else:
                        print('\nVnesli ste napačno letnico!')
                        continue
                    
                    
            #ANALIZA POVZROČITELJEV NESREČE GLEDE NA STAROST
            elif st_analize == '6':
                while True:
                    leto = input('Prosim vnesite letnico med 2009 do {}: '.format(pravilno_leto('2009', True)))
                    if pravilno_leto(leto):
                        povzrocitelji_PN_hist(os.getcwd()+ "/podatki/pn{}.csv".format(leto))
                        break
                    else:
                        print('\nVnesli ste napačno letnico!')
                        continue
                nadaljevanje = False
                    
            # ANALIZA VPLIVA POLNE LUNE NA ŠTEVILO PROMETNIH NESREČ
            #VSA LETA
            elif st_analize == '7':
                while True:
                    histagramPolnaLuna(os.getcwd()+'/podatki')
                    break
                nadaljevanje = False

            #ANALIZA POGOSTOSTI PROMETNIH NESREČ V STATISTIČNIH REGIJAH'
            elif st_analize == '8':
                while True:
                    leto = input('Prosim vnesite letnico med 2009 do {}: '.format(pravilno_leto('2009', True)))
                    if pravilno_leto(leto):
                        Gostota_PrometnihNesrec(os.getcwd()+ "/podatki/pn{}.csv".format(leto))
                        break
                    else:
                        print('\nVnesli ste napačno letnico!')
                        continue
                nadaljevanje = False
            
            elif st_analize == '9':
                while True:
                    leto = input('Prosim vnesite letnico med 2009 do {}: '.format(pravilno_leto('2009', True)))
                    if pravilno_leto(leto):
                        HistogramStNesrec_pozitivenAlkotest(Razmerje_PozitivenAlkotest_VseNesrece(os.getcwd()+ "/podatki/pn{}.csv".format(leto)))
                        break
                    else:
                        print('\nVnesli ste napačno letnico!')
                        continue
                nadaljevanje = False
            else:
                print('\nVnesli ste napačno število\n')
                continue

    elif zacetek == 'NE':
        print('\nHVALA, NASVIDENJE!\n')
        break
    else:
        print('\nVnos je napačen. Poskusite znova:')
        continue



