import streamlit as st
import pandas as pd

def calculate_rewards():
    st.set_page_config(page_title="Bilt 2.0: Before & After Conversion", layout="wide")
    st.title("💳 Bilt 2.0 Rewards Dashboard")
    st.write("Compare point yields before and after the manual housing unlock logic.")
    
    # --- Sidebar Inputs ---
    st.sidebar.header("Monthly Spend Profile")
    rent = st.sidebar.number_input("Monthly Rent/Mortgage ($)", min_value=0, value=2500)
    dining = st.sidebar.number_input("Dining ($)", min_value=0, value=600)
    groceries = st.sidebar.number_input("Groceries ($)", min_value=0, value=500)
    travel = st.sidebar.number_input("Travel ($)", min_value=0, value=300)
    other = st.sidebar.number_input("Other Spend ($)", min_value=0, value=600)

    reward_strategy = st.sidebar.selectbox(
        "Select Reward Strategy",
        ["Housing-only (Tiered Points)", "Flexible Bilt Cash (4% Back + Unlock)"]
    )

    total_everyday = dining + groceries + travel + other
    cards = {
        "Bilt Blue": {"fee": 0, "d": 1, "g": 1, "t": 1, "o": 1},
        "Bilt Obsidian": {"fee": 95, "d": 3, "g": 3, "t": 2, "o": 1},
        "Bilt Palladium": {"fee": 495, "d": 2, "g": 2, "t": 2, "o": 2}
    }

    cols = st.columns(3)

    for i, (name, specs) in enumerate(cards.items()):
        with cols[i]:
            st.markdown(f"### {name}")
            
            # 1. Base Points from Spending
            if name == "Bilt Obsidian":
                g_pts = min(groceries, 2083) * specs['g'] + max(0, groceries - 2083) * 1
                spend_pts = (dining * specs['d']) + g_pts + (travel * specs['t']) + (other * specs['o'])
            else:
                spend_pts = (dining * specs['d']) + (groceries * specs['g']) + (travel * specs['t']) + (other * specs['o'])

            # 2. Strategy Calculation
            if reward_strategy == "Housing-only (Tiered Points)":
                ratio = total_everyday / rent if rent > 0 else 0
                h_mult = 1.25 if ratio >= 1.0 else 1.0 if ratio >= 0.75 else 0.75 if ratio >= 0.50 else 0.50 if ratio >= 0.25 else 0.0
                housing_pts = rent * h_mult
                final_cash = 0
                
                st.metric("Total Monthly Points", f"{int(spend_pts + housing_pts):,}")
                st.caption(f"Includes {int(housing_pts):,} pts from {h_mult}x multiplier")

            else:
                # --- BEFORE CONVERSION ---
                gross_cash = total_everyday * 0.04
                
                # --- THE CONVERSION LOGIC ---
                # Rule: $30 Bilt Cash = 1,000 Pts (capped at 1x rent)
                cash_needed_for_max = (rent / 1000) * 30
                cash_to_spend = min(gross_cash, cash_needed_for_max)
                housing_pts_unlocked = (cash_to_spend / 30) * 1000
                final_cash = gross_cash - cash_to_spend

                # --- DASHBOARD DISPLAY ---
                st.metric("Total Monthly Points", f"{int(spend_pts + housing_pts_unlocked):,}")
                st.metric("Final Bilt Cash Balance", f"${final_cash:,.2f}")

                with st.expander("View Conversion Breakdown"):
                    data = {
                        "Metric": ["Spending Pts", "Bilt Cash Earned", "Bilt Cash Used", "Housing Pts Unlocked"],
                        "Value": [f"{int(spend_pts):,}", f"${gross_cash:,.2f}", f"-${cash_to_spend:,.2f}", f"+{int(housing_pts_unlocked):,}"]
                    }
                    st.table(pd.DataFrame(data))
            
            st.divider()
            st.write(f"**Annual Fee:** ${specs['fee']}")

if __name__ == "__main__":
    calculate_rewards()
