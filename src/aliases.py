def distancia_levenshtein(s1: str, s2: str) -> int:
    """Calcula a distância de Levenshtein entre duas strings."""
    if len(s1) < len(s2):
        return distancia_levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    linha_anterior = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        linha_atual = [i + 1]
        for j, c2 in enumerate(s2):
            insercoes = linha_anterior[j + 1] + 1
            delecoes = linha_atual[j] + 1
            substituicoes = linha_anterior[j] + (c1 != c2)
            linha_atual.append(min(insercoes, delecoes, substituicoes))
        linha_anterior = linha_atual
    
    return linha_anterior[-1]