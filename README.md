# 🔧 Sistema de Diagnóstico de PC Profissional v1.0

Um sistema completo de diagnóstico e monitoramento de hardware para Windows 10/11, desenvolvido em Python com interface gráfica avançada.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

## 🌟 Características Principais

### 📊 Detecção Completa de Hardware
- **CPU**: Modelo, fabricante, núcleos, threads, frequência, temperatura, uso em tempo real
- **GPU**: Modelo, memória VRAM, temperatura, uso, drivers, compatibilidade CUDA/OpenCL
- **RAM**: Capacidade total, uso, módulos instalados, velocidade, tipo (DDR3/DDR4/DDR5)
- **Armazenamento**: HDDs, SSDs, NVMe com informações S.M.A.R.T., saúde e temperaturas
- **Placa-mãe**: Modelo, fabricante, chipset, versão da BIOS
- **Sistema**: Windows, versão, build, tempo de atividade, usuários
- **Rede**: Interfaces, velocidades, estatísticas de tráfego

### 📈 Monitoramento em Tempo Real
- Monitoramento contínuo por até **30 minutos**
- Gráficos em tempo real de CPU, GPU, RAM e temperaturas
- Alertas visuais para valores críticos
- Logs detalhados de eventos significativos
- Exportação de dados em formato CSV

### ⚠️ Sistema de Alertas Inteligente
- **Alertas Críticos**: Temperaturas perigosas, uso excessivo de recursos
- **Avisos**: Situações que merecem atenção
- **Limites Configuráveis**: CPU (75°C/85°C), GPU (80°C/90°C)
- **Priorização**: CRÍTICA, ALTA, MÉDIA, BAIXA

### 💡 Recomendações Automáticas
- Análise inteligente da saúde do sistema
- Sugestões de melhoria categorizadas
- Recomendações de manutenção preventiva
- Orientações de segurança e otimização

### 📋 Relatórios Completos
- **Formato TXT**: Relatório detalhado em texto
- **Formato HTML**: Relatório visual com gráficos e métricas
- **Logs Históricos**: Arquivo .log com histórico completo
- **Dados CSV**: Exportação de dados de monitoramento

## 🔧 Instalação

### Pré-requisitos
- **Windows 10 ou 11**
- **Python 3.7 ou superior**
- **Privilégios de Administrador** (recomendado para acesso completo aos sensores)

### 1. Dependências Necessárias

Execute o comando abaixo para instalar todas as dependências:

```bash
pip install psutil GPUtil py-cpuinfo tabulate rich matplotlib wmi
```

### Dependências Individuais:
```bash
pip install psutil          # Informações do sistema
pip install GPUtil           # Informações da GPU
pip install py-cpuinfo       # Informações detalhadas do CPU
pip install tabulate         # Formatação de tabelas
pip install rich             # Interface colorida no terminal
pip install matplotlib       # Gráficos
pip install wmi              # Informações específicas do Windows
```

### 2. Download e Execução

1. **Download**: Baixe o arquivo `diagnostico_pc.py`
2. **Execução**: Clique duas vezes no arquivo ou execute via terminal:

```bash
python diagnostico_pc.py
```

### 3. Executar como Administrador (Recomendado)

Para acesso completo aos sensores de temperatura e informações de hardware:

1. Abra o **Prompt de Comando como Administrador**
2. Navegue até a pasta do arquivo
3. Execute: `python diagnostico_pc.py`

## 🖥️ Como Usar

### Interface Principal

O sistema possui **4 abas principais**:

#### 🖥️ **Aba Hardware**
- **Diagnóstico Completo**: Executa análise completa do sistema
- **Exportar TXT/HTML**: Salva relatórios em diferentes formatos
- **Visualização**: Mostra todas as informações detectadas

#### 📊 **Aba Monitoramento**
- **Iniciar Monitoramento**: Coleta dados em tempo real
- **Duração**: Configure de 1 a 30 minutos
- **Gráficos**: Visualize métricas ao vivo
- **Salvar CSV**: Exporte dados coletados

#### 📋 **Aba Relatórios**
- **Relatório Completo**: Gera análise abrangente
- **Abrir Pasta**: Acessa pasta de relatórios salvos
- **Limpar Logs**: Remove arquivos antigos

#### ⚠️ **Aba Alertas**
- **Alertas Críticos**: Situações que requerem ação imediata
- **Recomendações**: Sugestões categorizadas por prioridade

### Fluxo de Uso Recomendado

1. **Execute o Diagnóstico Completo** (aba Hardware)
2. **Analise os Alertas** (aba Alertas)
3. **Inicie Monitoramento** se necessário (aba Monitoramento)
4. **Gere Relatórios** para documentação (aba Relatórios)
5. **Exporte dados** em formatos apropriados

## 📊 Interpretando os Resultados

### 🚨 **Alertas Críticos**
- **Temperatura CPU > 85°C**: Risco de throttling e danos
- **Temperatura GPU > 90°C**: Risco de instabilidade
- **RAM > 90%**: Sistema pode ficar lento
- **Disco > 95%**: Risco de falha do sistema

### ⚠️ **Avisos**
- **Temperatura CPU > 75°C**: Monitorar de perto
- **Temperatura GPU > 80°C**: Considerar melhoria da ventilação
- **RAM > 80%**: Considerar upgrade
- **Disco > 85%**: Limpar arquivos desnecessários

### 💡 **Prioridades das Recomendações**

- **🔴 CRÍTICA**: Ação imediata necessária
- **🟠 ALTA**: Resolver em breve
- **🟡 MÉDIA**: Atenção quando possível
- **🟢 BAIXA**: Manutenção preventiva

## 📁 Arquivos Gerados

O sistema cria automaticamente:

### 📄 **Relatórios**
- `relatorio_pc_YYYYMMDD_HHMMSS.txt` - Relatório em texto
- `relatorio_pc_YYYYMMDD_HHMMSS.html` - Relatório visual

### 📊 **Dados de Monitoramento**
- `monitoramento_pc_YYYYMMDD_HHMMSS.csv` - Dados coletados
- `monitoramento_YYYYMMDD_HHMMSS.log` - Log do monitoramento

### 📋 **Logs do Sistema**
- `diagnostico_YYYYMMDD_HHMMSS.log` - Log do diagnóstico

## 🔍 Troubleshooting

### ❌ **Problemas Comuns**

#### "Dependências não instaladas"
**Solução**: Execute o comando de instalação completo:
```bash
pip install psutil GPUtil py-cpuinfo tabulate rich matplotlib wmi
```

#### "Informações limitadas/sensores não acessíveis"
**Solução**: 
1. Execute como Administrador
2. Verifique se os drivers estão atualizados
3. Alguns sensores podem não estar disponíveis em VMs

#### "GPU não detectada"
**Possíveis Causas**:
- GPU integrada (Intel/AMD APU)
- Drivers não instalados
- GPU muito antiga

#### "Temperaturas não disponíveis"
**Soluções**:
- Execute como Administrador
- Instale drivers do chipset da placa-mãe
- Alguns sistemas podem não expor sensores

### 🛠️ **Diagnóstico de Problemas**

1. **Verifique as dependências**:
```bash
python -c "import psutil, GPUtil, cpuinfo; print('OK')"
```

2. **Teste permissões**:
   - Execute como Administrador
   - Verifique UAC do Windows

3. **Logs de erro**:
   - Verifique os arquivos .log gerados
   - Analise mensagens de erro na interface

## 🔒 Segurança e Privacidade

- **Dados Locais**: Todas as informações ficam no seu computador
- **Sem Conexão**: Não envia dados para servidores externos
- **Código Aberto**: Pode ser auditado e modificado
- **Logs Locais**: Histórico salvo apenas localmente

## 🆘 Suporte e Limitações

### ✅ **Funciona Bem Com:**
- Windows 10/11 (todas as versões)
- Placas NVIDIA e AMD modernas
- Processadores Intel e AMD
- SSDs e HDDs com suporte S.M.A.R.T.

### ⚠️ **Limitações Conhecidas:**
- Alguns sensores podem não estar disponíveis em máquinas virtuais
- GPUs muito antigas podem não ser detectadas
- Temperaturas dependem dos drivers instalados
- Privilégios limitados podem reduzir informações disponíveis

### 📧 **Obtendo Ajuda**
1. Verifique se todas as dependências estão instaladas
2. Execute como Administrador
3. Consulte os logs gerados para detalhes de erros
4. Verifique se os drivers estão atualizados

## 🔄 Atualizações e Melhorias

### Versão Atual: **1.0**

#### 🆕 **Recursos Implementados:**
- ✅ Diagnóstico completo de hardware
- ✅ Monitoramento em tempo real (30 min máximo)
- ✅ Sistema de alertas inteligente
- ✅ Interface gráfica avançada
- ✅ Relatórios TXT e HTML
- ✅ Exportação CSV
- ✅ Sistema de recomendações
- ✅ Logs históricos

#### 🔮 **Melhorias Futuras Possíveis:**
- 🔄 Agendamento automático de diagnósticos
- 📱 Notificações do sistema
- 🌐 Interface web opcional
- 📊 Mais tipos de gráficos
- 🎯 Benchmarks integrados
- 📦 Versão executável (.exe)

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🙏 Créditos

Desenvolvido com as seguintes bibliotecas Python:
- **psutil** - Informações do sistema
- **GPUtil** - Informações da GPU
- **py-cpuinfo** - Detalhes do processador
- **wmi** - Interface WMI do Windows
- **matplotlib** - Gráficos
- **tkinter** - Interface gráfica
- **rich** - Formatação colorida

---

**Sistema de Diagnóstico de PC v1.0** - Seu consultor de hardware profissional! 🔧✨
