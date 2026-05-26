# Gwiezdnowyprawa - gra dla poszukiwaczy gwiezdnych przygód

## Witaj austronauto! Przed uruchomieniem silników musisz skonfigurować parametry lotu.

Witaj graczu gwiezdej przygody.
### Plan gry
1. musisz skonfigurować parametry lotu
2. wybieraj jedną z trzech możliwych opcji, uważaj, postępuj rozsądnie
3. spróbuj wygrać grę (nie wyleć w kosmos, nie zużyj całej energii, wytrwaj jak najdłużej)

### Przebieg gry

Po uruchomieniu gracz odpowiada na pytania początkowe ustawiające grę:

```text
~~~ TERMINAL STARTOWY MISJI BADAWCZEJ ~~~
Witaj austronauto! Przed uruchomieniem silników musisz skonfigurować parametry lotu.
OBJAŚNIENIE PARAMETRÓW:
- Jak ma się nazywać twój statek kosmiczny.
- Start X i Y: Skąd wyruszy twój statek (sugerowane od -50 do 50).
- Kąt startowy: Kierunek, w którym początkowo zwrócony jest dziób statku (0° to wschód, 90° północ).
- Zapas energii: Twój główny zasób życiowy. Każdy manewr i anomalia zużywa lub odnawia energię.

Podaj kryptonim misji (domyślnie Gwiezdnowyprawa): 
Podaj startowy X (domyślnie 0): 
Nieprawidłowy format. Przyjęto wartość domyślną: 0
Podaj startowy Y (domyślnie 0): 
Nieprawidłowy format. Przyjęto wartość domyślną: 0
Podaj początkowy kąt lotu w stopniach 0-359 (domyślnie 90): 
Nieprawidłowy format. Przyjęto wartość domyślną: 90°
Podaj początkowy zapas energii (domyślnie 150): 
Nieprawidłowy format. Przyjęto wartość domyślną: 150
```

Później wybiera jedną z 3 opcji: 
```text
--- [ KROK 1 / 40 ] ---
Wybierz strategię na ten krok:
1. Cała naprzód (Duży dystans, wysokie zużycie energii)
2. Precyzyjna nawigacja (Średni dystans, korekta kąta losowo o -15° do 15°, średni koszt)
3. Tryb przetrwania (Mały dystans, regeneracja energii, ryzyko dryfu)
Wybierz: (1/2/3): 
```

Przy każdej rundzie dostaje informację o jej przebiegu:
```text
Akcja:          Cała naprzód
Pozycja:        (-46, 113) -> (-71, 113) [Bieżący kąt: 180°]
Energia:        15 -> 0
Element świata: Brak
Wyjaśnienie:    Lot zgodnie z planem. Zużyto 15 energii na dystansie 25.
```
Na koniec gry wyświetlana jest informacja końcowa z raportem podsumowującym:
```text
==================================================
               RAPORT KOŃCOWY WYPRAWY             
==================================================
Nazwa wyprawy:         Gwiezdnowyprawa
Parametry początkowe:  Start w punkcie (0, 0), kąt 90°, zapas 150 energii
Końcowa pozycja:       (-71, 113)
Liczba wykonanych kroków: 10
Pozostały zasób:       0 jednostek energii
Przyczyna zakończenia: Skończyła ci się energia.

Rejestr najważniejszych zdarzeń i anomalii:
- Krok 1: Złoże Antymaterii
- Krok 6: Deszcz Asteroid
- Krok 9: Mgławica Jonowa
```
Na koniec gracz decyduje czy chce wyświetlić graficznie trasę statku i czy chce grać jeszcze raz.

***

Wymagania: python 3.11, przetestowane na laptopie windows.

Uruchomienie w katalogu z plikiem gry: ``` python main.py```
