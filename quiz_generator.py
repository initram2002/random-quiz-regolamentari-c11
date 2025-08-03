"""
Quiz Generator
================================================
Genera una batteria di 20 domande regolamentari rispettando:
- Una (e solo una) domanda per ciascuna delle 17 Regole del Giuoco del Calcio + 1 del Regolamento dell'Associazione Italiana Arbitri + 1 del Regolamento degli Organi Tecnici dell'Associazione Italiana Arbitri.
- La 20ª domanda può appartenere a qualunque Regola, purché l'ID non sia mai stato usato nei tre quiz precedenti.
- Nessun ID già apparso nei tre quiz precedenti può essere riproposto.

Formato di output
-----------------
Le linee prodotte sono del tipo:
```
Regola 1:  37
Regola 2:  51
…
Regola ASS:  630
Regola NFOT:  701
```

- Per le Regole 1-17 il prefisso resta «Regola n».  
- Per la Regola 18 il prefisso diventa «Regola ASS».  
- Per la Regola 19 il prefisso diventa «Regola NFOT».
"""
from __future__ import annotations

import random
from typing import Dict, List, Set, Tuple

# ---------------------------------------------------------------------------
# 1. Configurazione dei range per ciascuna Regola
# ---------------------------------------------------------------------------
# Mappa: numero di Regola → range() corrispondente (estremo superiore INCLUSO)
RULE_RANGES: Dict[int, range] = {
    1: range(1, 44),        # 1 ‑ 43
    2: range(44, 67),       # 44 ‑ 66
    3: range(67, 116),      # 67 ‑ 115
    4: range(116, 142),     # 116 ‑ 141
    5: range(142, 183),     # 142 ‑ 182
    6: range(183, 248),     # 183 ‑ 247
    7: range(248, 271),     # 248 ‑ 270
    8: range(271, 299),     # 271 ‑ 298
    9: range(299, 309),     # 299 ‑ 308
    10: range(309, 337),    # 309 ‑ 336
    11: range(337, 367),    # 337 ‑ 366
    12: range(367, 490),    # 367 ‑ 489
    13: range(490, 526),    # 490 ‑ 525
    14: range(526, 557),    # 526 ‑ 556
    15: range(557, 583),    # 557 ‑ 582
    16: range(583, 604),    # 583 ‑ 603
    17: range(604, 622),    # 604 ‑ 621
    18: range(622, 691),    # 622 ‑ 690 – Regolamento dell'Associazione Italiana Arbitri
    19: range(691, 717),    # 691 ‑ 716 – Regolamento degli Organi Tecnici dell'Associazione Italiana Arbitri
}

# Etichette da mostrare nell’output (solo eccezioni rispetto al default)
RULE_LABELS: Dict[int, str] = {
    18: "ASS",
    19: "NFOT",
}

# ---------------------------------------------------------------------------
# 2. Funzioni ausiliarie
# ---------------------------------------------------------------------------

def get_rule(question_id: int) -> int:
    """Restituisce il numero di Regola (1‑19) associata a *question_id*.

    Solleva ValueError se l'ID non è compreso tra 1 e 716.
    """
    for rule_no, rng in RULE_RANGES.items():
        if question_id in rng:
            return rule_no
    raise ValueError("ID domanda fuori range: deve essere tra 1 e 716")


def rule_label(rule_no: int) -> str:
    """Ritorna l'etichetta da stampare per la Regola indicata."""
    if rule_no in RULE_LABELS:
        return f"Regola {RULE_LABELS[rule_no]}"
    return f"Regola {rule_no}"


def format_line(rule_no: int, question_id: int) -> str:
    """Formatta la linea di output finale."""
    return f"{rule_label(rule_no)}: {question_id}"


# ---------------------------------------------------------------------------
# 3. Funzione principale di generazione
# ---------------------------------------------------------------------------

def generate_quiz(previous_ids: Set[int], *, seed: int | None = None) -> List[str]:
    """Genera l'elenco delle 20 domande secondo i vincoli richiesti.

    Parametri
    ---------
    previous_ids : set[int]
        Tutti gli ID apparsi nei tre quiz precedenti.
    seed : int | None
        Seed opzionale per `random.seed` (utile per test riproducibili).
    """
    if seed is not None:
        random.seed(seed)

    selected: List[Tuple[int, int]] = []    # (regola, id)
    rules_used: Set[int] = set()
    selected_ids: Set[int] = set()

    while len(selected) < 20:
        qid = random.randint(1, 716)

        # A) Scarta se già usato
        if qid in previous_ids or qid in selected_ids:
            continue

        rule_no = get_rule(qid)

        # B) Durante le prime 19 domande non si può ripetere la Regola
        if len(selected) < 19 and rule_no in rules_used:
            continue

        # C) Accetta la domanda
        selected.append((rule_no, qid))
        selected_ids.add(qid)
        rules_used.add(rule_no)

    # Mischia l'ordine finale
    random.shuffle(selected)
    return [format_line(r, q) for r, q in selected]


# ---------------------------------------------------------------------------
# 4. Esempio di esecuzione (può essere eliminato o personalizzato)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Inserire qui gli ID effettivamente usati nei tre quiz precedenti
    prev_quiz1 = [111, 25, 46, 676, 298, 537, 315, 511, 437, 604, 148, 577, 223, 596, 258, 346, 126, 712, 308, 135] # Quiz 1
    prev_quiz2 = [569, 625, 491, 379, 35, 208, 107, 314, 117, 277, 53, 146, 702, 527, 586, 266, 611, 359, 304, 692] # Quiz 2
    prev_quiz3 = [446, 264, 539, 206, 320, 29, 704, 686, 520, 141, 350, 574, 145, 597, 286, 110, 306, 58, 610, 239] # Quiz 3

    previous_ids = set(prev_quiz1 + prev_quiz2 + prev_quiz3)

    quiz_lines = generate_quiz(previous_ids, seed=42)  # seed per debug
    print("\n".join(quiz_lines))
