import os
import json

def create_categories():
    print("Creating category map...")
    
    final_categories = [
        {
            "name": "Primeiros passos",
            "parent": None
        },
        {
            "name": "Funcionalidades",
            "parent": None
        },
        {
            "name": "Clientes",
            "parent": "Funcionalidades"
        },
        {
            "name": "Fornecedores",
            "parent": "Funcionalidades"
        },
        {
            "name": "Transportadoras",
            "parent": "Funcionalidades"
        },
        {
            "name": "Produtos e Serviços",
            "parent": "Funcionalidades"
        },
        {
            "name": "Gestão de validade",
            "parent": "Produtos e Serviços"
        },
        {
            "name": "Estoque",
            "parent": "Funcionalidades"
        },
        {
            "name": "Registros (IMEI, Série)",
            "parent": "Estoque"
        },
        {
            "name": "Etiquetas",
            "parent": "Funcionalidades"
        },
        {
            "name": "Compras",
            "parent": "Funcionalidades"
        },
        {
            "name": "Cotação",
            "parent": "Funcionalidades"
        },
        {
            "name": "Ordem de Serviço",
            "parent": "Funcionalidades"
        },
        {
            "name": "Orçamento",
            "parent": "Funcionalidades"
        },
        {
            "name": "Pedidos",
            "parent": "Funcionalidades"
        },
        {
            "name": "Condicional",
            "parent": "Funcionalidades"
        },
        {
            "name": "Devolução",
            "parent": "Funcionalidades"
        },
        {
            "name": "Comissão",
            "parent": "Funcionalidades"
        },
        {
            "name": "Bonificação",
            "parent": "Funcionalidades"
        },
        {
            "name": "Financeiro",
            "parent": "Funcionalidades"
        },
        {
            "name": "Notificações",
            "parent": "Funcionalidades"
        },
        {
            "name": "Pré venda",
            "parent": "Funcionalidades"
        },
        {
            "name": "Entrega",
            "parent": "Funcionalidades"
        },
        {
            "name": "Delivery Sigecom",
            "parent": "Funcionalidades"
        },
        {
            "name": "Boletos",
            "parent": "Funcionalidades"
        },
        {
            "name": "Solicitação de compra",
            "parent": "Funcionalidades"
        },
        {
            "name": "Controle de promoções",
            "parent": "Funcionalidades"
        },
        {
            "name": "Kit de produtos",
            "parent": "Funcionalidades"
        },
        {
            "name": "Fiscal",
            "parent": None
        },
        {
            "name": "NF-e",
            "parent": "Fiscal"
        },
        {
            "name": "SAT",
            "parent": "Fiscal"
        },
        {
            "name": "NFS-e",
            "parent": "Fiscal"
        },
        {
            "name": "NFC-e",
            "parent": "Fiscal"
        },
        {
            "name": "Relatórios",
            "parent": None
        },
        {
            "name": "Vendas",
            "parent": "Relatórios"
        },
        {
            "name": "Ordem de serviço",
            "parent": "Relatórios"
        },
        {
            "name": "Orçamentos",
            "parent": "Relatórios"
        },
        {
            "name": "Compras",
            "parent": "Relatórios"
        },
        {
            "name": "Estoque",
            "parent": "Relatórios"
        },
        {
            "name": "Balança",
            "parent": "Relatórios"
        },
        {
            "name": "Devoluções",
            "parent": "Relatórios"
        },
        {
            "name": "Bonificação",
            "parent": "Relatórios"
        },
        {
            "name": "Financeiro",
            "parent": "Relatórios"
        },
        {
            "name": "Fiscal",
            "parent": "Relatórios"
        },
        {
            "name": "Migrações",
            "parent": None
        },
        {
            "name": "Integrações",
            "parent": None
        },
        {
            "name": "Buscadores de preços",
            "parent": "Integrações"
        },
        {
            "name": "Apps",
            "parent": None
        },
        {
            "name": "SigeDash",
            "parent": "Apps"
        },
        {
            "name": "Indicadores",
            "parent": None
        },
        {
            "name": "PDVgo",
            "parent": None
        }
    ]

    with open('categories.json', 'w', encoding='utf-8') as f:
        json.dump(final_categories, f, ensure_ascii=False, indent=4)
        
    print(f"Category map recreated successfully with {len(final_categories)} categories.")

if __name__ == "__main__":
    create_categories()