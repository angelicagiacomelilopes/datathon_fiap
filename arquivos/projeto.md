# Datathon: Case Passos Mágicos 

Base de dados e dicionário de dados  
Arquivo:
- BASE DE DADOS PEDE 2024 - DATATHON.xlsx

- desvendando_passos.pdf
``` bash
Desvendando a Passos Mágicos
Novo cais: da inscrição à matrícula
O início da transformação de vidas na Passos Mágicos

O processo de admissão de novos alunos
Durante o processo seletivo, priorizamos garantir dignidade e fortalecer a autoestima, sem reproduzir modelos tradicionais de hierarquização social. Nosso enfoque está em promover a inclusão por meio de um viés social ativo. As normas para oportunidades externas, apresentadas na reunião de boas-vindas, valorizam a dedicação e evolução de cada aluno no Programa de Aceleração do Conhecimento.

Etapa de Inscrição
A Associação divulga vagas à comunidade Passos Mágicos, incentivando a participação de crianças e jovens que desejam estudar em um ambiente acolhedor e motivador.

Prova de Sondagem
Realizamos uma prova para identificar os conhecimentos dos alunos, promovendo o autoconhecimento e encorajando cada um a acreditar em seu potencial.

Entrevistas
As equipes de psicologia, assistência social e pedagogia entrevistam os alunos e sua família para entender suas realidades, criando um ambiente seguro e de confiança para essa troca.

Consenso Psicopedagógico
Professores e psicopedagogos se reúnem para deliberar sobre o nível de adequação do aluno, garantindo um acompanhamento individualizado.

Avaliação Socioeconômica
Analisamos o perfil socioeconômico dos alunos para melhor direcionar as ações psicopedagógicas e psicológicas, considerando as vulnerabilidades das famílias.

Matrícula
Na última etapa, formalizamos a matrícula, conectando os propósitos dos alunos e suas famílias aos da Associação, celebrando o início de uma nova jornada juntos.
```

- Dicionário Dados Datathon.pdf
- Dicionário de Dados Dataset PEDE_PASSOS
Considerações
Dataset
Dataset gerado a partir dos dados captados pela Passos Mágicos para realização das Pesquisas do PEDE (Pesquisa Extensiva do Desenvolvimento Educacional) de 2020, 2021 e 2023.

Métricas e Conceitos
Métricas foram desenvolvidas por Dario Rodrigues Silva em parceria com a Passos Mágicos. É de extrema importância consultar as pesquisas do PEDE para um entendimento mais profundo e sucinto de como foi elaborada cada métrica e conceito.

| Variável                      | Descrição                                                                                                                                                                                                                  |
|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| INSTITUICAO_ENSINO_ALUNO_2020 | Mostra instituição de Ensino do Aluno em 2020                                                                                                                                                                              |
| NOME                          | Nome do Aluno (Dados estão Anonimizados)                                                                                                                                                                                   |
| IDADE_ALUNO_2020              | Idade do Aluno em 2020                                                                                                                                                                                                     |
| ANOS_NA_PM_2020               | Tempo (Em Anos) que o Alunos está na Passos Mágicos em 2020                                                                                                                                                                |
| FASE_TURMA_2020               | Fase e Turma do Aluno na Passos Mágicos em 2020; Fase está relacionado ao Nível de Aprendizado, enquanto Turma é dado pela quantidade de turmas que existam daquela fase/nível                                             |
| PONTO_VIRADA_2020             | Campo do Tipo Booleano que sinaliza se o Aluno atingiu o "Ponto de Virada" em 2020                                                                                                                                         |
| INDE_2020                     | Índice do Desenvolvimento Educacional – Métrica de Processo Avaliativo Geral do Aluno; Dado pela Ponderação dos indicadores: IAN, IDA, IEG, IAA, IPS, IPP e IPV em 2020                                                    |
| INDE_CONCEITO_2020            | -                                                                                                                                                                                                                          |
| PEDRA_2020                    | Classificação do Aluno baseado no número do INDE, o conceito de classificação é dado por: Quartzo – 2,405 a 5,506 Ágata – 5,506 a 6,868 Ametista – 6,868 a 8,230 Topázio – 8,230 a 9,294. Cada Pedra possui uma descrição. |
| DESTAQUE_IGG_2020             | Observações dos Avaliadores Sobre o Aluno referente ao "Indicador de Engajamento" em 2020                                                                                                                                  |
| DESTAQUE_IDA_2020             | Observações dos Avaliadores Sobre o Aluno referente ao "Indicador de Aprendizagem" em 2020                                                                                                                                 |
| DESTAQUE_IPV_2020             | Observações dos Avaliadores Sobre o Aluno referente ao "Indicador de Ponto de Virada" em 2020                                                                                                                              |
| IAA_2020                      | Indicador de Auto Avaliação – Média das Notas de Auto Avaliação do Aluno em 2020                                                                                                                                           |
| IEG_2020                      | Indicador de Engajamento - Média das Notas de Engajamento do Aluno em 2020                                                                                                                                                 |
| IPS_2020                      | Indicador Psicossocial - Média das Notas Psicossociais do Aluno em 2020                                                                                                                                                    |
| IDA_2020                      | Indicador de Aprendizagem - Média das Notas do Indicador de Aprendizagem                                                                                                                                                   |
| IPP_2020                      | Indicador Psicopedagógico - Média das Notas Psico Pedagógicas do Aluno em 2020                                                                                                                                             |
| IPV_2020                      | Indicador de Ponto de Virada - Média das Notas de Ponto de Virada do Aluno em 2020                                                                                                                                         |
| IAN_2020                      | Indicador de Adequação ao Nível - Média das Notas de Adequação do Aluno ao nível atual em 2020                                                                                                                             |
| FASE_2021                     | Fase é o Nível de Aprendizado do Aluno em 2021                                                                                                                                                                             |
| TURMA_2021                    | Turma é o número da Turma de cada fase (1A,1B,1C)                                                                                                                                                                          |
| INSTITUICAO_ENSINO_ALUNO_2021 | Mostra instituição de Ensino do Aluno em 2021                                                                                                                                                                              |
| SINALIZADOR_INGRESSANTE_2021  | Mostra se o Aluno Ingressou ou é Veterano no ano de 2021                                                                                                                                                                   |
| PEDRA_2021                    | Classificação do Aluno baseado no número do INDE, o conceito de classificação é dado por: Quartzo - 2,405 a 5,506 Ágata - 5,506 a 6,868 Ametista - 6,868 a 8,230 Topázio - 8,230 a 9,294. Cada Pedra possui uma descrição. |
| INDE_2021                     | Índice do Desenvolvimento Educacional - Métrica de Processo Avaliativo Geral do Aluno; Dado pela Ponderação dos indicadores: IAN, IDA, IEG, IAA, IPS, IPP e IPV em 2021                                                    |
| IAA_2021                      | Indicador de Auto Avaliação - Média das Notas de Auto Avaliação do Aluno em 2021                                                                                                                                           |
| IEG_2021                      | Indicador de Engajamento - Média das Notas de Engajamento do Aluno em 2021                                                                                                                                                 |
| IPS_2021                      | Indicador Psicossocial - Média das Notas Psicossociais do Aluno em 2021                                                                                                                                                    |
| REC_PSICO_2021                | Mostra qual a recomendação da equipe de psicologia sobre o Aluno em 2021                                                                                                                                                   |
| IDA_2021                      | Indicador de Aprendizagem - Média das Notas do Indicador de Aprendizagem em 2021                                                                                                                                           |
| IPP_2021                      | Indicador Psicopedagógico - Média das Notas Psicopedagógicas do Aluno em 2021                                                                                                                                              |
| REC_EQUIPE_1_2021             | Recomendação da Equipe de Avaliação 1 em 2021                                                                                                                                                                              |
| REC_EQUIPE_2_2021             | Recomendação da Equipe de Avaliação 2 em 2021                                                                                                                                                                              |
| REC_EQUIPE_3_2021             | Recomendação da Equipe de Avaliação 3 em 2021                                                                                                                                                                              |
| REC_EQUIPE_4_2021             | Recomendação da Equipe de Avaliação 4 em 2021                                                                                                                                                                              |
| PONTO_VIRADA_2021             | Campo do Tipo Booleano que sinaliza se o Aluno atingiu o "Ponto de Virada" em 2021                                                                                                                                         |
| IPV_2021                      | Indicador de Ponto de Virada - Média das Notas de Ponto de Virada do Aluno em 2021                                                                                                                                         |
| IAN_2021                      | Indicador de Adequação ao Nível - Média das Notas de Adequação do Aluno ao nível atual em 2021                                                                                                                             |
| NIVEL_IDEAL_2021              | Mostra qual o nível (Fase) ideal do Aluno na Passos Mágicos em 2021                                                                                                                                                        |
| DEFASAGEM_2021                | Mostra o nível de defasagem do ano em 2021                                                                                                                                                                                 |
| FASE_2022                     | Fase é o Nível de Aprendizado do Aluno                                                                                                                                                                                     |
| TURMA_2022                    | Turma é o número da Turma de cada fase (1A,1B,1C)                                                                                                                                                                          |
| ANO_INGRESSO_2022             | Ano que o Aluno Ingressou na Passos Mágicos (atualizado 2022)                                                                                                                                                              |
| BOLSISTA_2022                 | Campo do tipo booleano que mostra se o Aluno é Bolsista em alguma instituição pela Passos Mágicos em 2022                                                                                                                  |
| INDE_2022                     | Índice do Desenvolvimento Educacional - Métrica de Processo Avaliativo Geral do Aluno; Dado pela Ponderação dos indicadores: IAN, IDA, IEG, IAA, IPS, IPP e IPV em 2022                                                    |
| CG_2022                       | Classificação (Ranking) Geral do Aluno na Passos Mágicos em 2022                                                                                                                                                           |
| CF_2022                       | Classificação (Ranking) do Aluno na Fase em 2022                                                                                                                                                                           |
| CT_2022                       | Classificação (Ranking) do Aluno na Turma em 2022                                                                                                                                                                          |
| PEDRA_2022                    | Classificação do Aluno baseado no número do INDE, o conceito de classificação é dado por: Quartzo - 2,405 a 5,506 Ágata - 5,506 a 6,868 Ametista - 6,868 a 8,230 Topázio - 8,230 a 9,294. Cada Pedra possui uma descrição. |
| DESTAQUE_IGE_2022             | Observações dos Mestres Sobre o Aluno referente ao "Indicador de Engajamento" em 2022                                                                                                                                      |
| DESTAQUE_IDA_2022             | Observações dos Mestres Sobre o Aluno referente ao "Indicador de Aprendizagem" em 2022                                                                                                                                     |
| DESTAQUE_IPV_2022             | Observações dos Mestres Sobre o Aluno referente ao "Indicador de Ponto de Virada" em 2022                                                                                                                                  |
| IAA_2022                      | Indicador de Auto Avaliação - Média das Notas de Auto Avaliação do Aluno em 2022                                                                                                                                           |
| IEG_2022                      | Indicador de Engajamento - Média das Notas de Engajamento do Aluno em 2022                                                                                                                                                 |
| IPS_2022                      | Indicador Psicossocial - Média das Notas Psicossociais do Aluno em 2022                                                                                                                                                    |
| REC_PSICO_2022                | Mostra qual a recomendação da equipe de psicologia sobre o Aluno em 2022                                                                                                                                                   |
| IDA_2022                      | Indicador de Aprendizagem - Média das Notas do Indicador de Aprendizagem em 2022                                                                                                                                           |
| NOTA_PORT_2022                | Média das Notas de Português do Aluno em 2022                                                                                                                                                                              |
| NOTA_MAT_2022                 | Média das Notas de Matemática do Aluno em 2022                                                                                                                                                                             |
| NOTA_ING_2022                 | Média das Notas de Inglês do Aluno em 2022                                                                                                                                                                                 |
| QTDE_AVAL_2022                | Quantidade de Avaliações do Aluno em 2022                                                                                                                                                                                  |
| REC_AVA_1_2022                | Recomendação da Equipe de Avaliação 1 em 2022                                                                                                                                                                              |
| REC_AVAL_2_2022               | Recomendação da Equipe de Avaliação 2 em 2022                                                                                                                                                                              |
| REC_AVAL_3_2022               | Recomendação da Equipe de Avaliação 3 em 2022                                                                                                                                                                              |
| REC_AVAL_4_2022               | Recomendação da Equipe de Avaliação 3 em 2022                                                                                                                                                                              |
| INDICADO_BOLSA_2022           | Campo do Tipo Booleano que sinaliza se o Aluno foi indicado para alguma Bolsa no Ano de 2022                                                                                                                               |
| PONTO_VIRADA_2022             | Campo do Tipo Booleano que sinaliza se o Aluno atingiu o "Ponto de Virada" em 2022                                                                                                                                         |
| IPV_2022                      | Indicador de Ponto de Virada – Média das Notas de Ponto de Virada do Aluno em 2022                                                                                                                                         |
| IAN_2022                      | Indicador de Adequação ao Nível – Média das Notas de Adequação do Aluno ao nível atual em 2022                                                                                                                             |
| NIVEL_IDEAL_2022              | Mostra qual o nível (Fase) ideal do Aluno na Passos Mágicos em 2022                                                                                                                                                        |
```
  
- Links adicionais da passos.docx
- PEDE_ Pontos importantes.docx
- Relatório PEDE2020.pdf
- Relatório PEDE2021.pdf
- Relatório PEDE2022.pdf

Material para desenvolvimento:
- Datathon - Machine Learning Engineering.pdf

Sobre a entrega:
- desenvolver um modelo preditivo capaz de estimar o risco de defasagem escolar de cada estudante
- construir todo o ciclo de vida do modelo, aplicando as melhores práticas de MLOps, desde a construção do melhor modelo até o monitoramento contínuo em produção.

Requisitos de entrega:

- [ ] Treinamento do modelo preditivo: crie uma pipeline completa para treinamento do modelo, considerando feature engineering, pré processamento, treinamento e validação. Salve o modelo utilizando pickle ou joblib para posterior utilização na API. Deixe claro qual é a métrica utilizada na avaliação do modelo, descrevendo por que esse modelo é confiável para ser colocado em produção.

- [ ] Modularização do código: organize o projeto em arquivos .py separados, mantendo o código limpo e de fácil manutenção. Separe funções de pré processamento, engenharia de atributos, treinamento, avaliação e utilitários em módulos distintos para facilitar reuso e testes. 
- [ ] Crie uma API para deployment do modelo: crie uma API utilizando Flask ou FastAPI e implemente um endpoint /predict para receber dados e retornar previsões do modelo. Teste a API localmente utilizando Postman ou cURL para validar seu funcionamento. 
- [ ] Realize o empacotamento do modelo com Docker: crie um Dockerfile para empacotar a API e todas as dependências necessárias. Isso garante que o modelo possa ser executado em qualquer ambiente de maneira isolada e replicável. 
- [ ] Deploy do modelo: realize o deploy do modelo localmente ou na nuvem. Caso utilize um serviço de nuvem, pode optar por AWS, Google Cloud Run, Heroku ou a plataforma de sua preferência.  
- [ ] Teste da API: teste a API para validar sua funcionalidade.  
- [ ] Testes unitários: implemente os testes unitários para verificar o funcionamento correto de cada componente da pipeline, garantindo que seu código tenha maior qualidade (80% de cobertura mínima de testes unitários). 
- [ ] Monitoramento Contínuo: configure logs para monitoramento e disponibilize um painel para acompanhamento de drift no modelo.
- [ ] Documentação: sua documentação deve conter os seguintes requisitos:


 1) Visão Geral do Projeto 
- [ ] Objetivo: descrever de forma clara o problema de negócio que o modelo resolve  (ex.: previsão do risco de defasagem dos estudantes). 
- [ ] Solução Proposta: construção de uma pipeline completa de Machine 
- [ ] Learning, desde o pré-processamento até o deploy do modelo em produção via API. 
- [ ] Stack Tecnológica: 
  • Linguagem: Python 3.X. 
  • Frameworks de ML: scikit-learn, pandas, numpy. 
  • API: Flask ou FastAPI. 
  • Serialização: pickle ou joblib. 
  • Testes: pytest. 
  • Empacotamento: Docker. 
  • Deploy: Local / Cloud (Heroku, AWS, GCP etc.). 
  • Monitoramento: logging + dashboard de drift (se implementado).

2) Estrutura do Projeto (Diretórios e Arquivos):
``` bash
project-root/
├── app/ # Aplicação da API (FastAPI/Flask, etc.)
│ ├── main.py # Arquivo principal da API
│ ├── routes.py # Rotas e endpoints
│ └── model/ # Modelos serializados (.pkl/.joblib)
├── src/ # Código da pipeline de ML
│ ├── preprocessing.py # Funções de limpeza e preparação de dados
│ ├── feature_engineering.py # Engenharia de features
│ ├── train.py # Treinamento do modelo
│ ├── evaluate.py # Avaliação e métricas
│ └── utils.py # Funções auxiliares
│ ├── tests/ # Testes unitários
│ │ ├── test_preprocessing.py
│ │ └── test_model.py
│ ├── Dockerfile # Dockerfile para empacotamento
│ ├── requirements.txt # Dependências do projeto
│ └── README.md # Documentação principal
└── notebooks/ # Jupyter Notebooks (exploração, EDA, etc.)
```

Descrição dos Componentes

Diretório `app/`
Contém todos os arquivos relacionados à API que servirá o modelo treinado.

- **main.py**: Ponto de entrada principal da aplicação API.
- **routes.py**: Define os endpoints e rotas da API.
- **model/**: Armazena os modelos de machine learning serializados (formato .pkl ou .joblib).

iretório `src/`
Contém todo o código-fonte do pipeline de Machine Learning.

- **preprocessing.py**: Funções para limpeza, transformação e preparação dos dados.
- **feature_engineering.py**: Criação e transformação de features para o modelo.
- **train.py**: Scripts para treinamento do modelo.
- **evaluate.py**: Avaliação do modelo com métricas e validação.
- **utils.py**: Funções utilitárias e auxiliares reutilizáveis.
- **tests/**: Testes unitários para garantir a qualidade do código.
- **Dockerfile**: Instruções para criação da imagem Docker do projeto.
- **requirements.txt**: Lista de dependências Python do projeto.
- **README.md**: Documentação específica do módulo src.

### Diretório `notebooks/`
Armazena notebooks Jupyter para análise exploratória de dados (EDA), experimentos e prototipagem.

Workflow Típico

1. **Exploração**: Use notebooks em `notebooks/` para análise inicial.
2. **Desenvolvimento ML**: Implemente o pipeline em `src/`.
3. **Testes**: Execute testes unitários em `src/tests/`.
4. **Treinamento**: Use `train.py` para treinar o modelo.
5. **API**: Empacote o modelo e exponha via API em `app/`.
6. **Containerização**: Use o Dockerfile para criar uma imagem implantável.

Configuração

1. Instale as dependências: `pip install -r src/requirements.txt`
2. Execute testes: `pytest src/tests/`
3. Construa a imagem Docker: `docker build -t my-ml-project -f src/Dockerfile .`

4) Instruções de Deploy (como subir o ambiente):
- [ ] Deixe claro as instruções para subir o ambiente; ex.: docker build, docker run, 
kubectl apply. 
- [ ] Pré-requisitos (Python version, bibliotecas, etc.). 
- [ ] Instalação de dependências (requirements.txt ou environment.yml). 
- [ ] Comandos para treinar, validar e testar o modelo.

4) Exemplos de Chamadas à API 
- [ ] Coloque exemplos de chamadas à API (ex.: via curl, Postman ou scripts 
Python), com inputs esperados e outputs gerados.

5) Etapas do Pipeline de Machine Learning
Explique brevemente na sua documentação quais são as etapas de pré
processamento da sua pipeline.  
Exemplo: 
- [ ] Pré-processamento dos Dados. 
- [ ] Engenharia de Features. 
- [ ] Treinamento e Validação. 
- [ ] Seleção de Modelo. 
- [ ] Pós-processamento (se aplicável).

Sobre a entrega 
A sua entrega deve conter: 
1. Código-fonte organizado e documentado em um repositório GitHub. 
2. Documentação do projeto. 
3. Link para a API. 
4. Vídeo de até cinco minutos, com pelo menos uma pessoa do grupo, no formato gerencial e com a solução proposta do projeto. 

---------------------------------------------------------------------------------
Criação de ambiente
python -m venv .venv
.venv\Scripts\Activate.ps1; pip install -r requirements.txt
.venv\Scripts\Activate.ps1; pip install -r projeto_datathon/src/requirements.txt

Tratamento dos dados

Principais Correções e Melhorias:

Fonte de Dados Confiável: O script agora prioriza a leitura do arquivo Excel original (BASE DE DADOS PEDE 2024 - DATATHON.xlsx) em vez dos CSVs brutos (2022.csv, etc.). Isso resolve as discrepâncias de precisão numérica (ex: INDE 8 vs 7.61) e problemas de formatação que existiam nos CSVs exportados.
Padronização Automática: Adicionei lógica para validar campos padronizados pelo pipeline:
Gênero: Reconhece que "Menina" (Original) é equivalente a "Feminino" (Tratado).
Decimais: Usa tolerância matemática para comparar flutuantes, aceitando pequenas diferenças de arredondamento.
Datas: Suporta múltiplos formatos (PT-BR vs US) durante a comparação.
Relatório Visual: O script imprime a porcentagem de correspondência e destaca apenas discrepâncias reais acima de 1%.
Resultados da Validação:
Ao executar python src/comparacao_dados.py:

2022: 100% de sucesso. 43/43 colunas validadas.
2023: 47/48 colunas validadas.
Diferença esperada: A coluna Idade apresenta ~48% de match. Isso ocorre porque o file_utils.py recalcula a idade (Ano Referencia - Ano Nasc) para garantir consistência, enquanto os dados originais podem conter valores desatualizados ou calculados de forma diferente.
2024: 49/50 colunas validadas.
Diferença esperada: Idade com ~85% de match, pelo mesmo motivo acima.
