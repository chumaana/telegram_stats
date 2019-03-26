#!/usr/bin/env python3

"""
Klasickým příkladem dvourozměrné náhodné procházky je Brownův pohyb: Pylové zrnko je tepelným pohybem molekul kapaliny v každém časovém okamžiku strkáno náhodnými směry o nějakou vzdálenost nějakou rychlostí. 
Zaznamenejte graficky pohyb pylového zrnka ze středu obrazovky k jejímu okraji (výpočet tedy končí dosažením libovolného ze čtyř okrajů). Barevně namapujte počet navštívení toho kterého místa.
Pohyb zrnka do všech směrů pokládejte za stejně pravděpodobný. Za směry berte sever–východ–jih–západ a navíc i čtyři diagonální.

Pylové zrnko se sice dále sráží (a tudíž mění směr) zcela náhodně, ale před další srážkou může urazit i podstatně delší dráhu než právě jednu jednotku.
Prakticky druhý požadavek můžete nepřekvapivě nasimulovat tak, že ke srážce s okolními molekulami dochází s jistou pravděpodobností menší než 1, takže zrnko může klidně několik kroků cestovat původním směrem, než dojde ke srážce a změně směru.

Řešte úlohu číslo 7 z „Náhody a pravděpodobnosti“ (podrobnosti k implementaci jsou v jí předcházejících úlohách od čísla 4), tedy Náhodnou procházku s různě dlouhým krokem (aka Brownův pohyb), tj. především:

* výstup je místo konzole do matplotlibu;
* náhodná procházka končí dosažením libovolného okraje grafu;
* různěkrát navštívená místa obarvěte různou barvou, ať to pěkně vypadá;
* ukládání (a načítání) historie pohybu neřešte, stačí pouze výsledný obrázek.
* Vyřešte tedy pouze jedno zobrazení „Brownova pohybu“ pro jedno spuštění skriptu, přičemž dbejte na obarvování (rozdělte počty navštívení toho kterého místa do několika tříd; možná trošku překvapivě jich není potřeba zase tak moc) a proměnnou délku kroku.
"""

import matplotlib.pyplot as plt

# TODO: Implement your solution

