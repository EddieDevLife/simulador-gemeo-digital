# 🤖 Projeto Iris — Gêmeos Digitais para Chatbots Proativos

> A transformação do suporte técnico: saindo da análise reativa tradicional para a mitigação de fricção em tempo real através de Inteligência Artificial e Engenharia de Dados.

**[✨ Clique aqui para acessar o Simulador Interativo Online](https://eddiedevlife.github.io/simulador-gemeo-digital/)**


---

## 🚀 O Fascínio dos Gêmeos Digitais (Digital Twins)

Imagine um espelho dinâmico que não reflete apenas a imagem de um objeto, mas sim o seu comportamento, o seu ritmo e o seu estado interno a cada milissegundo. Isso é um **Gêmeo Digital**. 


Popularizado na engenharia aeroespacial e em fábricas inteligentes de alta tecnologia para monitorizar motores e turbinas, o conceito de Gémeo Digital evoluiu. No **Projeto Iris**, desafiámos os limites tradicionais desta tecnologia: em vez de replicar uma máquina física, criámos uma **réplica virtual viva do comportamento, da satisfação e da fricção do utilizador real** durante a sua jornada de atendimento.

### O Nosso Foco

1. **O Micro-Gêmeo (Camada Operacional / Tempo Real):** Cada sessão de conversação ativa possui o seu próprio gémeo virtual temporário. Se o gemeo detetar um desvio crítico na experiência, a IA intervém de imediato para salvar o atendimento.
2. **O Macro-Gêmeo (Camada Estratégica / Agrupamento):** Milhares de sessões individuais são consolidadas em grupos comportamentais (*Personas*), permitindo identificar falhas sistémicas de UX ou infraestrutura.

---

## 🛠️ Arquitetura Técnica & Fluxo de Dados

O ecossistema foi desenhado seguindo o paradigma de arquitetura orientada a eventos (*Event-Driven Architecture*), garantindo escalabilidade e total desacoplamento entre os microsserviços.



### 🏗️ Descrição do Fluxo
1. **Camada de Ingestão:** O chatbot (ServiceNow) dispara *Webhooks* a cada interação (`sys_cs_message`).
2. **Camada Cloud (AWS):** O **Amazon API Gateway** recebe os eventos e aciona funções **AWS Lambda** que persistem os dados no **Amazon S3** (Data Lake).
3. **Motor Preditivo (Cérebro):** Desenvolvido em **Python** (Deepnote/Databricks), o motor processa o texto e executa o algoritmo **K-Means (Scikit-Learn)**.
4. **Ação Proativa:** O modelo envia chamadas de volta para a **Table API do ServiceNow**, gerando incidentes automáticos ou alertas de monitorização.

---

## 📊 Insights Extraídos pelo Modelo (K-Means)

O algoritmo agrupou com precisão três estados operacionais distintos com base nos padrões matemáticos das mensagens. Esta visualização representa o "espaço de estado" monitorizado pelo Macro-Gêmeo:



| Cluster | Volume de Mensagens | Erros de Compreensão | Latência Média | Status Operacional | Ação do Gmeo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cluster 0** | Baixa (~10) | Próximo a 0 | ~12 segundos | 🟢 Saudável | Apenas Monitorização Passiva |
| **Cluster 1** | Alta (~13) | Elevada (1.38) | ~122 segundos | 🔴 Crítico (UX) | Abertura de Incidente P1 + Transbordo Humano |
| **Cluster 2** | Alta (~12.8) | Zero (0.00) | ~121 segundos | 🟡 Atenção (Infra) | Alerta Proativo para Equipa de Performance |

---

## 💻 Como Executar o Simulador Localmente

Este repositório inclui um protótipo visual interativo desenvolvido em Python para demonstrar a reação do polígono de estado (Casco Convexo) do Gémeo Digital conforme os parâmetros são manipulados.

### Pré-requisitos
```bash
pip install streamlit d3js
