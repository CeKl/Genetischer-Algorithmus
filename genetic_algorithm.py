# -*- coding: utf-8 -*-

import numpy as np
import random
import math
import csv
import pathlib


class genertic_algorithem():
    '''
    Genetischer Algortihmus zum Berechnen einer optimalen Verteilung von Hardware (hardware_data.csv) auf LKWs (fahrezug_data.csv).
    Das Ergebnis wird in Form einer CS-Datei mit dem Wert im Dateinamen bereitgestellt

    Args:
            show_status (bool): Ausgabe der aktuellen Generation an/aus
            num_backup (int): Anzahl der Individuen, welche genereirt werden soll, sobald alle bisherigen Individuen ungültig sind
            start_population (int): Anzahl Individuen in Startpopulation
            num_repeat_stop (int): Zahl an Generationen mit selbem Wert die für Abbruch sorgt
            num_max_gen (int): maximale Anzahl an Generationen        
    '''
    def __init__(self, show_status=True, num_backup=100, start_population=1000, num_repeat_stop=10, num_max_gen=200):
        self.path_parent = str(pathlib.Path(__file__).parent.absolute())
        self.path_parent = self.path_parent.replace("\\", '/')

        self.hardware_data = self.open_hardware_data()
        self.lkw_data = self.open_fahrzeug_data()

        self.num_max_gen = num_max_gen
        self.num_repeat_stop = num_repeat_stop

        self.num_backup = num_backup
        self.start_population = start_population

        self.show_status = show_status

    def open_hardware_data(self):
        '''Hardwaredaten aus csv laden.'''
        data_output = {}
        with open(self.path_parent + '/hardware_data.csv') as csvDataFile:
            csvReader = csv.reader(csvDataFile, delimiter=';')
            next(csvReader)
            for row in csvReader:
                data_output[row[0]] = {'anzahl': int(
                    row[1]), 'gewicht': int(row[2]), 'nutzen': int(row[3])}
        return data_output

    def open_fahrzeug_data(self):
        '''Fahrezugdaten aus csv laden.'''
        data_output = []
        with open(self.path_parent + '/fahrzeug_data.csv') as csvDataFile:
            csvReader = csv.reader(csvDataFile, delimiter=';')
            next(csvReader)
            for row in csvReader:
                data_output.append(int(row[1])*1000 - int(float(row[0])*1000))
        return data_output

    def generieren(self, n=1000):
        '''Population generieren.'''
        output = []
        for i in range(n):
            new_ind = [[], []]
            for item_key in self.hardware_data:
                item_max_number = self.hardware_data[item_key]['anzahl']

                # 2 zufällige Zahlen unter Maximalwert für Anzal an Items
                last_random = 0
                for rand_index in range(2):
                    last_random = random.randint(
                        0, int((item_max_number - last_random)/2))

                    gen_value = "{:010b}".format(last_random)
                    new_ind[rand_index].append(gen_value)

            output.append(new_ind)
        return output

    def validieren(self, val_ind):
        '''Nicht valide Individuen (zu schwer, kein Wert) aussortieren.'''
        val_ind_output = []
        val_fitness = []
        for individuum in val_ind:
            fitness_ind = 0
            valide_buffer = 0
            anzahl_max = [self.hardware_data[item_key]['anzahl'] for item_key in self.hardware_data]
            invalide_anzahl = True
            for lkw_index, lkw in enumerate(individuum):
                gewicht = 0
                wert = 0
                for item_index, item_key in enumerate(self.hardware_data):
                    anzahl = int(lkw[item_index], 2)
                    anzahl_max[item_index] = anzahl_max[item_index] - anzahl

                    if anzahl_max[item_index] <= 0:
                        invalide_anzahl = False
                        break

                    gewicht_objekt = self.hardware_data[item_key]['gewicht']
                    wert_objekt = self.hardware_data[item_key]['nutzen']

                    gewicht += anzahl * gewicht_objekt
                    wert += anzahl * wert_objekt

                if invalide_anzahl:
                    if ((gewicht <= self.lkw_data[lkw_index]) and (wert >= 1)):
                        fitness_ind += wert
                        valide_buffer += 1
                    else:
                        break
                else:
                    break

            if valide_buffer == 2:
                val_ind_output.append(individuum)
                val_fitness.append(fitness_ind)

        return val_ind_output, val_fitness

    def mix_ind(self, leb_1, leb_2):
        '''Zwei Individuen kreuzen.'''
        ind_1 = []
        ind_2 = []
        for lkw in range(2):
            gen_1_output = []
            gen_2_output = []
            for item_index, _ in enumerate(self.hardware_data):
                gen_1 = leb_1[lkw][item_index]
                gen_2 = leb_2[lkw][item_index]

                pos_cut = random.randint(1, 9)

                gen_1_new = gen_1[:pos_cut] + gen_2[pos_cut:]
                gen_2_new = gen_2[:pos_cut] + gen_1[pos_cut:]

                gen_1_output.append(gen_1_new)
                gen_2_output.append(gen_2_new)
            ind_1.append(gen_1_output)
            ind_2.append(gen_2_output)

        return ind_1, ind_2

    def flip(self, ind):
        '''Stelle mutieren / tauschen.'''
        lkw = random.randint(0, 1)
        gen = random.randint(0, 9)
        pos = random.randint(0, 9)

        base_gen = ind[lkw][gen]

        if base_gen[pos] == '1':
            new_flip = base_gen[:pos] + '0' + base_gen[pos + 1:]
        else:
            new_flip = base_gen[:pos] + '1' + base_gen[pos + 1:]

        ind[lkw][gen] = new_flip

        return ind

    def kreuzen(self, individuums, num_repeat=100):
        '''Hilfsfunktion Kreuzen.'''
        num_ind = len(individuums)

        output_individuums = []

        # Kreuzen
        for _ in range(num_repeat):
            cross_ind = np.random.permutation(num_ind)[:2].tolist()

            childes = self.mix_ind(
                individuums[cross_ind[0]], individuums[cross_ind[1]])

            output_individuums += childes

        # Mutieren einzelner Individuen -> Wechsel eriner Zahl (0 oder 1) an einer zufälligen stelle
        for ind in individuums:
            for _ in range(1, 10):
                if random.randint(0, 5) == 1:
                    ind = self.flip(ind)

        return output_individuums + individuums

    def best(self, search_ind):
        '''Beste Individuen mit Position ausgeben.'''

        if len(search_ind) <= 10:
            keep_faktor = 1
        elif len(search_ind) <= 100:
            keep_faktor = 0.5
        elif len(search_ind) <= 200:
            keep_faktor = 0.4
        elif len(search_ind) <= 300:
            keep_faktor = 0.3
        elif len(search_ind) <= 500:
            keep_faktor = 0.25
        elif len(search_ind) <= 1000:
            keep_faktor = 0.1
        else:
            keep_faktor = 0.01

        num_keep = math.ceil(len(search_ind)*keep_faktor)

        if len(search_ind) > 2000:
            num_keep = 2000

        ranks = sorted([(x, i)
                        for (i, x) in enumerate(search_ind)], reverse=True)
        values = []
        positions = []
        for x, y in ranks:
            if x not in values:
                values.append(x)
                positions.append(y)
                if len(values) == num_keep:
                    break
        return values, positions

    def run(self):

        # 1. Startpopulation generieren
        individuen = self.generieren(n=self.start_population)

        current_gen = 0
        child_ind_val = 0
        child_fit_val = 0

        best_tracking = [i*-1 for i in range(self.num_repeat_stop)]

        # Ende sobald der selebe Wert mehrmals erreicht wurde oder max generationen erreicht
        while ((best_tracking.count(best_tracking[0]) != len(best_tracking)) and (current_gen < self.num_max_gen)):

            # 2. Indiviuen Kreuzen
            child_ind = self.kreuzen(individuen, num_repeat=10*(current_gen+1))

            # 3. Ungültige Individuen (zu hohes Gewicht oder kein Wert) aussortieren
            child_ind_val, child_fit_val = self.validieren(child_ind)

            # Wenn alle Individuen nicht gültig mit 100 neune Individueen fortfahren
            if len(child_ind_val) == 0:
                child_ind_val = self.generieren(n=self.num_backup)
                child_fit_val = [0 for i in range(self.num_backup)]

            if self.show_status:
                print('Generation {} - Anzahl Individuen {} - Bester Wert {}'.format(current_gen,
                                                                                 len(child_ind_val), np.amax(np.array(child_fit_val))))

            # besten Indiviuden ermitteln
            _, best_list = self.best(child_fit_val)

            # tracken bester Wert für Abbruch
            best_tracking.pop(0)
            best_tracking.append(np.amax(np.array(child_fit_val)))

            # 4. Die betsen Individuen werden behalten + 10% zufällige Individuen
            keep_individuen = []
            for keep_index in best_list:
                keep_individuen.append(child_ind_val[keep_index])

            num_lucky_ind = math.ceil(len(child_ind_val)*0.1)
            individuen = keep_individuen + np.random.permutation(child_ind_val)[:num_lucky_ind].tolist() + self.generieren(n=100)

            current_gen += 1

        print('letzt Generation fertig')

        _, best_list = self.best(child_fit_val)
        best_ind = child_ind_val[best_list[0]]
        best_ind, best_fit = self.validieren([best_ind])
        if len(best_ind) == 0:
            print('error')

        # 5. Ausgabe der besten Lösung
        self.print_best(best_ind[0], best_fit[0])

        return best_ind[0], best_fit[0]

    def print_best(self, best_ind, best_fit):
        '''Endergebnis ausgeben und als csv speichern.'''
        csv_table = []
        for lkw_index, lkw in enumerate(best_ind):
            print('')
            print('LWK {}:'.format(lkw_index))
            gewicht = 0
            wert = 0
            for item_index, item_key in enumerate(self.hardware_data):
                anzahl = int(lkw[item_index], 2)

                gewicht_objekt = self.hardware_data[item_key]['gewicht']
                wert_objekt = self.hardware_data[item_key]['nutzen']

                gewicht += anzahl * gewicht_objekt
                wert += anzahl * wert_objekt

                row = []
                row.append(item_key)                    # Spaltenkopf
                row.append(anzahl)                      # Anzahl
                row.append(wert_objekt * anzahl)        # Wert
                row.append(gewicht_objekt * anzahl)     # Gewicht
                row.append(lkw_index + 1)               # LKW
                csv_table.append(row)

                print('item {} - anzahl {}'.format(item_key, anzahl))
            print('LWK-Gewicht: {} - LKW-Wert: {}'.format(gewicht, wert))
            row = []
            row.append('LKW {}'.format(lkw_index))
            row.append('LKW-Wert')
            row.append(wert)
            row.append('LKW-Gewicht')
            row.append(gewicht)
            csv_table.append(row)

        print('Wert {}'.format(best_fit))
        row = []
        row.append('Gesamtwert: ')
        row.append(best_fit)
        row.append('')
        row.append('')
        row.append('')
        csv_table.append(row)

        csv_top = ['Objekt', ' Anzahl', 'Wert', 'Gewicht', 'LKW']

        with open('{}/result_{}.csv'.format(self.path_parent, best_fit), 'w') as file:
            csv_write = csv.writer(file)
            csv_write.writerow(csv_top)
            csv_write.writerows(csv_table)


if __name__ == "__main__":
    # help(genertic_algorithem())
    genertic_algorithem().run()

    # test
    #"""
    werte = []
    for i in range(20):
        _, rundenwert = genertic_algorithem(show_status=False).run()
        werte.append(rundenwert)
        print('run test {} - Wert: {}'.format(i, rundenwert))

    print(sum(werte)/len(werte))
    #"""

print('done')
