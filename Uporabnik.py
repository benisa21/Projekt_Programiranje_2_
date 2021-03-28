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
print('- os')
print('- re')
print('- requests')
print('- Matplotlib.pyplot')
print('- ephem')
print('- urllib.requests')
print('- datetime')
print('- zipfile')
print('- Numpy')
print('- Pandas')
print('- GeoPandas')
print('')

while True:
    zacetek = input('Ali želite nadaljevati? (DA/NE): ')
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
                        print('Vnesli ste napačno letnico!')
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
                        print('Vnesli ste napačno letnico!')
                        continue
                nadaljevanje = False
            #VZROKI NESREČE PO STATISTIČNIH REGIJAH
            elif st_analize == '5':
                nadaljevanje = False
                while True:
                    leto = input('Prosim vnesite letnico med 2009 do {}: '.format(pravilno_leto('2009', True)))
                    if pravilno_leto(leto):
                        TortniDiagrami_StatisticneRegije(os.getcwd()+ "/podatki/pn{}.csv".format(leto))
                        ali_regija = input('Ali želite analizo za posamezno regijo? (DA/NE): ')
                        ponovitev = True
                        while ponovitev:
                            if ali_regija == 'DA':
                                print('Izbirate lahko med naslednjimi regijami:')
                                print('OSREDNJESLOVENSKA')
                                print('GORENJSKA')
                                print('GORIŠKA')
                                print('OBALNO-KRAŠKA')
                                print('KOROŠKA')
                                print('PODRAVSKA')
                                print('POMURSKA')
                                print('POSAVSKA')
                                print('PRIMORSKO-NOTRANJSKA')
                                print('SAVINJSKA')
                                print('ZASAVSKA')
                                regija = input('Prosimo vnesite statistično regijo: ')
                                while True:
                                    try:
                                        TortniDiagram_VzrokovNesrec(leto, regija)
                                        ponovitev = False
                                        break
                                    except:
                                        print('Vnesli ste napačno regijo!')
                                        continue

                            elif ali_regija == 'NE':
                                break
                            else:
                                print('Vnesli ste napačen niz!')
                                continue   
                        break
                    else:
                        print('Vnesli ste napačno letnico!')
                        continue
                    
                    
            #ANALIZA POVZROČITELJEV NESREČE GLEDE NA STAROST
            elif st_analize == '6':
                while True:
                    leto = input('Prosim vnesite letnico med 2009 do {}: '.format(pravilno_leto('2009', True)))
                    if pravilno_leto(leto):
                        povzrocitelji_PN_hist(os.getcwd()+ "/podatki/pn{}.csv".format(leto))
                        break
                    else:
                        print('Vnesli ste napačno letnico!')
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
                        print('Vnesli ste napačno letnico!')
                        continue
                nadaljevanje = False
            
            elif st_analize == '9':
                while True:
                    leto = input('Prosim vnesite letnico med 2009 do {}: '.format(pravilno_leto('2009', True)))
                    if pravilno_leto(leto):
                        HistogramStNesrec_pozitivenAlkotest(Razmerje_PozitivenAlkotest_VseNesrece(os.getcwd()+ "/podatki/pn{}.csv".format(leto)))
                        break
                    else:
                        print('Vnesli ste napačno letnico!')
                        continue
                nadaljevanje = False
            else:
                print('\nVnesli ste napačno število\n')
                continue

    elif zacetek == 'NE':
        print('\nHVALA, NASVIDENJE!\n')
        break
    else:
        print('Vnos je napačen. Poskusite znova:')
        continue


