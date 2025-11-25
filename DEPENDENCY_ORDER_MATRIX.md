# Matriz de Ordem de Dependências - RPGSim
# Otimizada para Agentes LLM - Ordem lógica de implementação

## Ordem de Dependências (Do mais simples para o mais complexo)

### Nível 1: Fundamentos (Sem dependências)
```
1. Modelos de Dados (core/models.py)
   - Estruturas de dados básicas
   - Validações internas
   - Sem dependências externas

2. Sistema de Validação (core/validation.py)
   - Funções de validação puras
   - Depende apenas de modelos
   - Sem efeitos colaterais

3. Utilitários Matemáticos (core/math_utils.py)
   - Funções matemáticas puras
   - Determinísticas
   - Sem dependências de estado
```

### Nível 2: Sistemas de Cálculo (Depende do Nível 1)
```
4. Sistema de Estatísticas (core/systems/stats.py)
   - Cálculo de estatísticas de personagem
   - Depende de modelos e validação
   - Funções puras e determinísticas

5. Sistema de Nível (core/systems/leveling.py)
   - Cálculo de experiência e progressão
   - Depende de estatísticas
   - Funções puras e determinísticas

6. Sistema de Habilidade (core/systems/abilities.py)
   - Gerenciamento de habilidades
   - Depende de modelos
   - Funções puras e determinísticas
```

### Nível 3: Sistemas de Entidade (Depende do Nível 2)
```
7. Sistema de Personagem (core/systems/character.py)
   - Criação e manipulação de personagens
   - Depende de estatísticas, nível, habilidades
   - Funções determinísticas com estado explícito

8. Sistema de Inimigo (core/systems/enemy.py)
   - Criação e manipulação de inimigos
   - Depende de estatísticas
   - Funções determinísticas com estado explícito

9. Sistema de Item (core/systems/items.py)
   - Criação e manipulação de itens
   - Depende de modelos
   - Funções determinísticas com estado explícito
```

### Nível 4: Sistemas de Interação (Depende do Nível 3)
```
10. Sistema de Combate (core/systems/combat.py)
    - Lógica de combate entre entidades
    - Depende de personagem e inimigo
    - Funções determinísticas com estado explícito

11. Sistema de Inventário (core/systems/inventory.py)
    - Gerenciamento de inventário
    - Depende de personagem e item
    - Funções determinísticas com estado explícito

12. Sistema de Quest (core/systems/quest.py)
    - Gerenciamento de missões
    - Depende de personagem
    - Funções determinísticas com estado explícito
```

### Nível 5: Sistemas de Mundo (Depende do Nível 4)
```
13. Sistema de Localização (core/systems/location.py)
    - Gerenciamento de locais
    - Depende de personagem e quest
    - Funções determinísticas com estado explícito

14. Sistema de Save/Load (core/systems/save_load.py)
    - Persistência de dados
    - Depende de todos os sistemas anteriores
    - Funções determinísticas com I/O explícito

15. Sistema de Jogo (core/systems/game.py)
    - Gerenciamento do estado do jogo
    - Depende de todos os sistemas anteriores
    - Funções determinísticas com estado explícito
```

### Nível 6: Interface do Usuário (Depende do Nível 5)
```
16. Renderizador Terminal (ui/renderer.py)
    - Renderização da interface
    - Depende de sistema de jogo
    - Funções determinísticas com efeitos colaterais explícitos

17. Sistema de Entrada (ui/input.py)
    - Processamento de entrada do usuário
    - Depende de renderizador
    - Funções determinísticas com efeitos colaterais explícitos

18. Sistema de UI (ui/ui_system.py)
    - Orquestração da interface
    - Depende de renderizador e entrada
    - Funções determinísticas com efeitos colaterais explícitos
```

---

## Ordem de Implementação BDD/TDD

### Fase 1: Fundamentos (Testes Unitários Simples)
```python
# 1.1. Testes de Modelos
tests/test_models.py
- Testar validação de Character
- Testar validação de Item
- Testar validação de Enemy
- Testar validação de Quest

# 1.2. Testes de Validação
tests/test_validation.py
- Testar validação de nome
- Testar validação de estatísticas
- Testar validação de personagem
- Testar validação de combate

# 1.3. Testes de Utilitários
tests/test_math_utils.py
- Testar funções matemáticas
- Testar cálculos determinísticos
- Testar casos de borda
```

### Fase 2: Sistemas de Cálculo (Testes Unitários)
```python
# 2.1. Testes de Estatísticas
tests/test_stats_system.py
- Testar cálculo de HP base
- Testar modificadores de estatísticas
- Testar validação de estatísticas

# 2.2. Testes de Nível
tests/test_leveling_system.py
- Testar cálculo de experiência
- Testar progressão de nível
- Testar limites de nível

# 2.3. Testes de Habilidades
tests/test_abilities_system.py
- Testar obtenção de habilidades
- Testar validação de habilidades
- Testar hierarquia de habilidades
```

### Fase 3: Sistemas de Entidade (Testes Unitários + Integração)
```python
# 3.1. Testes de Personagem
tests/test_character_system.py
- Testar criação de personagem
- Testar modificação de atributos
- Testar validação de estado

# 3.2. Testes de Inimigo
tests/test_enemy_system.py
- Testar criação de inimigo
- Testar comportamento de inimigo
- Testar validação de inimigo

# 3.3. Testes de Item
tests/test_item_system.py
- Testar criação de item
- Testar propriedades de item
- Testar validação de item
```

### Fase 4: Sistemas de Interação (Testes de Integração)
```python
# 4.1. Testes de Combate
tests/test_combat_system.py
- Testar cálculo de dano
- Testar resolução de combate
- Testar estado de combate

# 4.2. Testes de Inventário
tests/test_inventory_system.py
- Testar adição de item
- Testar remoção de item
- Testar validação de inventário

# 4.3. Testes de Quest
tests/test_quest_system.py
- Testar criação de quest
- Testar progressão de quest
- Testar conclusão de quest
```

### Fase 5: Sistemas de Mundo (Testes de Integração)
```python
# 5.1. Testes de Localização
tests/test_location_system.py
- Testar criação de localização
- Testar navegação entre locais
- Testar validação de localização

# 5.2. Testes de Save/Load
tests/test_save_load_system.py
- Testar salvamento de estado
- Testar carregamento de estado
- Testar validação de dados

# 5.3. Testes de Jogo
tests/test_game_system.py
- Testar estado do jogo
- Testar progressão do jogo
- Testar validação do jogo
```

### Fase 6: Interface do Usuário (Testes de Sistema)
```python
# 6.1. Testes de Renderização
tests/test_renderer.py
- Testar renderização de painéis
- Testar renderização de tabelas
- Testar formatação de texto

# 6.2. Testes de Entrada
tests/test_input.py
- Testar processamento de entrada
- Testar validação de entrada
- Testar mapeamento de teclas

# 6.3. Testes de UI
tests/test_ui_system.py
- Testar navegação de menus
- Testar interação de botões
- Testar estado da UI
```

---

## Ordem de Cenários BDD (Por Complexidade de Dependência)

### Nível 1: Cenários de Fundação (Sem dependências)
```gherkin
Feature: Validação de Dados Básicos
  Scenario: Validar nome de personagem
  Scenario: Validar estatísticas de personagem
  Scenario: Validar propriedades de item
```

### Nível 2: Cenários de Cálculo (Depende de validação)
```gherkin
Feature: Cálculos de Sistema
  Scenario: Calcular HP base
  Scenario: Calcular experiência necessária
  Scenario: Calcular dano base
```

### Nível 3: Cenários de Entidade (Depende de cálculo)
```gherkin
Feature: Criação de Entidades
  Scenario: Criar personagem básico
  Scenario: Criar inimigo básico
  Scenario: Criar item básico
```

### Nível 4: Cenários de Interação (Depende de entidades)
```gherkin
Feature: Interações de Sistema
  Scenario: Personagem ataca inimigo
  Scenario: Personagem usa item
  Scenario: Personagem completa quest
```

### Nível 5: Cenários de Mundo (Depende de interações)
```gherkin
Feature: Funcionamento do Mundo
  Scenario: Personagem navega entre locais
  Scenario: Personagem salva jogo
  Scenario: Personagem carrega jogo
```

### Nível 6: Cenários de Interface (Depende de mundo)
```gherkin
Feature: Interface do Usuário
  Scenario: Usuário cria personagem via UI
  Scenario: Usuário navega em menus
  Scenario: Usuário interage com jogo
```

---

## Estratégia de Implementação para Agentes LLM

### 1. Implementação por Nível de Dependência
```python
# Implementar e testar completamente o Nível 1 antes de passar para o Nível 2
# Isso garante que as dependências estejam sempre satisfeitas
```

### 2. Validação por Contrato Explícito
```python
# Cada função deve ter contrato explícito antes da implementação
def create_character(name: str, class_type: str) -> Character:
    """
    Create new character with explicit contract.
    
    Args:
        name: Character name (1-50 chars, valid characters)
        class_type: Character class
        
    Returns:
        Character: Created character with valid stats
        
    Raises:
        ValueError: If name is invalid or class_type is invalid
    """
    pass  # Implementar depois do contrato
```

### 3. Testes Antes da Implementação (TDD)
```python
# Escrever testes antes da implementação
# Isso garante que o comportamento esperado seja claramente definido
def test_create_character_warrior():
    """Test creating warrior character."""
    character = create_character("TestWarrior", "warrior")
    assert character.name == "TestWarrior"
    assert character.class_type == "warrior"
    # ... mais asserts
```

### 4. BDD Para Comportamento Complexo
```gherkin
# Usar BDD apenas para comportamentos complexos que envolvem múltiplas funções
# Para funções simples, usar testes unitários diretos
Feature: Criação de Personagem
  Scenario: Criar personagem com múltiplas validações
```

### 5. Migração Gradual
```python
# Implementar e testar cada nível completamente antes de avançar
# Usar integração contínua para validar que nada se quebra
```

---

## Fluxo de Trabalho Otimizado para Agentes

### 1. Definir Contrato
```python
# Escrever função com contrato explícito
# Definir tipos, validações, retornos, exceções
```

### 2. Escrever Testes Unitários
```python
# Escrever testes que validem o contrato
# Usar asserts diretos, sem framework magic
```

### 3. Implementar Função
```python
# Implementar função para satisfazer o contrato
# Manter comportamento determinístico
```

### 4. Executar Testes
```python
# Validar que todos os testes passam
# Corrigir quaisquer falhas
```

### 5. Validar Integração
```python
# Testar com outros sistemas já implementados
# Garantir que não há regressão
```

### 6. Documentar Comportamento
```python
# Documentar contrato e comportamento
# Usar exemplos executáveis
```

Esta ordem garante que agentes LLM possam implementar o sistema de forma incremental, com dependências sempre satisfeitas e comportamento sempre verificável.