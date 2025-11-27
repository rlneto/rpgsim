#!/bin/bash
# Script para iniciar o agente de refatoração contínua em background

PROJECT_ROOT="/home/jose/Disposable/code/rpgsim"
AGENT_SCRIPT="$PROJECT_ROOT/tools/refactor_agent.py"
PID_FILE="$PROJECT_ROOT/.refactor_agent.pid"
LOG_FILE="$PROJECT_ROOT/refactor_agent_background.log"

start_agent() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "🤖 Agente já está rodando (PID: $PID)"
            return 1
        else
            echo "🧹 Limpando PID file antigo"
            rm -f "$PID_FILE"
        fi
    fi
    
    echo "🚀 Iniciando agente de refatoração contínua..."
    
    # Ativar ambiente virtual e iniciar agente
    cd "$PROJECT_ROOT"
    source venv/bin/activate
    
    # Iniciar agente em background
    nohup python "$AGENT_SCRIPT" --continuous --interval 15 > "$LOG_FILE" 2>&1 &
    AGENT_PID=$!
    
    # Salvar PID
    echo $AGENT_PID > "$PID_FILE"
    
    echo "✅ Agente iniciado (PID: $AGENT_PID)"
    echo "📋 Log: $LOG_FILE"
    echo "🛑 Para parar: $0 stop"
    echo "📊 Status: $0 status"
}

stop_agent() {
    if [ ! -f "$PID_FILE" ]; then
        echo "❌ Agente não está rodando"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    
    if ps -p $PID > /dev/null 2>&1; then
        echo "🛑 Parando agente (PID: $PID)..."
        kill $PID
        
        # Esperar até 10 segundos para o processo terminar
        for i in {1..10}; do
            if ! ps -p $PID > /dev/null 2>&1; then
                break
            fi
            sleep 1
        done
        
        # Forçar kill se ainda estiver rodando
        if ps -p $PID > /dev/null 2>&1; then
            echo "⚡ Forçando parada do agente..."
            kill -9 $PID
        fi
        
        rm -f "$PID_FILE"
        echo "✅ Agente parado"
    else
        echo "❌ Agente não encontrado (PID: $PID)"
        rm -f "$PID_FILE"
    fi
}

status_agent() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "✅ Agente está rodando (PID: $PID)"
            
            # Mostrar últimas linhas do log
            echo ""
            echo "📋 Últimas atividades:"
            tail -10 "$LOG_FILE" 2>/dev/null || echo "Log não encontrado"
        else
            echo "❌ Agente não está rodando (PID file existe mas processo não encontrado)"
            rm -f "$PID_FILE"
        fi
    else
        echo "❌ Agente não está rodando"
    fi
}

restart_agent() {
    echo "🔄 Reiniciando agente..."
    stop_agent
    sleep 2
    start_agent
}

case "$1" in
    start)
        start_agent
        ;;
    stop)
        stop_agent
        ;;
    status)
        status_agent
        ;;
    restart)
        restart_agent
        ;;
    logs)
        if [ -f "$LOG_FILE" ]; then
            echo "📋 Logs do agente:"
            tail -50 "$LOG_FILE"
        else
            echo "❌ Log não encontrado"
        fi
        ;;
    *)
        echo "🤖 Agente de Refatoração Contínua RPGSim"
        echo ""
        echo "Uso: $0 {start|stop|status|restart|logs}"
        echo ""
        echo "Comandos:"
        echo "  start   - Inicia agente em background"
        echo "  stop    - Para agente"
        echo "  status  - Mostra status do agente"
        echo "  restart - Reinicia agente"
        echo "  logs    - Mostra logs recentes"
        echo ""
        echo "Exemplos:"
        echo "  $0 start    # Inicia agente"
        echo "  $0 status   # Verifica status"
        echo "  $0 stop     # Para agente"
        exit 1
        ;;
esac