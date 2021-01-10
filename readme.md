# Genetischer Algorithmus für ein Zwei-Rucksack-Problem
Code for BWI - Coding Challenge

## Problemstellung

Gegeben sind 2 LKWs, welche eine Bestimmte Menge an Objekten transportieren sollen. Anhand einer Liste an Objekten und Parametern der LKWs soll eine optimale Ladeliste erzeugt werden.

## Gewählter Algorithmus

Zur Lösung des Problems wurde ein genetischer Algorithmus gewählt. Hierbei werden die zu bestimmenden Größen in Sequenzen aus 0 und 1 codiert und mit aus der Natur bekannten Methoden der Evolution verändert, um eine optimale Lösung zu finden. Wichtig hierbei ist jedoch, dass die Lösung vom Startwert abhängig ist. Das bedeutet bei jedem Durchlauf des Algorithmus kann ein anderes Ergebnis erreicht werden. In den test wurden Ergebnisse von etwa 73000 für den Gesamtwert erzielt.

## Kurzanleitung

Die Datei [genetic_algorithm.py](https://github.com/CeKl/Genetischer-Algorithmus/blob/master/genetic_algorithm.py) kann entweder an sich unter Ptyhon 3 ausgeführt werden (Requirements am Ender dieser Seite beachten) oder importiert werden. Die Hardware, welche verteilt werden soll, wird in der Datei [hardware_data.csv](https://github.com/CeKl/Genetischer-Algorithmus/blob/master/hardware_data.csv) nach folgendem Schema hinterlegt:

| Hardware           | Anzahl Einheiten [-] | Gewicht [g] | Nutzwert pro Einheit [-] |
| ------------------ | -------------------- | ----------- | ------------------------ |
| Notebook Buero 13" | 205                  | 2451        | 40                       |
| Notebook Buero 14" | 420                  | 2978        | 35                       |

Die Daten der LKWs, auf welche Die Hardware verteilt werden soll wird in der Datei [fahrzeug_data.csv](https://github.com/CeKl/Genetischer-Algorithmus/blob/master/fahrzeug_data.csv) nach folgendem Schema hinterlegt:

| Gewicht Fahrer [kg] | Gewicht LKW [kg] |
| ------------------- | ---------------- |
| 72.4                | 1100             |
| 85.7                | 1100             |

Durch das Ausführen des Algorithmus wird eine CSV-Datei mit dem Namen result_WERT.csv erstellt. Diese enthält die Ladeliste für die jeweiligen LKWs, sowie das Gewicht und den Wert. Hier das Beispiel einer möglichen Ladeliste mit einem Wert von 73884:

| Objekt                  | Anzahl   | Wert  | Gewicht     | LKW     |
| ----------------------- | -------- | ----- | ----------- | ------- |
| Notebook Buero 13"      | 0        | 0     | 0           | 1       |
| Notebook Buero 14"      | 0        | 0     | 0           | 1       |
| Notebook outdoor        | 12       | 960   | 43500       | 1       |
| Mobiltelefon Buero      | 27       | 810   | 19359       | 1       |
| Mobiltelefon Outdoor    | 95       | 5700  | 93860       | 1       |
| Mobiltelefon Heavy Duty | 110      | 7150  | 134200      | 1       |
| Tablet Buero klein      | 246      | 9840  | 345630      | 1       |
| Tablet Buero gross      | 89       | 3560  | 129495      | 1       |
| Tablet outdoor klein    | 15       | 675   | 25350       | 1       |
| Tablet outdoor gross    | 119      | 8092  | 235620      | 1       |
| LKW 0                   | LKW-Wert | 36787 | LKW-Gewicht | 1027014 |
| Notebook Buero 13"      | 0        | 0     | 0           | 2       |
| Notebook Buero 14"      | 0        | 0     | 0           | 2       |
| Notebook outdoor        | 1        | 80    | 3625        | 2       |
| Mobiltelefon Buero      | 29       | 870   | 20793       | 2       |
| Mobiltelefon Outdoor    | 61       | 3660  | 60268       | 2       |
| Mobiltelefon Heavy Duty | 109      | 7085  | 132980      | 2       |
| Tablet Buero klein      | 124      | 4960  | 174220      | 2       |
| Tablet Buero gross      | 63       | 2520  | 91665       | 2       |
| Tablet outdoor klein    | 22       | 990   | 37180       | 2       |
| Tablet outdoor gross    | 249      | 16932 | 493020      | 2       |
| LKW 1                   | LKW-Wert | 37097 | LKW-Gewicht | 1013751 |
| Gesamtwert:             | 73884    |       |             |         |


## Funktionsweise

### 1. Population generieren:

Für jedes Element der Hardware-Liste wird zwei Mal eine zufällige Anzahl an Einheiten gewählt. Die Summe der gewählten Einheiten darf nicht größer sein als die maximmal mögliche Menge an Einheiten.

### 2. Individuen Kreuzen

Je zwei Individuen werden miteinander gekreuzt. Das bedeutet ein Teil des Genoms (Folge aus 0 und 1), welches der Anzahl an Elementen entspricht, wird ausgetauscht. Außerdem wird gibt es die Möglichkeit einer Mutation (Austausch von einer 0 gegen eine 1 oder andersherum).

### 3. Ungültige Individuen aussortieren:

Individuen, die das Maximalgewicht der LKWs überschreiten, mehr Elemente besitzen als tatsächlich vorhanden sind oder keinen Wert haben werden aussortiert. Falls alle Individuen ungültig sind werden neue Individuen erzeugt.
   
### 4. Individuen beibehalten

Die besten Individuen + 10% zufällig ausgewählte Individuen werden in der nächsten Generation genutzt.

### 5. Wiederhohlen

Diese Schritt werden wiederholt, bis die maximale Anzahl an Generationen oder bis derselbe Maximalwert der jeweiligen Generation mehrmals erreicht wurden. Anschließend wird die Beste Lösung im Terminal und als CSV_Datei (inklusive Wert in Dateiname) ausgegeben.

## Requirements
- numpy
