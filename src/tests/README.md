# Testes Unitários

Este diretório contém testes automatizados para garantir a estabilidade do pipeline de dados e do modelo.

## Como Executar

A partir da raiz do projeto (`projeto_datathon`), execute:

```bash
pytest src/tests/
```

Ou para ver logs detalhados:

```bash
pytest -v -s src/tests/
```

## Arquivos

- `test_preprocessing.py`: Testa as funções de limpeza e a classe `DataPreprocessor`.
- `test_model.py`: Testa a persistência e carregamento do modelo (save/load).
