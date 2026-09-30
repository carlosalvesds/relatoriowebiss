# Relatório NFS-e

Aplicação Streamlit para importar arquivos XML ou ZIP de NFS-e, visualizar totais e exportar os dados para Excel.

## Executar localmente

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Publicar no Streamlit Community Cloud

Siga o passo a passo em [PUBLICAR.md](PUBLICAR.md). Selecione Python 3.12 nas configurações avançadas do deploy.

Envie `app.py`, `analise_xml.py`, `tema.py`, `portal.css`, as pastas `kit-visual-diroma` e `.streamlit`, `requirements.txt`, `.gitignore` e este README ao GitHub. No Streamlit Community Cloud, crie o app apontando para o repositório, branch principal e arquivo `app.py`.

## Análise XML e painel de tributos

O botão no canto superior direito indica o tema de destino: **🌙 Modo escuro** ou **☀️ Modo claro**. A aplicação inicia no claro e mantém a preferência durante a sessão, preservando o lote e o Excel preparado. A logo conserva o fundo branco e as cores originais. `tema.py` aplica os tokens semânticos de `kit-visual-diroma/tema/tokens.json`; `portal.css` concentra os estilos dos componentes, foco de teclado e layout responsivo. Abaixo de 700px, os cards ocupam no máximo duas colunas e as tabelas mantêm rolagem horizontal.

O botão **Baixar planilha Excel (.xlsx)** fica logo após o resumo dos valores e antes da tabela das notas. Na primeira importação, aparece uma indicação de preparação. O arquivo pronto é reutilizado na sessão ao alternar o tema e substituído quando outro XML/ZIP é carregado. A opção de impressão/PDF fica ao lado do botão de download, acima da tabela.

A exportação mantém a aba `Dados NFS-e` com as mesmas colunas e formatação. A segunda aba, `Tributos por NFS-e`, mostra somente Número NFS-e, Data de Emissão, CPF/CNPJ Tomador, IBS, CBS, PIS Próprio, COFINS Próprio, PIS Retido, COFINS Retido, ISS, IR e Alíquota ISS. A segunda aba contém todas as notas do lote, com cabeçalhos e dados centralizados. CPF/CNPJ são formatados nas duas abas, preservando os zeros iniciais. A estrutura completa do XML não é exportada. A aba usa valores monetários numéricos, datas nativas do Excel, números de nota como texto, filtros e cabeçalho congelado, seguindo as cores diRoma.

IBS usa o total informado ou, na ausência dele, a soma UF + município. Os valores genéricos de PIS/COFINS são apresentados como próprios quando o indicador informa não retenção, ou como retidos quando informa retenção. Valores explícitos de retenção têm preferência. Quando há um valor genérico não zero e falta a classificação, as duas colunas do tributo exibem `Não informado`, evitando presumir o destino do valor.

O painel exibe as contagens de notas por tributo. IBS e CBS contam a presença dos campos específicos, inclusive valores zero. PIS/COFINS retidos usam `tpRetPisCofins` ou valores explícitos de retenção positivos; a existência de `ValorPis` ou `ValorCofins` isoladamente não confirma retenção. Indicadores ausentes ou desconhecidos aparecem como `Não informado`. IRRF conta valores positivos de `ValorIr`, `ValorIRRF` ou `vRetIRRF`.

O domínio de `tpRetPisCofins` segue a [Nota Técnica 007 do CGNFS-e](https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica/rtc/nt-007-se-cgnfse-v1-0.pdf): PIS retido nos códigos 1, 3, 4, 5 e 9; COFINS retido nos códigos 1, 3, 4, 6 e 7. O leitor de notas continua direcionado ao XML ABRASF/WebISS com `InfNfse`. As contagens representam registros importados; arquivos repetidos não são deduplicados.

Para validar extração, indicadores e exportação: `python -m unittest test_analise -v`. O teste do lote local usa `../LoteXMLNotasFiscais.zip` quando disponível.

A alíquota ISS é lida de ValoresNfse/Aliquota, com alternativa em Servico/Valores/Aliquota. O resumo mostra as alíquotas distintas do lote e as duas abas do Excel apresentam o percentual por nota.
