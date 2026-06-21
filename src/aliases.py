from typing import List, Dict
from src.git_loader import CommitInfo

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

def unificar_autores(commits: List[CommitInfo]) -> List[CommitInfo]:
    """
    Normaliza os autores dos commits resolvendo aliases baseados 
    em e-mail e na distância de Levenshtein.
    """
    mapa_emails: Dict[str, str] = {}
    nomes_unicos = set()

    # Passagem 1: Mapear e-mails para um único nome base
    for commit in commits:
        if commit.email != "<unknown>":
            if commit.email not in mapa_emails:
                mapa_emails[commit.email] = commit.author
                nomes_unicos.add(commit.author)

    # Passagem 2: Unificar nomes parecidos (Levenshtein <= 1)
    mapa_nomes: Dict[str, str] = {}
    nomes_lista = list(nomes_unicos)
    
    for i, nome in enumerate(nomes_lista):
        if nome not in mapa_nomes:
            mapa_nomes[nome] = nome 
            
        for outro_nome in nomes_lista[i+1:]:
            if outro_nome not in mapa_nomes:
                if distancia_levenshtein(nome.lower(), outro_nome.lower()) <= 1:
                    mapa_nomes[outro_nome] = mapa_nomes[nome] # Unifica

    # Passagem 3: Atualizar os commits
    for commit in commits:
        nome_base = mapa_emails.get(commit.email, commit.author)
        nome_final = mapa_nomes.get(nome_base, nome_base)
        commit.author = nome_final

    return commits