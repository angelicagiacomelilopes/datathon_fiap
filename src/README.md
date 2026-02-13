# Módulo de Machine Learning - Passos Mágicos

Este diretório contém o código fonte para o pipeline de machine learning do Case Datathon Passos Mágicos.

## Estrutura do Código

- `preprocessing.py`: Contém a classe `DataPreprocessor` e funções para limpeza inicial dos dados (`clean_data`).
- `feature_engineering.py`: Responsável pela criação de novas variáveis (features) que auxiliam na predição, como variações de INDE entre anos.
- `train.py`: Script principal para treinamento. Carrega os dados, processa, treina o modelo (RandomForest por padrão) e salva os artefatos em `app/model/`.
- `evaluate.py`: Carrega o modelo salvo e avalia sua performance em dados novos ou no conjunto de teste, gerando métricas de acurácia, recall, etc.
- `utils.py`: Funções auxiliares para carregamento de arquivos e persistência de objetos (pickle/joblib).

## Pré-requisitos

Certifique-se de estar na raiz do projeto `projeto_datathon` e ter o Python 3.9+ instalado.

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Execução

### Treinamento
Para treinar o modelo e gerar os arquivos `.pkl` para a API:
```bash
python src/train.py
```

### Avaliação
Para visualizar as métricas do modelo treinado:
```bash
python src/evaluate.py
```

### Testes
Para rodar os testes unitários:
```bash
pytest src/tests/
```
