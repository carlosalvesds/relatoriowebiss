"""Tema diRoma por sessão, com tokens compartilhados e estilos do portal."""
import json
from pathlib import Path

import streamlit as st


def alternar_tema():
    st.session_state.aparencia = "Escuro" if st.session_state.aparencia == "Claro" else "Claro"


def aplicar_tema():
    st.session_state.setdefault("aparencia", "Claro")
    escuro = st.session_state.aparencia == "Escuro"
    with st.container(key="alternador-tema"):
        st.button("☀️ Modo claro" if escuro else "🌙 Modo escuro",
                  key="alternar_tema", on_click=alternar_tema,
                  help="Alterar a aparência sem perder o lote carregado")
    raiz = Path(__file__).parent
    tokens = json.loads((raiz / "kit-visual-diroma/tema/tokens.json").read_text(encoding="utf-8-sig"))
    paleta = tokens["dark" if escuro else "light"]
    variaveis = {**paleta, **tokens["shared"],
        "portal-header-bg": "transparent" if escuro else paleta["portal-surface"],
        "portal-header-radius": "0" if escuro else "10px",
        "portal-header-border": "0" if escuro else "1px solid " + paleta["portal-field-border"],
        "portal-header-left": "0" if escuro else "5px solid " + paleta["portal-button"],
        "portal-header-bottom": "2px solid " + paleta["portal-border"] if escuro else "3px solid " + paleta["portal-secondary"],
        "portal-header-padding": "0 0 18px" if escuro else "18px",
        "portal-group-bg": "transparent" if escuro else paleta["portal-soft"],
        "portal-group-radius": "0" if escuro else "5px",
        "portal-active-bg": paleta["portal-surface"] if escuro else paleta["portal-button"],
        "portal-active-text": paleta["portal-secondary"] if escuro else "#ffffff",
        "portal-active-line": "none" if escuro else "inset 0 -3px " + paleta["portal-secondary"],
        "portal-scheme": "dark" if escuro else "light",
    }
    definicoes = ";".join(f"--{nome}:{valor}" for nome, valor in variaveis.items())
    css = (raiz / "portal.css").read_text(encoding="utf-8")
    st.markdown(f"<style>:root{{{definicoes}}}\n{css}</style>", unsafe_allow_html=True)
    return paleta
