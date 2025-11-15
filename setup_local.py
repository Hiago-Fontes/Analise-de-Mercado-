#!/usr/bin/env python3
"""
Script de setup local para o projeto Mercado de Investimentos
Uso: python setup_local.py
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, shell=False):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(cmd, shell=shell, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao executar: {cmd}")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    print("=" * 60)
    print("🚀 Setup Local - Mercado de Investimentos")
    print("=" * 60)
    
    is_windows = sys.platform == "win32"
    python_exe = sys.executable
    
    # 1. Criar venv
    print("\n1️⃣  Criando ambiente virtual...")
    if not os.path.exists(".venv"):
        if not run_command(f"{python_exe} -m venv .venv"):
            print("❌ Falha ao criar ambiente virtual")
            return
        print("✅ Ambiente virtual criado")
    else:
        print("✅ Ambiente virtual já existe")
    
    # Caminho do Python no venv
    if is_windows:
        venv_python = os.path.join(".venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join(".venv", "bin", "python")
    
    # 2. Upgrade pip
    print("\n2️⃣  Atualizando pip...")
    run_command(f"{venv_python} -m pip install --upgrade pip", shell=True)
    
    # 3. Instalar dependências
    print("\n3️⃣  Instalando dependências...")
    if not run_command(f"{venv_python} -m pip install -r requirements.txt", shell=True):
        print("❌ Falha ao instalar dependências")
        return
    print("✅ Dependências instaladas")
    
    # 4. Resumo e instruções
    print("\n" + "=" * 60)
    print("✅ Setup concluído com sucesso!")
    print("=" * 60)
    print("\n🎯 Para iniciar a aplicação:")
    if is_windows:
        print(f"   python run.py")
    else:
        print(f"   python3 run.py")
    print("\n📝 Então acesse: http://127.0.0.1:5000")
    print("\n📚 Documentação:")
    print("   - README.md - Visão geral")
    print("   - ESTRUTURA.md - Arquitetura do projeto")
    print("   - DEPLOY_RAPIDO.md - Como hospedar")
    print("=" * 60)

if __name__ == "__main__":
    main()
