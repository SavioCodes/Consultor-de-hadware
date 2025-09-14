#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Diagnóstico Completo de Hardware para PC
Versão: 1.0
Autor: SavioCodes
Data: 2025

Consultor profissional de hardware para Windows 10/11
Detecção completa, monitoramento em tempo real, alertas e recomendações
"""

import os
import sys
import time
import datetime
import threading
import json
import csv
import subprocess
import platform
import ctypes
from pathlib import Path

# Verificar se está rodando como administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("⚠️  AVISO: Para melhor funcionamento, execute como Administrador!")
    print("   Clique com botão direito no prompt e 'Executar como administrador'")
    print("   Continuando sem privilégios completos...\n")

# Lista de dependências necessárias
DEPENDENCIES = [
    "psutil",
    "GPUtil", 
    "py-cpuinfo",
    "tabulate",
    "rich",
    "matplotlib",
    "wmi"
]

print("🔧 SISTEMA DE DIAGNÓSTICO DE PC v1.0")
print("=" * 50)
print("📋 Verificando dependências necessárias...\n")

# Verificar e importar bibliotecas com fallback
missing_deps = []
available_libs = {}

# Importações padrão
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading

# Verificar dependências opcionais
for dep in DEPENDENCIES:
    try:
        if dep == "psutil":
            import psutil
            available_libs['psutil'] = True
        elif dep == "GPUtil":
            import GPUtil
            available_libs['GPUtil'] = True
        elif dep == "py-cpuinfo":
            import cpuinfo
            available_libs['cpuinfo'] = True
        elif dep == "tabulate":
            from tabulate import tabulate
            available_libs['tabulate'] = True
        elif dep == "rich":
            from rich.console import Console
            from rich.table import Table
            from rich.panel import Panel
            available_libs['rich'] = True
        elif dep == "matplotlib":
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            available_libs['matplotlib'] = True
        elif dep == "wmi":
            import wmi
            available_libs['wmi'] = True
        print(f"✅ {dep}: OK")
    except ImportError:
        missing_deps.append(dep)
        available_libs[dep.replace('-', '_')] = False
        print(f"❌ {dep}: NÃO INSTALADO")

if missing_deps:
    print(f"\n⚠️  Dependências faltando: {', '.join(missing_deps)}")
    print("📥 Para instalar todas as dependências:")
    print(f"   pip install {' '.join(DEPENDENCIES)}")
    print("\n🔄 Continuando com funcionalidades limitadas...\n")
else:
    print("\n✅ Todas as dependências estão instaladas!\n")

class DiagnosticoPCAvancado:
    def __init__(self):
        self.console = Console() if available_libs.get('rich') else None
        self.monitoring = False
        self.monitoring_data = {
            'cpu_usage': [],
            'gpu_usage': [],
            'memory_usage': [],
            'cpu_temp': [],
            'gpu_temp': [],
            'timestamps': []
        }
        self.alerts = []
        self.recommendations = []
        
        # Limites de temperatura (°C)
        self.temp_limits = {
            'cpu_warning': 75,
            'cpu_critical': 85,
            'gpu_warning': 80,
            'gpu_critical': 90,
            'disk_warning': 50,
            'disk_critical': 60
        }
        
        self.setup_gui()
        
    def setup_gui(self):
        """Configura a interface gráfica"""
        self.root = tk.Tk()
        self.root.title("🔧 Diagnóstico de PC Profissional v1.0")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2b2b2b')
        style.configure('TNotebook.Tab', background='#404040', foreground='white')
        style.map('TNotebook.Tab', background=[('selected', '#0078d4')])
        
        # Notebook principal
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Abas
        self.create_hardware_tab()
        self.create_monitoring_tab()
        self.create_reports_tab()
        self.create_alerts_tab()
        
        # Barra de status
        self.status_var = tk.StringVar()
        self.status_var.set("Sistema pronto - Execute um diagnóstico completo")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                            relief=tk.SUNKEN, anchor=tk.W, bg='#404040', fg='white')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_hardware_tab(self):
        """Aba de informações de hardware"""
        self.hardware_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.hardware_frame, text="🖥️ Hardware")
        
        # Botão de diagnóstico
        diag_frame = ttk.Frame(self.hardware_frame)
        diag_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(diag_frame, text="🔍 Executar Diagnóstico Completo", 
                  command=self.run_complete_diagnosis, 
                  style='Accent.TButton').pack(side='left', padx=5)
        
        ttk.Button(diag_frame, text="💾 Exportar Relatório TXT", 
                  command=self.export_txt_report).pack(side='left', padx=5)
        
        ttk.Button(diag_frame, text="🌐 Exportar Relatório HTML", 
                  command=self.export_html_report).pack(side='left', padx=5)
        
        # Área de texto para resultados
        self.hardware_text = scrolledtext.ScrolledText(
            self.hardware_frame, 
            wrap=tk.WORD, 
            bg='#1e1e1e', 
            fg='#ffffff',
            insertbackground='white',
            font=('Consolas', 10)
        )
        self.hardware_text.pack(fill='both', expand=True, padx=10, pady=10)
        
    def create_monitoring_tab(self):
        """Aba de monitoramento em tempo real"""
        self.monitoring_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.monitoring_frame, text="📊 Monitoramento")
        
        # Controles de monitoramento
        control_frame = ttk.Frame(self.monitoring_frame)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        self.monitoring_button = ttk.Button(
            control_frame, 
            text="▶️ Iniciar Monitoramento", 
            command=self.toggle_monitoring
        )
        self.monitoring_button.pack(side='left', padx=5)
        
        ttk.Button(control_frame, text="📈 Gráfico em Tempo Real", 
                  command=self.show_realtime_graph).pack(side='left', padx=5)
        
        ttk.Button(control_frame, text="💾 Salvar Dados CSV", 
                  command=self.save_monitoring_csv).pack(side='left', padx=5)
        
        # Duração do monitoramento
        duration_frame = ttk.Frame(control_frame)
        duration_frame.pack(side='right')
        ttk.Label(duration_frame, text="Duração (min):").pack(side='left')
        self.duration_var = tk.StringVar(value="5")
        duration_spinbox = ttk.Spinbox(duration_frame, from_=1, to=30, 
                                     width=5, textvariable=self.duration_var)
        duration_spinbox.pack(side='left', padx=5)
        
        # Frame para métricas em tempo real
        metrics_frame = ttk.LabelFrame(self.monitoring_frame, text="📊 Métricas em Tempo Real")
        metrics_frame.pack(fill='x', padx=10, pady=10)
        
        self.create_metric_displays(metrics_frame)
        
        # Log de monitoramento
        log_frame = ttk.LabelFrame(self.monitoring_frame, text="📝 Log de Monitoramento")
        log_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.monitoring_log = scrolledtext.ScrolledText(
            log_frame, 
            wrap=tk.WORD, 
            bg='#1e1e1e', 
            fg='#00ff00',
            font=('Consolas', 9),
            height=15
        )
        self.monitoring_log.pack(fill='both', expand=True, padx=5, pady=5)
        
    def create_metric_displays(self, parent):
        """Cria displays para métricas em tempo real"""
        # Frame principal para métricas
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # CPU Metrics
        cpu_frame = ttk.LabelFrame(main_frame, text="🖥️ CPU")
        cpu_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.cpu_usage_var = tk.StringVar(value="0%")
        self.cpu_temp_var = tk.StringVar(value="-- °C")
        
        ttk.Label(cpu_frame, text="Uso:").pack(anchor='w')
        cpu_usage_label = ttk.Label(cpu_frame, textvariable=self.cpu_usage_var, 
                                   font=('Arial', 14, 'bold'))
        cpu_usage_label.pack(anchor='w')
        
        ttk.Label(cpu_frame, text="Temperatura:").pack(anchor='w')
        cpu_temp_label = ttk.Label(cpu_frame, textvariable=self.cpu_temp_var, 
                                  font=('Arial', 14, 'bold'))
        cpu_temp_label.pack(anchor='w')
        
        # GPU Metrics
        gpu_frame = ttk.LabelFrame(main_frame, text="🎮 GPU")
        gpu_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.gpu_usage_var = tk.StringVar(value="0%")
        self.gpu_temp_var = tk.StringVar(value="-- °C")
        
        ttk.Label(gpu_frame, text="Uso:").pack(anchor='w')
        gpu_usage_label = ttk.Label(gpu_frame, textvariable=self.gpu_usage_var, 
                                   font=('Arial', 14, 'bold'))
        gpu_usage_label.pack(anchor='w')
        
        ttk.Label(gpu_frame, text="Temperatura:").pack(anchor='w')
        gpu_temp_label = ttk.Label(gpu_frame, textvariable=self.gpu_temp_var, 
                                  font=('Arial', 14, 'bold'))
        gpu_temp_label.pack(anchor='w')
        
        # Memory Metrics
        mem_frame = ttk.LabelFrame(main_frame, text="💾 Memória")
        mem_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.mem_usage_var = tk.StringVar(value="0%")
        self.mem_available_var = tk.StringVar(value="0 GB")
        
        ttk.Label(mem_frame, text="Uso:").pack(anchor='w')
        mem_usage_label = ttk.Label(mem_frame, textvariable=self.mem_usage_var, 
                                   font=('Arial', 14, 'bold'))
        mem_usage_label.pack(anchor='w')
        
        ttk.Label(mem_frame, text="Disponível:").pack(anchor='w')
        mem_available_label = ttk.Label(mem_frame, textvariable=self.mem_available_var, 
                                       font=('Arial', 14, 'bold'))
        mem_available_label.pack(anchor='w')
        
    def create_reports_tab(self):
        """Aba de relatórios"""
        self.reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reports_frame, text="📋 Relatórios")
        
        # Botões de relatório
        report_buttons_frame = ttk.Frame(self.reports_frame)
        report_buttons_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(report_buttons_frame, text="📊 Gerar Relatório Completo", 
                  command=self.generate_complete_report).pack(side='left', padx=5)
        
        ttk.Button(report_buttons_frame, text="📁 Abrir Pasta de Relatórios", 
                  command=self.open_reports_folder).pack(side='left', padx=5)
        
        ttk.Button(report_buttons_frame, text="🗑️ Limpar Logs", 
                  command=self.clear_logs).pack(side='left', padx=5)
        
        # Área de visualização de relatórios
        self.reports_text = scrolledtext.ScrolledText(
            self.reports_frame, 
            wrap=tk.WORD, 
            bg='#1e1e1e', 
            fg='#ffffff',
            font=('Consolas', 10)
        )
        self.reports_text.pack(fill='both', expand=True, padx=10, pady=10)
        
    def create_alerts_tab(self):
        """Aba de alertas e recomendações"""
        self.alerts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.alerts_frame, text="⚠️ Alertas")
        
        # Frame para alertas críticos
        critical_frame = ttk.LabelFrame(self.alerts_frame, text="🚨 Alertas Críticos")
        critical_frame.pack(fill='x', padx=10, pady=10)
        
        self.critical_alerts_text = scrolledtext.ScrolledText(
            critical_frame, 
            wrap=tk.WORD, 
            bg='#2d1b1b', 
            fg='#ff6b6b',
            font=('Consolas', 10),
            height=8
        )
        self.critical_alerts_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Frame para recomendações
        recommendations_frame = ttk.LabelFrame(self.alerts_frame, text="💡 Recomendações")
        recommendations_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.recommendations_text = scrolledtext.ScrolledText(
            recommendations_frame, 
            wrap=tk.WORD, 
            bg='#1b2d1b', 
            fg='#69db7c',
            font=('Consolas', 10)
        )
        self.recommendations_text.pack(fill='both', expand=True, padx=5, pady=5)

    def get_cpu_info(self):
        """Obtém informações detalhadas do CPU"""
        cpu_info = {"erro": "Informações não disponíveis"}
        
        try:
            if available_libs.get('psutil'):
                # Informações básicas do psutil
                cpu_info.update({
                    "uso_atual": f"{psutil.cpu_percent(interval=1):.1f}%",
                    "nucleos_fisicos": psutil.cpu_count(logical=False),
                    "nucleos_logicos": psutil.cpu_count(logical=True),
                    "frequencia_atual": f"{psutil.cpu_freq().current:.0f} MHz" if psutil.cpu_freq() else "N/A",
                    "frequencia_maxima": f"{psutil.cpu_freq().max:.0f} MHz" if psutil.cpu_freq() else "N/A",
                })
            
            if available_libs.get('cpuinfo'):
                # Informações detalhadas do py-cpuinfo
                info = cpuinfo.get_cpu_info()
                cpu_info.update({
                    "modelo": info.get('brand_raw', 'N/A'),
                    "fabricante": info.get('vendor_id_raw', 'N/A'),
                    "arquitetura": info.get('arch', 'N/A'),
                    "cache_l1": info.get('l1_data_cache_size', 'N/A'),
                    "cache_l2": info.get('l2_cache_size', 'N/A'),
                    "cache_l3": info.get('l3_cache_size', 'N/A'),
                    "flags": info.get('flags', [])
                })
            
            # Temperatura (requer sensores específicos)
            try:
                if available_libs.get('psutil'):
                    sensors = psutil.sensors_temperatures()
                    if sensors:
                        for name, entries in sensors.items():
                            if 'coretemp' in name.lower() or 'cpu' in name.lower():
                                if entries:
                                    temp = entries[0].current
                                    cpu_info["temperatura"] = f"{temp:.1f}°C"
                                    
                                    # Verificar alertas de temperatura
                                    if temp > self.temp_limits['cpu_critical']:
                                        self.alerts.append({
                                            'tipo': 'CRÍTICO',
                                            'componente': 'CPU',
                                            'mensagem': f'Temperatura crítica: {temp:.1f}°C (limite: {self.temp_limits["cpu_critical"]}°C)',
                                            'prioridade': 'ALTA'
                                        })
                                    elif temp > self.temp_limits['cpu_warning']:
                                        self.alerts.append({
                                            'tipo': 'AVISO',
                                            'componente': 'CPU', 
                                            'mensagem': f'Temperatura alta: {temp:.1f}°C (limite recomendado: {self.temp_limits["cpu_warning"]}°C)',
                                            'prioridade': 'MÉDIA'
                                        })
                                    break
            except:
                cpu_info["temperatura"] = "N/A (sensores não acessíveis)"
                
        except Exception as e:
            cpu_info["erro"] = f"Erro ao obter informações do CPU: {str(e)}"
            
        return cpu_info

    def get_gpu_info(self):
        """Obtém informações detalhadas da GPU"""
        gpu_info = {"erro": "Informações não disponíveis"}
        
        try:
            if available_libs.get('GPUtil'):
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]  # GPU principal
                    gpu_info = {
                        "modelo": gpu.name,
                        "memoria_total": f"{gpu.memoryTotal:.0f} MB",
                        "memoria_usada": f"{gpu.memoryUsed:.0f} MB",
                        "memoria_livre": f"{gpu.memoryFree:.0f} MB",
                        "uso_gpu": f"{gpu.load * 100:.1f}%",
                        "uso_memoria": f"{(gpu.memoryUsed / gpu.memoryTotal) * 100:.1f}%",
                        "temperatura": f"{gpu.temperature:.1f}°C",
                        "uuid": gpu.uuid,
                        "driver": gpu.driver if hasattr(gpu, 'driver') else 'N/A'
                    }
                    
                    # Verificar alertas de temperatura da GPU
                    if gpu.temperature > self.temp_limits['gpu_critical']:
                        self.alerts.append({
                            'tipo': 'CRÍTICO',
                            'componente': 'GPU',
                            'mensagem': f'Temperatura crítica: {gpu.temperature:.1f}°C (limite: {self.temp_limits["gpu_critical"]}°C)',
                            'prioridade': 'ALTA'
                        })
                    elif gpu.temperature > self.temp_limits['gpu_warning']:
                        self.alerts.append({
                            'tipo': 'AVISO',
                            'componente': 'GPU',
                            'mensagem': f'Temperatura alta: {gpu.temperature:.1f}°C (limite recomendado: {self.temp_limits["gpu_warning"]}°C)',
                            'prioridade': 'MÉDIA'
                        })
                    
                    # Verificar uso excessivo de memória
                    mem_usage_percent = (gpu.memoryUsed / gpu.memoryTotal) * 100
                    if mem_usage_percent > 90:
                        self.alerts.append({
                            'tipo': 'AVISO',
                            'componente': 'GPU',
                            'mensagem': f'Uso alto de memória VRAM: {mem_usage_percent:.1f}%',
                            'prioridade': 'MÉDIA'
                        })
                else:
                    gpu_info = {"erro": "Nenhuma GPU NVIDIA/AMD detectada"}
            else:
                gpu_info = {"erro": "GPUtil não disponível - instale com: pip install GPUtil"}
                
        except Exception as e:
            gpu_info["erro"] = f"Erro ao obter informações da GPU: {str(e)}"
            
        return gpu_info

    def get_memory_info(self):
        """Obtém informações detalhadas da memória RAM"""
        memory_info = {"erro": "Informações não disponíveis"}
        
        try:
            if available_libs.get('psutil'):
                mem = psutil.virtual_memory()
                memory_info = {
                    "total": f"{mem.total / (1024**3):.2f} GB",
                    "disponivel": f"{mem.available / (1024**3):.2f} GB",
                    "usada": f"{mem.used / (1024**3):.2f} GB",
                    "porcentagem_uso": f"{mem.percent:.1f}%",
                    "livre": f"{mem.free / (1024**3):.2f} GB",
                    "em_cache": f"{mem.cached / (1024**3):.2f} GB" if hasattr(mem, 'cached') else 'N/A',
                    "buffers": f"{mem.buffers / (1024**3):.2f} GB" if hasattr(mem, 'buffers') else 'N/A'
                }
                
                # Verificar uso excessivo de memória
                if mem.percent > 90:
                    self.alerts.append({
                        'tipo': 'CRÍTICO',
                        'componente': 'RAM',
                        'mensagem': f'Uso crítico de memória: {mem.percent:.1f}% (Recomendado: <85%)',
                        'prioridade': 'ALTA'
                    })
                elif mem.percent > 80:
                    self.alerts.append({
                        'tipo': 'AVISO',
                        'componente': 'RAM',
                        'mensagem': f'Uso alto de memória: {mem.percent:.1f}% (Recomendado: <80%)',
                        'prioridade': 'MÉDIA'
                    })
                
                # Informações de SWAP
                swap = psutil.swap_memory()
                if swap.total > 0:
                    memory_info.update({
                        "swap_total": f"{swap.total / (1024**3):.2f} GB",
                        "swap_usado": f"{swap.used / (1024**3):.2f} GB",
                        "swap_porcentagem": f"{swap.percent:.1f}%"
                    })
                    
                    if swap.percent > 50:
                        self.alerts.append({
                            'tipo': 'AVISO',
                            'componente': 'SWAP',
                            'mensagem': f'Uso alto de arquivo de troca: {swap.percent:.1f}%',
                            'prioridade': 'BAIXA'
                        })
                
                # Tentar obter informações detalhadas via WMI (Windows)
                if available_libs.get('wmi') and platform.system() == 'Windows':
                    try:
                        c = wmi.WMI()
                        memory_modules = []
                        for memory in c.Win32_PhysicalMemory():
                            module_info = {
                                'capacidade': f"{int(memory.Capacity) / (1024**3):.0f} GB" if memory.Capacity else 'N/A',
                                'velocidade': f"{memory.Speed} MHz" if memory.Speed else 'N/A',
                                'tipo': memory.SMBIOSMemoryType or 'N/A',
                                'fabricante': memory.Manufacturer or 'N/A',
                                'numero_serie': memory.SerialNumber or 'N/A',
                                'localizacao': memory.DeviceLocator or 'N/A'
                            }
                            memory_modules.append(module_info)
                        
                        if memory_modules:
                            memory_info["modulos"] = memory_modules
                            memory_info["slots_ocupados"] = len(memory_modules)
                    except:
                        pass  # WMI pode falhar, continuar sem informações detalhadas
                        
        except Exception as e:
            memory_info["erro"] = f"Erro ao obter informações da memória: {str(e)}"
            
        return memory_info

    def get_storage_info(self):
        """Obtém informações detalhadas de armazenamento"""
        storage_info = {"dispositivos": [], "erro": None}
        
        try:
            if available_libs.get('psutil'):
                # Informações de partições
                partitions = psutil.disk_partitions()
                for partition in partitions:
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        device_info = {
                            "dispositivo": partition.device,
                            "ponto_montagem": partition.mountpoint,
                            "sistema_arquivos": partition.fstype,
                            "tamanho_total": f"{usage.total / (1024**3):.2f} GB",
                            "usado": f"{usage.used / (1024**3):.2f} GB",
                            "livre": f"{usage.free / (1024**3):.2f} GB",
                            "porcentagem_uso": f"{(usage.used / usage.total) * 100:.1f}%"
                        }
                        
                        # Verificar espaço em disco
                        usage_percent = (usage.used / usage.total) * 100
                        if usage_percent > 95:
                            self.alerts.append({
                                'tipo': 'CRÍTICO',
                                'componente': 'DISCO',
                                'mensagem': f'Espaço crítico em {partition.device}: {usage_percent:.1f}% usado',
                                'prioridade': 'ALTA'
                            })
                        elif usage_percent > 85:
                            self.alerts.append({
                                'tipo': 'AVISO',
                                'componente': 'DISCO',
                                'mensagem': f'Espaço baixo em {partition.device}: {usage_percent:.1f}% usado',
                                'prioridade': 'MÉDIA'
                            })
                        
                        storage_info["dispositivos"].append(device_info)
                    except PermissionError:
                        continue  # Ignorar dispositivos sem permissão
                
                # Informações de I/O de disco
                try:
                    disk_io = psutil.disk_io_counters()
                    if disk_io:
                        storage_info["estatisticas_io"] = {
                            "bytes_lidos": f"{disk_io.read_bytes / (1024**3):.2f} GB",
                            "bytes_escritos": f"{disk_io.write_bytes / (1024**3):.2f} GB",
                            "operacoes_leitura": disk_io.read_count,
                            "operacoes_escrita": disk_io.write_count,
                            "tempo_leitura": f"{disk_io.read_time / 1000:.2f} s",
                            "tempo_escrita": f"{disk_io.write_time / 1000:.2f} s"
                        }
                except:
                    pass
                
                # Tentar obter informações S.M.A.R.T. via WMI (Windows)
                if available_libs.get('wmi') and platform.system() == 'Windows':
                    try:
                        c = wmi.WMI()
                        for disk in c.Win32_DiskDrive():
                            smart_info = {
                                'modelo': disk.Model or 'N/A',
                                'interface': disk.InterfaceType or 'N/A',
                                'tamanho': f"{int(disk.Size) / (1024**3):.2f} GB" if disk.Size else 'N/A',
                                'numero_serie': disk.SerialNumber or 'N/A',
                                'status': disk.Status or 'N/A'
                            }
                            
                            # Adicionar informações S.M.A.R.T. ao primeiro dispositivo correspondente
                            if storage_info["dispositivos"]:
                                storage_info["dispositivos"][0]["smart"] = smart_info
                            break
                    except:
                        pass  # WMI pode falhar, continuar sem informações S.M.A.R.T.
                        
        except Exception as e:
            storage_info["erro"] = f"Erro ao obter informações de armazenamento: {str(e)}"
            
        return storage_info

    def get_motherboard_info(self):
        """Obtém informações da placa-mãe"""
        mb_info = {"erro": "Informações não disponíveis"}
        
        try:
            if available_libs.get('wmi') and platform.system() == 'Windows':
                c = wmi.WMI()
                
                # Informações da placa-mãe
                for board in c.Win32_BaseBoard():
                    mb_info = {
                        "fabricante": board.Manufacturer or 'N/A',
                        "modelo": board.Product or 'N/A',
                        "versao": board.Version or 'N/A',
                        "numero_serie": board.SerialNumber or 'N/A'
                    }
                    break
                
                # Informações da BIOS
                for bios in c.Win32_BIOS():
                    mb_info.update({
                        "bios_fabricante": bios.Manufacturer or 'N/A',
                        "bios_versao": bios.SMBIOSBIOSVersion or 'N/A',
                        "bios_data": bios.ReleaseDate[:8] if bios.ReleaseDate else 'N/A'
                    })
                    break
                
                # Informações do processador/chipset
                for processor in c.Win32_Processor():
                    mb_info.update({
                        "socket": processor.SocketDesignation or 'N/A',
                        "chipset": processor.Description or 'N/A'
                    })
                    break
            else:
                mb_info = {"erro": "WMI não disponível - informações limitadas no seu sistema"}
                
        except Exception as e:
            mb_info["erro"] = f"Erro ao obter informações da placa-mãe: {str(e)}"
            
        return mb_info

    def get_system_info(self):
        """Obtém informações do sistema operacional"""
        sys_info = {}
        
        try:
            sys_info = {
                "sistema": platform.system(),
                "versao": platform.version(),
                "release": platform.release(),
                "arquitetura": platform.architecture()[0],
                "processador": platform.processor(),
                "maquina": platform.machine(),
                "no_computador": platform.node()
            }
            
            if available_libs.get('psutil'):
                boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
                uptime = datetime.datetime.now() - boot_time
                sys_info.update({
                    "tempo_inicializacao": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "tempo_atividade": str(uptime).split('.')[0],
                    "usuarios_logados": len(psutil.users()) if psutil.users() else 0
                })
                
        except Exception as e:
            sys_info["erro"] = f"Erro ao obter informações do sistema: {str(e)}"
            
        return sys_info

    def get_network_info(self):
        """Obtém informações de rede"""
        network_info = {"interfaces": [], "erro": None}
        
        try:
            if available_libs.get('psutil'):
                interfaces = psutil.net_if_addrs()
                stats = psutil.net_if_stats()
                
                for interface_name, addresses in interfaces.items():
                    interface_info = {
                        "nome": interface_name,
                        "ativo": stats[interface_name].isup if interface_name in stats else False,
                        "enderecos": []
                    }
                    
                    for addr in addresses:
                        addr_info = {
                            "familia": str(addr.family),
                            "endereco": addr.address,
                            "mascara": addr.netmask,
                            "broadcast": addr.broadcast
                        }
                        interface_info["enderecos"].append(addr_info)
                    
                    if interface_name in stats:
                        stat = stats[interface_name]
                        interface_info.update({
                            "velocidade": f"{stat.speed} Mbps" if stat.speed > 0 else 'N/A',
                            "mtu": stat.mtu
                        })
                    
                    network_info["interfaces"].append(interface_info)
                
                # Estatísticas de rede
                net_io = psutil.net_io_counters()
                if net_io:
                    network_info["estatisticas"] = {
                        "bytes_enviados": f"{net_io.bytes_sent / (1024**2):.2f} MB",
                        "bytes_recebidos": f"{net_io.bytes_recv / (1024**2):.2f} MB",
                        "pacotes_enviados": net_io.packets_sent,
                        "pacotes_recebidos": net_io.packets_recv,
                        "erros_entrada": net_io.errin,
                        "erros_saida": net_io.errout
                    }
                    
        except Exception as e:
            network_info["erro"] = f"Erro ao obter informações de rede: {str(e)}"
            
        return network_info

    def analyze_health_and_recommendations(self):
        """Analisa a saúde do sistema e gera recomendações"""
        self.recommendations.clear()
        
        try:
            # Análise de CPU
            cpu_info = self.get_cpu_info()
            if "uso_atual" in cpu_info:
                cpu_usage = float(cpu_info["uso_atual"].replace("%", ""))
                if cpu_usage > 80:
                    self.recommendations.append({
                        'categoria': 'Performance',
                        'prioridade': 'ALTA',
                        'componente': 'CPU',
                        'problema': f'Uso alto de CPU: {cpu_usage:.1f}%',
                        'recomendacao': 'Feche programas desnecessários, verifique processos em segundo plano, considere upgrade do processador'
                    })
            
            # Análise de GPU
            gpu_info = self.get_gpu_info()
            if "uso_gpu" in gpu_info:
                gpu_usage = float(gpu_info["uso_gpu"].replace("%", ""))
                if gpu_usage > 90:
                    self.recommendations.append({
                        'categoria': 'Performance',
                        'prioridade': 'MÉDIA',
                        'componente': 'GPU',
                        'problema': f'Uso alto de GPU: {gpu_usage:.1f}%',
                        'recomendacao': 'Reduza configurações gráficas em jogos/aplicações, verifique drivers atualizados'
                    })
            
            # Análise de memória
            memory_info = self.get_memory_info()
            if "porcentagem_uso" in memory_info:
                mem_usage = float(memory_info["porcentagem_uso"].replace("%", ""))
                if mem_usage > 85:
                    self.recommendations.append({
                        'categoria': 'Hardware',
                        'prioridade': 'ALTA',
                        'componente': 'RAM',
                        'problema': f'Uso alto de memória: {mem_usage:.1f}%',
                        'recomendacao': 'Considere adicionar mais RAM, feche aplicações não utilizadas, verifique vazamentos de memória'
                    })
            
            # Análise de armazenamento
            storage_info = self.get_storage_info()
            for device in storage_info.get("dispositivos", []):
                if "porcentagem_uso" in device:
                    storage_usage = float(device["porcentagem_uso"].replace("%", ""))
                    if storage_usage > 90:
                        self.recommendations.append({
                            'categoria': 'Armazenamento',
                            'prioridade': 'CRÍTICA',
                            'componente': 'DISCO',
                            'problema': f'Espaço crítico em {device["dispositivo"]}: {storage_usage:.1f}%',
                            'recomendacao': 'Libere espaço urgentemente, mova arquivos para disco externo, execute limpeza de disco'
                        })
                    elif storage_usage > 80:
                        self.recommendations.append({
                            'categoria': 'Armazenamento',
                            'prioridade': 'MÉDIA',
                            'componente': 'DISCO',
                            'problema': f'Espaço baixo em {device["dispositivo"]}: {storage_usage:.1f}%',
                            'recomendacao': 'Execute limpeza de arquivos temporários, desinstale programas não utilizados'
                        })
            
            # Recomendações de manutenção preventiva
            self.recommendations.append({
                'categoria': 'Manutenção',
                'prioridade': 'BAIXA',
                'componente': 'GERAL',
                'problema': 'Manutenção preventiva',
                'recomendacao': 'Execute limpeza física do PC a cada 6 meses, atualize drivers regularmente, faça backup dos dados importantes'
            })
            
            # Recomendações de segurança
            self.recommendations.append({
                'categoria': 'Segurança',
                'prioridade': 'MÉDIA',
                'componente': 'SISTEMA',
                'problema': 'Segurança do sistema',
                'recomendacao': 'Mantenha o sistema operacional atualizado, use antivírus atualizado, ative o firewall do Windows'
            })
            
        except Exception as e:
            self.recommendations.append({
                'categoria': 'Sistema',
                'prioridade': 'BAIXA',
                'componente': 'DIAGNÓSTICO',
                'problema': 'Erro na análise',
                'recomendacao': f'Erro durante análise de saúde: {str(e)}'
            })

    def run_complete_diagnosis(self):
        """Executa diagnóstico completo do hardware"""
        self.status_var.set("Executando diagnóstico completo...")
        self.hardware_text.delete('1.0', tk.END)
        
        def diagnosis_thread():
            try:
                self.alerts.clear()
                self.recommendations.clear()
                
                # Cabeçalho
                report = "🔧 RELATÓRIO DE DIAGNÓSTICO COMPLETO DE PC\n"
                report += "=" * 60 + "\n"
                report += f"Data/Hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                report += f"Sistema: {platform.system()} {platform.release()}\n\n"
                
                # Diagnóstico de CPU
                self.root.after(0, lambda: self.status_var.set("Analisando CPU..."))
                report += "🖥️  PROCESSADOR (CPU)\n" + "-" * 30 + "\n"
                cpu_info = self.get_cpu_info()
                for key, value in cpu_info.items():
                    if key != "flags":
                        report += f"{key.replace('_', ' ').title()}: {value}\n"
                report += "\n"
                
                # Diagnóstico de GPU
                self.root.after(0, lambda: self.status_var.set("Analisando GPU..."))
                report += "🎮 PLACA DE VÍDEO (GPU)\n" + "-" * 30 + "\n"
                gpu_info = self.get_gpu_info()
                for key, value in gpu_info.items():
                    report += f"{key.replace('_', ' ').title()}: {value}\n"
                report += "\n"
                
                # Diagnóstico de Memória
                self.root.after(0, lambda: self.status_var.set("Analisando Memória RAM..."))
                report += "💾 MEMÓRIA RAM\n" + "-" * 30 + "\n"
                memory_info = self.get_memory_info()
                for key, value in memory_info.items():
                    if key != "modulos":
                        report += f"{key.replace('_', ' ').title()}: {value}\n"
                
                if "modulos" in memory_info:
                    report += "\n📋 Módulos de Memória Detectados:\n"
                    for i, module in enumerate(memory_info["modulos"], 1):
                        report += f"  Módulo {i}:\n"
                        for mod_key, mod_value in module.items():
                            report += f"    {mod_key.replace('_', ' ').title()}: {mod_value}\n"
                report += "\n"
                
                # Diagnóstico de Armazenamento
                self.root.after(0, lambda: self.status_var.set("Analisando Armazenamento..."))
                report += "💿 ARMAZENAMENTO\n" + "-" * 30 + "\n"
                storage_info = self.get_storage_info()
                
                if storage_info.get("erro"):
                    report += f"Erro: {storage_info['erro']}\n"
                else:
                    for i, device in enumerate(storage_info.get("dispositivos", []), 1):
                        report += f"Dispositivo {i}:\n"
                        for dev_key, dev_value in device.items():
                            if dev_key != "smart":
                                report += f"  {dev_key.replace('_', ' ').title()}: {dev_value}\n"
                        
                        if "smart" in device:
                            report += "  Informações S.M.A.R.T.:\n"
                            for smart_key, smart_value in device["smart"].items():
                                report += f"    {smart_key.replace('_', ' ').title()}: {smart_value}\n"
                        report += "\n"
                    
                    if "estatisticas_io" in storage_info:
                        report += "📊 Estatísticas de I/O:\n"
                        for stat_key, stat_value in storage_info["estatisticas_io"].items():
                            report += f"  {stat_key.replace('_', ' ').title()}: {stat_value}\n"
                        report += "\n"
                
                # Informações da Placa-mãe
                self.root.after(0, lambda: self.status_var.set("Analisando Placa-mãe..."))
                report += "⚡ PLACA-MÃE\n" + "-" * 30 + "\n"
                mb_info = self.get_motherboard_info()
                for key, value in mb_info.items():
                    report += f"{key.replace('_', ' ').title()}: {value}\n"
                report += "\n"
                
                # Informações do Sistema
                self.root.after(0, lambda: self.status_var.set("Analisando Sistema..."))
                report += "🖥️  SISTEMA OPERACIONAL\n" + "-" * 30 + "\n"
                sys_info = self.get_system_info()
                for key, value in sys_info.items():
                    report += f"{key.replace('_', ' ').title()}: {value}\n"
                report += "\n"
                
                # Informações de Rede
                self.root.after(0, lambda: self.status_var.set("Analisando Rede..."))
                report += "🌐 REDE\n" + "-" * 30 + "\n"
                network_info = self.get_network_info()
                
                if network_info.get("erro"):
                    report += f"Erro: {network_info['erro']}\n"
                else:
                    # Mostrar apenas interfaces ativas
                    active_interfaces = [iface for iface in network_info.get("interfaces", []) if iface.get("ativo")]
                    if active_interfaces:
                        report += "Interfaces Ativas:\n"
                        for interface in active_interfaces:
                            report += f"  {interface['nome']}:\n"
                            if "velocidade" in interface:
                                report += f"    Velocidade: {interface['velocidade']}\n"
                            if "mtu" in interface:
                                report += f"    MTU: {interface['mtu']}\n"
                            
                            # Mostrar apenas endereços IPv4
                            ipv4_addresses = [addr for addr in interface.get("enderecos", []) 
                                            if "IPv4" in addr.get("familia", "") or "2" in addr.get("familia", "")]
                            if ipv4_addresses:
                                for addr in ipv4_addresses[:1]:  # Mostrar apenas o primeiro
                                    report += f"    IP: {addr['endereco']}\n"
                    
                    if "estatisticas" in network_info:
                        report += "\n📊 Estatísticas de Rede:\n"
                        for stat_key, stat_value in network_info["estatisticas"].items():
                            report += f"  {stat_key.replace('_', ' ').title()}: {stat_value}\n"
                report += "\n"
                
                # Análise de saúde e recomendações
                self.root.after(0, lambda: self.status_var.set("Gerando recomendações..."))
                self.analyze_health_and_recommendations()
                
                # Alertas críticos
                critical_alerts = [alert for alert in self.alerts if alert['tipo'] == 'CRÍTICO']
                if critical_alerts:
                    report += "🚨 ALERTAS CRÍTICOS\n" + "-" * 30 + "\n"
                    for alert in critical_alerts:
                        report += f"⚠️  {alert['componente']}: {alert['mensagem']}\n"
                    report += "\n"
                
                # Avisos
                warnings = [alert for alert in self.alerts if alert['tipo'] == 'AVISO']
                if warnings:
                    report += "⚠️  AVISOS\n" + "-" * 30 + "\n"
                    for warning in warnings:
                        report += f"🔶 {warning['componente']}: {warning['mensagem']}\n"
                    report += "\n"
                
                # Recomendações por prioridade
                if self.recommendations:
                    report += "💡 RECOMENDAÇÕES\n" + "-" * 30 + "\n"
                    
                    priorities = ['CRÍTICA', 'ALTA', 'MÉDIA', 'BAIXA']
                    for priority in priorities:
                        priority_recs = [rec for rec in self.recommendations if rec['prioridade'] == priority]
                        if priority_recs:
                            report += f"\n🔴 Prioridade {priority}:\n"
                            for rec in priority_recs:
                                report += f"  • {rec['componente']}: {rec['recomendacao']}\n"
                    report += "\n"
                
                # Rodapé
                report += "=" * 60 + "\n"
                report += "✅ Diagnóstico concluído com sucesso!\n"
                report += f"🕐 Tempo de execução: ~{datetime.datetime.now().strftime('%H:%M:%S')}\n"
                report += "💾 Para salvar este relatório, use os botões 'Exportar' acima.\n"
                
                # Mostrar resultado na GUI
                self.root.after(0, lambda: self.hardware_text.insert('1.0', report))
                self.root.after(0, lambda: self.update_alerts_tab())
                self.root.after(0, lambda: self.status_var.set("Diagnóstico completo finalizado!"))
                
                # Salvar log
                self.save_diagnosis_log(report)
                
            except Exception as e:
                error_msg = f"❌ Erro durante o diagnóstico: {str(e)}\n"
                self.root.after(0, lambda: self.hardware_text.insert('1.0', error_msg))
                self.root.after(0, lambda: self.status_var.set("Erro no diagnóstico"))
        
        # Executar em thread separada para não travar a GUI
        thread = threading.Thread(target=diagnosis_thread)
        thread.daemon = True
        thread.start()

    def update_alerts_tab(self):
        """Atualiza a aba de alertas com os alertas atuais"""
        # Limpar textos anteriores
        self.critical_alerts_text.delete('1.0', tk.END)
        self.recommendations_text.delete('1.0', tk.END)
        
        # Alertas críticos
        critical_alerts = [alert for alert in self.alerts if alert['tipo'] == 'CRÍTICO']
        warnings = [alert for alert in self.alerts if alert['tipo'] == 'AVISO']
        
        if critical_alerts or warnings:
            alert_text = "🚨 ALERTAS DETECTADOS\n" + "=" * 40 + "\n\n"
            
            if critical_alerts:
                alert_text += "🔴 CRÍTICOS:\n"
                for alert in critical_alerts:
                    alert_text += f"⚠️  {alert['componente']}: {alert['mensagem']}\n"
                alert_text += "\n"
            
            if warnings:
                alert_text += "🟡 AVISOS:\n"
                for warning in warnings:
                    alert_text += f"🔶 {warning['componente']}: {warning['mensagem']}\n"
            
        else:
            alert_text = "✅ SISTEMA SAUDÁVEL\n\nNenhum alerta crítico detectado."
        
        self.critical_alerts_text.insert('1.0', alert_text)
        
        # Recomendações
        if self.recommendations:
            rec_text = "💡 RECOMENDAÇÕES DE MELHORIA\n" + "=" * 40 + "\n\n"
            
            priorities = ['CRÍTICA', 'ALTA', 'MÉDIA', 'BAIXA']
            for priority in priorities:
                priority_recs = [rec for rec in self.recommendations if rec['prioridade'] == priority]
                if priority_recs:
                    rec_text += f"🔴 PRIORIDADE {priority}:\n"
                    for i, rec in enumerate(priority_recs, 1):
                        rec_text += f"{i}. [{rec['categoria']}] {rec['componente']}:\n"
                        rec_text += f"   Problema: {rec['problema']}\n"
                        rec_text += f"   Solução: {rec['recomendacao']}\n\n"
        else:
            rec_text = "✅ SISTEMA OTIMIZADO\n\nNenhuma recomendação específica no momento."
        
        self.recommendations_text.insert('1.0', rec_text)

    def toggle_monitoring(self):
        """Inicia/para o monitoramento em tempo real"""
        if not self.monitoring:
            self.start_monitoring()
        else:
            self.stop_monitoring()

    def start_monitoring(self):
        """Inicia o monitoramento em tempo real"""
        self.monitoring = True
        self.monitoring_button.config(text="⏹️ Parar Monitoramento")
        
        # Limpar dados anteriores
        for key in self.monitoring_data:
            self.monitoring_data[key].clear()
        
        # Duração do monitoramento em minutos
        duration_minutes = int(self.duration_var.get())
        
        self.monitoring_log.delete('1.0', tk.END)
        self.monitoring_log.insert(tk.END, f"🟢 Monitoramento iniciado por {duration_minutes} minutos...\n")
        self.monitoring_log.insert(tk.END, f"Início: {datetime.datetime.now().strftime('%H:%M:%S')}\n\n")
        
        def monitoring_thread():
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)  # Converter para segundos
            
            while self.monitoring and time.time() < end_time:
                try:
                    current_time = datetime.datetime.now()
                    self.monitoring_data['timestamps'].append(current_time)
                    
                    # Coletar dados de CPU
                    if available_libs.get('psutil'):
                        cpu_percent = psutil.cpu_percent(interval=1)
                        self.monitoring_data['cpu_usage'].append(cpu_percent)
                        
                        # Tentar obter temperatura da CPU
                        cpu_temp = self.get_cpu_temperature()
                        if cpu_temp:
                            self.monitoring_data['cpu_temp'].append(cpu_temp)
                        
                        # Dados de memória
                        memory = psutil.virtual_memory()
                        self.monitoring_data['memory_usage'].append(memory.percent)
                    
                    # Coletar dados de GPU
                    if available_libs.get('GPUtil'):
                        try:
                            gpus = GPUtil.getGPUs()
                            if gpus:
                                gpu = gpus[0]
                                self.monitoring_data['gpu_usage'].append(gpu.load * 100)
                                self.monitoring_data['gpu_temp'].append(gpu.temperature)
                        except:
                            pass
                    
                    # Atualizar GUI com valores atuais
                    self.root.after(0, lambda: self.update_realtime_display())
                    
                    # Log de eventos significativos
                    if cpu_percent > 80:
                        log_msg = f"[{current_time.strftime('%H:%M:%S')}] ⚠️  CPU alta: {cpu_percent:.1f}%\n"
                        self.root.after(0, lambda msg=log_msg: self.monitoring_log.insert(tk.END, msg))
                    
                    if available_libs.get('psutil'):
                        memory = psutil.virtual_memory()
                        if memory.percent > 85:
                            log_msg = f"[{current_time.strftime('%H:%M:%S')}] ⚠️  RAM alta: {memory.percent:.1f}%\n"
                            self.root.after(0, lambda msg=log_msg: self.monitoring_log.insert(tk.END, msg))
                    
                    # Aguardar 2 segundos antes da próxima coleta
                    time.sleep(2)
                    
                except Exception as e:
                    error_msg = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ❌ Erro: {str(e)}\n"
                    self.root.after(0, lambda msg=error_msg: self.monitoring_log.insert(tk.END, msg))
                    time.sleep(2)
            
            # Finalizar monitoramento
            self.root.after(0, self.finish_monitoring)
        
        # Iniciar thread de monitoramento
        monitor_thread = threading.Thread(target=monitoring_thread)
        monitor_thread.daemon = True
        monitor_thread.start()

    def get_cpu_temperature(self):
        """Tenta obter temperatura da CPU"""
        try:
            if available_libs.get('psutil'):
                sensors = psutil.sensors_temperatures()
                if sensors:
                    for name, entries in sensors.items():
                        if 'coretemp' in name.lower() or 'cpu' in name.lower():
                            if entries:
                                return entries[0].current
        except:
            pass
        return None

    def update_realtime_display(self):
        """Atualiza os displays de métricas em tempo real"""
        try:
            if self.monitoring_data['cpu_usage']:
                cpu_usage = self.monitoring_data['cpu_usage'][-1]
                self.cpu_usage_var.set(f"{cpu_usage:.1f}%")
            
            if self.monitoring_data['cpu_temp'] and self.monitoring_data['cpu_temp'][-1]:
                cpu_temp = self.monitoring_data['cpu_temp'][-1]
                self.cpu_temp_var.set(f"{cpu_temp:.1f}°C")
            
            if self.monitoring_data['gpu_usage']:
                gpu_usage = self.monitoring_data['gpu_usage'][-1]
                self.gpu_usage_var.set(f"{gpu_usage:.1f}%")
            
            if self.monitoring_data['gpu_temp']:
                gpu_temp = self.monitoring_data['gpu_temp'][-1]
                self.gpu_temp_var.set(f"{gpu_temp:.1f}°C")
            
            if self.monitoring_data['memory_usage']:
                mem_usage = self.monitoring_data['memory_usage'][-1]
                self.mem_usage_var.set(f"{mem_usage:.1f}%")
                
                # Calcular memória disponível
                if available_libs.get('psutil'):
                    memory = psutil.virtual_memory()
                    self.mem_available_var.set(f"{memory.available / (1024**3):.1f} GB")
                    
        except Exception as e:
            pass  # Ignorar erros de atualização de display

    def stop_monitoring(self):
        """Para o monitoramento em tempo real"""
        self.monitoring = False
        
    def finish_monitoring(self):
        """Finaliza o monitoramento e atualiza a GUI"""
        self.monitoring = False
        self.monitoring_button.config(text="▶️ Iniciar Monitoramento")
        
        end_msg = f"\n🔴 Monitoramento finalizado: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
        end_msg += f"📊 Dados coletados: {len(self.monitoring_data['timestamps'])} amostras\n"
        
        if self.monitoring_data['cpu_usage']:
            avg_cpu = sum(self.monitoring_data['cpu_usage']) / len(self.monitoring_data['cpu_usage'])
            max_cpu = max(self.monitoring_data['cpu_usage'])
            end_msg += f"   CPU - Média: {avg_cpu:.1f}%, Máximo: {max_cpu:.1f}%\n"
        
        if self.monitoring_data['memory_usage']:
            avg_mem = sum(self.monitoring_data['memory_usage']) / len(self.monitoring_data['memory_usage'])
            max_mem = max(self.monitoring_data['memory_usage'])
            end_msg += f"   RAM - Média: {avg_mem:.1f}%, Máximo: {max_mem:.1f}%\n"
        
        self.monitoring_log.insert(tk.END, end_msg)
        
        # Salvar log de monitoramento
        self.save_monitoring_log()

    def show_realtime_graph(self):
        """Mostra gráfico em tempo real dos dados de monitoramento"""
        if not available_libs.get('matplotlib'):
            messagebox.showerror("Erro", "Matplotlib não disponível.\nInstale com: pip install matplotlib")
            return
        
        if not self.monitoring_data['timestamps']:
            messagebox.showwarning("Aviso", "Nenhum dado de monitoramento disponível.\nInicie o monitoramento primeiro.")
            return
        
        # Criar janela de gráfico
        graph_window = tk.Toplevel(self.root)
        graph_window.title("📈 Gráficos de Monitoramento em Tempo Real")
        graph_window.geometry("1000x600")
        graph_window.configure(bg='#2b2b2b')
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.patch.set_facecolor('#2b2b2b')
        
        # Gráfico de CPU
        if self.monitoring_data['cpu_usage']:
            ax1.plot(self.monitoring_data['timestamps'], self.monitoring_data['cpu_usage'], 
                    color='#ff6b6b', linewidth=2, label='CPU %')
            ax1.set_title('Uso de CPU', color='white')
            ax1.set_ylabel('Percentual (%)', color='white')
            ax1.tick_params(colors='white')
            ax1.set_facecolor('#1e1e1e')
            ax1.grid(True, alpha=0.3)
        
        # Gráfico de GPU
        if self.monitoring_data['gpu_usage']:
            ax2.plot(self.monitoring_data['timestamps'], self.monitoring_data['gpu_usage'], 
                    color='#4ecdc4', linewidth=2, label='GPU %')
            ax2.set_title('Uso de GPU', color='white')
            ax2.set_ylabel('Percentual (%)', color='white')
            ax2.tick_params(colors='white')
            ax2.set_facecolor('#1e1e1e')
            ax2.grid(True, alpha=0.3)
        
        # Gráfico de Memória
        if self.monitoring_data['memory_usage']:
            ax3.plot(self.monitoring_data['timestamps'], self.monitoring_data['memory_usage'], 
                    color='#45b7d1', linewidth=2, label='RAM %')
            ax3.set_title('Uso de Memória RAM', color='white')
            ax3.set_ylabel('Percentual (%)', color='white')
            ax3.tick_params(colors='white')
            ax3.set_facecolor('#1e1e1e')
            ax3.grid(True, alpha=0.3)
        
        # Gráfico de Temperatura
        if self.monitoring_data['cpu_temp'] or self.monitoring_data['gpu_temp']:
            if self.monitoring_data['cpu_temp']:
                # Filtrar valores válidos de temperatura
                valid_temps = [(t, temp) for t, temp in zip(self.monitoring_data['timestamps'], self.monitoring_data['cpu_temp']) if temp is not None]
                if valid_temps:
                    times, temps = zip(*valid_temps)
                    ax4.plot(times, temps, color='#f39c12', linewidth=2, label='CPU °C')
            
            if self.monitoring_data['gpu_temp']:
                ax4.plot(self.monitoring_data['timestamps'], self.monitoring_data['gpu_temp'], 
                        color='#e74c3c', linewidth=2, label='GPU °C')
            
            ax4.set_title('Temperaturas', color='white')
            ax4.set_ylabel('Temperatura (°C)', color='white')
            ax4.tick_params(colors='white')
            ax4.set_facecolor('#1e1e1e')
            ax4.grid(True, alpha=0.3)
            ax4.legend()
        
        # Ajustar layout
        plt.tight_layout()
        
        # Integrar matplotlib com tkinter
        canvas = FigureCanvasTkAgg(fig, graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def save_monitoring_csv(self):
        """Salva os dados de monitoramento em arquivo CSV"""
        if not self.monitoring_data['timestamps']:
            messagebox.showwarning("Aviso", "Nenhum dado de monitoramento disponível.")
            return
        
        try:
            filename = f"monitoramento_pc_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = Path.cwd() / filename
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Cabeçalho
                headers = ['Timestamp', 'CPU_Usage_%', 'Memory_Usage_%']
                if self.monitoring_data['gpu_usage']:
                    headers.append('GPU_Usage_%')
                if self.monitoring_data['cpu_temp'] and any(t for t in self.monitoring_data['cpu_temp'] if t):
                    headers.append('CPU_Temp_C')
                if self.monitoring_data['gpu_temp']:
                    headers.append('GPU_Temp_C')
                
                writer.writerow(headers)
                
                # Dados
                for i, timestamp in enumerate(self.monitoring_data['timestamps']):
                    row = [
                        timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        self.monitoring_data['cpu_usage'][i] if i < len(self.monitoring_data['cpu_usage']) else '',
                        self.monitoring_data['memory_usage'][i] if i < len(self.monitoring_data['memory_usage']) else ''
                    ]
                    
                    if self.monitoring_data['gpu_usage'] and i < len(self.monitoring_data['gpu_usage']):
                        row.append(self.monitoring_data['gpu_usage'][i])
                    elif self.monitoring_data['gpu_usage']:
                        row.append('')
                    
                    if self.monitoring_data['cpu_temp'] and any(t for t in self.monitoring_data['cpu_temp'] if t):
                        temp = self.monitoring_data['cpu_temp'][i] if i < len(self.monitoring_data['cpu_temp']) else None
                        row.append(temp if temp is not None else '')
                    
                    if self.monitoring_data['gpu_temp'] and i < len(self.monitoring_data['gpu_temp']):
                        row.append(self.monitoring_data['gpu_temp'][i])
                    elif self.monitoring_data['gpu_temp']:
                        row.append('')
                    
                    writer.writerow(row)
            
            messagebox.showinfo("Sucesso", f"Dados salvos em: {filepath}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar CSV: {str(e)}")

    def export_txt_report(self):
        """Exporta relatório em formato TXT"""
        content = self.hardware_text.get('1.0', tk.END).strip()
        if not content:
            messagebox.showwarning("Aviso", "Execute um diagnóstico primeiro.")
            return
        
        try:
            filename = f"relatorio_pc_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivos de Texto", "*.txt")],
                initialname=filename
            )
            
            if filepath:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                messagebox.showinfo("Sucesso", f"Relatório salvo em: {filepath}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar relatório: {str(e)}")

    def export_html_report(self):
        """Exporta relatório em formato HTML com gráficos"""
        content = self.hardware_text.get('1.0', tk.END).strip()
        if not content:
            messagebox.showwarning("Aviso", "Execute um diagnóstico primeiro.")
            return
        
        try:
            filename = f"relatorio_pc_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("Arquivos HTML", "*.html")],
                initialname=filename
            )
            
            if filepath:
                html_content = self.generate_html_report(content)
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(html_content)
                messagebox.showinfo("Sucesso", f"Relatório HTML salvo em: {filepath}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar relatório HTML: {str(e)}")

    def generate_html_report(self, content):
        """Gera relatório em formato HTML"""
        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Diagnóstico de PC</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1a1a1a;
            color: #ffffff;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: #2d2d2d;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}
        h1 {{
            color: #00d4ff;
            text-align: center;
            border-bottom: 2px solid #00d4ff;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #ffaa00;
            border-left: 4px solid #ffaa00;
            padding-left: 10px;
            margin-top: 30px;
        }}
        .section {{
            background-color: #3a3a3a;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #00d4ff;
        }}
        .alert-critical {{
            background-color: #4a1a1a;
            border-left-color: #ff4444;
        }}
        .alert-warning {{
            background-color: #4a3a1a;
            border-left-color: #ffaa00;
        }}
        .alert-success {{
            background-color: #1a4a1a;
            border-left-color: #44ff44;
        }}
        pre {{
            background-color: #1e1e1e;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 14px;
            border: 1px solid #444;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background-color: #404040;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #00d4ff;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #555;
            color: #aaa;
        }}
        .timestamp {{
            float: right;
            color: #888;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Relatório de Diagnóstico de PC</h1>
        <div class="timestamp">Gerado em: {datetime.datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</div>
        
        <div class="section">
            <h2>📊 Resumo Executivo</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value">{len(self.alerts)}</div>
                    <div>Alertas Detectados</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{len([a for a in self.alerts if a['tipo'] == 'CRÍTICO'])}</div>
                    <div>Alertas Críticos</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{len(self.recommendations)}</div>
                    <div>Recomendações</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{'✅' if not any(a['tipo'] == 'CRÍTICO' for a in self.alerts) else '⚠️'}</div>
                    <div>Status Geral</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 Relatório Completo</h2>
            <pre>{content}</pre>
        </div>
        
        <div class="footer">
            <p>Sistema de Diagnóstico de PC v1.0</p>
            <p>Relatório gerado automaticamente</p>
        </div>
    </div>
</body>
</html>
"""
        return html

    def generate_complete_report(self):
        """Gera relatório completo com análise avançada"""
        if not self.hardware_text.get('1.0', tk.END).strip():
            messagebox.showinfo("Info", "Execute um diagnóstico completo primeiro.")
            return
        
        report = "📊 RELATÓRIO COMPLETO DE SISTEMA\n"
        report += "=" * 50 + "\n\n"
        
        # Informações básicas
        report += self.hardware_text.get('1.0', tk.END)
        
        # Adicionar dados de monitoramento se disponíveis
        if self.monitoring_data['timestamps']:
            report += "\n📈 DADOS DE MONITORAMENTO\n" + "-" * 30 + "\n"
            report += f"Período: {len(self.monitoring_data['timestamps'])} amostras coletadas\n"
            
            if self.monitoring_data['cpu_usage']:
                avg_cpu = sum(self.monitoring_data['cpu_usage']) / len(self.monitoring_data['cpu_usage'])
                max_cpu = max(self.monitoring_data['cpu_usage'])
                report += f"CPU - Média: {avg_cpu:.1f}%, Máximo: {max_cpu:.1f}%\n"
            
            if self.monitoring_data['memory_usage']:
                avg_mem = sum(self.monitoring_data['memory_usage']) / len(self.monitoring_data['memory_usage'])
                max_mem = max(self.monitoring_data['memory_usage'])
                report += f"RAM - Média: {avg_mem:.1f}%, Máximo: {max_mem:.1f}%\n"
            
            if self.monitoring_data['gpu_usage']:
                avg_gpu = sum(self.monitoring_data['gpu_usage']) / len(self.monitoring_data['gpu_usage'])
                max_gpu = max(self.monitoring_data['gpu_usage'])
                report += f"GPU - Média: {avg_gpu:.1f}%, Máximo: {max_gpu:.1f}%\n"
        
        self.reports_text.delete('1.0', tk.END)
        self.reports_text.insert('1.0', report)

    def open_reports_folder(self):
        """Abre a pasta de relatórios"""
        try:
            current_dir = Path.cwd()
            if platform.system() == 'Windows':
                os.startfile(current_dir)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', current_dir])
            else:  # Linux
                subprocess.run(['xdg-open', current_dir])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir pasta: {str(e)}")

    def clear_logs(self):
        """Limpa todos os logs"""
        try:
            # Limpar logs na pasta atual
            log_files = list(Path.cwd().glob("*.log"))
            csv_files = list(Path.cwd().glob("monitoramento_pc_*.csv"))
            txt_files = list(Path.cwd().glob("relatorio_pc_*.txt"))
            html_files = list(Path.cwd().glob("relatorio_pc_*.html"))
            
            all_files = log_files + csv_files + txt_files + html_files
            
            if all_files:
                result = messagebox.askyesno("Confirmar", f"Deseja apagar {len(all_files)} arquivo(s) de log e relatórios?")
                if result:
                    for file in all_files:
                        file.unlink()
                    messagebox.showinfo("Sucesso", f"{len(all_files)} arquivo(s) removido(s).")
            else:
                messagebox.showinfo("Info", "Nenhum arquivo de log encontrado.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao limpar logs: {str(e)}")

    def save_diagnosis_log(self, content):
        """Salva log do diagnóstico"""
        try:
            log_filename = f"diagnostico_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            with open(log_filename, 'w', encoding='utf-8') as log_file:
                log_file.write(f"LOG DE DIAGNÓSTICO - {datetime.datetime.now()}\n")
                log_file.write("=" * 60 + "\n")
                log_file.write(content)
        except Exception as e:
            print(f"Erro ao salvar log: {e}")

    def save_monitoring_log(self):
        """Salva log do monitoramento"""
        try:
            log_content = self.monitoring_log.get('1.0', tk.END)
            if log_content.strip():
                log_filename = f"monitoramento_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
                with open(log_filename, 'w', encoding='utf-8') as log_file:
                    log_file.write(f"LOG DE MONITORAMENTO - {datetime.datetime.now()}\n")
                    log_file.write("=" * 60 + "\n")
                    log_file.write(log_content)
        except Exception as e:
            print(f"Erro ao salvar log de monitoramento: {e}")

    def run(self):
        """Executa a aplicação"""
        try:
            # Executar diagnóstico inicial automaticamente
            self.root.after(1000, self.run_complete_diagnosis)
            
            # Iniciar a GUI
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n🛑 Aplicação interrompida pelo usuário.")
        except Exception as e:
            print(f"❌ Erro crítico: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando Sistema de Diagnóstico de PC...")
    print("⏳ Carregando interface gráfica...\n")
    
    try:
        # Criar e executar o sistema de diagnóstico
        diagnostico = DiagnosticoPCAvancado()
        diagnostico.run()
    except Exception as e:
        print(f"❌ Erro ao iniciar o sistema: {e}")
        input("\nPressione Enter para sair...")
