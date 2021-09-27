# Find strings in binary

This code is a overhaul of this of the code http://www.arcade-cabinets.com/patreon/rom_hacks/tools/findString.py described in the youtube channel arcade-cabinets.com in this video https://www.youtube.com/watch?v=4JFO_MEPHsE

It is now coded in python 3 and support multiprocessing.

This code is a way to find text with unknown encodings (but with a latin alphabet where characters ABCDEFGHIKLMNOPQRSTUVWXYZ are followig each others).
This script cannot find text directly written in pictures.

# Usage (python 3)

## 1 - Frogger

(Game - Frogger - Search the location of the "RANKING" string )

```findStringV2.py "ranking" frsm3.7```
	Match in frsm3.7 at offset 0xeeb

## 2 - Wario Land 4

(Game - Wario Land 4 - Search the location of the name of the first level "Hall of Hieroglyph" - Search the location of "PRODUCER" in Credits )

If the first letter is an uppercase letter it is recommended to drop it.

```python findStringV2.py "ieroglyph" Wario\ Land\ 4\ \(UE\).gba```
	Match in Wario Land 4 (UE).gba at offset 0x65ceea

In some case there is an extra byte, the option -s is here to skip it.

```findStringV2.py -s 2 "producer" Wario\ Land\ 4\ \(UE\).gba```
	Match in Wario Land 4 (UE).gba at offset 0x78a12c
	Match in Wario Land 4 (UE).gba at offset 0x78a622