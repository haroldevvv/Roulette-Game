import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------
# Roulette Simulation (Fair vs Tweaked)
# -----------------------------------------------
# Game: Simplified roulette — bet on RED or BLACK only.
# Fair Game: 18 RED, 18 BLACK, 1 GREEN (House wins on GREEN).
# Tweaked Game: Slightly increased GREEN probability (house edge).

# Define roulette wheel numbers
fair_wheel = ['RED'] * 18 + ['BLACK'] * 18 + ['GREEN']
tweaked_wheel = ['RED'] * 18 + ['BLACK'] * 18 + ['GREEN']

# Tweaked probabilities (GREEN slightly more likely)
fair_prob = [1/37] * 37
tweaked_prob = [0.026] * 36 + [0.064]  # GREEN goes from ~2.7% to 6.4%

# Simulation function
def simulate_roulette(n_rounds, bet_amount, wheel, probabilities):
    results = np.random.choice(wheel, size=n_rounds, p=probabilities)
    outcomes = []
    for r in results:
        if r == 'GREEN':
            outcomes.append(-bet_amount)
        else:
            outcomes.append(bet_amount if r == 'RED' else -bet_amount)
    return pd.DataFrame({
        'Result': results,
        'Outcome': outcomes
    })

# Streamlit Interface
st.title("🎰 Roulette Simulation: Fair vs Tweaked Game")
st.write("This app simulates a simplified Roulette game (RED vs BLACK bets only). \n"
         "Compare a FAIR wheel vs a TWEAKED wheel with increased GREEN probability.")

n_rounds = st.slider("Number of simulated rounds", 1000, 50000, 10000)
bet_amount = st.number_input("Bet amount per round", 1, 10000, 100)

if st.button("Run Simulation"):
    st.subheader("Running Monte Carlo Simulation...")

    fair_df = simulate_roulette(n_rounds, bet_amount, fair_wheel, fair_prob)
    tweaked_df = simulate_roulette(n_rounds, bet_amount, tweaked_wheel, tweaked_prob)

    # Calculate totals
    fair_total = fair_df['Outcome'].sum()
    tweaked_total = tweaked_df['Outcome'].sum()

    # Display results
    st.metric("Fair Game Profit (Player)", f"{fair_total:,}")
    st.metric("Tweaked Game Profit (Player)", f"{tweaked_total:,}")

    st.subheader("Distribution of Outcomes")

    fig1, ax1 = plt.subplots()
    fair_df['Outcome'].hist(ax=ax1)
    ax1.set_title("Fair Game Outcome Distribution")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    tweaked_df['Outcome'].hist(ax=ax2)
    ax2.set_title("Tweaked Game Outcome Distribution")
    st.pyplot(fig2)

    # Cumulative profit plot
    st.subheader("Cumulative Profit Over Time")

    fig3, ax3 = plt.subplots()
    ax3.plot(fair_df['Outcome'].cumsum(), label='Fair Game')
    ax3.plot(tweaked_df['Outcome'].cumsum(), label='Tweaked Game')
    ax3.legend()
    ax3.set_xlabel("Rounds")
    ax3.set_ylabel("Cumulative Profit")
    st.pyplot(fig3)

    # Summary
    st.subheader("Summary")
    st.write(f"**House Edge (difference):** {tweaked_total - fair_total}")
    st.write("The tweaked game increases the GREEN probability, causing more consistent losses for the player.")
