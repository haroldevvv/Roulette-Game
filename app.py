import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------
# Enhanced Roulette Simulation Using Board
# -----------------------------------------------

# Define the roulette board numbers and colors
roulette_board = {
    0: 'GREEN',
    1: 'RED', 2: 'BLACK', 3: 'RED', 4: 'BLACK', 5: 'RED', 6: 'BLACK',
    7: 'RED', 8: 'BLACK', 9: 'RED', 10: 'BLACK', 11: 'BLACK', 12: 'RED',
    13: 'BLACK', 14: 'RED', 15: 'BLACK', 16: 'RED', 17: 'BLACK', 18: 'RED',
    19: 'RED', 20: 'BLACK', 21: 'RED', 22: 'BLACK', 23: 'RED', 24: 'BLACK',
    25: 'RED', 26: 'BLACK', 27: 'RED', 28: 'BLACK', 29: 'BLACK', 30: 'RED',
    31: 'BLACK', 32: 'RED', 33: 'BLACK', 34: 'RED', 35: 'BLACK', 36: 'RED'
}

# Simulation function for number betting
def simulate_roulette_number(n_rounds, bet_amount, board, player_choice, starting_balance):
    numbers = list(board.keys())
    probabilities = [1/37] * 37  # Fair probabilities

    results = np.random.choice(numbers, size=n_rounds, p=probabilities)

    balances = []
    balance = starting_balance

    for r in results:
        if r == player_choice:
            win = bet_amount * 35  # Straight number payout
        else:
            win = -bet_amount
        balance += win
        balances.append(balance)

    df = pd.DataFrame({
        'Result': results,
        'Color': [board[r] for r in results],
        'Balance': balances
    })
    return df

# -----------------------------------------------
# Streamlit UI
# -----------------------------------------------
st.title("🎰 Roulette Simulator Using Board")

# st.image("/mnt/data/2384464d-658d-4d1f-8d29-4b077cf29ae6.png", caption="Roulette Board", width=700)

# User selections
player_choice = st.number_input("Choose a number to bet on (0-36):", min_value=0, max_value=36, value=17)
n_rounds = st.slider("Number of simulated rounds", 1000, 50000, 10000)
bet_amount = st.number_input("Bet amount per round", 1, 10000, 100)
starting_balance = st.number_input("Starting Balance", 100, 1_000_000, 1000)

st.markdown("---")

# Buttons
run_simulation = st.button("Run Simulation 🎯")

if run_simulation:
    st.subheader("🎲 Simulation Results")
    df = simulate_roulette_number(n_rounds, bet_amount, roulette_board, player_choice, starting_balance)

    final_balance = df['Balance'].iloc[-1]
    st.metric("Final Balance", f"{final_balance:,}")

    st.subheader("Outcome Distribution")
    fig1, ax1 = plt.subplots()
    ax1.hist(df['Result'], bins=np.arange(-0.5,37,1), edgecolor='black')
    ax1.set_xlabel("Number")
    ax1.set_ylabel("Frequency")
    st.pyplot(fig1)

    st.subheader("Balance Over Time")
    fig2, ax2 = plt.subplots()
    ax2.plot(df['Balance'])
    ax2.set_xlabel("Rounds")
    ax2.set_ylabel("Balance")
    st.pyplot(fig2)