import os
import django
import re
from bs4 import BeautifulSoup

# Configura o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from kb.models import Categoria, Artigo

ICON_MAP = {
    # Top-level
    "Primeiros passos": "fa-solid fa-shoe-prints",
    "Funcionalidades": "fa-solid fa-star",
    "Fiscal": "fa-solid fa-landmark",
    "Relatórios": "fa-solid fa-chart-bar",
    "Migrações": "fa-solid fa-right-left",
    "Integrações": "fa-solid fa-puzzle-piece",
    "Apps": "fa-solid fa-mobile-screen-button",
    "Indicadores": "fa-solid fa-gauge-high",
    "PDVgo": "fa-solid fa-cash-register",

    # Sub-categorias
    "Clientes": "fa-solid fa-users",
    "Fornecedores": "fa-solid fa-truck-fast",
    "Transportadoras": "fa-solid fa-truck",
    "Produtos e Serviços": "fa-solid fa-box-archive",
    "Estoque": "fa-solid fa-boxes-stacked",
    "Etiquetas": "fa-solid fa-tags",
    "Compras": "fa-solid fa-shopping-cart",
    "Cotação": "fa-solid fa-file-invoice-dollar",
    "Ordem de Serviço": "fa-solid fa-screwdriver-wrench",
    "Orçamento": "fa-solid fa-file-invoice",
    "Pedidos": "fa-solid fa-dolly",
    "Condicional": "fa-solid fa-retweet",
    "Devolução": "fa-solid fa-arrow-left",
    "Comissão": "fa-solid fa-percent",
    "Bonificação": "fa-solid fa-gift",
    "Financeiro": "fa-solid fa-dollar-sign",
    "Notificações": "fa-solid fa-bell",
    "Pré venda": "fa-solid fa-clipboard-list",
    "Entrega": "fa-solid fa-truck-ramp-box",
    "Delivery Sigecom": "fa-solid fa-motorcycle",
    "Boletos": "fa-solid fa-barcode",
    "Solicitação de compra": "fa-solid fa-file-signature",
    "Controle de promoções": "fa-solid fa-bullhorn",
    "Kit de produtos": "fa-solid fa-boxes-packing",
    "NF-e": "fa-solid fa-file-lines",
    "SAT": "fa-solid fa-satellite-dish",
    "NFS-e": "fa-solid fa-file-alt",
    "NFC-e": "fa-solid fa-receipt",
    "Vendas": "fa-solid fa-chart-line",
    "SigeDash": "fa-solid fa-tachometer-alt",
    "Gestão de validade": "fa-solid fa-calendar-times",
    "Registros (IMEI, Série)": "fa-solid fa-barcode",
}

DEFAULT_ICON = "fa-solid fa-folder"

def extract_order_and_name(text):
    match = re.match(r'^(\d+)\s*-\s*(.*)
