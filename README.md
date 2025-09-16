# Quiz Generator (Regole 1–17)

Script Python per generare una batteria di 20 domande regolamentari esclusivamente dalle Regole 1–17 del Giuoco del Calcio.

Criteri:
- 17 domande: una (e solo una) per ciascuna Regola 1–17.
- 3 domande extra (18ª–20ª):
  - ID mai apparsi nei tre quiz precedenti;
  - ciascuna da una Regola diversa tra loro (sempre 1–17);
  - possono ripetere Regole già usate tra le prime 17, ma con ID diversi.
- Nessun ID si può ripetere all’interno del quiz corrente.

Per aumentare la varietà, il generatore preferisce (quando possibile) evitare ID immediatamente adiacenti (±1) a quelli usati nei tre quiz precedenti.

## Output
Ogni riga è del tipo:

```
Regola x: y
```

Dove `x` ∈ {1,…,17} e `y` ∈ {1,…,621} (secondo i range mappati alle Regole 1–17).
Al termine viene stampato anche il vettore con i soli ID nell’ordine mostrato.

## Uso da CLI

Esecuzione standard (non deterministica, usa entropia di sistema):

```bash
python quiz_generator.py
```

Esecuzione riproducibile con seed fisso:

```bash
python quiz_generator.py --seed 12345
```

Per personalizzare gli ID già apparsi nei tre quiz precedenti, modifica i vettori `prev_quiz1`, `prev_quiz2`, `prev_quiz3` nel `__main__` del file `quiz_generator.py`.

## Note
- Il generatore solleva un errore se una o più Regole non hanno ID residui disponibili.
- L’anti-adiacenza è una preferenza: se non rimangono alternative valide, potrebbe selezionare comunque un ID adiacente.
