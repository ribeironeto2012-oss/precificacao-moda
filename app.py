import streamlit as st
import math

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
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    
    /* Card de Resultados */
    .result-card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 14px;
        border: 1px solid #e9ecef;
        margin-top: 10px;
        margin-bottom: 10px;
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
        margin-bottom: 6px;
        font-size: 13px;
    }
    
    .result-highlight {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 2px dashed #dee2e6;
        font-size: 16px;
        font-weight: bold;
        color: #2e7d32;
    }
    
    @media (prefers-color-scheme: dark) {
        .result-highlight {
            border-top-color: #2d3139;
            color: #4caf50;
        }
    }
    
    /* Ajuste fino de margem entre os inputs para telas pequenas */
    div[data-testid="column"] {
        padding-left: 4px !important;
        padding-right: 4px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("👕 Precificação Rápida")

# --- ENTRADA DE DADOS ---

# 1. Custos de Aquisição (3 colunas lado a lado)
st.subheader("Custos de Aquisição")
col_aq1, col_aq2, col_aq3 = st.columns(3)
with col_aq1:
    custo_fornecedor = st.number_input("Fornecedor", min_value=0.0, value=45.00, step=1.0)
with col_aq2:
    custo_frete = st.number_input("Frete/Peça", min_value=0.0, value=3.50, step=0.5)
with col_aq3:
    qtd_estoque = st.number_input("Qtd Lote", min_value=1, value=10, step=5)

# 2. Taxas e Deduções (Grid ultra compacto 3x2)
st.subheader("Taxas e Deduções")
col_tx1, col_tx2, col_tx3 = st.columns(3)
with col_tx1:
    custo_embalagem = st.number_input("Embalagem", min_value=0.0, value=4.00, step=0.5)
    imposto = st.number_input("Imposto %", min_value=0.0, max_value=100.0, value=4.0, step=0.5) / 100
with col_tx2:
    custo_fixo = st.number_input("Custo Fixo", min_value=0.0, value=14.33, step=1.0)
    margem_troca = st.number_input("Trocas %", min_value=0.0, max_value=100.0, value=2.0, step=0.5) / 100
with col_tx3:
    taxa_cartao = st.number_input("Cartão %", min_value=0.0, max_value=100.0, value=7.99, step=0.1) / 100

# 3. Venda e Desconto (2 colunas lado a lado)
st.subheader("Venda Praticada")
col_vd1, col_vd2 = st.columns(2)
with col_vd1:
    preco_praticado = st.number_input("Preço Alvo", min_value=0.1, value=119.90, step=5.0)
with col_vd2:
    desconto_pct = st.number_input("Desconto %", min_value=0.0, max_value=100.0, value=0.0, step=1.0)


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

# 6. Estoque & Lote
capital_investido_fornecedor = custo_fornecedor * qtd_estoque
custo_total_lote = (custo_fornecedor + custo_frete) * qtd_estoque
faturamento_potencial = preco_praticado * qtd_estoque
lucro_total_lote = lucro_liquido_real * qtd_estoque

# 7. Cálculo de Ponto de Equilíbrio (Break-even)
receita_liquida_un = preco_praticado * (1 - soma_taxas_variaveis) - custo_embalagem
if receita_liquida_un > 0:
    pecas_break_even = math.ceil(custo_total_lote / receita_liquida_un)
else:
    pecas_break_even = 0

# 8. Cálculos do Simulador de Desconto
preco_com_desconto = preco_praticado * (1 - desconto_pct / 100)
lucro_liquido_desconto = preco_com_desconto - (preco_com_desconto * soma_taxas_variaveis) - custo_total_real
margem_lucro_desconto_pct = (lucro_liquido_desconto / preco_com_desconto) * 100 if preco_com_desconto > 0 else 0


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
            <span>LUCRO LÍQUIDO/PEÇA:</span>
            <span>R$ {lucro_liquido_real:.2f}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Alertas de Markup / Desconto
if desconto_pct > 0:
    st.subheader("💸 Impacto do Desconto")
    col_desc1, col_desc2 = st.columns(2)
    with col_desc1:
        st.metric(label="Novo Preço", value=f"R$ {preco_com_desconto:.2f}")
    with col_desc2:
        st.metric(label="Novo Lucro", value=f"R$ {lucro_liquido_desconto:.2f}", delta=f"{margem_lucro_desconto_pct:.1f}% Margem")

    if lucro_liquido_desconto < 0:
        st.error("🚨 **PREJUÍZO:** O desconto engoliu todo o seu lucro.")
    elif margem_lucro_desconto_pct < 10:
        st.warning("⚠️ **Atenção:** Margem muito baixa (menor que 10%).")
    else:
        st.success("✅ **Lucrativo:** Desconto dentro do limite seguro.")
else:
    if markup_aplicado < 2.0:
        st.warning(f"⚠️ **Atenção:** Markup de {markup_aplicado:.2f}x está abaixo de 2.0x.")
    else:
        st.success(f"✅ **Saudável:** Markup de {markup_aplicado:.2f}x excelente.")

# --- CARD VISUAL DO LOTE ---
if qtd_estoque > 0:
    st.subheader("📊 Projeção do Lote")
    
    col_est1, col_est2 = st.columns(2)
    with col_est1:
        st.metric(label="Custo Lote", value=f"R$ {custo_total_lote:.2f}")
        st.metric(label="Lucro Lote", value=f"R$ {lucro_total_lote:.2f}")
    with col_est2:
        st.metric(label="Faturamento", value=f"R$ {faturamento_potencial:.2f}")
        st.metric(label="Inves. Fornecedor", value=f"R$ {capital_investido_fornecedor:.2f}")

    # Painel de Ponto de Equilíbrio (Break-even)
    st.subheader("🎯 Ponto de Equilíbrio")
    if pecas_break_even > 0:
        if pecas_break_even <= qtd_estoque:
            st.info(
                f"Venda **{pecas_break_even} de {qtd_estoque} peças** para cobrir o custo (R$ {custo_total_lote:.2f}). "
                f"A partir da **{pecas_break_even + 1}ª**, o lucro é 100% livre!"
            )
        else:
            st.error(
                f"⚠️ **Atenção:** Necessário vender **{pecas_break_even} peças**, mas o lote só tem **{qtd_estoque}**. "
                f"Ajuste os valores para não fechar no prejuízo!"
            )
    else:
        st.error("⚠️ **Preço Inviável:** O valor praticado não cobre nem as taxas de venda.")
