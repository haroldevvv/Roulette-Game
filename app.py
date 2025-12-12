import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------
# Enhanced Roulette Simulation with Balance Tracking,
# Side-by-Side Charts, and Wheel Graphic
# -----------------------------------------------

# Wheel definitions
fair_wheel = ['RED'] * 18 + ['BLACK'] * 18 + ['GREEN']
tweaked_wheel = ['RED'] * 18 + ['BLACK'] * 18 + ['GREEN']

fair_prob = [1/37] * 37
# Tweaked: make GREEN more likely
# GREEN: 6.4%, Others: 2.6% each
tweaked_prob = [0.026] * 36 + [0.064]

# Simulation function
def simulate_roulette(n_rounds, bet_amount, wheel, probabilities, player_choice, starting_balance):
    results = np.random.choice(wheel, size=n_rounds, p=probabilities)

    balances = []
    balance = starting_balance

    for r in results:
        if r == player_choice:
            if r == 'GREEN':
                win = bet_amount * 14
            else:
                win = bet_amount
        else:
            win = -bet_amount

        balance += win
        balances.append(balance)

    df = pd.DataFrame({
        'Result': results,
        'Balance': balances
    })
    return df

# -----------------------------------------------
# Streamlit UI
# -----------------------------------------------
st.title("🎰 Fully Interactive Roulette Simulator (Fair vs Tweaked)")

st.image("https://www.freepik.com/premium-vector/traditional-european-roulette-wheel-with-single-zero_237485099.htm", caption="Roulette Wheel", width=350)

st.write("Compare **Fair** and **Tweaked** wheel behavior with balance tracking and visual analysis.")

# User selections
player_choice = st.radio("Choose your betting color:", ['RED', 'BLACK', 'GREEN'])
n_rounds = st.slider("Number of simulated rounds", 1000, 50000, 10000)
bet_amount = st.number_input("Bet amount per round", 1, 10000, 100)
starting_balance = st.number_input("Starting Balance", 100, 1_000_000, 1000)

st.markdown("---")

# Buttons
a, b = st.columns(2)
run_fair = a.button("Run FAIR Game 🎯")
run_tweaked = b.button("Run TWEAKED Game ⚠️")

# Containers to store results
if "fair_df" not in st.session_state:
    st.session_state.fair_df = None
if "tweaked_df" not in st.session_state:
    st.session_state.tweaked_df = None

# -----------------------------------------------
# FAIR GAME
# -----------------------------------------------
if run_fair:
    st.subheader("🎯 FAIR Game Simulation Results")

    fair_df = simulate_roulette(n_rounds, bet_amount, fair_wheel, fair_prob, player_choice, starting_balance)
    st.session_state.fair_df = fair_df

    final_balance = fair_df['Balance'].iloc[-1]

    st.metric("Final Balance (FAIR)", f"{final_balance:,}")

    # Animation of 20 spins
    st.subheader("🎡 Sample Spins (FAIR Wheel)")
    sample_spins = np.random.choice(fair_wheel, size=20, p=fair_prob)
    placeholder = st.empty()
    for s in sample_spins:
        placeholder.markdown(f"## 🎡 Spin Result: **{s}**")
        st.sleep(0.1)

    # Side-by-side charts
    st.subheader("Charts — FAIR Game")
    c1, c2 = st.columns(2)

    with c1:
        fig1, ax1 = plt.subplots()
        ax1.hist(np.diff([starting_balance] + fair_df['Balance'].tolist()))
        ax1.set_title("Outcome Distribution")
        st.pyplot(fig1)

    with c2:
        fig2, ax2 = plt.subplots()
        ax2.plot(fair_df['Balance'])
        ax2.set_title("Balance Over Time")
        st.pyplot(fig2)

# -----------------------------------------------
# TWEAKED GAME
# -----------------------------------------------
if run_tweaked:
    st.subheader("⚠️ Tweaked Game Results — Increased House Edge")

    tweaked_df = simulate_roulette(n_rounds, bet_amount, tweaked_wheel, tweaked_prob, player_choice, starting_balance)
    st.session_state.tweaked_df = tweaked_df

    final_balance = tweaked_df['Balance'].iloc[-1]

    st.metric("Final Balance (TWEAKED)", f"{final_balance:,}")

    st.subheader("🎡 Sample Spins (TWEAKED Wheel)")
    sample_spins = np.random.choice(tweaked_wheel, size=20, p=tweaked_prob)
    placeholder = st.empty()
    for s in sample_spins:
        placeholder.markdown(f"## 🎡 Spin Result: **{s}**")
        st.sleep(0.1)

    # Side-by-side charts
    st.subheader("Charts — TWEAKED Game")
    c1, c2 = st.columns(2)

    with c1:
        fig3, ax3 = plt.subplots()
        ax3.hist(np.diff([starting_balance] + tweaked_df['Balance'].tolist()))
        ax3.set_title("Outcome Distribution")
        st.pyplot(fig3)

    with c2:
        fig4, ax4 = plt.subplots()
        ax4.plot(tweaked_df['Balance'])
        ax4.set_title("Balance Over Time")
        st.pyplot(fig4)

# -----------------------------------------------
# SUMMARY (only if both tests are run)
# -----------------------------------------------
if st.session_state.fair_df is not None and st.session_state.tweaked_df is not None:
    st.markdown("---")
    st.subheader("📊 Comparison Summary")

    fair_final = st.session_state.fair_df['Balance'].iloc[-1]
    tweaked_final = st.session_state.tweaked_df['Balance'].iloc[-1]

    st.write(f"**Fair Final Balance:** {fair_final:,}")
    st.write(f"**Tweaked Final Balance:** {tweaked_final:,}")
    st.write(f"**Difference:** {tweaked_final - fair_final:,}")

    st.info("The tweaked wheel consistently leads to lower long-term balances due to the increased GREEN probability.")
