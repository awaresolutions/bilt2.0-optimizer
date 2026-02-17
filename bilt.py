import streamlit as st

def calculate_rewards():
    st.set_page_config(page_title="Bilt 2.0 Rewards Calculator", layout="wide")
    st.title("💳 Bilt 2.0 Rewards Calculator (Updated Conversion)")
    
    # --- Sidebar Inputs ---
    st.sidebar.header("Monthly Spending")
    rent_mortgage = st.sidebar.number_input("Rent/Mortgage Payment ($)", min_value=0, value=2500, step=100)
    dining = st.sidebar.number_input("Dining ($)", min_value=0, value=600, step=50)
    groceries = st.sidebar.number_input("Groceries ($)", min_value=0, value=500, step=50)
    travel = st.sidebar.number_input("Travel ($)", min_value=0, value=300, step=50)
    other = st.sidebar.number_input("Other Spend ($)", min_value=0, value=600, step=50)

    st.sidebar.header("Strategy Selection")
    reward_strategy = st.sidebar.selectbox(
        "Select Reward Strategy",
        ["Housing-only (Tiered Points)", "Flexible Bilt Cash (4% Back + Unlock)"]
    )

    # Core Logic Setup
    total_everyday = dining + groceries + travel + other
    spend_to_rent_ratio = (total_everyday / rent_mortgage) if rent_mortgage > 0 else 0

    # Card Data Definitions
    cards = {
        "Bilt Blue": {"fee": 0, "d_mult": 1, "g_mult": 1, "t_mult": 1, "o_mult": 1},
        "Bilt Obsidian": {"fee": 95, "d_mult": 3, "g_mult": 3, "t_mult": 2, "o_mult": 1},
        "Bilt Palladium": {"fee": 495, "d_mult": 2, "g_mult": 2, "t_mult": 2, "o_mult": 2}
    }

    cols = st.columns(3)

    for i, (card_name, specs) in enumerate(cards.items()):
        with cols[i]:
            st.subheader(card_name)
            
            # 1. Calculate Base Points from Spending
            if card_name == "Bilt Obsidian":
                g_pts = min(groceries, 2083) * specs['g_mult'] + max(0, groceries - 2083) * 1
                spend_pts = (dining * specs['d_mult']) + g_pts + (travel * specs['t_mult']) + (other * specs['o_mult'])
            else:
                spend_pts = (dining * specs['d_mult']) + (groceries * specs['g_mult']) + (travel * specs['t_mult']) + (other * specs['o_mult'])

            # 2. Strategy Logic
            if reward_strategy == "Housing-only (Tiered Points)":
                if spend_to_rent_ratio >= 1.0: h_mult = 1.25
                elif spend_to_rent_ratio >= 0.75: h_mult = 1.0
                elif spend_to_rent_ratio >= 0.50: h_mult = 0.75
                elif spend_to_rent_ratio >= 0.25: h_mult = 0.50
                else: h_mult = 0.0
                
                housing_pts = rent_mortgage * h_mult
                final_cash = 0
                explanation = f"Housing Multiplier: {h_mult}x"

            else:
                # Flexible Bilt Cash Strategy
                # You earn 4% Cash on ALL everyday spend
                earned_cash = total_everyday * 0.04
                
                # Conversion: $30 Bilt Cash = 1,000 Points (Capped at 1x rent)
                max_housing_pts_allowed = rent_mortgage * 1.0
                cash_needed_for_max = (max_housing_pts_allowed / 1000) * 30
                
                if earned_cash >= cash_needed_for_max:
                    housing_pts = max_housing_pts_allowed
                    final_cash = earned_cash - cash_needed_for_max
                    explanation = "Unlocked full 1x Rent Pts"
                else:
                    housing_pts = (earned_cash / 30) * 1000
                    final_cash = 0
                    explanation = f"Partial Unlock: {int(housing_pts)} pts"

            total_monthly_pts = spend_pts + housing_pts

            # Display Results
            st.metric("Monthly Points", f"{int(total_monthly_pts):,}")
            st.metric("Remaining Bilt Cash", f"${final_cash:,.2f}")
            st.caption(explanation)
            
            st.write("---")
            st.write(f"**Annual Points:** {int(total_monthly_pts * 12):,}")
            st.write(f"**Annual Fee:** ${specs['fee']}")

    st.info(f"Spending Ratio: {spend_to_rent_ratio:.1%} of housing cost.")

if __name__ == "__main__":
    calculate_rewards()
