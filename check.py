import itertools
import re

ALPHABET = ("a", "b", "c")
STATES = ("q0", "q1", "q2", "q3")

START_STATE = "q0"
ACCEPTING_STATES = {"q0", "q1", "q2"}

TRANSITIONS = {
    "q0": {"a": "q1", "b": "q0", "c": "q0"},
    "q1": {"a": "q2", "b": "q0", "c": "q0"},
    "q2": {"a": "q3", "b": "q0", "c": "q0"},
    "q3": {"a": "q3", "b": "q3", "c": "q3"},
}

REGEX = r"((|a|aa)(b|c))*(|a|aa)"

GRAMMAR = {
    "S": ["aA", "bS", "cS", ""],
    "A": ["aB", "bS", "cS", ""],
    "B": ["bS", "cS", ""],
}
GRAMMAR_START = "S"


def in_language(w):
    """Определение языка L12: нет подстроки из трёх и более a подряд."""
    return "aaa" not in w


def run_automaton(input_string, verbose=True):
    current_state = START_STATE
    if verbose:
        print(f'Строка: "{input_string}"')
        print(f"  Старт: {current_state}")
    for position, symbol in enumerate(input_string):
        next_state = TRANSITIONS[current_state][symbol]
        if verbose:
            print(
                f"  Шаг {position + 1}: состояние {current_state}, "
                f"читаем '{symbol}' -> {next_state}"
            )
        current_state = next_state
    accepted = current_state in ACCEPTING_STATES
    if verbose:
        verdict = "ДОПУЩЕНА" if accepted else "ОТКЛОНЕНА"
        print(f"  Итоговое состояние: {current_state} -> строка {verdict}\n")
    return accepted


def regex_accepts(w):
    return re.fullmatch(REGEX, w) is not None


def grammar_derivation(w):
    """Ищет вывод строки w в праволинейной грамматике. Возвращает список шагов или None."""
    steps = [GRAMMAR_START]
    nonterminal = GRAMMAR_START
    prefix = ""
    for symbol in w:
        rule = next((r for r in GRAMMAR[nonterminal] if r and r[0] == symbol), None)
        if rule is None:
            return None
        prefix += symbol
        nonterminal = rule[1]
        steps.append(prefix + nonterminal)
    if "" not in GRAMMAR[nonterminal]:
        return None
    steps.append(prefix if prefix else "λ")
    return steps


def compare_all(max_len):
    total = 0
    for length in range(max_len + 1):
        for chars in itertools.product(ALPHABET, repeat=length):
            w = "".join(chars)
            expected = in_language(w)
            results = (
                run_automaton(w, verbose=False),
                regex_accepts(w),
                grammar_derivation(w) is not None,
            )
            if any(r != expected for r in results):
                print(
                    f"  РАСХОЖДЕНИЕ на строке '{w}': ожидалось {expected}, получено {results}"
                )
                return False
            total += 1
    print(
        f"  ДКА, РВ и грамматика совпадают с определением языка на всех {total} строках длины <= {max_len}"
    )
    return True


def pumping_demo(n):
    """Часть 3: L38 = {a^m b a^m : m >= 1}. Для w = a^n b a^n перебираем все разбиения xyz."""
    w = "a" * n + "b" + "a" * n

    def in_l38(s):
        m = re.fullmatch(r"(a+)b(a+)", s)
        return m is not None and len(m.group(1)) == len(m.group(2))

    print(f"  w = a^{n} b a^{n} = {w}, w в L38: {in_l38(w)}")
    for i in range(n + 1):
        for j in range(i + 1, n + 1):
            x, y, z = w[:i], w[i:j], w[j:]
            pumped = x + z
            print(
                f"  x='{x}', y='{y}', z='{z}' -> xy^0z = '{pumped}' в L38: {in_l38(pumped)}"
            )


def main():
    print("Таблица переходов ДКА (вариант 12):")
    print("состояние".ljust(10) + "".join(s.center(6) for s in ALPHABET))
    for state in STATES:
        mark = ("->" if state == START_STATE else "  ") + (
            "*" if state in ACCEPTING_STATES else " "
        )
        print(
            (mark + state).ljust(10)
            + "".join(TRANSITIONS[state][s].center(6) for s in ALPHABET)
        )
    print()

    for s in ["", "aabaa", "cacaab", "aaa", "baaab"]:
        run_automaton(s)

    print("Выводы строк в грамматике:")
    for s in ["aaba", "caab", "aaa"]:
        steps = grammar_derivation(s)
        print(f"  {s}: " + (" => ".join(steps) if steps else "вывода нет"))
    print()

    print("Сравнение ДКА, РВ и грамматики:")
    compare_all(8)
    print()

    print("Часть 3, лемма о разрастании (n = 3):")
    pumping_demo(3)


if __name__ == "__main__":
    main()
