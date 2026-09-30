# Publicação no GitHub e Streamlit

1. Extraia o ZIP e envie todo o conteúdo para a raiz do repositório GitHub, preservando as subpastas. Não envie o ZIP como código da aplicação.
2. Confira especialmente `.streamlit/config.toml`, a logo e `tokens.json` nas pastas indicadas abaixo.
3. No Streamlit Community Cloud, clique em Create app e selecione o repositório e a branch em que enviou os arquivos (normalmente `main`).
4. Main file path: `app.py`.
5. Em Advanced settings, selecione Python `3.12` e salve. Não são necessários secrets.
6. Clique em Deploy.

Se a aplicação já existe, atualize os arquivos na branch configurada. Caso ainda apresente a versão antiga, use Reboot app.

## Conteúdo exato do pacote

- `app.py`
- `analise_xml.py`
- `tema.py`
- `portal.css`
- `requirements.txt`
- `.gitignore`
- `.streamlit/config.toml`
- `kit-visual-diroma/assets/diroma-logo.png`
- `kit-visual-diroma/tema/tokens.json`
- `README.md`
- `PUBLICAR.md`
- `test_analise.py`

## Conferência após publicar

Importe um XML/ZIP. Confira razão social e CNPJ, resumo com Alíquota ISS, botões de download e impressão lado a lado e as duas abas do Excel. A aba Tributos por NFS-e contém CPF/CNPJ com máscara, alíquota percentual e dados centralizados.

O pacote não contém notas fiscais, logs, caches, ambiente Python ou credenciais. Os XMLs são carregados pela interface.

## Execução local

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Testes: `python -m unittest test_analise -v`. O teste do lote real é ignorado quando o ZIP fiscal não está disponível.

Documentação: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
