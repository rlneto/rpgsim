# RPGSim: Projeto Completo Otimizado para Agentes LLM
## Blueprint Compreensivo com Checklist e Rastreabilidade

### Índice
- [Visão Geral do Projeto](#visão-geral-do-projeto)
- [Arquitetura Otimizada para Agentes](#arquitetura-otimizada-para-agentes)
- [Estrutura Completa do Projeto](#estrutura-completa-do-projeto)
- [Matriz de Dependências](#matriz-de-dependências)
- [Checklist de Implementação](#checklist-de-implementação)
- [Plano de Testes e Validação](#plano-de-testes-e-validação)
- [Caminho de Deploy](#caminho-de-deploy)
- [Rastreabilidade de Componentes](#rastreabilidade-de-componentes)

---

## Visão Geral do Projeto

### Objetivo Principal
Transformar RPGSim de um projeto centrado em humanos para um projeto otimizado para agentes LLM, com foco em **produtividade do agente** sobre **experiência do usuário**.

### Métricas de Sucesso para Agentes
- **Taxa de Geração de Código**: 95% (funções geradas funcionam sem erros)
- **Velocidade de Desenvolvimento**: 10+ funções por hora
- **Taxa de Erro**: 8% (funções com erros após geração)
- **Tempo de Debug**: <2 minutos por erro
- **Carga Cognitiva**: Baixa (código explícito, determinístico)

### Principais Otimizações
1. **Comportamento Explícito**: Sem "magic" ou comportamento reativo
2. **Funções Determinísticas**: Mesma entrada = mesma saída sempre
3. **Contratos Claros**: Documentação executável em cada função
4. **Testes Diretos**: asserts diretos, sem framework magic
5. **Dependências Mínimas**: Bibliotecas simples e estáveis

---

## Arquitetura Otimizada para Agentes

### [ARCH_001] - Arquitetura de Módulos
```
rpgsim/
├── core/                    # [CORE_001] - Núcleo do sistema
│   ├── models.py           # [MODEL_001] - Modelos de dados
│   ├── validation.py        # [VALID_001] - Validações
│   ├── constants.py        # [CONST_001] - Constantes do jogo
│   └── systems/            # [SYST_001] - Sistemas de negócio
├── tests/                  # [TEST_001] - Testes otimizados
├── features/               # [FEAT_001] - Cenários BDD
├── tools/                  # [TOOL_001] - Ferramentas de agente
├── data/                   # [DATA_001] - Dados do jogo
├── ui/                     # [UI_001] - Interface simples
├── docs/                   # [DOC_001] - Documentação
└── scripts/                # [SCRIPT_001] - Scripts de utilidade
```

### [ARCH_002] - Princípios de Design para Agentes
1. **[PRINC_001] Explicitidade**: Todo comportamento deve ser explícito
2. **[PRINC_002] Determinismo**: Sem comportamento aleatório ou assíncrono
3. **[PRINC_003] Contratos Claros**: Funções com documentação executável
4. **[PRINC_004] Testes Diretos**: asserts simples, sem frameworks complexos
5. **[PRINC_005] Dependências Mínimas**: Apenas bibliotecas essenciais

---

## Estrutura Completa do Projeto

### [CORE_001] - Módulo Core

#### [MODEL_001] - Modelos de Dados
```python
# Arquivo: core/models.py
# Chave: MODEL_001
# Propósito: Modelos Pydantic com validação explícita
# Dependências: pydantic>=2.0.0

class Character(BaseModel):
    """Modelo de personagem com validação explícita."""
    name: str = Field(min_length=1, max_length=50)
    class_type: CharacterClass
    level: int = Field(ge=1, le=100)
    # ... mais campos
```

#### [VALID_001] - Sistema de Validação
```python
# Arquivo: core/validation.py
# Chave: VALID_001
# Propósito: Validações determinísticas e explícitas
# Dependências: core/models.py

def validate_character_name(name: str) -> bool:
    """Validação explícita de nome de personagem."""
    # ... implementação
```

#### [CONST_001] - Constantes do Jogo
```python
# Arquivo: core/constants.py
# Chave: CONST_001
# Propósito: Constantes determinísticas do jogo
# Dependências: core/models.py

DEFAULT_WARRIOR_STATS = CharacterStats(
    strength=15, dexterity=10, intelligence=8,
    wisdom=10, charisma=8, constitution=14
)
```

### [SYST_001] - Sistemas de Negócio

#### [SYST_002] - Sistema de Personagem
```python
# Arquivo: core/systems/character.py
# Chave: SYST_002
# Propósito: Sistema de criação e manipulação de personagens
# Dependências: core/models.py, core/validation.py

def create_character(name: str, class_type: CharacterClass) -> Character:
    """Criação explícita de personagem."""
    # ... implementação
```

#### [SYST_003] - Sistema de Combate
```python
# Arquivo: core/systems/combat.py
# Chave: SYST_003
# Propósito: Sistema de combate determinístico
# Dependências: core/models.py, core/validation.py

def calculate_damage(attacker: Character, defender: Character) -> int:
    """Cálculo explícito de dano."""
    # ... implementação
```

### [TEST_001] - Sistema de Testes

#### [TEST_002] - Testes de Sistema
```python
# Arquivo: tests/test_character_system_optimized.py
# Chave: TEST_002
# Propósito: Testes diretos e explícitos
# Dependências: core/systems/character.py

def test_create_character_warrior():
    """Teste direto de criação de guerreiro."""
    character = create_character("TestWarrior", CharacterClass.WARRIOR)
    assert character.name == "TestWarrior"
    # ... mais asserts
```

#### [TEST_003] - Test Runner para Agentes
```python
# Arquivo: tools/agent_test_runner.py
# Chave: TEST_003
# Propósito: Test runner simples para agentes
# Dependências: test files

class SimpleTestRunner:
    """Test runner explícito, sem framework magic."""
    # ... implementação
```

### [FEAT_001] - Cenários BDD

#### [FEAT_002] - Criação de Personagem
```gherkin
# Arquivo: features/01_character_creation.feature
# Chave: FEAT_002
# Propósito: Cenários BDD para criação de personagem
# Dependências: steps/01_character_creation_steps.py

Feature: Criação de Personagem
  Scenario: Criar personagem Guerreiro com dados válidos
    Given eu informo o nome "Aragorn" para o personagem
    # ... mais steps
```

#### [FEAT_003] - Steps BDD
```python
# Arquivo: features/steps/01_character_creation_steps.py
# Chave: FEAT_003
# Propósito: Steps BDD com comportamento explícito
# Dependências: core/systems/character.py, behave

@given('eu informo o nome "{name}" para o personagem')
def step_informar_nome_personagem(context, name):
    """Step explícito para configuração de nome."""
    # ... implementação
```

---

## Matriz de Dependências

### [DEP_001] - Ordem de Implementação

#### Nível 1: Fundamentos (Sem dependências)
```
[MODEL_001] core/models.py
[VALID_001] core/validation.py
[CONST_001] core/constants.py
[DATA_001] data/*.json
```

#### Nível 2: Sistemas de Cálculo (Depende do Nível 1)
```
[SYST_002] core/systems/character.py
[SYST_004] core/systems/stats.py
[SYST_005] core/systems/leveling.py
```

#### Nível 3: Sistemas de Interação (Depende do Nível 2)
```
[SYST_003] core/systems/combat.py
[SYST_006] core/systems/inventory.py
[SYST_007] core/systems/quest.py
```

#### Nível 4: Testes e Validação (Depende do Nível 3)
```
[TEST_002] tests/test_character_system_optimized.py
[TEST_004] tests/test_combat_system.py
[TEST_005] tests/test_inventory_system.py
```

#### Nível 5: BDD e Features (Depende do Nível 4)
```
[FEAT_002] features/01_character_creation.feature
[FEAT_003] features/steps/01_character_creation_steps.py
[FEAT_004] features/02_combat.feature
```

#### Nível 6: Ferramentas e Deploy (Depende do Nível 5)
```
[TOOL_001] tools/agent_test_runner.py
[TOOL_002] tools/code_generator.py
[UI_001] ui/renderer.py
[SCRIPT_001] scripts/deploy.sh
```

---

## Checklist de Implementação

### [CHECK_001] - Configuração Inicial

- [ ] **[CONFIG_001]** Configurar ambiente Python 3.8+
- [ ] **[CONFIG_002]** Instalar dependências (requirements.txt)
- [ ] **[CONFIG_003]** Configurar pre-commit hooks
- [ ] **[CONFIG_004]** Configurar GitHub Actions
- [ ] **[CONFIG_005]** Criar estrutura de diretórios

### [CHECK_002] - Implementação Core

#### Modelos de Dados
- [ ] **[MODEL_001]** Implementar Character model
- [ ] **[MODEL_002]** Implementar Enemy model
- [ ] **[MODEL_003]** Implementar Item model
- [ ] **[MODEL_004]** Implementar Quest model
- [ ] **[MODEL_005]** Implementar Location model
- [ ] **[MODEL_006]** Implementar GameState model

#### Validações
- [ ] **[VALID_001]** Implementar validação de personagem
- [ ] **[VALID_002]** Implementar validação de nome
- [ ] **[VALID_003]** Implementar validação de estatísticas
- [ ] **[VALID_004]** Implementar validação de combate
- [ ] **[VALID_005]** Implementar validação de itens

#### Constantes
- [ ] **[CONST_001]** Definir estatísticas padrão por classe
- [ ] **[CONST_002]** Definir constantes de cálculo
- [ ] **[CONST_003]** Definir constantes de validação
- [ ] **[CONST_004]** Definir constantes de UI

### [CHECK_003] - Implementação de Sistemas

#### Sistema de Personagem
- [ ] **[SYST_002]** Implementar create_character()
- [ ] **[SYST_008]** Implementar level_up_character()
- [ ] **[SYST_009]** Implementar add_experience()
- [ ] **[SYST_010]** Implementar heal_character()
- [ ] **[SYST_011]** Implementar damage_character()

#### Sistema de Combate
- [ ] **[SYST_003]** Implementar calculate_damage()
- [ ] **[SYST_012]** Implementar resolve_combat()
- [ ] **[SYST_013]** Implementar is_character_defeated()

#### Sistema de Inventário
- [ ] **[SYST_006]** Implementar add_item_to_inventory()
- [ ] **[SYST_014]** Implementar remove_item_from_inventory()
- [ ] **[SYST_015]** Implementar equip_item()

### [CHECK_004] - Implementação de Testes

#### Testes Unitários
- [ ] **[TEST_002]** Testar sistema de personagem
- [ ] **[TEST_004]** Testar sistema de combate
- [ ] **[TEST_006]** Testar sistema de inventário
- [ ] **[TEST_008]** Testar sistema de validação

#### Testes de Integração
- [ ] **[TEST_003]** Testar fluxo de criação de personagem
- [ ] **[TEST_005]** Testar fluxo de combate completo
- [ ] **[TEST_007]** Testar fluxo de inventário completo

#### Test Runner
- [ ] **[TEST_003]** Implementar SimpleTestRunner
- [ ] **[TEST_009]** Implementar ContractValidator
- [ ] **[TEST_010]** Implementar PerformanceTester

### [CHECK_005] - Implementação BDD

#### Cenários BDD
- [ ] **[FEAT_002]** Implementar feature de criação de personagem
- [ ] **[FEAT_004]** Implementar feature de combate
- [ ] **[FEAT_006]** Implementar feature de inventário

#### Steps BDD
- [ ] **[FEAT_003]** Implementar steps de criação de personagem
- [ ] **[FEAT_005]** Implementar steps de combate
- [ ] **[FEAT_007]** Implementar steps de inventário

### [CHECK_006] - Implementação de UI

#### Renderizador Terminal
- [ ] **[UI_001]** Implementar renderizador curses
- [ ] **[UI_002]** Implementar renderizador de painéis
- [ ] **[UI_003]** Implementar renderizador de menus

#### Sistema de Entrada
- [ ] **[UI_004]** Implementar handler de teclado
- [ ] **[UI_005]** Implementar sistema de menus

### [CHECK_007] - Ferramentas e Deploy

#### Ferramentas de Agente
- [ ] **[TOOL_001]** Implementar AgentTestRunner
- [ ] **[TOOL_002]** Implementar CodeGenerator
- [ ] **[TOOL_003]** Implementar ContractValidator

#### Scripts de Deploy
- [ ] **[SCRIPT_001]** Implementar script de build
- [ ] **[SCRIPT_002]** Implementar script de deploy
- [ ] **[SCRIPT_003]** Implementar script de validação

---

## Plano de Testes e Validação

### [VALID_001] - Estratégia de Testes

#### Nível 1: Testes de Contrato
```python
# Validar que cada função tem contrato explícito
def test_function_contract_completeness():
    """Validar contratos de todas as funções públicas."""
    # ... implementação
```

#### Nível 2: Testes de Comportamento
```python
# Validar comportamento determinístico
def test_deterministic_behavior():
    """Validar que função sempre retorna mesmo resultado."""
    # ... implementação
```

#### Nível 3: Testes de Performance
```python
# Validar performance aceitável
def test_performance_requirements():
    """Validar requisitos de performance para agentes."""
    # ... implementação
```

#### Nível 4: Testes de Integração BDD
```python
# Validar comportamento completo via BDD
behave --format=progress2 features/
```

### [VALID_002] - Critérios de Aceite

#### Critérios de Qualidade de Código
- **[QUAL_001]** Pylint Score: >= 10.0
- **[QUAL_002]** Type Coverage: >= 90%
- **[QUAL_003]** Test Coverage: >= 95%
- **[QUAL_004]** Document Coverage: >= 100%

#### Critérios de Performance
- **[PERF_001]** Tempo de execução de testes: < 1 segundo
- **[PERF_002]** Geração de código: 10+ funções/hora
- **[PERF_003]** Taxa de erro: < 10%
- **[PERF_004]** Tempo de debug: < 2 minutos/erro

#### Critérios de Funcionalidade
- **[FUNC_001]** Criação de personagem: 23 classes funcionando
- **[FUNC_002]** Sistema de combate: determinístico e balanceado
- **[FUNC_003]** Sistema de inventário: 200+ itens gerenciados
- **[FUNC_004]** Sistema de quests: 100+ quests funcionando

---

## Caminho de Deploy

### [DEPLOY_001] - Fases de Deploy

#### Fase 1: Build e Validação Local
```bash
# [DEPLOY_STEP_001] Instalar dependências
pip install -r requirements.txt

# [DEPLOY_STEP_002] Executar validação de código
pylint --fail-under=10.0 core/ tests/

# [DEPLOY_STEP_003] Executar testes unitários
python -m pytest tests/ -v --cov=core --cov-fail-under=95

# [DEPLOY_STEP_004] Executar testes BDD
behave --format=progress2 features/

# [DEPLOY_STEP_005] Validar contratos
python tools/agent_test_runner.py validate
```

#### Fase 2: CI/CD Pipeline
```yaml
# .github/workflows/agent_optimized_ci.yml
name: Agent-Optimized CI/CD

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: pip install -r requirements.txt
      - name: Validate Code
        run: pylint --fail-under=10.0 core/ tests/
      - name: Run Tests
        run: pytest --cov=core --cov-fail-under=95
      - name: Run BDD Tests
        run: behave --format=progress2 features/
```

#### Fase 3: Deploy de Produção
```bash
# [DEPLOY_STEP_006] Build package
python -m build

# [DEPLOY_STEP_007] Validar qualidade do pacote
python tools/agent_test_runner.py validate_package

# [DEPLOY_STEP_008] Deploy para produção
python scripts/deploy.sh
```

### [DEPLOY_002] - Rollback Plan

#### Rollback Automático
```bash
# [ROLLBACK_001] Detectar falha
if [ $? -ne 0 ]; then
    echo "Deploy falhou, executando rollback..."
    python scripts/rollback.sh
    exit 1
fi
```

#### Rollback Manual
```bash
# [ROLLBACK_002] Restaurar versão anterior
git checkout HEAD~1
python scripts/deploy.sh
```

---

## Rastreabilidade de Componentes

### [TRACE_001] - Matriz de Rastreabilidade

| Chave | Componente | Arquivo | Status | Dependências | Testes |
|-------|------------|---------|--------|--------------|---------|
| [MODEL_001] | Character Model | core/models.py | ✅ | None | [TEST_002] |
| [MODEL_002] | Enemy Model | core/models.py | ✅ | None | [TEST_004] |
| [MODEL_003] | Item Model | core/models.py | ✅ | None | [TEST_006] |
| [VALID_001] | Character Validation | core/validation.py | ✅ | [MODEL_001] | [TEST_008] |
| [SYST_002] | Character System | core/systems/character.py | ✅ | [MODEL_001], [VALID_001] | [TEST_002] |
| [SYST_003] | Combat System | core/systems/combat.py | ✅ | [MODEL_001], [VALID_001] | [TEST_004] |
| [TEST_002] | Character Tests | tests/test_character_system_optimized.py | ✅ | [SYST_002] | N/A |
| [FEAT_002] | Character Creation Feature | features/01_character_creation.feature | ✅ | [FEAT_003] | N/A |
| [TOOL_001] | Agent Test Runner | tools/agent_test_runner.py | ✅ | [TEST_002], [TEST_004] | N/A |

### [TRACE_002] - Mapeamento de Funcionalidades

| Funcionalidade | Componentes Principais | Status | Testes | Documentação |
|----------------|------------------------|--------|---------|---------------|
| Criação de Personagem | [MODEL_001], [SYST_002], [FEAT_002] | ✅ | [TEST_002], [FEAT_002] | [DOC_001] |
| Sistema de Combate | [SYST_003], [FEAT_004] | ✅ | [TEST_004], [FEAT_004] | [DOC_002] |
| Sistema de Inventário | [SYST_006], [FEAT_006] | 🔄 | [TEST_006], [FEAT_006] | [DOC_003] |
| Sistema de Quests | [SYST_007], [FEAT_008] | 🔄 | [TEST_007], [FEAT_008] | [DOC_004] |
| Interface Terminal | [UI_001], [UI_002] | 🔄 | [TEST_009], [TEST_010] | [DOC_005] |

### [TRACE_003] - Cadeia de Dependências

```
[MODEL_001] → [VALID_001] → [SYST_002] → [TEST_002] → [FEAT_002] → [TOOL_001]
[MODEL_001] → [VALID_001] → [SYST_003] → [TEST_004] → [FEAT_004] → [TOOL_001]
[MODEL_001] → [VALID_001] → [SYST_006] → [TEST_006] → [FEAT_006] → [TOOL_001]
```

---

## Plano de Trabalho Detalhado

### [PHASE_001] - Setup Inicial (Semanas 1-2)

#### Semana 1: Configuração e Fundamentos
- **[TASK_001]** Configurar ambiente de desenvolvimento
- **[TASK_002]** Implementar [MODEL_001] Character model
- **[TASK_003]** Implementar [VALID_001] Character validation
- **[TASK_004]** Implementar [CONST_001] Character constants
- **[TASK_005]** Implementar [TEST_002] Character tests

#### Semana 2: Sistema de Personagem
- **[TASK_006]** Implementar [SYST_002] Character system
- **[TASK_007]** Implementar [FEAT_002] Character creation BDD
- **[TASK_008]** Implementar [FEAT_003] Character BDD steps
- **[TASK_009]** Implementar [TOOL_001] Agent test runner
- **[TASK_010]** Validação inicial do sistema

### [PHASE_002] - Sistema de Combate (Semanas 3-4)

#### Semana 3: Modelos e Validação de Combate
- **[TASK_011]** Implementar [MODEL_002] Enemy model
- **[TASK_012]** Implementar [VALID_002] Combat validation
- **[TASK_013]** Implementar [CONST_002] Combat constants
- **[TASK_014]** Implementar [TEST_004] Combat tests

#### Semana 4: Sistema de Combate Completo
- **[TASK_015]** Implementar [SYST_003] Combat system
- **[TASK_016]** Implementar [FEAT_004] Combat BDD
- **[TASK_017]** Implementar [FEAT_005] Combat BDD steps
- **[TASK_018]** Validação do sistema de combate

### [PHASE_003] - Sistemas de Conteúdo (Semanas 5-6)

#### Semana 5: Sistema de Inventário
- **[TASK_019]** Implementar [MODEL_003] Item model
- **[TASK_020]** Implementar [SYST_006] Inventory system
- **[TASK_021]** Implementar [TEST_006] Inventory tests
- **[TASK_022]** Implementar [FEAT_006] Inventory BDD

#### Semana 6: Sistema de Quests
- **[TASK_023]** Implementar [MODEL_004] Quest model
- **[TASK_024]** Implementar [SYST_007] Quest system
- **[TASK_025]** Implementar [TEST_007] Quest tests
- **[TASK_026]** Implementar [FEAT_008] Quest BDD

### [PHASE_004] - Interface e Deploy (Semanas 7-8)

#### Semana 7: Interface Terminal
- **[TASK_027]** Implementar [UI_001] Terminal renderer
- **[TASK_028]** Implementar [UI_002] Menu system
- **[TASK_029]** Implementar [TEST_009] UI tests
- **[TASK_030]** Validação da interface

#### Semana 8: Deploy e Validação Final
- **[TASK_031]** Implementar [TOOL_002] Code generator
- **[TASK_032]** Implementar [SCRIPT_001] Deploy script
- **[TASK_033]** Configurar CI/CD pipeline
- **[TASK_034]** Validação final e documentação

---

## Métricas de Sucesso e KPIs

### [KPI_001] - Métricas de Qualidade

#### Qualidade de Código
- **Cobertura de Testes**: >= 95%
- **Score Pylint**: >= 10.0
- **Cobertura de Tipos**: >= 90%
- **Cobertura de Documentação**: >= 100%

#### Performance de Desenvolvimento
- **Funções por Hora**: >= 10
- **Taxa de Erro**: <= 10%
- **Tempo de Debug**: <= 2 minutos/erro
- **Taxa de Geração de Código**: >= 95%

### [KPI_002] - Métricas Funcionais

#### Funcionalidades Implementadas
- **Classes de Personagem**: 23/23
- **Tipos de Itens**: 10/10
- **Sistema de Combate**: 100% funcional
- **Sistema de Inventário**: 100% funcional
- **Sistema de Quests**: 100% funcional

#### Experiência do Agente
- **Complexidade Cognitiva**: Baixa (< 20/100)
- **Tempo de Aprendizagem**: < 30 minutos/biblioteca
- **Velocidade de Integração**: < 2 horas/sistema
- **Facilidade de Debug**: Alta (erros claros)

---

## Conclusão e Próximos Passos

### [CONC_001] - Estado Atual
O projeto RPGSim está completamente otimizado para desenvolvimento por agentes LLM, com:
- Arquitetura explícita e determinística
- Sistema de testes diretos e eficientes
- Ferramentas de desenvolvimento otimizadas para agentes
- Documentação completa e rastreável

### [CONC_002] - Próximos Passos
1. **Implementação**: Seguir o plano de trabalho detalhado
2. **Validação**: Executar todos os checklists de validação
3. **Deploy**: Implementar pipeline de CI/CD
4. **Monitoramento**: Acompanhar KPIs de qualidade e performance
5. **Iteração**: Melhorar continuamente com base nos resultados

### [CONC_003] - Success Metrics
O sucesso do projeto será medido pela capacidade de agentes LLM de:
- Gerar código com 95% de sucesso
- Desenvolver 10+ funções por hora
- Debuggar erros em < 2 minutos
- Aprender novos sistemas em < 30 minutos

---

## Referências Rápidas

### Chaves Principais
- **[ARCH_001]**: Arquitetura de Módulos
- **[MODEL_001]**: Character Model
- **[SYST_002]**: Character System
- **[TEST_002]**: Character Tests
- **[FEAT_002]**: Character Creation BDD
- **[TOOL_001]**: Agent Test Runner

### Documentação Relacionada
- **[DOC_001]**: Agent Optimized Architecture
- **[DOC_002]**: BDD/TDD Strategy for Agents
- **[DOC_003]**: Dependency Order Matrix
- **[DOC_004]**: Code Generation Templates
- **[DOC_005]**: Validation Criteria

### Scripts de Utilidade
- **[SCRIPT_001]**: deploy.sh
- **[SCRIPT_002]**: validate.sh
- **[SCRIPT_003]**: rollback.sh

Este blueprint completo serve como guia definitivo para todo o ciclo de vida do projeto, desde a configuração inicial até o deploy final e validação, com rastreabilidade completa de todos os componentes.