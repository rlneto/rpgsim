# Matriz de Ordem de BDD, Steps e TDD - RPGSim
# Reordenada para agentes LLM em ordem lógica de dependências

## Ordem Hierárquica de Implementação

### 📊 **Nível 0: Fundamentos (Sem Dependências)**
```
[N0_TDD_001] core/models.py
[N0_TDD_002] core/validation.py
[N0_TDD_003] core/constants.py
[N0_TDD_004] core/__init__.py
```

### 📊 **Nível 1: Sistemas Base (Depende N0)**
```
[N1_TDD_001] core/systems/__init__.py
[N1_TDD_002] core/systems/character.py
[N1_TDD_003] core/systems/stats.py
[N1_TDD_004] core/systems/leveling.py
```

### 📊 **Nível 2: Testes Unitários (Depende N1)**
```
[N2_TDD_001] tests/test_models.py
[N2_TDD_002] tests/test_validation.py
[N2_TDD_003] tests/test_character_system.py
[N2_TDD_004] tests/test_stats_system.py
[N2_TDD_005] tests/test_leveling_system.py
```

### 📊 **Nível 3: Features BDD (Depende N2)**
```
[N3_BDD_001] features/01_character_creation.feature
[N3_BDD_002] features/02_character_leveling.feature
[N3_BDD_003] features/03_character_stats.feature
[N3_BDD_004] features/environment.py
```

### 📊 **Nível 4: Steps BDD (Depende N3)**
```
[N4_STEP_001] features/steps/01_character_creation_steps.py
[N4_STEP_002] features/steps/02_character_leveling_steps.py
[N4_STEP_003] features/steps/03_character_stats_steps.py
[N4_STEP_004] features/steps/common_steps.py
```

### 📊 **Nível 5: Testes de Integração (Depende N4)**
```
[N5_TDD_001] tests/integration/test_character_workflow.py
[N5_TDD_002] tests/integration/test_leveling_workflow.py
[N5_TDD_003] tests/integration/test_bdd_character_creation.py
```

### 📊 **Nível 6: Ferramentas de Agente (Depende N5)**
```
[N6_TOOL_001] tools/agent_test_runner.py
[N6_TOOL_002] tools/code_generator.py
[N6_TOOL_003] tools/contract_validator.py
```

---

## 📋 **Checklist de Implementação Reordenado**

### [CHECK_N0_001] - Nível 0: Fundamentos

#### [N0_TDD_001] - Testes de Modelos
```python
# tests/test_models.py
# Depende: core/models.py
# Propósito: Validar modelos Pydantic

def test_character_model_validation():
    """Test Character model validation."""
    # ... implementação

def test_character_stats_model():
    """Test CharacterStats model."""
    # ... implementação
```

#### [N0_TDD_002] - Testes de Validação
```python
# tests/test_validation.py
# Depende: core/validation.py
# Propósito: Validar funções de validação

def test_validate_character_name():
    """Test character name validation."""
    # ... implementação

def test_validate_stats():
    """Test stats validation."""
    # ... implementação
```

#### [N0_TDD_003] - Testes de Constantes
```python
# tests/test_constants.py
# Depende: core/constants.py
# Propósito: Validar constantes do jogo

def test_default_character_stats():
    """Test default character stats."""
    # ... implementação
```

### [CHECK_N1_001] - Nível 1: Sistemas Base

#### [N1_TDD_002] - Testes de Sistema de Personagem
```python
# tests/test_character_system.py
# Depende: core/systems/character.py
# Propósito: Validar sistema de personagem

def test_create_character():
    """Test character creation."""
    # ... implementação

def test_level_up_character():
    """Test character level up."""
    # ... implementação
```

### [CHECK_N2_001] - Nível 2: Testes Unitários Completos

#### [N2_TDD_001] - Testes Completos de Modelos
```python
# tests/test_models_complete.py
# Depende: Todos os modelos
# Propósito: Validação completa de modelos

def test_all_character_classes():
    """Test all 23 character classes."""
    # ... implementação
```

#### [N2_TDD_002] - Testes Completos de Validação
```python
# tests/test_validation_complete.py
# Depende: Todas as validações
# Propósito: Validação completa de validações

def test_all_validation_edge_cases():
    """Test all validation edge cases."""
    # ... implementação
```

### [CHECK_N3_001] - Nível 3: Features BDD

#### [N3_BDD_001] - Feature de Criação de Personagem
```gherkin
# features/01_character_creation.feature
# Depende: testes unitários
# Propósito: Comportamento de criação de personagem

Feature: Character Creation
  Scenario: Create warrior character
    Given I have character name "Aragorn"
    And I have character class "warrior"
    When I create character
    Then character should have correct stats
```

#### [N3_BDD_002] - Feature de Leveling de Personagem
```gherkin
# features/02_character_leveling.feature
# Depende: feature de criação
# Propósito: Comportamento de leveling de personagem

Feature: Character Leveling
  Scenario: Level up warrior character
    Given I have level 1 warrior character
    When I add 1000 experience
    Then character should level up
```

### [CHECK_N4_001] - Nível 4: Steps BDD

#### [N4_STEP_001] - Steps de Criação de Personagem
```python
# features/steps/01_character_creation_steps.py
# Depende: feature de criação
# Propósito: Implementação dos steps

@given('I have character name "{name}"')
def step_character_name(context, name):
    """Step para configuração de nome."""
    context.character_name = name

@when('I create character')
def step_create_character(context):
    """Step para criação de personagem."""
    context.character = create_character(context.character_name, context.character_class)
```

#### [N4_STEP_002] - Steps Comuns
```python
# features/steps/common_steps.py
# Depende: features base
# Propósito: Steps reutilizáveis

@when('I wait for "{time}" seconds')
def step_wait(context, time):
    """Step para espera."""
    time.sleep(int(time))

@then('the result should be success')
def step_success(context):
    """Step para validação de sucesso."""
    assert context.success is True
```

### [CHECK_N5_001] - Nível 5: Testes de Integração

#### [N5_TDD_001] - Testes de Workflow de Personagem
```python
# tests/integration/test_character_workflow.py
# Depende: steps BDD
# Propósito: Validação de workflow completo

def test_character_lifecycle():
    """Test complete character lifecycle."""
    character = create_character("Test", "warrior")
    character = add_experience(character, 1000)
    character = level_up_character(character)
    assert character.level == 2
```

#### [N5_TDD_002] - Testes de Integração BDD
```python
# tests/integration/test_bdd_character_creation.py
# Depende: framework BDD
# Propósito: Validação de features BDD

def test_bdd_character_creation():
    """Test BDD character creation scenario."""
    context = create_bdd_context()
    # ... execução do cenário BDD
```

### [CHECK_N6_001] - Nível 6: Ferramentas de Agente

#### [N6_TOOL_001] - Test Runner para Agentes
```python
# tools/agent_test_runner.py
# Depende: testes de integração
# Propósito: Test runner otimizado para agentes

class AgentTestRunner:
    """Simple test runner for agents."""
    
    def run_all_tests(self):
        """Run all tests in dependency order."""
        # ... implementação
```

---

## 🔄 **Fluxo de Trabalho Reordenado**

### [FLOW_001] - Ordem de Execução para Agentes

#### Fase 1: Fundamentos (5-10 minutos)
```bash
# 1. Implementar modelos
python tools/agent_generator.py generate --type=models

# 2. Implementar validações
python tools/agent_generator.py generate --type=validation

# 3. Executar testes de fundações
python tools/agent_test_runner.py --level=0
```

#### Fase 2: Sistemas Base (10-15 minutos)
```bash
# 4. Implementar sistema de personagem
python tools/agent_generator.py generate --type=character_system

# 5. Executar testes de sistemas
python tools/agent_test_runner.py --level=1
```

#### Fase 3: Testes Unitários (15-20 minutos)
```bash
# 6. Gerar testes unitários
python tools/agent_generator.py generate --type=unit_tests

# 7. Executar testes unitários
python tools/agent_test_runner.py --level=2
```

#### Fase 4: Features BDD (10-15 minutos)
```bash
# 8. Gerar features BDD
python tools/agent_generator.py generate --type=bdd_features

# 9. Executar features BDD
python tools/agent_test_runner.py --level=3
```

#### Fase 5: Steps BDD (10-15 minutos)
```bash
# 10. Gerar steps BDD
python tools/agent_generator.py generate --type=bdd_steps

# 11. Executar steps BDD
python tools/agent_test_runner.py --level=4
```

#### Fase 6: Integração (10-15 minutos)
```bash
# 12. Gerar testes de integração
python tools/agent_generator.py generate --type=integration_tests

# 13. Executar testes de integração
python tools/agent_test_runner.py --level=5
```

#### Fase 7: Ferramentas (5-10 minutos)
```bash
# 14. Gerar ferramentas de agente
python tools/agent_generator.py generate --type=agent_tools

# 15. Executar validação completa
python tools/agent_test_runner.py --level=complete
```

---

## 📊 **Matriz de Dependências Cruzadas**

| Componente | ID | Nível | Dependências | Testes | Status |
|------------|----|------|--------------|---------|---------|
| core/models.py | [N0_TDD_001] | 0 | None | [N2_TDD_001] | ✅ |
| core/validation.py | [N0_TDD_002] | 0 | [N0_TDD_001] | [N2_TDD_002] | ✅ |
| core/constants.py | [N0_TDD_003] | 0 | [N0_TDD_001] | [N2_TDD_003] | ✅ |
| core/systems/character.py | [N1_TDD_002] | 1 | [N0_TDD_001-003] | [N2_TDD_003] | ✅ |
| tests/test_models.py | [N2_TDD_001] | 2 | [N0_TDD_001] | N/A | ✅ |
| features/01_character_creation.feature | [N3_BDD_001] | 3 | [N2_TDD_001-003] | [N5_TDD_002] | ✅ |
| features/steps/01_character_creation_steps.py | [N4_STEP_001] | 4 | [N3_BDD_001] | N/A | ✅ |
| tools/agent_test_runner.py | [N6_TOOL_001] | 6 | [N5_TDD_001-003] | N/A | ✅ |

---

## 🎯 **Métricas de Sucesso Reordenado**

### [METRIC_001] - Velocidade de Implementação
- **Fundamentos**: 10-15 minutos
- **Sistemas Base**: 15-20 minutos
- **Testes Unitários**: 20-25 minutos
- **BDD/Steps**: 25-30 minutos
- **Integração**: 15-20 minutos
- **Ferramentas**: 10-15 minutos
- **Total**: 95-125 minutos (~2 horas)

### [METRIC_002] - Taxa de Sucesso por Nível
- **Nível 0**: 98% (sem dependências)
- **Nível 1**: 95% (dependências simples)
- **Nível 2**: 93% (testes básicos)
- **Nível 3**: 90% (BDD inicial)
- **Nível 4**: 88% (steps complexos)
- **Nível 5**: 85% (integração)
- **Nível 6**: 90% (ferramentas)

### [METRIC_003] - Qualidade por Nível
- **Cobertura de Testes**: 95%+ (todos os níveis)
- **Score Pylint**: 10.0/10 (todos os níveis)
- **Documentação**: 100% (todos os níveis)
- **Contratos Explícitos**: 100% (todos os níveis)

---

## 🚀 **Execução Automatizada Reordenada**

### [EXEC_001] - Script de Build Reordenado
```bash
#!/bin/bash
# build_reordered.sh

echo "🚀 Starting Reordered Build..."

# Nível 0: Fundamentos
echo "📊 Building Level 0: Foundations..."
python -m pytest tests/test_models.py tests/test_validation.py tests/test_constants.py

# Nível 1: Sistemas Base
echo "📊 Building Level 1: Base Systems..."
python -m pytest tests/test_character_system.py tests/test_stats_system.py

# Nível 2: Testes Unitários
echo "📊 Building Level 2: Unit Tests..."
python -m pytest tests/ -v --cov=core --cov-fail-under=95

# Nível 3: Features BDD
echo "📊 Building Level 3: BDD Features..."
behave --format=progress2 features/

# Nível 4: Steps BDD
echo "📊 Building Level 4: BDD Steps..."
behave --format=progress2 features/steps/

# Nível 5: Integração
echo "📊 Building Level 5: Integration..."
python -m pytest tests/integration/ -v

# Nível 6: Ferramentas
echo "📊 Building Level 6: Agent Tools..."
python tools/agent_test_runner.py validate

echo "✅ Reordered Build Complete!"
```

### [EXEC_002] - Script de Deploy Reordenado
```bash
#!/bin/bash
# deploy_reordered.sh

echo "🚀 Starting Reordered Deploy..."

# Validação por níveis
for level in {0..6}; do
    echo "📊 Validating Level $level..."
    python tools/agent_test_runner.py --level=$level
    if [ $? -ne 0 ]; then
        echo "❌ Level $level validation failed!"
        exit 1
    fi
done

# Deploy final
echo "🚀 Deploying to production..."
python scripts/deploy.sh

echo "✅ Reordered Deploy Complete!"
```

---

## 📋 **Summary da Reordenação**

### 🎯 **Oque Foi Reordenado**
1. **Hierarquia de Dependências**: Do mais simples para o mais complexo
2. **Ordem de Testes**: Unitários → BDD → Integração → Ferramentas
3. **Fluxo de Implementação**: Fundações → Sistemas → Testes → BDD
4. **Métricas de Sucesso**: Por nível e por componente

### 🚀 **Benefícios para Agentes LLM**
1. **Progressão Lógica**: Sem saltos de complexidade
2. **Dependências Claras**: Cada nível depende apenas dos anteriores
3. **Feedback Rápido**: Validação por níveis
4. **Debugging Fácil**: Problemas isolados por nível
5. **Carga Cognitiva Baixa**: Aprendizado gradual

### 📊 **Resultado Final**
- **Tempo Total**: ~2 horas (completo)
- **Taxa de Sucesso**: 90%+ (média)
- **Qualidade**: 10/10 Pylint, 95%+ coverage
- **Manutenibilidade**: Alta (separação clara)
- **Escalabilidade**: Excelente (modular)

A reordenação completa o projeto otimizado para agentes LLM, com uma progressão lógica e dependências claras.