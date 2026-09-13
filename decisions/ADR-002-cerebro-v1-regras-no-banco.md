# ADR-002: cérebro v1 em regras no banco, ML depois só no termômetro

- **Status:** aceita
- **Data:** 13/09/2026
- **Decisores:** Jota

## Contexto

O produto depende de três saídas por veículo: etiqueta, termômetro de 0 a 100 e ação sugerida. O forward-ml tem K-means (quatro personas) e um classificador de churn V3. Esse classificador tem três problemas:

- vazamento de rótulo provável (`tenure_days` e `years_since_sale` quase reconstroem o alvo);
- nenhum artefato versionado, e o código exige CUDA;
- desempenho ruim em veículos vendidos há menos de 12 meses.

## Decisão

- As três camadas nascem como **regras numeradas em SQL** (ETQ, TRM, REC), rodando de madrugada pelo pg_cron, com motivos explicáveis gravados em cada decisão.
- As etiquetas são as quatro personas do K-means (fiel, econômico, esquecido, abandono) mais **novo**, reescritas como regra com limiares tirados das médias dos clusters.
- O termômetro soma componentes com base em fatos da Ford:
  - intervalo de 10.000 km ou 12 meses;
  - Curva da Morte;
  - troca de concessionária;
  - garantia;
  - modelo descontinuado;
  - recall;
  - engajamento.
- O ML entra depois **só no termômetro**, pelo contrato TRM-L: leitura com `engine = model`, primeiro em modo sombra e comparada pela APR, sem mudar app nem tabelas.

## Consequências

- A consultora vê o porquê de cada número ("12 meses sem revisão").
- Cada regra tem teste pgTAP e mutação. O cenário do João tem números-ouro: 78, 73, 71, 51, 22.
- A distribuição das etiquetas por regra difere da do K-means (Abandono 40,5% contra 11,5%). O pitch não chama a etiqueta de "rótulo do ML".
- O forward-ml ganha uma trilha clara: termômetro por modelo sem vazamento, avaliado em sombra.

## Alternativas consideradas

| Alternativa | Por que não |
| --- | --- |
| Usar o V3 já | herda o vazamento, não explica o porquê, exige retreino com CUDA |
| Híbrido (etiqueta pelo K-means, resto por regra) | amarra a etiqueta a um artefato que não está versionado |
