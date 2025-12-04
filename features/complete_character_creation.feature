# language: pt-br
# BDD Feature: Complete Character Creation (All Scenarios)
# Optimized for LLM agents - explicit language, no ambiguity

Feature: Complete Character Creation
  As a RPGSim player
  I want to create a new character with full validation
  To start my epic adventure

  # Cenário 1: Criação Básica (Primeiro cenário - sem dependências)
  Scenario: Criar personagem Guerreiro com dados válidos
    Given eu informo o nome "Aragorn" para o personagem
    And eu seleciono a classe "guerreiro" para o personagem
    When eu crio o personagem
    Then o personagem deve ter o nome "Aragorn"
    And o personagem deve ter a classe "guerreiro"
    And o personagem deve estar no nível 1
    And o personagem deve ter força 15
    And o personagem deve ter destreza 10
    And o personagem deve ter inteligência 8
    And o personagem deve ter sabedoria 10
    And o personagem deve ter carisma 8
    And o personagem deve ter constituição 14
    And o personagem deve ter HP 60
    And o personagem deve ter HP máximo 60
    And o personagem deve ter 100 gold
    And o personagem deve ter as habilidades ["Attack", "Defend", "Power Strike"]
    And o personagem deve ter inventário vazio

  # Cenário 2: Criação de Mago (Depende do sistema de classes)
  Scenario: Criar personagem Mago com dados válidos
    Given eu informo o nome "Gandalf" para o personagem
    And eu seleciono a classe "mago" para o personagem
    When eu crio o personagem
    Then o personagem deve ter o nome "Gandalf"
    And o personagem deve ter a classe "mago"
    And o personagem deve estar no nível 1
    And o personagem deve ter força 8
    And o personagem deve ter destreza 12
    And o personagem deve ter inteligência 16
    And o personagem deve ter sabedoria 14
    And o personagem deve ter carisma 10
    And o personagem deve ter constituição 8
    And o personagem deve ter HP 24
    And o personagem deve ter HP máximo 24
    And o personagem deve ter 100 gold
    And o personagem deve ter as habilidades ["Attack", "Defend", "Fireball"]
    And o personagem deve ter inventário vazio

  # Cenário 3: Validação de Nome (Depende do sistema de validação)
  Scenario: Falhar ao criar personagem com nome inválido
    Given eu informo o nome "" para o personagem
    And eu seleciono a classe "guerreiro" para o personagem
    When eu tento criar o personagem
    Then a criação deve falhar com erro "Character name cannot be empty"

  Scenario: Falhar ao criar personagem com nome muito longo
    Given eu informo o nome "NomeMuitoLongoQueExcedeOLimitePermitidoDeCinquentaCaracteres" para o personagem
    And eu seleciono a classe "guerreiro" para o personagem
    When eu tento criar o personagem
    Then a criação deve falhar com erro "Character name cannot exceed 50 characters"

  # Cenário 4: Validação de Classe (Depende do sistema de classes)
  Scenario: Falhar ao criar personagem com classe inválida
    Given eu informo o nome "Test" para o personagem
    And eu seleciono a classe "classe_inexistente" para o personagem
    When eu tento criar o personagem
    Then a criação deve falhar com erro "Invalid character class: classe_inexistente"

  # Cenário 5: Personagens de Todas as Classes (Depende do sistema completo de classes)
  Scenario: Criar personagens de todas as 23 classes
    Given eu tenho um mapeamento de classes e estatísticas esperadas
    When eu crio personagens para todas as classes disponíveis
    Then cada personagem deve ter as estatísticas corretas para sua classe
    And cada personagem deve ter as habilidades corretas para sua classe
    And cada personagem deve ter o HP correto para sua classe

  # Cenário 6: Validação de Estatísticas (Depende do sistema de balanço)
  Scenario: Todas as classes devem ter estatísticas válidas
    Given eu analiso todas as 23 classes disponíveis
    When eu verifico as estatísticas de cada classe
    Then todas as classes devem ter força entre 5 e 18
    And todas as classes devem ter destreza entre 5 e 18
    And todas as classes devem ter inteligência entre 4 e 18
    And todas as classes devem ter sabedoria entre 4 e 18
    And todas as classes devem ter carisma entre 4 e 18
    And todas as classes devem ter constituição entre 6 e 16
    And todas as classes devem ter HP entre 20 e 80
    And todas as classes devem ter pelo menos 3 habilidades

  # Cenário 7: Habilidades Únicas (Depende do sistema de habilidades)
  Scenario: Cada classe deve ter habilidades únicas
    Given eu examino as habilidades de todas as classes
    When eu comparo as habilidades entre classes
    Then cada classe deve ter pelo menos 1 habilidade única
    And nenhuma classe deve ter exatamente as mesmas 3 habilidades que outra classe
    And as habilidades devem ser tematicamente apropriadas para cada classe

  # Cenário 8: Personagens Específicos (Testes de integração)
  Scenario: Criar personagem Bárbaro
    Given eu informo o nome "Conan" para o personagem
    And eu seleciono a classe "bárbaro" para o personagem
    When eu crio o personagem
    Then o personagem deve ter força 16
    And o personagem deve ter inteligência 6
    And o personagem deve ter HP 64
    And o personagem deve ter habilidades ["Attack", "Defend", "Rage"]

  Scenario: Criar personagem Ninja
    Given eu informo o nome "Shadow" para o personagem
    And eu seleciono a classe "ninja" para o personagem
    When eu crio o personagem
    Then o personagem deve ter destreza 17
    And o personagem deve ter carisma 6
    And o personagem deve ter HP 40
    And o personagem deve ter habilidades ["Attack", "Defend", "Shadow Clone"]

  # Cenário 9: Teste de Balanço de Classes
  Scenario: Verificar balanço de poder entre classes
    Given eu calculo o poder total de cada classe
    When eu comparo os valores de poder
    Then nenhuma classe deve ser mais de 15% mais poderosa que qualquer outra
    And cada classe deve ter pontos fortes claros
    And cada classe deve ter pontos fracos claros

  # Cenário 10: Teste de Persistência (Depende do sistema de save)
  Scenario: Personagem deve persistir após criação
    Given eu crio um personagem com nome "TestHero" e classe "guerreiro"
    When eu salvo o jogo
    And eu carrego o jogo
    Then o personagem deve ter nome "TestHero"
    And o personagem deve ter classe "guerreiro"
    And o personagem deve ter estatísticas idênticas às da criação