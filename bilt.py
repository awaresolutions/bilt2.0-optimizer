import streamlit as st

def calculate_rewards():
    st.set_page_config(page_title="Bilt 2.0 Rewards Calculator", layout="wide")
    st.title("💳 Bilt 2.0 Rewards Calculator (2026)")
    st.write("Determine your monthly and yearly earnings for the Blue, Obsidian, and Palladium cards.")

    # --- Sidebar Inputs ---
    st.sidebar.header("Monthly Spending")
    rent_mortgage = st.sidebar.number_input("Rent/Mortgage Payment ($)", min_value=0, value=2000, step=100)
    dining = st.sidebar.number_input("Dining ($)", min_value=0, value=500, step=50)
    groceries = st.sidebar.number_input("Groceries ($)", min_value=0, value=400, step=50)
    travel = st.sidebar.number_input("Travel ($)", min_value=0, value=200, step=50)
    other = st.sidebar.number_input("Other Everyday Spend ($)", min_value=0, value=500, step=50)

    st.sidebar.header("Strategy Selection")
    reward_strategy = st.sidebar.selectbox(
        "Select Reward Strategy",
        ["Housing-only (Tiered Points)", "Flexible Bilt Cash (4% Back)"]
    )

    # Calculation logic
    total_everyday = dining + groceries + travel + other
    housing_percent = (total_everyday / rent_mortgage) if rent_mortgage > 0 else 0

    # Housing Multiplier logic (Option 1: Tiered)
    if housing_percent >= 1.0:
        housing_mult = 1.25
    elif housing_percent >= 0.75:
        housing_mult = 1.0
    elif housing_percent >= 0.50:
        housing_mult = 0.75
    elif housing_percent >= 0.25:
        housing_mult = 0.50
    else:
        housing_mult = 0.0 # Standard base (usually 250 flat pts if <25%)

    # Card Data
    cards = {
        "Bilt Blue": {
            "fee": 0,
            "bonus_cash": 100,
            "base_pt": 1,
            "dining_pt": 1,
            "grocery_pt": 1,
            "travel_pt": 1,
            "authorized_user": 0
        },
        "Bilt Obsidian": {
            "fee": 95,
            "bonus_cash": 200,
            "base_pt": 1,
            "dining_pt": 3, # Assumes dining/grocery choice
            "grocery_pt": 3,
            "travel_pt": 2,
            "authorized_user": 50
        },
        "Bilt Palladium": {
            "fee": 495,
            "bonus_cash": 300, # Initial signup
            "base_pt": 2,
            "dining_pt": 2,
            "grocery_pt": 2,
            "travel_pt": 2,
            "authorized_user": 95
        }
    }

    cols = st.columns(3)

    for i, (card_name, data) in enumerate(cards.items()):
        with cols[i]:
            st.subheader(card_name)
            
            # 1. Calculate Points
            if card_name == "Bilt Obsidian":
                # Obsidian caps 3x Groceries at $25k/yr ($2,083/mo)
                g_pts = min(groceries, 2083) * 3 + max(0, groceries - 2083) * 1
                pts_from_spend = (dining * 3) + g_pts + (travel * 2) + (other * 1)
            elif card_name == "Bilt Palladium":
                pts_from_spend = total_everyday * 2
            else: # Blue
                pts_from_spend = total_everyday * 1

            # Housing Points Logic
            if reward_strategy == "Housing-only (Tiered Points)":
                housing_pts = rent_mortgage * housing_mult
                bilt_cash_earned = 0
            else:
                # Option 2: 4% Bilt Cash on non-housing
                # In this mode, housing pts are usually unlocked manually (often 1x)
                housing_pts = rent_mortgage * 1.0
                bilt_cash_earned = total_everyday * 0.04

            monthly_pts = pts_from_spend + housing_pts
            
            st.metric("Monthly Points", f"{int(monthly_pts):,}")
            st.metric("Monthly Bilt Cash", f"${bilt_cash_earned:,.2f}")
            
            st.markdown("---")
            st.write(f"**Annual Fee:** ${data['fee']}")
            st.write(f"**Annual Points:** {int(monthly_pts * 12):,}")
            st.write(f"**Annual Bilt Cash:** ${bilt_cash_earned * 12:,.2f}")
            
            if card_name == "Bilt Palladium":
                st.info("Includes Priority Pass & $400 Hotel Credit")
            elif card_name == "Bilt Obsidian":
                st.info("Includes $100 Hotel Credit")

    st.success(f"Strategy Insight: Using '{reward_strategy}', you are currently spending {housing_percent:.1%} of your rent/mortgage on everyday items.")

if __name__ == "__main__":
    calculate_rewards()