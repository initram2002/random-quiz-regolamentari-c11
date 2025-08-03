# random-quiz-regolamentari-c11

Script Python per generare gli ID delle domande per comporre una batteria di 20 quiz dal file "quiz_regolamentari_c11_v2023.6.30".
I criteri per la generazione della batteria di quiz sono:
- Una (e solo una) domanda per ciascuna delle 17 Regole del Giuoco del Calcio + 1 del Regolamento dell'Associazione Italiana Arbitri + 1 del Regolamento degli Organi Tecnici dell'Associazione Italiana Arbitri.
- La 20ª domanda può appartenere a qualunque Regola, purché l'ID non sia mai stato usato nei tre quiz precedenti.
- Nessun ID già apparso nei tre quiz precedenti può essere riproposto.

## Formato di output

Le linee prodotte sono del tipo:

```plain-text
Regola 1:  37
Regola 2:  51
…
Regola ASS:  630
Regola NFOT:  701
```

- Per le Regole 1-17 il prefisso resta «Regola n».  
- Per la Regola 18 il prefisso diventa «Regola ASS».  
- Per la Regola 19 il prefisso diventa «Regola NFOT».
