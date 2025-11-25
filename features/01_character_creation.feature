# language: en
# BDD Feature: Character Creation
# Optimized for LLM agents - explicit language, no ambiguity

Feature: Character Creation
  As a RPGSim player
  I want to create a new character
  To start my adventure

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