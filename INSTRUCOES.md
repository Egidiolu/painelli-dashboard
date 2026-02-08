# Painelli Vendas Dashboard - Instruções

## 1. Rodar Localmente (no seu Mac)

Abra o Terminal e execute:

```bash
cd ~/Downloads/painelli_dashboard
streamlit run app.py
```

O dashboard abrirá automaticamente no navegador em `http://localhost:8501`

---

## 2. Hospedar Online (Streamlit Cloud - GRATUITO)

### Passo 1: Criar conta no GitHub (se não tiver)
1. Acesse https://github.com
2. Clique em "Sign up" e crie uma conta

### Passo 2: Criar um repositório no GitHub
1. Clique no botão "+" no canto superior direito e selecione "New repository"
2. Nome do repositório: `painelli-dashboard`
3. Deixe como **Private** (privado) se quiser que só você acesse
4. Clique em "Create repository"

### Passo 3: Fazer upload dos arquivos
1. Na página do repositório, clique em "uploading an existing file"
2. Arraste os 3 arquivos da pasta `painelli_dashboard`:
   - `app.py`
   - `requirements.txt`
   - `PAINELLI VENDAS 25 (2) - lucas.xlsx`
3. Clique em "Commit changes"

### Passo 4: Conectar ao Streamlit Cloud
1. Acesse https://share.streamlit.io
2. Faça login com sua conta GitHub
3. Clique em "New app"
4. Selecione o repositório `painelli-dashboard`
5. Branch: `main`
6. Main file path: `app.py`
7. Clique em "Deploy!"

### Passo 5: Aguardar o deploy
O Streamlit Cloud vai instalar as dependências e iniciar seu app.
Em alguns minutos, você terá um link público para acessar de qualquer lugar!

Exemplo de URL: `https://seuusuario-painelli-dashboard.streamlit.app`

---

## 3. Atualizar os Dados

### Localmente:
Basta substituir o arquivo Excel na pasta e reiniciar o dashboard.

### No Streamlit Cloud:
1. Vá no seu repositório GitHub
2. Delete o arquivo Excel antigo
3. Faça upload do novo arquivo Excel
4. O Streamlit Cloud detecta a mudança e atualiza automaticamente

---

## Recursos do Dashboard

- **Filtros interativos**: Período, Situação, Tipo de Entrega
- **Escolha de métrica**: Lucro (sem NF) ou Lucro Com NF
- **5 abas de visualização**:
  1. Evolução Mensal (gráficos de linha e barra)
  2. Análises (pizza, comparativo anual)
  3. Rankings (top compradores, recorrentes)
  4. Sazonalidade (padrões por mês)
  5. Dados (tabela + download CSV)

---

## Suporte

Se precisar de ajuda, entre em contato!
