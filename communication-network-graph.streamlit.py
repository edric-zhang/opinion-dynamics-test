import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Opinion Dynamics Simulator")



# ── Controls ──────────────────────────────────────────────────
st.markdown("### Parameters")

col1, col2, col3, col4 = st.columns(4)
with col1:
    feedback = st.radio("Feedback", [1, -1])
with col2:
    b = st.radio("Input push b", [0.1, 0.3])
with col3:
    noise_level = st.slider("Noise level", 0.0, 0.1, 0.02, step=0.01)
with col4:
    steps = st.slider("Steps", 50, 300, 120, step=10)

run = st.button("▶ Run Simulation")

# ── Figure and reference ──────────────────────────────────────
st.image("experiment.png", width=600)
st.caption("Experiment setup from Leonard et al (2024). Each node in the graph represents an agent (individual, robot, satellite etc .), and each edge represents a communication link between agents. Opinions evolve iteratively according to the network structure and model parameters. https://github.com/edric-zhang/opinion-dynamics-test ")

# ── Model ────────────────────────────────────────────────────
if run:
    N = 13
    edges = [
        (1,2),(1,3),(1,7),(1,12),(1,13),
        (2,3),(2,4),(2,8),(2,13),
        (3,10),
        (4,5),(4,6),(4,10),
        (5,6),(5,11),(5,13),
        (6,8),(6,10),(6,12),
        (7,11),
        (8,9),
        (9,10),(9,11),(9,12),
        (10,13),
        (11,13)
    ]

    A = np.zeros((N, N))
    for u, v in edges:
        A[u-1, v-1] = feedback
        A[v-1, u-1] = feedback
    for i in range(N):
        A[i, i] = 1

    largest = np.max(np.abs(np.linalg.eigvals(A)))
    A = A / largest

    x = np.zeros(N)
    history = [x.copy()]

    for i in range(1, steps):
        x = x + noise_level * np.random.randn(N)
        if 70 <= i <= 80:
            x[2]  -= b
            x[5]  += b
            x[9]  += b
            x[10] -= b
        x = A @ x
        history.append(x.copy())

    history = np.array(history)

    # ── Plot ─────────────────────────────────────────────────
    colors = plt.cm.tab20(np.linspace(0, 1, N))
    fig, ax = plt.subplots(figsize=(10, 6))
    for node in range(N):
        ax.plot(history[:, node], color=colors[node], label=f"agent {node+1}")
    ax.set_xlabel("Step (n)")
    ax.set_ylabel("Opinion")
    ax.set_xlim(0, steps)
    ax.set_ylim(-0.8, 0.8)
    ax.set_title(f"feedback={feedback}    b={b}    noise={noise_level}")
    ax.legend(loc="upper left", fontsize=8, ncol=2)
    ax.axvspan(70, 80, alpha=0.1, color="red", label="input window")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

    # ── Summary ───────────────────────────────────────────────
    st.markdown(f"""
    **Final opinion range:** `{history[-1].min():.3f}` to `{history[-1].max():.3f}`  
    """)
