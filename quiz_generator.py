"""
Quiz Generator per Women Project AIA Chivasso
================================================
Genera settimanalmente una batteria di 20 domande regolamentari, **solo** dalle
Regole 1-17 del Giuoco del Calcio (niente Regolamento associativo AIA, niente
Norme di Funzionamento degli Organi Tecnici).

Vincoli
-------
1) Le prime 17 domande: una per ciascuna Regola 1-17, tutte diverse tra loro.
2) Le ultime 3 domande (18ª, 19ª, 20ª):
   • devono essere ID mai apparsi nei tre quiz precedenti;
   • devono appartenere a **tre Regole diverse tra loro** (scelte tra 1-17);
   • è ammesso che ripetano Regole già usate nelle prime 17 (ovviamente con ID diversi).
3) Nessun ID si può ripetere all'interno del quiz corrente.

Formato di output
-----------------
Ogni riga è del tipo:
```
Regola x: y
```
Dove `x` ∈ {1,…,17} e `y` è l'ID domanda (1-621).
"""
from __future__ import annotations

import random
from typing import Dict, List, Set, Tuple

# ---------------------------------------------------------------------------
# 1) Range ID per ciascuna Regola (SOLO 1–17)
# ---------------------------------------------------------------------------
RULE_RANGES: Dict[int, range] = {
    1: range(1, 44),        # 1 - 43
    2: range(44, 67),       # 44 - 66
    3: range(67, 116),      # 67 - 115
    4: range(116, 142),     # 116 - 141
    5: range(142, 183),     # 142 - 182
    6: range(183, 248),     # 183 - 247
    7: range(248, 271),     # 248 - 270
    8: range(271, 299),     # 271 - 298
    9: range(299, 309),     # 299 - 308
    10: range(309, 337),    # 309 - 336
    11: range(337, 367),    # 337 - 366
    12: range(367, 490),    # 367 - 489
    13: range(490, 526),    # 490 - 525
    14: range(526, 557),    # 526 - 556
    15: range(557, 583),    # 557 - 582
    16: range(583, 604),    # 583 - 603
    17: range(604, 622),    # 604 - 621
}

ALL_VALID_IDS: Set[int] = set().union(*[set(r) for r in RULE_RANGES.values()])  # 1..621

# ---------------------------------------------------------------------------
# 2) Funzioni ausiliarie
# ---------------------------------------------------------------------------

def get_rule(question_id: int) -> int:
    """Restituisce la Regola (1-17) associata all'ID o solleva ValueError."""
    for rule_no, rng in RULE_RANGES.items():
        if question_id in rng:
            return rule_no
    raise ValueError("ID fuori range per le Regole 1-17 (1..621)")


def format_line(rule_no: int, question_id: int) -> str:
    return f"Regola {rule_no}: {question_id}"


def _available_pool(rule_no: int, previous_ids: Set[int], selected_ids: Set[int]) -> List[int]:
    """Ritorna la lista degli ID disponibili per una regola, esclusi precedenti e già scelti."""
    rng = RULE_RANGES[rule_no]
    return [qid for qid in rng if qid not in previous_ids and qid not in selected_ids]


def _prefer_non_adjacent(pool: List[int], previous_ids: Set[int]) -> List[int]:
    """Dato un pool disponibile, preferisce ID non adiacenti (±1) a quelli già usati.
    Se la preferenza azzera il pool, restituisce il pool originale.
    """
    if not pool:
        return pool
    # Costruisci insieme di ID da evitare in via preferenziale (adiacenti)
    adj = set()
    for pid in previous_ids:
        if pid - 1 in ALL_VALID_IDS:
            adj.add(pid - 1)
        if pid + 1 in ALL_VALID_IDS:
            adj.add(pid + 1)
    preferred = [q for q in pool if q not in adj]
    return preferred if preferred else pool


# ---------------------------------------------------------------------------
# 3) Generazione robusta e (di default) non deterministica
# ---------------------------------------------------------------------------

def generate_quiz(previous_ids: Set[int], *, seed: int | None = None) -> List[str]:
    """Genera 20 righe "Regola x: y" secondo i vincoli descritti.

    Se non esistono abbastanza ID residui per una o più Regole, solleva un
    RuntimeError con un messaggio esplicativo.
    """
    # Usa RNG locale per non toccare lo stato globale e per evitare pattern.
    rng: random.Random
    if seed is None:
        rng = random.SystemRandom()  # forte entropia di sistema
    else:
        rng = random.Random(seed)

    # Assicura che eventuali ID > 621 (es. da vecchi quiz) non interferiscano
    previous_ids = {qid for qid in previous_ids if qid in ALL_VALID_IDS}

    selected: List[Tuple[int, int]] = []    # (regola, id)
    selected_ids: Set[int] = set()

    # --- Fase 1: una domanda per ciascuna Regola 1–17 ---
    rules = list(RULE_RANGES.keys())
    rng.shuffle(rules)

    for r in rules:
        pool = _available_pool(r, previous_ids, selected_ids)
        if not pool:
            raise RuntimeError(
                f"Nessun ID disponibile per la Regola {r} (tutti già usati nei tre quiz precedenti?)"
            )
        # Preferenza anti-adiacenza per ridurre incrementi ±1 rispetto ai quiz precedenti
        pool = _prefer_non_adjacent(pool, previous_ids)
        qid = rng.choice(pool)
        selected.append((r, qid))
        selected_ids.add(qid)

    # --- Fase 2: tre domande aggiuntive, ognuna da una Regola diversa ---
    extra_rule_candidates = [
        r for r in rules if _available_pool(r, previous_ids, selected_ids)
    ]
    if len(extra_rule_candidates) < 3:
        raise RuntimeError(
            "Non ci sono almeno tre Regole con ID residui per le domande 18-20."
        )

    rng.shuffle(extra_rule_candidates)
    for r in extra_rule_candidates[:3]:
        pool = _available_pool(r, previous_ids, selected_ids)
        # Applica anche qui la preferenza anti-adiacenza
        pool = _prefer_non_adjacent(pool, previous_ids)
        qid = rng.choice(pool)
        selected.append((r, qid))
        selected_ids.add(qid)

    # Ordine finale casuale e formattazione
    rng.shuffle(selected)
    return [format_line(r, q) for r, q in selected]


# ---------------------------------------------------------------------------
# 4) Esempio eseguibile da CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Genera una batteria di 20 domande (Regole 1–17)")
    parser.add_argument("--seed", type=int, default=None, help="Seed opzionale per riprodurre l'estrazione")
    args = parser.parse_args()

    # Inserire qui gli ID realmente usati nei tre quiz precedenti (solo 1..621)
    prev_quiz1 = [557, 160, 511, 25, 593, 547, 116, 305, 198, 134, 49, 292, 148, 304, 259, 485, 615, 342, 324, 115] # Quiz 1
    prev_quiz2 = [469, 128, 102, 59, 492, 282, 541, 205, 122, 588, 151, 542, 152, 617, 5, 575, 331, 269, 359, 307] # Quiz 2
    prev_quiz3 = [608, 301, 322, 38, 252, 549, 399, 585, 91, 595, 182, 138, 214, 61, 490, 620, 346, 570, 440, 294] # Quiz 3

    previous_ids = set(prev_quiz1 + prev_quiz2 + prev_quiz3)

    quiz_lines = generate_quiz(previous_ids, seed=args.seed)
    print("\n".join(quiz_lines))

    # Stampa in aggiunta il vettore con i soli ID, nello stesso ordine delle righe sopra
    try:
        ids_vector = [int(line.split(":", 1)[1].strip()) for line in quiz_lines]
        print()  # riga vuota di separazione
        print("[" + ", ".join(str(x) for x in ids_vector) + "]")
    except Exception:
        # In caso di formati imprevisti, evita di interrompere l'esecuzione
        pass
