import os
import webbrowser

html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Simulador Gêmeo Digital - Iris</title>
    <style>
        body {
            background-color: #0f172a;
            color: #f8fafc;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .header { text-align: center; margin-bottom: 20px; }
        .header h1 { color: #2dd4bf; margin: 0 0 5px 0; }
        
        .view-controls {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        .btn-view {
            background: #3b82f6;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.3s;
        }
        .btn-view:hover, .btn-view.active { background: #2dd4bf; }
        
        .main-container {
            display: flex;
            gap: 30px;
            width: 1000px;
            max-width: 100%;
        }

        .panel {
            background: #1e293b;
            padding: 25px;
            border-radius: 16px;
            border: 1px solid #334155;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .controls-panel { width: 350px; display: flex; flex-direction: column; gap: 20px; }
        
        .control-group { display: flex; flex-direction: column; gap: 8px; }
        .control-group label { font-weight: bold; color: #94a3b8; font-size: 14px; }
        .control-group span.val { color: #2dd4bf; float: right; font-weight: bold; }
        
        input[type=range] { width: 100%; cursor: pointer; accent-color: #3b82f6; }

        .viz-panel { flex-grow: 1; display: flex; flex-direction: column; gap: 20px; }
        
        #canvas-container {
            width: 100%;
            height: 350px;
            background: #0f172a;
            border-radius: 12px;
            border: 1px dashed #475569;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }

        .status-cards { display: flex; flex-direction: column; gap: 15px; }
        
        .card {
            padding: 15px 20px;
            border-radius: 8px;
            border-left: 5px solid #2dd4bf;
            background: #0f172a;
            font-size: 15px;
        }
        .card strong { color: #94a3b8; display: block; margin-bottom: 5px; font-size: 13px; text-transform: uppercase; }
        .card.card-acao { font-weight: bold; font-size: 16px; }

        .state-success { border-left-color: #2dd4bf; color: #2dd4bf; }
        .state-warning { border-left-color: #f59e0b; color: #f59e0b; }
        .state-error { border-left-color: #fb7185; color: #fb7185; }

    </style>
    <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>

    <div class="header">
        <h1>Simulador Interativo: Gêmeo Digital</h1>
        <p>Ajuste a telemetria ou visualize o agrupamento do algoritmo K-Means.</p>
    </div>

    <div class="view-controls">
        <button class="btn-view active" id="btn-indiv" onclick="setMode('individual')">Visão Individual (Micro)</button>
        <button class="btn-view" id="btn-cluster" onclick="setMode('cluster')">Visão de Clusters (Macro)</button>
    </div>

    <div class="main-container">
        <div class="panel controls-panel" id="painel-sliders">
            <h3 style="margin-top: 0; color: #f8fafc; border-bottom: 1px solid #334155; padding-bottom: 10px;">Parâmetros da Sessão</h3>
            
            <div class="control-group">
                <label>Sentimento do Usuário <span class="val" id="val-sentimento">0.2</span></label>
                <input type="range" id="sentimento" min="-1.0" max="1.0" step="0.1" value="0.2" oninput="updateLogic()">
            </div>
            
            <div class="control-group">
                <label>Volume de Mensagens Trocadas <span class="val" id="val-turnos">4</span></label>
                <input type="range" id="turnos" min="1" max="20" step="1" value="4" oninput="updateLogic()">
            </div>
            
            <div class="control-group">
                <label>Intenções Não Entendidas <span class="val" id="val-intencoes">0</span></label>
                <input type="range" id="intencoes" min="0" max="8" step="1" value="0" oninput="updateLogic()">
            </div>
            
            <div class="control-group">
                <label>Latência do Sistema (s) <span class="val" id="val-latencia">1.5</span></label>
                <input type="range" id="latencia" min="0.5" max="10.0" step="0.5" value="1.5" oninput="updateLogic()">
            </div>
        </div>

        <div class="panel viz-panel">
            <div id="canvas-container"></div>
            
            <div class="status-cards">
                <div style="display: flex; gap: 15px;">
                    <div class="card state-success" id="card-estado" style="flex: 1;">
                        <strong>Estado do Gêmeo Usuário</strong>
                        <span id="txt-estado">Saudável</span>
                    </div>
                    <div class="card state-success" id="card-persona" style="flex: 1;">
                        <strong>Persona Identificada</strong>
                        <span id="txt-persona">Usuário XPTO</span>
                    </div>
                </div>
                <div class="card card-acao state-success" id="card-acao">
                    <strong>Ação Proativa SNOW</strong>
                    <span id="txt-acao">Nenhuma Ação Necessária. Apenas Monitoramento.</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        const width = 580;
        const height = 350;
        const svg = d3.select("#canvas-container").append("svg")
            .attr("width", width)
            .attr("height", height);

        let mode = 'individual';
        
        let animRadius = 140;
        let animColor = "#2dd4bf";
        let animJitter = 20;
        let animText = "Sessão Fluida";

        function setMode(newMode) {
            mode = newMode;
            
            // Controle de UI dos botões
            document.getElementById('btn-indiv').classList.toggle('active', mode === 'individual');
            document.getElementById('btn-cluster').classList.toggle('active', mode === 'cluster');
            
            // Oculta/Mostra sliders e cards dependendo do modo
            document.getElementById('painel-sliders').style.opacity = mode === 'individual' ? '1' : '0.3';
            document.getElementById('painel-sliders').style.pointerEvents = mode === 'individual' ? 'auto' : 'none';
            
            if (mode === 'cluster') {
                document.getElementById('txt-estado').innerText = "Visão Global";
                document.getElementById('txt-persona').innerText = "Múltiplos Clusters";
                document.getElementById('txt-acao').innerText = "Monitoramento Sistêmico de Infraestrutura e UX.";
                ['card-estado', 'card-persona', 'card-acao'].forEach(id => {
                    const el = document.getElementById(id);
                    el.className = 'card state-success';
                });
            } else {
                updateLogic();
            }
            draw();
        }

        function updateLogic() {
            if (mode !== 'individual') return;

            const sentimento = parseFloat(document.getElementById('sentimento').value);
            const turnos = parseInt(document.getElementById('turnos').value);
            const intencoes = parseInt(document.getElementById('intencoes').value);
            const latencia = parseFloat(document.getElementById('latencia').value);

            document.getElementById('val-sentimento').innerText = sentimento.toFixed(1);
            document.getElementById('val-turnos').innerText = turnos;
            document.getElementById('val-intencoes').innerText = intencoes;
            document.getElementById('val-latencia').innerText = latencia.toFixed(1) + "s";

            let estado = "Saudável";
            let persona = "Usuário XPTO";
            let acao = "Nenhuma Ação Necessária. Apenas Monitoramento.";
            let cssClass = "state-success";

            // Lógica de Fricção baseada em Turnos e Erros
            if (intencoes >= 2 || sentimento <= -0.5 || turnos >= 12) {
                estado = "Crítico (Fricção UX)";
                persona = "Frustrado / Fricção Completa";
                acao = "🚨 ACIONAR API: Criar Incidente P1 e Transferir p/ Humano";
                cssClass = "state-error";
                
                animRadius = 60;
                animColor = "#fb7185";
                animJitter = 45;
                animText = "Risco de Abandono!";
            } 
            else if (latencia >= 5.0) {
                estado = "Atenção (Infraestrutura)";
                persona = "Lentidão Sistêmica";
                acao = "⚠️ REGISTRAR ALERTA: Notificar time de Integração/Datadog";
                cssClass = "state-warning";
                
                animRadius = 100;
                animColor = "#f59e0b";
                animJitter = 15;
                animText = "Gargalo de Latência";
            } 
            else {
                estado = "Saudável";
                persona = "Usuário XPTO";
                acao = "Nenhuma Ação Necessária. Apenas Monitoramento.";
                cssClass = "state-success";
                
                animRadius = 140;
                animColor = "#2dd4bf";
                animJitter = 20;
                animText = "Sessão Fluida";
            }

            document.getElementById('txt-estado').innerText = estado;
            document.getElementById('txt-persona').innerText = persona;
            document.getElementById('txt-acao').innerText = acao;

            ['card-estado', 'card-persona', 'card-acao'].forEach(id => {
                const el = document.getElementById(id);
                el.className = 'card ' + cssClass;
                if(id === 'card-acao') el.classList.add('card-acao');
            });
        }

        function generatePolygonPoints(cx, cy, radius, jitter) {
            const points = [];
            const numPoints = 6; // Menos pontos cria arestas mais duras/visíveis
            for (let i = 0; i < numPoints; i++) {
                const angle = (i / numPoints) * Math.PI * 2;
                const r = radius + (Math.random() - 0.5) * jitter;
                points.push([ cx + Math.cos(angle) * r, cy + Math.sin(angle) * r ]);
            }
            return points;
        }

        function draw() {
            svg.selectAll("*").remove();
            
            if (mode === 'individual') {
                const cx = width / 2;
                const cy = height / 2;
                const points = generatePolygonPoints(cx, cy, animRadius, animJitter);
                
                // curveLinearClosed faz as linhas ficarem retas (criando o polígono)
                svg.append("path")
                    .attr("d", d3.line().curve(d3.curveLinearClosed)(points))
                    .attr("fill", animColor)
                    .attr("fill-opacity", 0.2)
                    .attr("stroke", animColor)
                    .attr("stroke-width", 3);

                svg.append("circle")
                    .attr("cx", cx)
                    .attr("cy", cy)
                    .attr("r", 6)
                    .attr("fill", "#fff");
                    
                svg.append("text")
                    .attr("x", cx)
                    .attr("y", cy - animRadius - 35)
                    .attr("text-anchor", "middle")
                    .attr("fill", "#94a3b8")
                    .attr("font-family", "sans-serif")
                    .text(animText);
            } else {
                // Modo Cluster
                const clusters = [
                    {x: width * 0.2, y: height * 0.45, color: "#2dd4bf", count: 7, label: "Cluster 0 (Fluido)"},
                    {x: width * 0.8, y: height * 0.45, color: "#fb7185", count: 5, label: "Cluster 1 (Crítico)"},
                    {x: width * 0.5, y: height * 0.65, color: "#f59e0b", count: 6, label: "Cluster 2 (Infra)"}
                ];

                clusters.forEach(c => {
                    for (let i = 0; i < c.count; i++) {
                        const offset_x = (Math.random() - 0.5) * 80;
                        const offset_y = (Math.random() - 0.5) * 80;
                        const points = generatePolygonPoints(c.x + offset_x, c.y + offset_y, 25, 10);
                        
                        svg.append("path")
                            .attr("d", d3.line().curve(d3.curveLinearClosed)(points))
                            .attr("fill", c.color)
                            .attr("fill-opacity", 0.3)
                            .attr("stroke", c.color)
                            .attr("stroke-width", 1);
                    }
                    
                    svg.append("text")
                        .attr("x", c.x)
                        .attr("y", c.y - 80)
                        .attr("text-anchor", "middle")
                        .attr("fill", c.color)
                        .attr("font-weight", "bold")
                        .text(c.label);
                });
            }
        }

        updateLogic();
        draw();
        setInterval(() => { draw(); }, 600);
    </script>
</body>
</html>
"""

file_name = "simulador_final.html"
with open(file_name, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"Interface gerada com sucesso! Abrindo {file_name}...")
webbrowser.open('file://' + os.path.realpath(file_name))