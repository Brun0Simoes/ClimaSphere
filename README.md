# ClimaSphere — Observatório Climático Global

Painel climático 3D interativo: globo com camadas de satélite, chuva e temperatura,
avisos em tempo real, previsão com GPS, rede de estações de observação e portal de
serviços. Front-end 100% estático (React via CDN + Three.js + D3), hospedado no
GitHub Pages, com dados dinâmicos de duas formas:

1. **Fontes públicas ao vivo, direto no navegador** — NASA GIBS (satélite, chuva,
   temperatura), Open-Meteo (previsão com GPS, busca de cidades, datas), GDACS e
   USGS (ocorrências), atualizadas automaticamente.
2. **Backend ClimWeb (opcional)** — previsões oficiais, alertas CAP, estações
   OSCAR/WMO, rasters do GeoManager e as páginas do portal.

## Acesso

- **Site**: https://brun0simoes.github.io/ClimaSphere/
- Sem backend: o painel roda em *modo autônomo* com as fontes públicas ao vivo e o
  snapshot de estações do repositório (atualizado diariamente por GitHub Actions).

## Conectando o backend (ClimWeb local)

O painel procura o backend nesta ordem:

1. Parâmetro na URL: `?api=http://localhost:8000`
2. Variável global: `window.CLIMASPHERE_API_BASE`
3. Padrão quando servido de `*.github.io`: `http://localhost:8000`

Ou seja: com o ClimWeb rodando localmente (`docker compose up`), basta abrir o site
do GitHub Pages no mesmo computador — o navegador conversa com `http://localhost:8000`
(o CORS do ClimWeb já permite, e navegadores tratam `localhost` como origem segura
mesmo em página HTTPS). Para expor o backend a outras pessoas, use um túnel
(ex.: `cloudflared tunnel --url http://localhost:8000`) e abra
`https://brun0simoes.github.io/ClimaSphere/?api=https://SEU-TUNEL`.

## Estrutura

| Caminho | Descrição |
|---|---|
| `index.html` | O painel (template + lógica) |
| `support.js` | Runtime do painel (carrega React de CDN) |
| `uploads/` | Imagens |
| `data/stations.json` | Snapshot real de estações (NOAA ISD), renovado todo dia às 03:00 UTC |
| `scripts/build_stations.py` | Gerador do snapshot |
| `.github/workflows/pages.yml` | Publica o site no GitHub Pages a cada push |
| `.github/workflows/refresh-stations.yml` | Atualiza `data/stations.json` diariamente |

## Fontes de dados

NASA GIBS · Open-Meteo (GFS/ECMWF) · GDACS · USGS · NOAA ISD · Natural Earth ·
ClimWeb/WMO (backend opcional: ForecastManager, CAP, GeoManager, OSCAR, WDQMS).
