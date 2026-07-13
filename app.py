import streamlit as st

# Configuração da página otimizada para mobile
st.set_page_config(
    page_title="Preço Rápido Moda",
    page_icon="👕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS para emular um app nativo e criar o card de resultado
st.markdown("""
    <style>
    /* Ajustes gerais para mobile */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    
    /* Card de Resultados */
    .result-card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #e9ecef;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    
    /* Tema escuro do Streamlit (caso ativo) */
    @media (prefers-color-scheme: dark) {
        .result-card {
            background-color: #1e222b;
            border-color: #2d3139;
        }
    }
    
    .result-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-size: 14px;
    }
    
    .result-highlight {
        display: flex;
        justify-content: space-between;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 2px dashed #dee2e6;
        font-size: 18px;
        font-weight: bold;
        color: #2e7d32;
    }
    
    @media (prefers-color-scheme: dark) {
        .result-highlight {
            border-top-color: #2d3139;
            color: #4caf50;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("👕 Precificação Rápida")
st.caption("Moda Masculina • Versão Mobile")

# --- ENTRADA DE DADOS ---
# Custos de aquisição física + quantidade integrados no topo
st.subheader("Custos de Aquisição")
col1, col2 = st.columns(2)
with col1:
    custo_fornecedor = st.number_input("Fornecedor (R$)", min_value=0.0, value=45.00, step=1.0)
    qtd_estoque = st.number_input("Qtd de Peças", min_value=0, value=10, step=5)
with col2:
    custo_frete = st.number_input("Frete/Peça (R$)", min_value=0.0, value=3.50, step=0.5)

# Embalagem, custos operacionais e tributos
st.subheader("Taxas e Deduções")
col3, col4 = st.columns(2)
with col3:
    custo_embalagem = st.number_input("Embalagem (R$)", min_value=0.0, value=4.00, step=0.5)
    imposto = st.number_input("Imposto (%)", min_value=0.0, max_value=100.0, value=4.0, step=0.5) / 100
    margem_troca = st.number_input("Trocas (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.5) / 100
with col4:
    custo_fixo = st.number_input("Custo Fixo (R$)", min_value=0.0, value=14.33, step=1.0)
    taxa_cartao = st.number_input("Cartão (%)", min_value=0.0, max_value=100.0, value=7.99, step=0.1) / 100

st.subheader("Venda Praticada")
preco_praticado = st.number_input("Preço Final Alvo (R$)", min_value=0.1, value=119.90, step=5.0)


# --- CÁLCULOS INTERNOS ---
# 1. Custo Total Real por Peça
custo_total_real = custo_fornecedor + custo_frete + custo_embalagem + custo_fixo

# 2. Preço Mínimo Recomendado (Margem de Contribuição de 40%)
margem_padrao_desejada = 0.40
divisor = 1 - imposto - taxa_cartao - margem_troca - margem_padrao_desejada

if divisor > 0:
    preco_sugerido = custo_total_real / divisor
else:
    preco_sugerido = custo_total_real / 0.1

# 3. Lucro Líquido Real Unitário
soma_taxas_variaveis = imposto + taxa_cartao + margem_troca
lucro_liquido_real = preco_praticado - (preco_praticado * soma_taxas_variaveis) - custo_total_real

# 4. Margem de Lucro Real %
margem_lucro_real_pct = (lucro_liquido_real / preco_praticado) * 100 if preco_praticado > 0 else 0

# 5. Markup Aplicado
markup_aplicado = preco_praticado / custo_total_real if custo_total_real > 0 else 0

# 6. NOVO: Cálculos de Estoque Alterados conforme solicitação
capital_investido_fornecedor = custo_fornecedor * qtd_estoque
# Nova regra matemática: (Fornecedor + Frete) * Quantidade
custo_total_lote = (custo_fornecedor + custo_frete) * qtd_estoque
faturamento_potencial = preco_praticado * qtd_estoque
lucro_total_lote = lucro_liquido_real * qtd_estoque


# --- EXIBIÇÃO DOS RESULTADOS ---
st.subheader("Análise Financeira")

# Card Customizado HTML/CSS
st.markdown(f"""
    <div class="result-card">
        <div class="result-row">
            <span><strong>Custo Unitário Real:</strong></span>
            <span>R$ {custo_total_real:.2f}</span>
        </div>
        <div class="result-row">
            <span><strong>Preço Sugerido (40% liq):</strong></span>
            <span>R$ {preco_sugerido:.2f}</span>
        </div>
        <div class="result-row">
            <span><strong>Markup Praticado:</strong></span>
            <span>{markup_aplicado:.2f}x</span>
        </div>
        <div class="result-row">
            <span><strong>Margem Lucro Real:</strong></span>
            <span>{margem_lucro_real_pct:.1f}%</span>
        </div>
        <div class="result-highlight">
            <span>LUCRO LÍQUIDO REAL/PEÇA:</span>
            <span>R$ {lucro_liquido_real:.2f}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Alertas de Markup
if markup_aplicado < 2.0:
    st.warning(f"⚠️ **Atenção:** Markup de {markup_aplicado:.2f}x está abaixo de 2.0x. Margem perigosa para o varejo de moda.")
else:
    st.success(f"✅ **Saudável:** Markup de {markup_aplicado:.2f}x está excelente para o varejo.")

# --- CARD VISUAL DO LOTE (Métricas de Estoque) ---
if qtd_estoque > 0:
    st.subheader("📊 Projeção do Lote Inteiro")
    
    col_est1, col_est2 = st.columns(2)
    with col_est1:
        st.metric(label="Investimento Fornecedor", value=f"R$ {capital_investido_fornecedor:.2f}")
        st.metric(label="Custo Direto do Lote", value=f"R$ {custo_total_lote:.2f}")
    with col_est2:
        st.metric(label="Faturamento Total", value=f"R$ {faturamento_potencial:.2f}")
        st.metric(label="Lucro Líquido do Lote", value=f"R$ {lucro_total_lote:.2f}", delta=f"{margem_lucro_real_pct:.1f}% Margem")
