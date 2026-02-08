import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Painelli Vendas - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para visual profissional e moderno
st.markdown("""
<style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Reset e base */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }

    /* Sidebar estilizada */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }

    [data-testid="stSidebar"] label {
        color: #94a3b8 !important;
    }

    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .sub-header {
        color: #64748b;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Cards de KPI */
    .kpi-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }

    .kpi-card {
        flex: 1;
        min-width: 180px;
        padding: 1.5rem;
        border-radius: 1rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        pointer-events: none;
    }

    .kpi-card.vendas {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    }

    .kpi-card.faturamento {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }

    .kpi-card.lucro {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    }

    .kpi-card.margem {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }

    .kpi-card.ticket {
        background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
    }

    .kpi-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.25rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }

    .kpi-label {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.85);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Esconder métricas padrão do Streamlit */
    [data-testid="stMetric"] {
        display: none;
    }

    /* Info box de filtros */
    .filter-info {
        background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 1rem;
        padding: 1rem 1.5rem;
        margin-bottom: 2rem;
        color: #e2e8f0;
        display: flex;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .filter-badge {
        background: rgba(59, 130, 246, 0.2);
        border: 1px solid #3b82f6;
        color: #60a5fa;
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .filter-badge.green {
        background: rgba(16, 185, 129, 0.2);
        border-color: #10b981;
        color: #34d399;
    }

    .filter-badge.purple {
        background: rgba(139, 92, 246, 0.2);
        border-color: #8b5cf6;
        color: #a78bfa;
    }

    /* Tabs customizadas */
    .stTabs [data-baseweb="tab-list"] {
        background: #1e293b;
        border-radius: 1rem;
        padding: 0.5rem;
        gap: 0.5rem;
        border: 1px solid #334155;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #94a3b8;
        border-radius: 0.75rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: #334155;
        color: #e2e8f0;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        color: white !important;
    }

    /* Títulos de seção */
    .section-title {
        color: #e2e8f0;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #334155;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .section-title-icon {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        padding: 0.5rem;
        border-radius: 0.5rem;
    }

    /* Cards de conteúdo */
    .content-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    /* Dataframes */
    .stDataFrame {
        background: #1e293b;
        border-radius: 1rem;
        border: 1px solid #334155;
    }

    [data-testid="stDataFrame"] {
        background: #1e293b;
    }

    /* Texto geral */
    .stMarkdown {
        color: #e2e8f0;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }

    p, li {
        color: #cbd5e1;
    }

    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
    }

    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 0.75rem 2rem;
        font-weight: 600;
    }

    /* Multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        background: #3b82f6;
        color: white;
    }

    /* Radio buttons */
    .stRadio > div {
        background: #1e293b;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }

    /* Insights cards */
    .insight-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #1e293b 100%);
        border: 1px solid #334155;
        border-radius: 1rem;
        padding: 1.25rem;
        text-align: center;
    }

    .insight-card.success {
        border-left: 4px solid #10b981;
    }

    .insight-card.warning {
        border-left: 4px solid #f59e0b;
    }

    .insight-card.info {
        border-left: 4px solid #3b82f6;
    }

    .insight-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #f1f5f9;
    }

    .insight-label {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 0.25rem;
    }

    /* Footer */
    .footer {
        background: #0f172a;
        border-top: 1px solid #334155;
        padding: 2rem;
        text-align: center;
        margin-top: 3rem;
        border-radius: 1rem 1rem 0 0;
    }

    .footer-text {
        color: #64748b;
        font-size: 0.9rem;
    }

    .footer-brand {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Ranking cards */
    .ranking-item {
        display: flex;
        align-items: center;
        padding: 0.75rem 1rem;
        background: #1e293b;
        border-radius: 0.75rem;
        margin-bottom: 0.5rem;
        border: 1px solid #334155;
    }

    .ranking-position {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin-right: 1rem;
    }

    .ranking-info {
        flex: 1;
    }

    .ranking-name {
        color: #f1f5f9;
        font-weight: 600;
    }

    .ranking-value {
        color: #10b981;
        font-weight: 700;
    }

    /* Animação de loading */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .loading {
        animation: pulse 2s infinite;
    }

    /* Responsividade */
    @media (max-width: 768px) {
        .kpi-card {
            min-width: 100%;
        }
        .main-header {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Função para carregar dados
@st.cache_data
def load_data():
    """Carrega e processa os dados do CSV"""
    try:
        df = pd.read_csv('dados.csv')
    except:
        st.error("Arquivo dados.csv não encontrado.")
        return None

    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

    numeric_cols = ['R$ Pedido', 'R$ Venda', 'R$ Frete Cli', 'R$ Frete Loja', 'R$ Taxa',
                    'R$ Custo', 'R$ Líquido', 'Lucro', 'Lucro Com NF', '% Lucro']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df['Ano'] = df['Data'].dt.year
    df['Mes'] = df['Data'].dt.month
    df['Ano_Mes'] = df['Data'].dt.to_period('M').astype(str)

    situacoes_validas = ['ENTREGUE', 'CANCELADO', 'DEVOLVIDO', 'EXTRAVIADO', 'A CAMINHO', 'EM DEVOLUÇÃO']
    df = df[df['Situação'].isin(situacoes_validas)]
    df['ENTREGA'] = df['ENTREGA'].fillna('Não informado')

    return df

# Função para criar card de KPI customizado
def create_kpi_cards(total_vendas, faturamento, lucro, margem, ticket_medio, metrica_lucro):
    kpi_html = f"""
    <div class="kpi-container">
        <div class="kpi-card vendas">
            <div class="kpi-icon">🛒</div>
            <div class="kpi-value">{total_vendas:,}</div>
            <div class="kpi-label">Total de Vendas</div>
        </div>
        <div class="kpi-card faturamento">
            <div class="kpi-icon">💵</div>
            <div class="kpi-value">R$ {faturamento:,.0f}</div>
            <div class="kpi-label">Faturamento</div>
        </div>
        <div class="kpi-card lucro">
            <div class="kpi-icon">💰</div>
            <div class="kpi-value">R$ {lucro:,.0f}</div>
            <div class="kpi-label">{metrica_lucro}</div>
        </div>
        <div class="kpi-card margem">
            <div class="kpi-icon">📈</div>
            <div class="kpi-value">{margem:.1f}%</div>
            <div class="kpi-label">Margem</div>
        </div>
        <div class="kpi-card ticket">
            <div class="kpi-icon">🎫</div>
            <div class="kpi-value">R$ {ticket_medio:,.0f}</div>
            <div class="kpi-label">Ticket Médio</div>
        </div>
    </div>
    """
    return kpi_html

# Template de gráfico com tema escuro
def apply_dark_theme(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(30, 41, 59, 0.8)',
        font=dict(color='#e2e8f0', family='Inter'),
        title_font=dict(size=18, color='#f1f5f9'),
        legend=dict(
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='#334155',
            font=dict(color='#e2e8f0')
        ),
        xaxis=dict(
            gridcolor='#334155',
            linecolor='#334155',
            tickfont=dict(color='#94a3b8')
        ),
        yaxis=dict(
            gridcolor='#334155',
            linecolor='#334155',
            tickfont=dict(color='#94a3b8')
        )
    )
    return fig

# Carregar dados
df = load_data()

if df is not None:
    # ========================================
    # SIDEBAR - FILTROS
    # ========================================
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <h2 style="background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       font-size: 1.5rem; margin: 0;">🎛️ Painel de Filtros</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Filtro de período
        st.markdown("##### 📅 Período")
        meses_ordem = ['DEZ 23', 'JAN 24', 'FEV 24', 'MAR 24', 'ABR 24', 'MAIO 24', 'JUN 24',
                       'JUL 24', 'AGO 24', 'SET 24', 'OUT 24', 'NOV 24', 'DEZ 24', 'JAN 25',
                       'FEV 25', 'MAR 25', 'ABR 25', 'MAI 25', 'JUN 25', 'JUL 25', 'AGO 25',
                       'SET 25', 'OUT 25', 'NOV 25', 'DEZ 25', 'JAN 26']
        periodos_disponiveis = [p for p in meses_ordem if p in df['Periodo_Aba'].unique()]

        periodo_selecionado = st.multiselect(
            "Selecione os meses:",
            options=periodos_disponiveis,
            default=periodos_disponiveis,
            key="periodo"
        )

        st.markdown("---")

        # Filtro de situação
        st.markdown("##### 📦 Situação")
        situacoes = df['Situação'].unique().tolist()
        situacao_selecionada = st.multiselect(
            "Status dos pedidos:",
            options=situacoes,
            default=['ENTREGUE'],
            key="situacao"
        )

        st.markdown("---")

        # Filtro de tipo de entrega
        st.markdown("##### 🚚 Tipo de Entrega")
        tipos_entrega = df['ENTREGA'].unique().tolist()
        entrega_selecionada = st.multiselect(
            "Modalidade:",
            options=tipos_entrega,
            default=tipos_entrega,
            key="entrega"
        )

        st.markdown("---")

        # Escolha da métrica de lucro
        st.markdown("##### 💰 Métrica de Lucro")
        metrica_lucro = st.radio(
            "Calcular margem com:",
            options=['Lucro (sem NF)', 'Lucro Com NF'],
            index=0,
            key="metrica"
        )
        coluna_lucro = 'Lucro' if metrica_lucro == 'Lucro (sem NF)' else 'Lucro Com NF'

    # Aplicar filtros
    df_filtrado = df[
        (df['Periodo_Aba'].isin(periodo_selecionado)) &
        (df['Situação'].isin(situacao_selecionada)) &
        (df['ENTREGA'].isin(entrega_selecionada))
    ]

    # ========================================
    # HEADER
    # ========================================
    st.markdown('<h1 class="main-header">Painelli Vendas</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Dashboard de Performance e Análise de Vendas</p>', unsafe_allow_html=True)

    # Info do filtro ativo
    st.markdown(f"""
    <div class="filter-info">
        <span style="color: #94a3b8;">Filtros ativos:</span>
        <span class="filter-badge">{len(periodo_selecionado)} períodos</span>
        <span class="filter-badge green">{', '.join(situacao_selecionada)}</span>
        <span class="filter-badge purple">{metrica_lucro}</span>
        <span style="margin-left: auto; color: #f1f5f9; font-weight: 600;">
            {len(df_filtrado):,} registros
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ========================================
    # KPIs PRINCIPAIS
    # ========================================
    total_vendas = len(df_filtrado)
    faturamento = df_filtrado['R$ Venda'].sum()
    lucro = df_filtrado[coluna_lucro].sum()
    margem = (lucro / faturamento * 100) if faturamento > 0 else 0
    ticket_medio = faturamento / total_vendas if total_vendas > 0 else 0

    st.markdown(create_kpi_cards(total_vendas, faturamento, lucro, margem, ticket_medio, metrica_lucro),
                unsafe_allow_html=True)

    # ========================================
    # ABAS DE VISUALIZAÇÃO
    # ========================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Evolução",
        "📊 Análises",
        "🏆 Rankings",
        "📅 Sazonalidade",
        "📋 Dados"
    ])

    # ----------------------------------------
    # TAB 1: EVOLUÇÃO MENSAL
    # ----------------------------------------
    with tab1:
        st.markdown('<div class="section-title"><span class="section-title-icon">📈</span> Evolução Mensal</div>',
                    unsafe_allow_html=True)

        # Preparar dados mensais
        mensal = df_filtrado.groupby('Periodo_Aba').agg({
            'Pedido': 'count',
            'R$ Venda': 'sum',
            coluna_lucro: 'sum'
        }).reset_index()
        mensal.columns = ['Período', 'Qtd Vendas', 'Faturamento', 'Lucro']
        mensal['ordem'] = mensal['Período'].apply(lambda x: meses_ordem.index(x) if x in meses_ordem else 999)
        mensal = mensal.sort_values('ordem').drop('ordem', axis=1)
        mensal['Margem %'] = (mensal['Lucro'] / mensal['Faturamento'] * 100).round(2)
        mensal['Ticket Médio'] = (mensal['Faturamento'] / mensal['Qtd Vendas']).round(2)

        # Gráfico principal de Faturamento e Lucro
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Bar(
                x=mensal['Período'],
                y=mensal['Faturamento'],
                name='Faturamento',
                marker=dict(
                    color='#3b82f6',
                    line=dict(width=0)
                ),
                opacity=0.9
            ),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(
                x=mensal['Período'],
                y=mensal['Lucro'],
                name='Lucro',
                mode='lines+markers',
                line=dict(color='#10b981', width=4),
                marker=dict(size=12, symbol='circle', line=dict(width=2, color='white'))
            ),
            secondary_y=True
        )

        fig.update_layout(
            title=dict(text='Faturamento e Lucro por Mês', font=dict(size=20)),
            height=450,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=80)
        )
        fig.update_yaxes(title_text="Faturamento (R$)", secondary_y=False, tickprefix="R$ ", tickformat=",.0f")
        fig.update_yaxes(title_text="Lucro (R$)", secondary_y=True, tickprefix="R$ ", tickformat=",.0f")
        fig = apply_dark_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

        # Gráficos secundários
        col1, col2 = st.columns(2)

        with col1:
            fig_qtd = px.area(
                mensal, x='Período', y='Qtd Vendas',
                title='Quantidade de Vendas por Mês'
            )
            fig_qtd.update_traces(
                fill='tozeroy',
                line=dict(color='#8b5cf6', width=3),
                fillcolor='rgba(139, 92, 246, 0.3)'
            )
            fig_qtd.update_layout(height=350)
            fig_qtd = apply_dark_theme(fig_qtd)
            st.plotly_chart(fig_qtd, use_container_width=True)

        with col2:
            fig_margem = go.Figure()
            fig_margem.add_trace(go.Scatter(
                x=mensal['Período'],
                y=mensal['Margem %'],
                mode='lines+markers+text',
                line=dict(color='#f59e0b', width=3),
                marker=dict(size=10),
                text=[f"{v:.1f}%" for v in mensal['Margem %']],
                textposition='top center',
                textfont=dict(color='#f59e0b', size=10)
            ))
            fig_margem.add_hline(
                y=mensal['Margem %'].mean(),
                line_dash="dash",
                line_color="#ef4444",
                annotation_text=f"Média: {mensal['Margem %'].mean():.1f}%",
                annotation_font_color="#ef4444"
            )
            fig_margem.update_layout(
                title='Evolução da Margem (%)',
                height=350,
                yaxis_title='Margem %'
            )
            fig_margem = apply_dark_theme(fig_margem)
            st.plotly_chart(fig_margem, use_container_width=True)

        # Tabela resumo
        st.markdown("#### 📊 Tabela Resumo Mensal")
        mensal_display = mensal.copy()
        mensal_display['Faturamento'] = mensal_display['Faturamento'].apply(lambda x: f"R$ {x:,.2f}")
        mensal_display['Lucro'] = mensal_display['Lucro'].apply(lambda x: f"R$ {x:,.2f}")
        mensal_display['Ticket Médio'] = mensal_display['Ticket Médio'].apply(lambda x: f"R$ {x:,.2f}")
        mensal_display['Margem %'] = mensal_display['Margem %'].apply(lambda x: f"{x:.2f}%")
        st.dataframe(mensal_display, use_container_width=True, hide_index=True)

    # ----------------------------------------
    # TAB 2: ANÁLISES
    # ----------------------------------------
    with tab2:
        st.markdown('<div class="section-title"><span class="section-title-icon">📊</span> Análises Detalhadas</div>',
                    unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de Situação
            situacao_df = df_filtrado.groupby('Situação').agg({
                'Pedido': 'count',
                'R$ Venda': 'sum'
            }).reset_index()
            situacao_df.columns = ['Situação', 'Quantidade', 'Faturamento']

            colors_situacao = {
                'ENTREGUE': '#10b981',
                'CANCELADO': '#ef4444',
                'DEVOLVIDO': '#f59e0b',
                'EXTRAVIADO': '#8b5cf6',
                'A CAMINHO': '#3b82f6',
                'EM DEVOLUÇÃO': '#6b7280'
            }

            fig_sit = px.pie(
                situacao_df,
                values='Quantidade',
                names='Situação',
                title='Distribuição por Situação',
                color='Situação',
                color_discrete_map=colors_situacao,
                hole=0.5
            )
            fig_sit.update_traces(
                textposition='outside',
                textinfo='percent+label',
                textfont=dict(color='white', size=12)
            )
            fig_sit.update_layout(height=400)
            fig_sit = apply_dark_theme(fig_sit)
            st.plotly_chart(fig_sit, use_container_width=True)

        with col2:
            # Gráfico de Tipo de Entrega
            entrega_df = df_filtrado.groupby('ENTREGA').agg({
                'Pedido': 'count',
                coluna_lucro: 'sum'
            }).reset_index()
            entrega_df.columns = ['Tipo Entrega', 'Quantidade', 'Lucro']
            entrega_df = entrega_df.sort_values('Quantidade', ascending=True)

            fig_ent = px.bar(
                entrega_df,
                y='Tipo Entrega',
                x='Quantidade',
                title='Vendas por Tipo de Entrega',
                orientation='h',
                color='Quantidade',
                color_continuous_scale=['#1e3a5f', '#3b82f6', '#60a5fa']
            )
            fig_ent.update_layout(height=400, coloraxis_showscale=False)
            fig_ent = apply_dark_theme(fig_ent)
            st.plotly_chart(fig_ent, use_container_width=True)

        # Comparativo Anual
        st.markdown("#### 📅 Comparativo Anual")

        anual = df_filtrado.groupby('Ano').agg({
            'Pedido': 'count',
            'R$ Venda': 'sum',
            coluna_lucro: 'sum'
        }).reset_index()
        anual.columns = ['Ano', 'Qtd Vendas', 'Faturamento', 'Lucro']
        anual = anual[anual['Ano'] >= 2023]
        anual['Ano'] = anual['Ano'].astype(int).astype(str)
        anual['Margem %'] = (anual['Lucro'] / anual['Faturamento'] * 100).round(2)

        col1, col2, col3 = st.columns(3)

        with col1:
            fig_anual1 = px.bar(
                anual, x='Ano', y='Faturamento',
                title='Faturamento por Ano',
                text=anual['Faturamento'].apply(lambda x: f"R$ {x/1000000:.1f}M")
            )
            fig_anual1.update_traces(
                marker_color=['#1e40af', '#3b82f6', '#60a5fa'][:len(anual)],
                textposition='outside',
                textfont=dict(color='#60a5fa', size=14, family='Inter')
            )
            fig_anual1.update_layout(height=350)
            fig_anual1 = apply_dark_theme(fig_anual1)
            st.plotly_chart(fig_anual1, use_container_width=True)

        with col2:
            fig_anual2 = px.bar(
                anual, x='Ano', y='Lucro',
                title='Lucro por Ano',
                text=anual['Lucro'].apply(lambda x: f"R$ {x/1000:.0f}K")
            )
            fig_anual2.update_traces(
                marker_color=['#065f46', '#10b981', '#34d399'][:len(anual)],
                textposition='outside',
                textfont=dict(color='#34d399', size=14, family='Inter')
            )
            fig_anual2.update_layout(height=350)
            fig_anual2 = apply_dark_theme(fig_anual2)
            st.plotly_chart(fig_anual2, use_container_width=True)

        with col3:
            fig_anual3 = px.bar(
                anual, x='Ano', y='Qtd Vendas',
                title='Quantidade por Ano',
                text=anual['Qtd Vendas'].apply(lambda x: f"{x:,}")
            )
            fig_anual3.update_traces(
                marker_color=['#9a3412', '#f59e0b', '#fbbf24'][:len(anual)],
                textposition='outside',
                textfont=dict(color='#fbbf24', size=14, family='Inter')
            )
            fig_anual3.update_layout(height=350)
            fig_anual3 = apply_dark_theme(fig_anual3)
            st.plotly_chart(fig_anual3, use_container_width=True)

    # ----------------------------------------
    # TAB 3: RANKINGS
    # ----------------------------------------
    with tab3:
        st.markdown('<div class="section-title"><span class="section-title-icon">🏆</span> Rankings</div>',
                    unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🥇 Top 15 Compradores (por Faturamento)")
            top_compradores = df_filtrado.groupby('Comprador').agg({
                'Pedido': 'count',
                'R$ Venda': 'sum',
                coluna_lucro: 'sum'
            }).reset_index()
            top_compradores.columns = ['Comprador', 'Qtd Compras', 'Total Gasto', 'Lucro Gerado']
            top_compradores = top_compradores.sort_values('Total Gasto', ascending=False).head(15)

            # Criar visual de ranking
            for i, row in enumerate(top_compradores.itertuples(), 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
                st.markdown(f"""
                <div class="ranking-item">
                    <div class="ranking-position">{medal}</div>
                    <div class="ranking-info">
                        <div class="ranking-name">{row.Comprador[:30]}...</div>
                        <div class="ranking-value">R$ {row._3:,.2f} | {row._2} compras</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### 🔄 Compradores Mais Recorrentes")
            recorrentes = df_filtrado.groupby('Comprador').agg({
                'Pedido': 'count',
                'R$ Venda': 'sum'
            }).reset_index()
            recorrentes.columns = ['Comprador', 'Qtd Compras', 'Total Gasto']
            recorrentes = recorrentes[recorrentes['Qtd Compras'] > 1].sort_values('Qtd Compras', ascending=False).head(15)

            for i, row in enumerate(recorrentes.itertuples(), 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
                st.markdown(f"""
                <div class="ranking-item">
                    <div class="ranking-position">{medal}</div>
                    <div class="ranking-info">
                        <div class="ranking-name">{row.Comprador[:30]}...</div>
                        <div class="ranking-value">{row._2} compras | R$ {row._3:,.2f}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Melhores períodos
        st.markdown("---")
        st.markdown("#### 📈 Melhores Períodos")

        periodos_fat = df_filtrado.groupby('Periodo_Aba')['R$ Venda'].sum().sort_values(ascending=False)
        periodos_lucro = df_filtrado.groupby('Periodo_Aba')[coluna_lucro].sum().sort_values(ascending=False)
        periodos_qtd = df_filtrado.groupby('Periodo_Aba')['Pedido'].count().sort_values(ascending=False)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="insight-card success">
                <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">💵 Por Faturamento</div>
            </div>
            """, unsafe_allow_html=True)
            for i, (periodo, valor) in enumerate(periodos_fat.head(5).items(), 1):
                st.markdown(f"**{i}.** {periodo}: R$ {valor:,.2f}")

        with col2:
            st.markdown("""
            <div class="insight-card info">
                <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">💰 Por Lucro</div>
            </div>
            """, unsafe_allow_html=True)
            for i, (periodo, valor) in enumerate(periodos_lucro.head(5).items(), 1):
                st.markdown(f"**{i}.** {periodo}: R$ {valor:,.2f}")

        with col3:
            st.markdown("""
            <div class="insight-card warning">
                <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">📦 Por Quantidade</div>
            </div>
            """, unsafe_allow_html=True)
            for i, (periodo, valor) in enumerate(periodos_qtd.head(5).items(), 1):
                st.markdown(f"**{i}.** {periodo}: {valor:,} vendas")

    # ----------------------------------------
    # TAB 4: SAZONALIDADE
    # ----------------------------------------
    with tab4:
        st.markdown('<div class="section-title"><span class="section-title-icon">📅</span> Análise de Sazonalidade</div>',
                    unsafe_allow_html=True)

        meses_nomes = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
                       5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
                       9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}

        sazon = df_filtrado.groupby('Mes').agg({
            'Pedido': 'count',
            'R$ Venda': 'sum',
            coluna_lucro: 'sum'
        }).reset_index()
        sazon.columns = ['Mês', 'Qtd Vendas', 'Faturamento', 'Lucro']
        sazon['Mês Nome'] = sazon['Mês'].map(meses_nomes)
        sazon['Margem %'] = (sazon['Lucro'] / sazon['Faturamento'] * 100).round(2)

        # Gráfico de barras agrupadas
        fig_sazon = go.Figure()

        fig_sazon.add_trace(go.Bar(
            x=sazon['Mês Nome'],
            y=sazon['Faturamento'],
            name='Faturamento',
            marker_color='#3b82f6',
            text=sazon['Faturamento'].apply(lambda x: f"R$ {x/1000:.0f}K"),
            textposition='outside',
            textfont=dict(color='#60a5fa', size=10)
        ))

        fig_sazon.add_trace(go.Bar(
            x=sazon['Mês Nome'],
            y=sazon['Lucro'],
            name='Lucro',
            marker_color='#10b981',
            text=sazon['Lucro'].apply(lambda x: f"R$ {x/1000:.0f}K"),
            textposition='outside',
            textfont=dict(color='#34d399', size=10)
        ))

        fig_sazon.update_layout(
            title='Faturamento e Lucro por Mês do Ano (Agregado)',
            barmode='group',
            height=450,
            xaxis_title='Mês',
            yaxis_title='Valor (R$)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        fig_sazon = apply_dark_theme(fig_sazon)
        st.plotly_chart(fig_sazon, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            fig_qtd_sazon = px.bar(
                sazon, x='Mês Nome', y='Qtd Vendas',
                title='Quantidade de Vendas por Mês do Ano',
                text='Qtd Vendas'
            )
            fig_qtd_sazon.update_traces(
                marker_color='#f59e0b',
                textposition='outside',
                textfont=dict(color='#fbbf24', size=12)
            )
            fig_qtd_sazon.update_layout(height=350)
            fig_qtd_sazon = apply_dark_theme(fig_qtd_sazon)
            st.plotly_chart(fig_qtd_sazon, use_container_width=True)

        with col2:
            fig_margem_sazon = go.Figure()

            # Cores baseadas na média
            media_margem = sazon['Margem %'].mean()
            colors = ['#10b981' if m >= media_margem else '#ef4444' for m in sazon['Margem %']]

            fig_margem_sazon.add_trace(go.Bar(
                x=sazon['Mês Nome'],
                y=sazon['Margem %'],
                marker_color=colors,
                text=sazon['Margem %'].apply(lambda x: f"{x:.1f}%"),
                textposition='outside',
                textfont=dict(size=12)
            ))

            fig_margem_sazon.add_hline(
                y=media_margem,
                line_dash="dash",
                line_color="#f59e0b",
                annotation_text=f"Média: {media_margem:.1f}%",
                annotation_font_color="#f59e0b"
            )

            fig_margem_sazon.update_layout(
                title='Margem por Mês do Ano',
                height=350,
                yaxis_title='Margem %'
            )
            fig_margem_sazon = apply_dark_theme(fig_margem_sazon)
            st.plotly_chart(fig_margem_sazon, use_container_width=True)

        # Insights
        st.markdown("#### 💡 Insights de Sazonalidade")

        melhor_mes_fat = sazon.loc[sazon['Faturamento'].idxmax(), 'Mês Nome']
        pior_mes_fat = sazon.loc[sazon['Faturamento'].idxmin(), 'Mês Nome']
        melhor_mes_margem = sazon.loc[sazon['Margem %'].idxmax(), 'Mês Nome']
        melhor_fat_valor = sazon['Faturamento'].max()
        pior_fat_valor = sazon['Faturamento'].min()
        melhor_margem_valor = sazon['Margem %'].max()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="insight-card success">
                <div class="insight-value">📈 {melhor_mes_fat}</div>
                <div class="insight-label">Melhor Faturamento</div>
                <div style="color: #10b981; font-weight: 600; margin-top: 0.5rem;">R$ {melhor_fat_valor:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="insight-card warning">
                <div class="insight-value">📉 {pior_mes_fat}</div>
                <div class="insight-label">Mês Mais Fraco</div>
                <div style="color: #f59e0b; font-weight: 600; margin-top: 0.5rem;">R$ {pior_fat_valor:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="insight-card info">
                <div class="insight-value">💰 {melhor_mes_margem}</div>
                <div class="insight-label">Melhor Margem</div>
                <div style="color: #3b82f6; font-weight: 600; margin-top: 0.5rem;">{melhor_margem_valor:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

    # ----------------------------------------
    # TAB 5: DADOS
    # ----------------------------------------
    with tab5:
        st.markdown('<div class="section-title"><span class="section-title-icon">📋</span> Dados Filtrados</div>',
                    unsafe_allow_html=True)

        st.markdown(f"""
        <div class="filter-info" style="justify-content: space-between;">
            <span style="color: #f1f5f9; font-size: 1.1rem;">
                📊 <strong>{len(df_filtrado):,}</strong> registros encontrados
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Opção de download
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar dados filtrados (CSV)",
            data=csv,
            file_name="painelli_dados_filtrados.csv",
            mime="text/csv"
        )

        # Mostrar amostra dos dados
        st.markdown("#### Amostra dos Dados")
        colunas_exibir = ['Data', 'Comprador', 'R$ Venda', 'Lucro', 'Lucro Com NF',
                         'Situação', 'ENTREGA', 'Periodo_Aba']
        df_display = df_filtrado[colunas_exibir].head(100).copy()
        df_display['Data'] = df_display['Data'].dt.strftime('%d/%m/%Y')
        df_display['R$ Venda'] = df_display['R$ Venda'].apply(lambda x: f"R$ {x:,.2f}")
        df_display['Lucro'] = df_display['Lucro'].apply(lambda x: f"R$ {x:,.2f}")
        df_display['Lucro Com NF'] = df_display['Lucro Com NF'].apply(lambda x: f"R$ {x:,.2f}")
        st.dataframe(df_display, use_container_width=True, hide_index=True, height=500)

    # ========================================
    # FOOTER
    # ========================================
    st.markdown("""
    <div class="footer">
        <p class="footer-text">
            📊 <span class="footer-brand">Painelli Vendas Dashboard</span> |
            Desenvolvido com Streamlit & Plotly
        </p>
        <p class="footer-text" style="font-size: 0.8rem; margin-top: 0.5rem;">
            Dados de DEZ/2023 a JAN/2026 • Atualizado em tempo real
        </p>
    </div>
    """, unsafe_allow_html=True)
