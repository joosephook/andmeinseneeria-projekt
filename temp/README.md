Hei!

Ma tegin siin dashboardid ära niipalju kui kiiruga oskasin. Probleemiks on ilmselt see, et see ei haaku teiste poolt tehtud koodiga. Asi on pisut lappes, peaksime mõtlema kuidas edasi.

Selleks, et dashboardi kuvada tegin lihtsustatult kogu ahela läbi. Failid on siin kataloogis
1) Kõigepealt teha postgres vajalikud tabelid ära (ühekordne teema) käivitada skriptid mis asuvad: ettevalmistus.sql
2) seejärel fail: sisselugemine.py loeb excelist sisse paneb stagingusse ja seejärel põhitabelisse.
3) php failid loevad view pealt andmed, ühes neist on puhtalt baasi andmed.
4) cart1.html kuvab apache echart abil view poolt edastatud andmed graafikuna.

Ma tegin selle tööarvuti peal ja seal kogu ahel töötas. Selleks, et seda testida peaks muutma kõik fail paths ja login data. Docker ei ole veel väga selge. Hakkan tutvuma täna üles laetud failidega. Kõik nõuanded teretulnud, koosolek ei teeks ka paha.

Jaan
