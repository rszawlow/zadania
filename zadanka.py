import csv
import math
import matplotlib.pylab as plt
import numpy as np
import statistics

# wyswietlilem  punkty pomiarowe z CH2 i CH3, w następnym zadaniu wczytam je sobie do tablicy dwuwymiarowej,
def read_csv(csv_file):
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)

            for x in reader:
                print('{} {}, {} {}'.format(headers[1], x[1], headers[2], x[2]))
    except FileNotFoundError as err:
        print(f"Error: File '{csv_file}' not found - {err}")
# wczytalem sobie te punkty do tablicy
def dodanieczasuizapisaniedotablicyy(csv_file):
    tablica = []
    try:
        with open(csv_file) as file:
            reader = csv.reader(file)

            for line in reader:
                if line[0] in['X', 'Sequence']:
                    tablica.append(line)
                    if line[-1] == '':
                        line.pop()
                else:
                    line[3] = 0
                    line[0] = int(line[0])
                    for i in range(1, 3):
                        line[i] = float(line[i].strip())

                    tablica.append(line)
                # stworzylem tablice dwuwymiarowa

            czas_startu = float(tablica[1][3])
            okres_probkowania = float(tablica[1][4])

            for y in tablica:
                if y[0] not in ['X', 'Sequence']:
                    numer_probki = float(y[0])
                    czas_obecny = czas_startu + numer_probki * okres_probkowania
                    y[3] = round(czas_obecny, 7)
                    y.insert(4, okres_probkowania)
        return tablica
    except ValueError as err:
        print("Błąd przy zapisywaniu do tablicy wynikający najprawdopodbniej z braku możliwości przekonwertowania stringa na float", err)

def zapisdopliku(csv_file, nazwapliku_txt):
    tablicarekordow = dodanieczasuizapisaniedotablicyy(csv_file)
    try:
        with open(nazwapliku_txt, 'w') as file:

            for tablicajednowymiarowa in tablicarekordow:
                for pojedynczerekordy in tablicajednowymiarowa:
                    file.write(str(pojedynczerekordy) + '  ')
                file.write('\n')

    except FileNotFoundError as err:
        print("Nie ma takiego pliku źródłowego", err)



def wpisaniedopojedynczychtablic(csv_file):
    tablicarekordow = dodanieczasuizapisaniedotablicyy(csv_file)
    tablicach2 = []
    tablicach3 = []
    tablicaczas = []
    for y in tablicarekordow:
        if y[0] == "X" or y[0] == 'Sequence':
            continue
        else:
            tablicach2.append(y[1])
            tablicach3.append(y[2])
            tablicaczas.append((y[3] + 0.0012) * 1000)
    return tablicach2, tablicach3, tablicaczas


def rysowaniewykresow(csv_file):
    x = wpisaniedopojedynczychtablic(csv_file)

    plt.figure()
    plt.subplot(211)
    plt.plot(x[2], x[0], 'r-', label=r'$ch2$')
    plt.grid()
    plt.ylabel('u[V]')
    plt.title("Wykres dla ch2 i ch3 oddzielnie przed wyskalowaniem")
    plt.legend(loc='upper right')
    plt.subplot(212)
    plt.plot(x[2], x[1], 'b-', label=r'$ch3$')
    plt.grid()
    plt.xlabel('t[ms]')
    plt.ylabel('u[V]')
    plt.legend(loc='upper right')
    plt.savefig('wykresy_ch2_ch3.png')

    zmienna_do_wyskalowania_ch2 = (max(x[0]) + min(x[0]))/2
    tablica_ch2_wyskalowana=[]
    for y in x[0]:
        y = y - zmienna_do_wyskalowania_ch2
        tablica_ch2_wyskalowana.append(y)

    zmienna_do_wyskalowania_ch3 = (max(x[1]) + min(x[1])) / 2
    tablica_ch3_wyskalowana = []
    for y in x[1]:
        y = y - zmienna_do_wyskalowania_ch3
        tablica_ch3_wyskalowana.append(y)
    plt.figure()
    plt.subplot(211)
    plt.plot(x[2], tablica_ch2_wyskalowana, 'r-', label=r'$ch2$')
    plt.grid()
    plt.ylabel('u[V]')
    plt.title("Wykres dla ch2 i ch3 oddzielnie po wyskalowaniu")
    plt.legend(loc='upper right')
    plt.subplot(212)
    plt.plot(x[2], tablica_ch3_wyskalowana, 'b-', label=r'$ch3$')
    plt.grid()
    plt.xlabel('t[ms]')
    plt.ylabel('u[V]')
    plt.legend(loc='upper right')
    plt.savefig('wykrese_ch2_ch3_wyskalowane.png')

    "zadanie 5"
    tablica_50_ch3 = []
    for y in x[1]:
        y *= 50
        tablica_50_ch3.append(y)
    plt.figure()
    plt.plot(x[2], x[0], 'r-', label=r'$ch2$')
    plt.plot(x[2], tablica_50_ch3, 'b-', label=r'$50 x ch3$')
    plt.grid()
    plt.xlabel('t [ms]')
    plt.ylabel('u [V]')
    plt.title("Wykres funkcji ch2 oraz ch3 przed wyskalowaniem")
    plt.legend(loc='upper right')
    plt.savefig('wykreswspolny.png')



def rysowaniewykresu_ch3_ch2(csv_file):
    x = wpisaniedopojedynczychtablic(csv_file)
    plt.figure()
    plt.plot(x[0], x[1], 'ro', label=r'$ch3(ch2)$')

    plt.xlabel('ch2 [V]')
    plt.ylabel('ch3 [V]')
    plt.title("Wykres funkcji ch3(ch2)")
    plt.legend(loc='upper right')
    plt.grid()
    plt.savefig('wykresch3(ch2).png')
def wartoscimaksminsrednia(csv_file):
    x = wpisaniedopojedynczychtablic(csv_file)
    tablicach2 = x[0]
    tablicach3 = x[1]
    maks_ch2 = max(tablicach2)
    min_ch2 = min(tablicach2)
    maks_ch3 = max(tablicach3)
    min_ch3 = min(tablicach3)
    suma_ch2 = 0
    for y in tablicach2:
        suma_ch2 += y
    srednia_ch2 = suma_ch2 / len(tablicach2)

    suma_ch3 = 0
    for y in tablicach3:
        suma_ch3 += y
    srednia_ch3 = suma_ch3 / len(tablicach3)

    print("wartość maksymalna dla przebiegu ch2 to {}, wartość minimalna to {} a wartość średnia to {}".format(maks_ch2,
                                                                                                               min_ch2,
                                                                                                               srednia_ch2))
    print("wartość maksymalna dla przebiegu ch3 to {}, wartość minimalna to {} a wartość średnia to {}".format(maks_ch3,
                                                                                                               min_ch3,
                                                                                                               srednia_ch3))
def okresprzebiegu(csv_file):
    x = wpisaniedopojedynczychtablic(csv_file)
    tablicach2 = x[0]
    tablicach3 = x[1]
    tablicaczas = x[2]

    szukane_mz = 0
    indeksy_mz_ch2 = [n for n, m in enumerate(tablicach2) if m == szukane_mz]
    new_indeks_mz_ch2 = []
    for i in range(0, len(indeksy_mz_ch2) - 1):
        if indeksy_mz_ch2[i + 1] - indeksy_mz_ch2[i] > 8:
            new_indeks_mz_ch2.append(indeksy_mz_ch2[i + 1])

    szukany_czas_ch2 = [m for n, m in enumerate(tablicaczas) for y in range(0, len(new_indeks_mz_ch2)) if
                        n == new_indeks_mz_ch2[y]]
    okres_ch2 = szukany_czas_ch2[-1] - szukany_czas_ch2[-3]
    czestotliwosc_ch2 = 1 / okres_ch2

    indeksy_mz_ch3 = [n for n, m in enumerate(tablicach3) if m == szukane_mz]
    new_indeks_mz_ch3 = []
    for i in range(0, len(indeksy_mz_ch3) - 1):
        if indeksy_mz_ch3[i + 1] - indeksy_mz_ch3[i] > 8:
            new_indeks_mz_ch3.append(indeksy_mz_ch3[i + 1])
    szukany_czas_ch3 = [m for n, m in enumerate(tablicaczas) for y in range(0, len(new_indeks_mz_ch3)) if
                        n == new_indeks_mz_ch3[y]]
    okres_ch3 = szukany_czas_ch3[-1] - szukany_czas_ch3[-3]
    czestotliwosc_ch3 = 1 / okres_ch3

    print('Okres dla przebiegu ch2 to {} ms, natomiast częstotliwość to {} kHz'.format(okres_ch2, czestotliwosc_ch2))
    print('Okres dla przebiegu ch3 to {} ms, natomiast częstotliwość to {} kHz'.format(okres_ch3, czestotliwosc_ch3))



def wartoscsrednia_odchyleniestandardowe(csv_file):
    x = wpisaniedopojedynczychtablic(csv_file)
    tablicach2 = x[0]
    tablicach3 = x[1]

    zmienna_do_wyskalowania_ch2 = (max(tablicach2) + min(tablicach2)) / 2
    tablica_ch2_wyskalowana = []
    for y in tablicach2:
        y = y - zmienna_do_wyskalowania_ch2
        tablica_ch2_wyskalowana.append(y)
    wartoscsrednia_ch2_wyskalowana = np.mean(tablica_ch2_wyskalowana)
    odchyleniestandardowe_ch2_wyskalowane = statistics.stdev(tablica_ch2_wyskalowana)

    wartoscsrednia_ch2 = np.mean(tablicach2)
    odchyleniestandardowe_ch2 = statistics.stdev(tablicach2)
    wart_powiekszonach2 = wartoscsrednia_ch2 + 3 * odchyleniestandardowe_ch2
    wart_pomniejszonach2 = wartoscsrednia_ch2 - 3 * odchyleniestandardowe_ch2
    licznik_0 = 0
    licznik_1 = 0
    for y in tablicach2:
        if y > wart_powiekszonach2:
            licznik_0 += 1
        elif y < wart_pomniejszonach2:
            licznik_1 += 1
        else:
            continue
    print('Wartośc średnia dla ch2 to {} V, natomiast odchylenie standardowe {}'.format(wartoscsrednia_ch2,
                                                                                        odchyleniestandardowe_ch2))
    print('')
    print('Po wyskalowaniu wartośc średnia dla ch2 to {} V, natomiast odchylenie standardowe {}'.format(
        wartoscsrednia_ch2_wyskalowana,
        odchyleniestandardowe_ch2_wyskalowane))
    print('')
    print(
        "Dla ch2 wartośc średnia powiększona o trzykrotnośc odchylenia standardowego to {}, a wiekszych rekordow od tej wartosci jest {}".format(
            wart_powiekszonach2, licznik_0))
    print('')
    print(
        "Dla ch2 wartośc średnia pomniejszona o trzykrotnośc odchylenia standardowego to {}, a mniejszych rekordow od tej wartosci jest {}".format(
            wart_pomniejszonach2, licznik_1))
    print('')

    zmienna_do_wyskalowania_ch3 = (max(tablicach3) + min(tablicach3)) / 2
    tablica_ch3_wyskalowana = []
    for y in tablicach3:
        y = y - zmienna_do_wyskalowania_ch3
        tablica_ch3_wyskalowana.append(y)
    wartoscsrednia_ch3_wyskalowana = np.mean(tablica_ch3_wyskalowana)
    odchyleniestandardowe_ch3_wyskalowane = statistics.stdev(tablica_ch3_wyskalowana)

    wartoscsrednia_ch3 = np.mean(tablicach3)
    odchyleniestandardowe_ch3 = statistics.stdev(tablicach3)
    wart_powiekszona_ch3 = wartoscsrednia_ch3 + 3 * odchyleniestandardowe_ch3
    wart_pomniejszona_ch3 = wartoscsrednia_ch3 - 3 * odchyleniestandardowe_ch3

    licznik_00 = 0
    licznik_11 = 0
    for y in tablicach3:
        if y > wart_powiekszona_ch3:
            licznik_00 += 1
        elif y < wart_pomniejszona_ch3:
            licznik_11 += 1
        else:
            continue
    print('Wartośc średnia dla ch3 to {} V, natomiast odchylenie standardowe {}'.format(wartoscsrednia_ch3,
                                                                                        odchyleniestandardowe_ch3))
    print('')
    print('Po wyskalowaniu wartośc średnia dla ch3 to {} V, natomiast odchylenie standardowe {}'.format(
        wartoscsrednia_ch3_wyskalowana,
        odchyleniestandardowe_ch3_wyskalowane))
    print('')
    print(
        "Dla ch3 wartośc średnia powiększona o trzykrotnośc odchylenia standardowego to {}, a wiekszych rekordow od tej wartosci jest {}".format(
            wart_powiekszona_ch3, licznik_00))
    print('')
    print(
        "Dla ch3 wartośc średnia pomniejszona o trzykrotnośc odchylenia standardowego to {}, a mniejszych rekordow od tej wartosci jest {}".format(
            wart_pomniejszona_ch3, licznik_11))
    print('')


    


def rysowaniehistogramu(csv_file):
    x = wpisaniedopojedynczychtablic(csv_file)
    tablicach2 = x[0]
    tablicach3 = x[1]

    k = round(math.sqrt(len(tablicach2)))

    plt.subplot(211)
    plt.hist(tablicach2, bins=k, rwidth=0.5, color='blue', edgecolor='black', label=r'$ch2$')
    plt.legend(loc='best')
    plt.ylabel('liczebność')
    plt.title('Histogramy ch2 oraz ch3')

    plt.subplot(212)
    plt.hist(tablicach3, bins=k, rwidth=0.5, color='red', edgecolor='black', label=r'$ch3$')
    plt.legend(loc='best')
    plt.xlabel('[V]')
    plt.ylabel('liczebność')
    plt.savefig('histogramy.png')

    '''Z histogramu ch2 widzimy, że wartości wystepujące najczęściej to te blisko najmniejszej i największej wartości, 
    natomiast reszta wartości występuje niemal równomiernie, jesli wystepują różnice to w podobnych odstępach i z tego 
    można z teog wywnioskować że może być to histogram funkcji sinosoidalnej.
    Z histogramu ch3 można zauważyć że rozłożenie wartości jest rózne i ciężko wyciągnąć z tego jakieś wnioski, 
    jedynie mozna zauważyć że wartośc występująca najczęsciej to w okolicy -0.002'''

if __name__ == '__main__':
    
    #read_csv('01169356.csv')
    print(dodanieczasuizapisaniedotablicyy('01169356.csv')) 
    zapisdopliku('01169356.csv', 'mojplik.txt')
    rysowaniewykresow('01169356.csv')
    rysowaniewykresu_ch3_ch2('01169356.csv')
    wartoscimaksminsrednia('01169356.csv')
    okresprzebiegu('01169356.csv')
    wartoscsrednia_odchyleniestandardowe('01169356.csv')
    rysowaniehistogramu('01169356.csv')