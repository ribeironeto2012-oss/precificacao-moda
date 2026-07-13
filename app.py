# ... (Mantenha os cálculos anteriores iguais) ...

# 5. Markup Aplicado
markup_aplicado = preco_praticado / custo_total_real if custo_total_real > 0 else 0

# --- NOVO: GERENCIAMENTO DE ESTOQUE ---
st.subheader("📦 Estoque do Lote")
qtd_estoque = st.number_input("Qtd de Peças", min_value=0, value=10, step=5)

# Cálculos do Estoque
capital_investido_fornecedor = custo_fornecedor * qtd_estoque
custo_total_lote = custo_total_real * qtd_estoque
faturamento_potencial = preco_praticado * qtd_estoque
lucro_total_lote = lucro_liquido_real * qtd_estoque

# --- EXIBIÇÃO DOS RESULTADOS ---
st.subheader("Análise Financeira")

# Card Customizado HTML/CSS (Atualizado com dados de estoque)
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
            <span>LUCRO LÍQUIDO REA/PEÇA:</span>
            <span>R$ {lucro_liquido_real:.2f}</span>
        </div>
    </div>
""", unsafe_with_html=True)

# Alertas de Markup
if markup_aplicado < 2.0:
    st.warning(f"⚠️ **Atenção:** Markup de {markup_aplicado:.2f}x está abaixo de 2.0x. Margem perigosa para o varejo de moda.")
else:
    st.success(f"✅ **Saudável:** Markup de {markup_aplicado:.2f}x está excelente para o varejo.")

# --- NOVO: CARD VISUAL DO LOTE (Métricas de Estoque) ---
if qtd_estoque > 0:
    st.subheader("📊 Projeção do Lote Inteiro")
    
    col_est1, col_est2 = st.columns(2)
    with col_est1:
        st.metric(label="Investimento no Fornecedor", value=f"R$ {capital_investido_fornecedor:.2f}")
        st.metric(label="Custo Total do Lote", value=f"R$ {custo_total_lote:.2f}")
    with col_est2:
        st.metric(label="Faturamento Total", value=f"R$ {faturamento_potencial:.2f}")
        st.metric(label="Lucro Líquido do Lote", value=f"R$ {lucro_total_lote:.2f}", delta=f"{margem_lucro_real_pct:.1f}% Margem")
