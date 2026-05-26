import random
import math
import time
import turtle

# ==========================================
# 1. PARAMETRY STARTOWE
# ==========================================
def pobierz_parametry():
    print("~~~ TERMINAL STARTOWY MISJI BADAWCZEJ ~~~")
    print("Witaj austronauto! Przed uruchomieniem silników musisz skonfigurować parametry lotu.")
    print("OBJAŚNIENIE PARAMETRÓW:")
    print("- Jak ma się nazywać twój statek kosmiczny.")
    print("- Start X i Y: Skąd wyruszy twój statek (sugerowane od -50 do 50).")
    print("- Kąt startowy: Kierunek, w którym początkowo zwrócony jest dziób statku (0° to wschód, 90° północ).")
    print("- Zapas energii: Twój główny zasób życiowy. Każdy manewr i anomalia zużywa lub odnawia energię.\n")
    
    nazwa = input("Podaj kryptonim misji (domyślnie Gwiezdnowyprawa): ") or "Gwiezdnowyprawa"
    
    try:
        start_x = int(input("Podaj startowy X (domyślnie 0): "))
    except ValueError:
        print("Nieprawidłowy format. Przyjęto wartość domyślną: 0")
        start_x = 0
        
    try:
        start_y = int(input("Podaj startowy Y (domyślnie 0): "))
    except ValueError:
        print("Nieprawidłowy format. Przyjęto wartość domyślną: 0")
        start_y = 0
        
    try:
        ## % 360 - modulo 360 zeby zawsze dostac dobry kat, np 370 % 360 = 10 (nadmiarowe 10 stopni staje sie wynikiem)
        kat_startowy = int(input("Podaj początkowy kąt lotu w stopniach 0-359 (domyślnie 90): ")) % 360
    except ValueError:
        print("Nieprawidłowy format. Przyjęto wartość domyślną: 90°")
        kat_startowy = 90
        
    while True:
        try:
            energia = int(input("Podaj początkowy zapas energii (domyślnie 150): "))
            if energia <= 0:
                print("Energia musi być liczbą dodatnią. Spróbuj ponownie.")
                continue
            break
        except ValueError:
            print("Nieprawidłowy format. Przyjęto wartość domyślną: 150")
            energia = 150
            break
    limit_granic = 200
    print("\n=========================================")
    print("        PARAMETRY PRZEDSTARTOWE          ")
    print("=========================================")
    print(f"Nazwa wyprawy:      {nazwa}")
    print(f"Pozycja startowa:   ({start_x}, {start_y})")
    print(f"Kąt startowy:       {kat_startowy}°")
    print(f"Początkowa energia b:   {energia} jedn. energii")
    print(f"Granice świata:     Od -{limit_granic} do {limit_granic} na osiach X i Y")
    print("Warunki końca:      1. Spadek energii do 0")
    print("                    2. Zagubienie w głębokim kosmosie (ucieczka poza sektor)")
    print("                    3. Osiągnięcie maksymalnego czasu trwania misji (40 kroków)")
    print("Cel wyprawy:        Przelecieć jak najdłuższy dystans, optymalizując zasoby.")
    print("=========================================\n")
    ## funkcja zwaraca slowni (dict)
    return {
        "nazwa": nazwa,
        "x": start_x,
        "y": start_y,
        "kat": kat_startowy,
        "energia": energia,
        "limit": limit_granic,
        "start_pos": (start_x, start_y)
    }

# ==========================================
# 2. AKCJA - WYBOR
# ==========================================
def wybor_akcji():
    print("Wybierz strategię na ten krok:")
    print("1. Cała naprzód (Duży dystans, wysokie zużycie energii)")
    print("2. Precyzyjna nawigacja (Średni dystans, korekta kąta losowo o -15° do 15°, średni koszt)")
    print("3. Tryb przetrwania (Mały dystans, regeneracja energii, ryzyko dryfu)")
    
    while True:
        wybor = input("Wybierz: (1/2/3): ").strip()
        if wybor in ["1", "2", "3"]:
            return wybor
        print("Błąd. Wybierz poprawną cyfrę: 1, 2 lub 3.")

# ==========================================
# 3. SYMULACJA KROK PO KROKU
# ==========================================
def uruchom_symulacje(p):
    x, y = p["x"], p["y"]
    kat = p["kat"]
    energia = p["energia"]
    limit = p["limit"]
    
    krok = 0
    historia_lotu = [(x, y)]
    zdarzenia_log = []
    odleglosc_od_startu = 0.0
    
    while True:
        krok += 1
        stare_x, stare_y = x, y
        stara_energia = energia
        
        print(f"\n--- [ KROK {krok} / 40 ] ---")
        wybor = wybor_akcji()
        
        if wybor == "1":
            dystans = 25
            koszt = 15
            nazwa_akcji = "Cała naprzód"
            wyjasnienie = f"Lot zgodnie z planem. Zużyto {koszt} energii na dystansie {dystans}."
        elif wybor == "2":
            dystans = 15
            koszt = 8
            kat = (kat + random.randint(-15, 15)) % 360
            nazwa_akcji = "Precyzyjna nawigacja"
            wyjasnienie = f"Lot zgodnie z planem. Zużyto {koszt} energii na dystansie {dystans}."
        else:
            dystans = 5
            koszt = -5  
            kat = (kat + random.randint(-45, 45)) % 360
            nazwa_akcji = "Tryb przetrwania"
            wyjasnienie = f"Dryf i regeneracja. Odzyskano {-koszt} energii, dystans {dystans}."
        ## korzystamy z wlasciwosci trojkata prostokatnego zeby obliczyc x,y
        ## radians - funkcje w python oczekuja radianow
        ## math.cos(kat) - cosinus, znamy przeciwprostokatna, musimy obliczyc x
        ## math.sin(kat) - sinus, znamy przeciwprostokatna, musimy obliczyc y
        x += int(math.cos(math.radians(kat)) * dystans)
        y += int(math.sin(math.radians(kat)) * dystans)
        energia -= koszt
        
        element_swiata = "Brak"
        
        # Elementy swiata i zdarzenia losowe (3 typy)  -- moj komentarz: fajnie byloby utworzyc wiecej, cala biblioteke :) 
        szansa = random.random()
        if szansa < 0.15:
            # Element 1: Deszcz asteroid (Przeszkoda)
            energia -= 20
            kat = (kat + 90) % 360
            element_swiata = "Deszcz Asteroid"
            wyjasnienie = "Kadłub uszkodzony meteorami (-20 energii), statek gwałtownie obróciło o 90 stopni!"
        elif 0.15 <= szansa < 0.30:
            # Element 2: Zloze antymaterii (Bonus)
            energia += 30
            element_swiata = "Złoże Antymaterii"
            wyjasnienie = "Kolektory statku zassały kosmiczne paliwo z otoczenia (+30 energii)."
        elif 0.30 <= szansa < 0.35:
            # Element 3: Mglawica Jonowa (Niebezpieczne pole / Skrot)
            ## losuje liczbe z przedzialu -40 do 40, zamiast plynnego przelotu jest skok w przestrzeni
            x += random.randint(-40, 40)
            y += random.randint(-40, 40)
            energia -= 10
            element_swiata = "Mgławica Jonowa"
            wyjasnienie = "Silne wyładowania i niestabilność grawitacyjna przeniosły statek w nieznane koordynaty (-10 energii)."

        # Kontrola barier swiata
        if x > limit or x < -limit or y > limit or y < -limit:
            energia -= 25
            element_swiata += " (Uderzenie w barierę)"
            wyjasnienie += " Próba opuszczenia sektora! Pola siłowe odrzuciły statek z powrotem (-25 energii)."
            x, y = stare_x, stare_y  # Bezpieczne cofnicie pozycji
            
        historia_lotu.append((x, y))
        if element_swiata != "Brak":
            zdarzenia_log.append(f"Krok {krok}: {element_swiata}")
            
        # Wypisywanie stanu w konsoli krok po kroku
        print(f"Akcja:          {nazwa_akcji}")
        ## symbol ° po option + shift + 8
        print(f"Pozycja:        ({stare_x}, {stare_y}) -> ({x}, {y}) [Bieżący kąt: {kat}°]")
        print(f"Energia:        {stara_energia} -> {energia}")
        print(f"Element świata: {element_swiata}")
        print(f"Wyjaśnienie:    {wyjasnienie}")
        ## odleglosc euklidesowa - miedzy dwoma punktami na plaszczyznie (twierdzenie Pitagorasa)
        odleglosc_od_startu = math.sqrt((x - p["start_pos"][0])**2 + (y - p["start_pos"][1])**2)
        
        # Sprawdzanie 3 warunkow zakonczenia symulacji
        if energia <= 0:
            powod_konca = "Skończyła ci się energia."
            break
        if odleglosc_od_startu > limit + 50: 
            powod_konca = "Wyleciałeś poza mapę i zaginąłeś w głębokim kosmosie."
            break
        if krok >= 40:
            powod_konca = "Skończył się czas (40 kroków)."
            break
            
    # Algorytm punktacji
    wynik_punktowy = int(odleglosc_od_startu + (energia if energia > 0 else 0) * 2)
    if wynik_punktowy > 250 and energia > 0:
        status = "WYGRAŁEŚ"
    elif wynik_punktowy > 100:
        status = "PRAWIE WYGRAŁEŚ"
    else:
        status = "PRZEGRAŁEŚ"
        
    return {
        "historia": historia_lotu,
        "kroki": krok,
        "energia": energia,
        "zdarzenia": zdarzenia_log,
        "powod": powod_konca,
        "koniec_x": x,
        "koniec_y": y,
        "wynik": wynik_punktowy,
        "status": status
    }

# ==========================================
# 4. PODSUMOWANIE
# ==========================================
def wyswietl_raport(wynik, p):
    print("\n" + "="*50)
    print("               RAPORT KOŃCOWY WYPRAWY             ")
    print("="*50)
    print(f"Nazwa wyprawy:         {p['nazwa']}")
    print(f"Parametry początkowe:  Start w punkcie {p['start_pos']}, kąt {p['kat']}°, zapas {p['energia']} energii")
    print(f"Końcowa pozycja:       ({wynik['koniec_x']}, {wynik['koniec_y']})")
    print(f"Liczba wykonanych kroków: {wynik['kroki']}")
    print(f"Pozostały zasób:       {max(0, wynik['energia'])} jednostek energii")
    print(f"Przyczyna zakończenia: {wynik['powod']}")
    
    print("\nRejestr najważniejszych zdarzeń i anomalii:")
    if not wynik['zdarzenia']:
        print("- Cały lot przebiegł w spokojnej próżni.")
    else:
        for z in wynik['zdarzenia']:
            print(f"- {z}")
            
    print("\n--------------------------------------------------")
    print(f"KOŃCOWY WYNIK PUNKTOWY: {wynik['wynik']} punktów")
    print(f"STATUS MISJI:           {wynik['status']}")
    print("="*50)

# ==========================================
# 5. WIZUALIZACJA TURTLE 
# ==========================================
def narysuj_trase(historia, p):
    odpowiedz = input("\nCzy chcesz zobaczyć wizualizację trasy? (t/n): ")
    if odpowiedz.lower() != 't':
        return

    try:
        # Konfiguracja poczatkowa
        screen = turtle.Screen()
        screen.setup(650, 650)
        screen.clear()
        screen.bgcolor("#080810")
        screen.title(f"Droga: {p['nazwa']}")
        
        t = turtle.Turtle()
        t.speed(0)
        t.hideturtle()
        
        # Rysowanie osi pomocniczych
        t.color("#202035")
        t.pensize(1)
        # Os X
        t.penup()
        t.goto(-p["limit"] - 20, 0)
        t.pendown()
        t.goto(p["limit"] + 20, 0)
        # Os Y
        t.penup()
        t.goto(0, -p["limit"] - 20)
        t.pendown()
        t.goto(0, p["limit"] + 20)
        
        # Rysowanie granicy swiata
        t.penup()
        t.goto(-p["limit"], -p["limit"])
        t.pendown()
        t.color("red")
        t.pensize(2)
        for _ in range(4):
            t.forward(p["limit"] * 2)
            t.left(90)
            
        # Punkt startowy
        t.penup()
        start_x, start_y = historia[0]
        t.goto(start_x, start_y)
        t.color("cyan")
        t.dot(10)
        
        # Scieżka lotu
        t.color("white")
        t.pensize(2)
        t.pendown()
        t.speed(3)
        for pkt_x, pkt_y in historia:
            t.goto(pkt_x, pkt_y)
            
        # Punkt koncowy
        t.color("gold")
        t.dot(12)
        
        print("\n[Grafika zaktualizowana] Przejdź z powrotem do terminala, aby kontynuować.")
        print("WAŻNE: Nie zamykaj okna wizualizacji krzyżykiem, zaktualizuje się ono samo w kolejnej grze!")

    except turtle.Terminator:
        print("\n[Błąd] Okno wizualizacji zostało ręcznie zamknięte. Aby przywrócić grafikę, musisz zrestartować program.")
    except Exception as e:
        print(f"\n[Błąd wizualizacji]: {e}")

# ==========================================
# 6. GŁÓWNA PĘTLA PROGRAMU
# ==========================================
def main():
    while True:
        parametry = pobierz_parametry()
        wynik = uruchom_symulacje(parametry)
        wyswietl_raport(wynik, parametry)
        narysuj_trase(wynik["historia"], parametry)
        
        decyzja = input("\nCzy chcesz uruchomić symulację ponownie z nowymi parametrami? (t/n): ")
        if decyzja.lower() != 't':
            print("System nawigacji wyłączony. Powodzenia w kolejnych misjach!")
            break

if __name__ == "__main__":
    main()
