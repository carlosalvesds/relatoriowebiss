"""Tributos por NFS-e e indicadores, sem alterar as colunas do relatório principal."""
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from datetime import datetime

COLUNAS_TRIBUTOS = ["Número NFS-e", "Data de Emissão", "CPF/CNPJ Tomador", "IBS", "CBS", "PIS Próprio",
                   "COFINS Próprio", "PIS Retido", "COFINS Retido", "ISS", "IR", "Alíquota ISS"]


def aliquota_iss_nfse(nfse):
    """Lê a alíquota ABRASF em pontos percentuais e retorna fração para Excel."""
    for caminho in (".//{*}ValoresNfse/{*}Aliquota", ".//{*}Servico/{*}Valores/{*}Aliquota"):
        no = nfse.find(caminho)
        if no is not None and no.text:
            try:
                valor = Decimal(no.text.strip().replace(",", "."))
                if valor.is_finite():
                    return float(valor / 100)
            except InvalidOperation:
                pass
    return None


def tributos_nfse(nfse, indicadores):
    """Valores por nota; não presume retenção quando o indicador está ausente."""
    campos = defaultdict(list)
    for no in nfse.iter():
        campos[nome_local(no.tag)].append((no.text or "").strip())

    def valor(*tags):
        for tag in tags:
            for texto in campos[tag]:
                try:
                    numero = Decimal(texto.replace(",", "."))
                    if numero.is_finite():
                        return float(numero)
                except InvalidOperation:
                    pass
        return None

    def separar(status, generico, retido):
        if retido is not None:
            return (0.0 if status == "Sim" else generico), retido
        if generico in (None, 0):
            return 0.0, 0.0
        if status == "Sim":
            return 0.0, generico
        if status == "Não":
            return generico, 0.0
        return None, None

    pis, pis_retido = separar(indicadores["PIS retido"], valor("ValorPis", "vPis"), valor("ValorPisRetido", "vRetPis"))
    cofins, cofins_retido = separar(indicadores["COFINS retido"], valor("ValorCofins", "vCofins"), valor("ValorCofinsRetido", "vRetCofins"))
    ibs = valor("vIBSTot", "vIBS")
    if ibs is None:
        ibs = (valor("vIBSUF") or 0.0) + (valor("vIBSMun") or 0.0)
    data = next(iter(campos["DataEmissao"]), "")
    try:
        data = datetime.fromisoformat(data.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        data = None
    documento = "N/A"
    for tomador in nfse.iter():
        if nome_local(tomador.tag) == "IdentificacaoTomador":
            documentos = {nome_local(no.tag): (no.text or "").strip() for no in tomador.iter()}
            documento = documentos.get("Cpf") or documentos.get("Cnpj") or "N/A"
            break
    return dict(zip(COLUNAS_TRIBUTOS, [indicadores["Número NFS-e"], data, documento, ibs,
        valor("vCBS") or 0.0, pis, cofins, pis_retido, cofins_retido, valor("ValorIss") or 0.0,
        valor("ValorIr", "ValorIRRF", "vRetIRRF") or 0.0, aliquota_iss_nfse(nfse)]))

def nome_local(tag):
    return tag.rsplit("}", 1)[-1]


def indicadores_nfse(nfse, arquivo):
    campos = defaultdict(list)
    for no in nfse.iter():
        campos[nome_local(no.tag)].append((no.text or "").strip())

    def primeiro(*tags):
        return next((v for t in tags for v in campos[t] if v), "")

    def positivo(*tags):
        for tag in tags:
            for valor in campos[tag]:
                try:
                    if Decimal(valor.replace(",", ".")) > 0:
                        return True
                except InvalidOperation:
                    pass
        return False

    codigo = primeiro("tpRetPisCofins")

    def retencao(codigos, *tags):
        if positivo(*tags) or codigo in codigos:
            return "Sim"
        if codigo in set("0123456789"):
            return "Não"
        return "Não informado"

    return {
        "Arquivo": arquivo,
        "Número NFS-e": primeiro("Numero"),
        "ID NFS-e": nfse.get("Id", ""),
        "IBS": any(t in campos for t in ("pIBSUF", "pIBSMun", "vIBSUF", "vIBSMun", "vIBSTot", "vIBS")),
        "CBS": any(t in campos for t in ("pCBS", "vCBS")),
        "PIS informado": "ValorPis" in campos or "vPis" in campos,
        "COFINS informado": "ValorCofins" in campos or "vCofins" in campos,
        "PIS retido": retencao({"1", "3", "4", "5", "9"}, "ValorPisRetido", "vRetPis"),
        "COFINS retido": retencao({"1", "3", "4", "6", "7"}, "ValorCofinsRetido", "vRetCofins"),
        "IRRF": positivo("ValorIr", "ValorIRRF", "vRetIRRF"),
        "IRRF informado": any(t in campos for t in ("ValorIr", "ValorIRRF", "vRetIRRF")),
        "Indicador PIS/COFINS": codigo or "Não informado",
        "Valor PIS no XML": primeiro("ValorPis", "vPis"),
        "Valor COFINS no XML": primeiro("ValorCofins", "vCofins"),
        "Valor IRRF no XML": primeiro("ValorIr", "ValorIRRF", "vRetIRRF"),
    }
