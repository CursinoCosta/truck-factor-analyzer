# Truck Factor Analyzer

## Integrantes

* Beatriz Reis Gama Barbosa
* Izadora Monken Ganem
* Mateus Cursino Gomes Costa
* Luisa Lopes Carvalhaes

## Descrição

O Truck Factor Analyzer é uma ferramenta de linha de comando para análise de repositórios de software. Seu objetivo é identificar riscos de manutenção e evolução por meio da estimativa do Truck Factor, uma métrica que avalia a concentração de conhecimento em um projeto.

A ferramenta utiliza técnicas de mineração de repositórios para analisar o histórico de desenvolvimento e identificar dependências excessivas em desenvolvedores específicos, auxiliando na detecção de possíveis gargalos de manutenção.

## Funcionalidades

* Análise de repositórios Git.
* Cálculo de Truck Factor utilizando diferentes estratégias.
* Ranking de desenvolvedores por contribuição.
* Relatórios de concentração de conhecimento.
* Identificação de possíveis riscos associados à dependência de poucos desenvolvedores.

## Estratégias de Cálculo

### Commit-Based

Calcula o Truck Factor com base na distribuição de commits. Os desenvolvedores são ordenados pelo volume de contribuição, e a heurística contabiliza o número mínimo de autores cuja remoção faz com que a soma de seus commits represente mais de 50% do total de modificações do repositório. É uma métrica direta de volume de trabalho.

### File-Based Ownership

Calcula o Truck Factor com base na métrica *Degree-of-Authorship* (DOA), fundamentada em heurísticas acadêmicas (Avelino et al., 2016). O processo é dividido nas seguintes etapas:

* **Higienização e Filtragem:** Exclusão de arquivos que distorcem o conhecimento central do sistema, como bibliotecas de terceiros (`node_modules`, `vendor`), documentações e arquivos de mídia.
* **Resolução de Aliases:** Unificação de desenvolvedores com múltiplos nomes de usuário ou erros de digitação no Git, utilizando o cruzamento de e-mails e a Distância de Levenshtein.
* **Mapeamento de Autoria (DOA):** O grau de autoria de cada arquivo considera o criador original (FA - *First Authorship*), o número de entregas realizadas pelo autor (DL - *Deliveries*) e o desgaste causado pelas modificações de terceiros (AC - *Acceptances*).
* **Heurística de Cobertura:** O algoritmo remove iterativamente os principais autores de código até que a cobertura de arquivos mantidos pelo restante da equipe caia para menos de 50%. A quantidade de desenvolvedores removidos até esse ponto de falha determina o Truck Factor.

## Tecnologias Utilizadas

As tecnologias utilizadas serão:

* GitHub Search Tool (GHS) para seleção dos repositórios analisados.
* GitEvo para extração e processamento de métricas relacionadas à evolução de software.
* PyDriller para mineração de repositórios Git e coleta de informações históricas.
* Typer para implementação da interface de linha de comando.
* Pytest para testes automatizados.
* GitHub Actions para integração contínua e execução automática dos testes.

## Artefatos Analisados

A ferramenta realiza a análise dos seguintes artefatos:

* Histórico de commits para identificação de autoria e participação dos desenvolvedores.
* Arquivos de código-fonte para análise de propriedade e distribuição de conhecimento.
* Logs de modificação para mensuração do volume de contribuição técnica ao longo da evolução do projeto.
* Métricas históricas obtidas a partir da mineração do repositório.

## Estrutura do Projeto

```text
src/
├── aliases.py
├── cli.py
├── git_loader.py
├── metrics.py
├── models.py
├── truck_factor.py
└── strategies/
    ├── commits.py
    └── files.py

tests/
├── test_aliases.py
├── test_loader.py
├── test_metrics.py
├── test_truck_factor_commits.py
└── test_truck_factor_files.py

.github/workflows/
└── tests.yml

```

## Instalação

```bash
git clone <repository-url>
cd truck-factor-analyzer

python -m venv venv

# Linux/MacOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt

```

## Uso

Antes de utilizar uma das estratégias, é necessário clonar o repositório a ser analisado:

```bash
git clone <link do repositorio>
```

Análise utilizando a estratégia baseada em commits:

```bash
python -m src.cli analyze --repo-path <pasta do repositorio> --strategy commits
```

Análise utilizando a estratégia baseada em propriedade de arquivos (DOA):

```bash
python -m src.cli analyze --repo-path <pasta do repositorio> --strategy files
```

### Campos da saída

| Campo | Descrição |
|---|---|
| Truck Factor | Número mínimo de desenvolvedores cuja saída comprometeria o projeto |
| Strategy | Estratégia utilizada no cálculo (`commits` ou `files`) |
| Coverage | Fração do repositório coberta pelos autores críticos identificados |

### Interpretação do resultado

- **TF = 1** (vermelho): risco alto — um único desenvolvedor concentra conhecimento crítico
- **TF 2–3** (amarelo): risco moderado
- **TF ≥ 4** (verde): conhecimento bem distribuído entre a equipe

### Estratégia `commits`

Contabiliza o total de arquivos modificados por commit para cada autor.
Ordena os autores por volume de contribuição e acumula até ultrapassar
50% do total de modificações. O número de autores necessários é o Truck Factor.

### Estratégia `files`

Calcula o *Degree of Authorship* (DOA) de cada desenvolvedor em cada arquivo,
conforme Avelino et al. (2016). Remove iterativamente o principal autor de código
enquanto a cobertura de arquivos com dono primário permanecer acima de 50%.

## Testes

Para executar os testes localmente:

```bash
python -m pytest

```

Os testes são executados automaticamente por meio do GitHub Actions a cada push e pull request.

## Objetivo Acadêmico

Projeto desenvolvido para a disciplina Engenharia de Software II com foco na aplicação de técnicas de mineração de repositórios para identificação de problemas relacionados à manutenção e evolução de software por meio da análise de Truck Factor.

## Referências

* Avelino, Guilherme, Leonardo Passos, Andre Hora, and Marco Tulio Valente. "A novel approach for estimating truck factors." In *Proceedings of the 24th International Conference on Program Comprehension*, pp. 1-10. 2016. Disponível em: <https://arxiv.org/abs/1604.06766>
