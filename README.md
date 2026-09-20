# Better Calculator

Prosty kalkulator desktopowy dla Windows, inspirowany układem kalkulatora Google. Ma tryb jasny i ciemny, historię działań, pamięć i obsługę klawiatury.

## Funkcje

- jasny, szeroki interfejs desktopowy,
- działania `+`, `-`, `×`, `÷`, `%`, potęgi przez `**` oraz nawiasy,
- historia trzech ostatnich obliczeń,
- pamięć kalkulatora: `M+`, `M−`, `MRC`,
- szybkie akcje: zmiana znaku, wklejenie wyniku i kopiowanie do schowka,
- przycisk czyszczenia historii działań,
- obsługa klawiatury: Enter oblicza, Esc czyści, Backspace usuwa znak,
- bezpieczne obliczanie wyrażeń bez używania `eval`,
- instalator dodający komendę `better-calculator` do CMD i PowerShell,
- skrót na pulpicie i w menu Start.

## Wymagania

- Windows 10 lub nowszy,
- Python 3.10+ z zaznaczoną opcją dodania do PATH.

Tkinter jest dołączony do standardowej instalacji Pythona dla Windows.

## Uruchomienie bez instalacji

```powershell
python calculator.py
```

## Budowanie EXE i instalacja

Najprościej uruchomić dwuklikiem plik `install.bat`. Skrypt zbuduje EXE, doinstaluje
PyInstaller, jeśli go brakuje, i zainstaluje aplikację bez uprawnień administratora.
Na komputerze musi być zainstalowany Python 3.10+ oraz dostęp do internetu przy
pierwszym uruchomieniu.

Uruchom PowerShell w tym folderze:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\build.ps1
```

Skrypt doinstaluje PyInstaller, zbuduje `dist\BetterCalculator.exe`, skopiuje aplikację do `%LOCALAPPDATA%\Programs\Better Calculator` i utworzy skrót na pulpicie oraz w menu Start.

## Instalacja samej komendy `better-calculator`

Uruchom PowerShell w tym folderze:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1
```

Po ponownym otwarciu terminala aplikację uruchomisz komendą:

```text
better-calculator
```

Instalator kopiuje program do `%LOCALAPPDATA%\Programs\Better Calculator`, tworzy plik wykonywalny `better-calculator.cmd` i dodaje ten katalog do PATH użytkownika. Nie wymaga uprawnień administratora.

## Odinstalowanie

Możesz uruchomić dwuklikiem `uninstall.bat` albo wykonać w PowerShell:

```powershell
.\uninstall.ps1
```

## Licencja

Projekt prywatny do dowolnego użytku lokalnego.
