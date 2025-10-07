import streamlit as st
import requests
import networkx as nx
import matplotlib.pyplot as plt

API = 'http://localhost:8000'

st.title('LLM Misuse Detection - Prototype Dashboard')

if st.button('Refresh Graph Summary'):
    try:
        r = requests.get(API + '/graph/summary', timeout=5)
        st.json(r.json())
    except Exception as e:
        st.error(str(e))

st.markdown('### Quick Detect')
text = st.text_area('Paste content to analyze', height=150)
if st.button('Detect'):
    payload = {'id': 'ui-'+str(abs(hash(text)))[:8], 'text': text, 'source': 'ui'}
    try:
        r = requests.post(API + '/detect', json=payload, timeout=5)
        st.json(r.json())
    except Exception as e:
        st.error(str(e))

st.markdown('### Network Graph (simulated)')
if st.button('Show sample graph'):
    # fetch summary to discover nodes (prototype only)
    try:
        r = requests.get(API + '/graph/summary', timeout=5)
        data = r.json()
        st.write('nodes:', data.get('nodes'), 'edges:', data.get('edges'))
    except Exception as e:
        st.write('Could not fetch graph summary:', e)
        data = {}
    # draw a tiny random graph for demo
    G = nx.erdos_renyi_graph(15, 0.05, seed=42)
    plt.figure(figsize=(6,4))
    nx.draw(G, with_labels=True)
    st.pyplot(plt)
