import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Roulette Simulator Using Board (Fair vs Tweaked)

# Define the roulette board numbers and colors
roulette_board = {
    0: 'GREEN',
    1: 'RED', 2: 'BLACK', 3: 'RED', 4: 'BLACK', 5: 'RED', 6: 'BLACK',
    7: 'RED', 8: 'BLACK', 9: 'RED', 10: 'BLACK', 11: 'BLACK', 12: 'RED',
    13: 'BLACK', 14: 'RED', 15: 'BLACK', 16: 'RED', 17: 'BLACK', 18: 'RED',
    19: 'RED', 20: 'BLACK', 21: 'RED', 22: 'BLACK', 23: 'RED', 24: 'BLACK',
    25: 'RED', 26: 'BLACK', 27: 'RED', 28: 'BLACK', 29: 'BLACK', 30: 'RED',
    31: 'BLACK', 32: 'RED', 33: 'BLACK', 34: 'RED', 35: 'BLACK', 36: 'RED'}

# Probabilities
fair_prob = [1/37] * 37

# Tweaked: increase GREEN slightly to 6.4% and normalize remaining numbers
tweaked_prob = [0.026] * 37
tweaked_prob[0] = 0.064
tweaked_prob = np.array(tweaked_prob)
tweaked_prob /= tweaked_prob.sum()  # Ensure sum = 1

# Simulation functions
def simulate_roulette_number(n_rounds, bet_amount, probabilities, player_choice, starting_balance, tweaked=False):
    numbers = list(roulette_board.keys())
    results = np.random.choice(numbers, size=n_rounds, p=probabilities)

    balances = []
    balance = starting_balance

    for r in results:
        if r == player_choice:
            if tweaked:
                win = bet_amount * 34.8  # Slightly reduced payout for house edge
            else:
                win = bet_amount * 35  # Standard payout
        else:
            win = -bet_amount
        balance += win
        balances.append(balance)

    df = pd.DataFrame({
        'Result': results,
        'Color': [roulette_board[r] for r in results],
        'Balance': balances})
    return df

st.title(" Roulette Simulator Using Board (Fair vs Tweaked)")

st.image("static/roulette-board.png", caption="Roulette Board", use_column_width=True)

player_choice = st.number_input("Choose a number to bet on (0-36):", min_value=0, max_value=36, value=17)
n_rounds = st.slider("Number of simulated rounds", 1000, 50000, 10000)
bet_amount = st.number_input("Bet amount per round", 1, 10000, 100)
starting_balance = st.number_input("Starting Balance", 100, 1_000_000, 1000)

st.markdown("---")

# Buttons 
a, b = st.columns(2)
run_fair = a.button("Run FAIR Game")
run_tweaked = b.button("Run TWEAKED Game")

if "fair_df" not in st.session_state:
    st.session_state.fair_df = None
if "tweaked_df" not in st.session_state:
    st.session_state.tweaked_df = None

# FAIR GAME
if run_fair:
    st.subheader("FAIR Game Results")
    fair_df = simulate_roulette_number(n_rounds, bet_amount, fair_prob, player_choice, starting_balance)
    st.session_state.fair_df = fair_df

    st.metric("Final Balance (FAIR)", f"{fair_df['Balance'].iloc[-1]:,}")

    st.subheader("Outcome Distribution — FAIR")
    fig1, ax1 = plt.subplots()
    ax1.hist(fair_df['Result'], bins=np.arange(-0.5,37,1), edgecolor='black')
    ax1.set_xlabel("Number")
    ax1.set_ylabel("Frequency")
    st.pyplot(fig1)

    st.subheader("Balance Over Time — FAIR")
    fig2, ax2 = plt.subplots()
    ax2.plot(fair_df['Balance'])
    ax2.set_xlabel("Rounds")
    ax2.set_ylabel("Balance")
    st.pyplot(fig2)

# TWEAKED GAME
if run_tweaked:
    st.subheader("TWEAKED Game Results")
    tweaked_df = simulate_roulette_number(n_rounds, bet_amount, tweaked_prob, player_choice, starting_balance, tweaked=True)
    st.session_state.tweaked_df = tweaked_df

    st.metric("Final Balance (TWEAKED)", f"{tweaked_df['Balance'].iloc[-1]:,}")

    st.subheader("Outcome Distribution — TWEAKED")
    fig3, ax3 = plt.subplots()
    ax3.hist(tweaked_df['Result'], bins=np.arange(-0.5,37,1), edgecolor='black')
    ax3.set_xlabel("Number")
    ax3.set_ylabel("Frequency")
    st.pyplot(fig3)

    st.subheader("Balance Over Time — TWEAKED")
    fig4, ax4 = plt.subplots()
    ax4.plot(tweaked_df['Balance'])
    ax4.set_xlabel("Rounds")
    ax4.set_ylabel("Balance")
    st.pyplot(fig4)


if st.session_state.fair_df is not None and st.session_state.tweaked_df is not None:
    st.markdown("---")
    st.subheader("Comparison Summary")

    fair_final = st.session_state.fair_df['Balance'].iloc[-1]
    tweaked_final = st.session_state.tweaked_df['Balance'].iloc[-1]

    st.write(f"**Fair Game Final Balance (Pesos):** {fair_final:,}")
    st.write(f"**Tweaked Game Final Balance (Pesos):** {tweaked_final:,}")
    st.write(f"**Difference:** {tweaked_final - fair_final:,}")

    st.info("The tweaked game slightly favors the house due to the increased GREEN probability and slightly reduced payout.")

