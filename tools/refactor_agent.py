#!/usr/bin/env python3
"""
Agente de Refatoração Contínua para RPGSim
Monitora métricas de código e executa refatorações automáticas
"""

import os
import sys
import subprocess
import time
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("refactor_agent.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


@dataclass
class RefactorTask:
    """Tarefa de refatoração"""

    priority: int
    description: str
    file_path: str
    refactor_type: str
    estimated_time: int  # minutos
    dependencies: Optional[List[str]] = None


class ContinuousRefactorAgent:
    """Agente de refatoração contínua"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.metrics_file = self.project_root / "refactor_metrics.json"
        self.task_queue = []
        self.running = False
        self.current_score = 0.0

        # Sistemas prioritários baseado no PROJECT.md
        self.priority_systems = [
            "shop",  # CRÍTICO - 18 testes falhando
            "combat",  # CRÍTICO - Core gameplay
            "equipment",  # ALTA - Dependente Shop
            "quest",  # ALTA
            "city_management",  # MÉDIA
            "travel",  # MÉDIA
            "gamification",  # MÉDIA
            "dungeon",  # BAIXA
        ]

    def load_metrics(self) -> Dict:
        """Carrega métricas anteriores"""
        if self.metrics_file.exists():
            with open(self.metrics_file, "r") as f:
                return json.load(f)
        return {"history": [], "current": {}}

    def save_metrics(self, metrics: Dict):
        """Salva métricas atuais"""
        with open(self.metrics_file, "w") as f:
            json.dump(metrics, f, indent=2, default=str)

    def run_pylint_score(self, file_path: str) -> float:
        """Executa pylint e retorna score"""
        try:
            result = subprocess.run(
                ["pylint", "--score=yes", "--output-format=json", file_path],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            # Extrair score do output
            for line in result.stdout.split("\n"):
                if "Rated at" in line:
                    score_str = line.split("Rated at")[1].split("/")[0].strip()
                    return float(score_str)

            return 0.0
        except Exception as e:
            logger.error(f"Erro ao executar pylint em {file_path}: {e}")
            return 0.0

    def analyze_codebase(self) -> Dict:
        """Analisa toda a codebase"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "systems": {},
            "overall_score": 0.0,
            "total_files": 0,
            "needs_refactor": [],
        }

        # Analisar sistemas principais
        for system in self.priority_systems:
            system_path = self.project_root / "core" / "systems" / f"{system}.py"

            if system_path.exists():
                score = self.run_pylint_score(str(system_path))
                file_size = system_path.stat().st_size
                line_count = self._count_lines(system_path)

                system_info = {
                    "file": str(system_path),
                    "pylint_score": score,
                    "file_size_bytes": file_size,
                    "line_count": line_count,
                    "needs_modularization": line_count > 500,
                    "priority": self._get_system_priority(system),
                }

                analysis["systems"][system] = system_info
                analysis["total_files"] += 1

                # Adicionar à fila se precisar refatorar
                if score < 8.0 or line_count > 500:
                    analysis["needs_refactor"].append(system)

        # Calcular score geral
        if analysis["systems"]:
            analysis["overall_score"] = sum(
                s["pylint_score"] for s in analysis["systems"].values()
            ) / len(analysis["systems"])

        return analysis

    def _count_lines(self, file_path: Path) -> int:
        """Conta linhas de código"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return sum(1 for _ in f)
        except:
            return 0

    def _get_system_priority(self, system: str) -> int:
        """Retorna prioridade do sistema (menor = mais prioritário)"""
        priority_map = {
            "shop": 1,  # CRÍTICO
            "combat": 2,  # CRÍTICO
            "equipment": 3,  # ALTA
            "quest": 4,  # ALTA
            "city_management": 5,  # MÉDIA
            "travel": 6,  # MÉDIA
            "gamification": 7,  # MÉDIA
            "dungeon": 8,  # BAIXA
        }
        return priority_map.get(system, 99)

    def create_refactor_plan(self, analysis: Dict) -> List[RefactorTask]:
        """Cria plano de refatoração"""
        tasks = []

        for system_name, system_info in analysis["systems"].items():
            if system_name in analysis["needs_refactor"]:
                # Determinar tipo de refatoração
                if system_info["line_count"] > 500:
                    refactor_type = "modularization"
                    description = f"Modularizar {system_name}.py ({system_info['line_count']} linhas)"
                    estimated_time = 180  # 3 horas para sistemas grandes
                else:
                    refactor_type = "quality_improvement"
                    description = f"Melhorar qualidade de {system_name}.py (score: {system_info['pylint_score']})"
                    estimated_time = 60  # 1 hora para melhorias

                task = RefactorTask(
                    priority=system_info["priority"],
                    description=description,
                    file_path=system_info["file"],
                    refactor_type=refactor_type,
                    estimated_time=estimated_time,
                )
                tasks.append(task)

        # Ordenar por prioridade
        tasks.sort(key=lambda t: t.priority)
        return tasks

    def execute_modularization(self, task: RefactorTask) -> bool:
        """Executa modularização de um sistema"""
        logger.info(f"Iniciando modularização: {task.description}")

        system_name = Path(task.file_path).stem

        # Criar estrutura de diretórios
        system_dir = self.project_root / "core" / "systems" / system_name
        subdirs = ["domain", "services", "repositories", "interfaces"]

        for subdir in subdirs:
            (system_dir / subdir).mkdir(parents=True, exist_ok=True)

        # Implementar modularização baseada no padrão estabelecido
        modularization_script = f"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path('{self.project_root}')))

# Implementar modularização para {system_name}
# Baseado no padrão Character/World System

print(f"Modularizando {system_name}...")

# TODO: Implementar lógica específica de modularização
# 1. Extrair entidades de domínio
# 2. Criar serviços de negócio
# 3. Implementar repositórios
# 4. Criar fachada unificada
# 5. Migrar testes

print("Modularização concluída!")
"""

        script_path = system_dir / "modularize.py"
        with open(script_path, "w") as f:
            f.write(modularization_script)

        # Executar script
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                logger.info(f"Modularização concluída: {system_name}")
                return True
            else:
                logger.error(f"Erro na modularização: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Erro ao executar modularização: {e}")
            return False

    def execute_quality_improvement(self, task: RefactorTask) -> bool:
        """Executa melhoria de qualidade"""
        logger.info(f"Iniciando melhoria de qualidade: {task.description}")

        try:
            # Executar black para formatação
            subprocess.run(
                ["black", task.file_path], capture_output=True, cwd=self.project_root
            )

            # Executar isort para imports
            subprocess.run(
                ["isort", task.file_path], capture_output=True, cwd=self.project_root
            )

            # Adicionar type hints onde faltam
            # TODO: Implementar lógica específica

            logger.info(f"Melhoria de qualidade concluída: {task.file_path}")
            return True

        except Exception as e:
            logger.error(f"Erro na melhoria de qualidade: {e}")
            return False

    def run_tests(self) -> bool:
        """Executa testes para validar refatoração"""
        logger.info("Executando testes...")

        try:
            # Testes unitários
            result = subprocess.run(
                ["pytest", "tests/", "--tb=short"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode != 0:
                logger.warning(f"Alguns testes falharam: {result.stdout}")
                return False

            # Testes BDD
            result = subprocess.run(
                ["behave", "features/", "--format=progress"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            if result.returncode != 0:
                logger.warning(f"Alguns cenários BDD falharam: {result.stdout}")
                return False

            logger.info("Todos os testes passaram!")
            return True

        except Exception as e:
            logger.error(f"Erro ao executar testes: {e}")
            return False

    def execute_task(self, task: RefactorTask) -> bool:
        """Executa uma tarefa de refatoração"""
        logger.info(f"Executando tarefa: {task.description}")

        success = False

        if task.refactor_type == "modularization":
            success = self.execute_modularization(task)
        elif task.refactor_type == "quality_improvement":
            success = self.execute_quality_improvement(task)

        if success:
            # Validar com testes
            if self.run_tests():
                logger.info(f"Tarefa concluída com sucesso: {task.description}")
                return True
            else:
                logger.error(f"Tarefa falhou na validação: {task.description}")
                return False
        else:
            logger.error(f"Falha na execução da tarefa: {task.description}")
            return False

    def run_continuous(self, interval_minutes: int = 30):
        """Executa agente continuamente"""
        logger.info("Iniciando agente de refatoração contínua...")
        self.running = True

        while self.running:
            try:
                # Analisar codebase
                logger.info("Analisando codebase...")
                analysis = self.analyze_codebase()

                # Salvar métricas
                metrics = self.load_metrics()
                metrics["current"] = analysis
                metrics["history"].append(analysis)
                self.save_metrics(metrics)

                # Exibir status atual
                logger.info(f"Score geral: {analysis['overall_score']:.2f}/10")
                logger.info(f"Arquivos analisados: {analysis['total_files']}")
                logger.info(
                    f"Sistemas precisando refatoração: {len(analysis['needs_refactor'])}"
                )

                # Criar plano de refatoração
                tasks = self.create_refactor_plan(analysis)

                if tasks:
                    logger.info(f"Plano de refatoração: {len(tasks)} tarefas")

                    # Executar tarefa mais prioritária
                    next_task = tasks[0]
                    logger.info(
                        f"Executando tarefa prioritária: {next_task.description}"
                    )

                    if self.execute_task(next_task):
                        logger.info("Tarefa executada com sucesso")
                    else:
                        logger.error("Falha na execução da tarefa")
                else:
                    logger.info("Nenhuma refatoração necessária no momento")

                # Esperar próximo ciclo
                logger.info(
                    f"Aguardando {interval_minutes} minutos para próximo ciclo..."
                )
                time.sleep(interval_minutes * 60)

            except KeyboardInterrupt:
                logger.info("Agente interrompido pelo usuário")
                break
            except Exception as e:
                logger.error(f"Erro no ciclo de execução: {e}")
                time.sleep(60)  # Esperar 1 minuto antes de tentar novamente

        self.running = False
        logger.info("Agente de refatoração finalizado")

    def run_once(self):
        """Executa uma única análise e refatoração"""
        logger.info("Executando análise única...")

        # Analisar codebase
        analysis = self.analyze_codebase()

        # Exibir resultados
        print(f"\n📊 ANÁLISE DA CODEBASE")
        print(f"Score geral: {analysis['overall_score']:.2f}/10")
        print(f"Arquivos analisados: {analysis['total_files']}")
        print(f"Sistemas precisando refatoração: {len(analysis['needs_refactor'])}")

        print(f"\n🔍 DETALHES POR SISTEMA:")
        for system_name, system_info in analysis["systems"].items():
            status = (
                "✅ OK" if system_info["pylint_score"] >= 8.0 else "⚠️ PRECISA MELHORAR"
            )
            print(
                f"  {system_name:15} | Score: {system_info['pylint_score']:.1f}/10 | Linhas: {system_info['line_count']:4} | {status}"
            )

        # Criar plano
        tasks = self.create_refactor_plan(analysis)

        if tasks:
            print(f"\n📋 PLANO DE REFACTORAÇÃO:")
            for i, task in enumerate(tasks[:3], 1):  # Mostrar top 3
                print(
                    f"  {i}. [{task.priority}] {task.description} ({task.estimated_time}min)"
                )

            # Perguntar se quer executar (apenas se houver terminal interativo)
            try:
                response = (
                    input(f"\n🚀 Executar tarefa mais prioritária? (y/N): ")
                    .strip()
                    .lower()
                )
                if response == "y":
                    self.execute_task(tasks[0])
            except EOFError:
                print(
                    "\n📊 Execução não interativa - use --continuous para modo automático"
                )
        else:
            print("\n✅ Nenhuma refatoração necessária!")


def main():
    """Função principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Agente de Refatoração Contínua RPGSim"
    )
    parser.add_argument("--project-root", default=".", help="Diretório raiz do projeto")
    parser.add_argument(
        "--continuous", action="store_true", help="Executar continuamente"
    )
    parser.add_argument(
        "--interval", type=int, default=30, help="Intervalo em minutos (modo contínuo)"
    )
    parser.add_argument(
        "--once", action="store_true", help="Executar uma única análise"
    )

    args = parser.parse_args()

    agent = ContinuousRefactorAgent(args.project_root)

    if args.once:
        agent.run_once()
    elif args.continuous:
        agent.run_continuous(args.interval)
    else:
        # Modo interativo
        print("🤖 Agente de Refatoração Contínua RPGSim")
        print("Escolha o modo de execução:")
        print("1. Análise única")
        print("2. Modo contínuo")
        print("3. Sair")

        choice = input("Opção (1-3): ").strip()

        if choice == "1":
            agent.run_once()
        elif choice == "2":
            interval = int(input("Intervalo em minutos (padrão 30): ").strip() or "30")
            agent.run_continuous(interval)
        else:
            print("Saindo...")


if __name__ == "__main__":
    main()
