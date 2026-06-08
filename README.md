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

Calcula o Truck Factor com base na distribuição de commits por desenvolvedor.

### File-Based Ownership

Calcula o Truck Factor com base na propriedade dos arquivos e módulos do sistema, considerando a participação dos desenvolvedores nas modificações realizadas ao longo da evolução do projeto.

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
├── cli.py
├── git_loader.py
├── metrics.py
├── truck_factor.py
└── strategies/
    ├── commits.py
    └── files.py

tests/
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

Análise utilizando a estratégia baseada em commits:

```bash
python -m src.cli analyze --repo-path <repositorio> --strategy commits
```

Análise utilizando a estratégia baseada em propriedade de arquivos:

```bash
python -m src.cli analyze --repo-path <repositorio> --strategy files
```

## Testes

Para executar os testes localmente:

```bash
pytest
```

Os testes são executados automaticamente por meio do GitHub Actions a cada push e pull request.

## Objetivo Acadêmico

Projeto desenvolvido para a disciplina Engenharia de Software II com foco na aplicação de técnicas de mineração de repositórios para identificação de problemas relacionados à manutenção e evolução de software por meio da análise de Truck Factor.
