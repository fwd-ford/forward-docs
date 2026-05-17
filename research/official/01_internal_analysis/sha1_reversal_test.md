# Teste de reversao SHA1 do VIN_Hash

## Objetivo
Confirmar se o `VIN_Hash` (SHA1) usa salt ou e SHA1 puro do VIN.
Se for puro, e teoricamente reversivel por rainbow table (VIN tem estrutura fixa de 17 chars).

## Metodo
- Amostra: 50 hashes do dataset
- Espaco testado: prefixes Ford BR (9BF, 8AF, 9BB) + 6 chars de VDS aleatorio + 8 chars placeholder
- Limite: 5,000,000 tentativas

## Resultado
- Tentativas executadas: 5,000,000
- Hashes encontrados (SHA1 puro): **0**

**Nenhum match** com ate 5,000,000 tentativas.

Interpretacao:
- E provavel que tenha salt (ou seja outro algoritmo).
- MAS espaco real do VIN e ~17^32 (excluindo IOQ), inviavel exaustivamente.
- Recomendacao: se assumir 'sem salt' como pior caso, e tratar como pseudonimizado (LGPD).