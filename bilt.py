import streamlit as st
import pandas as pd

def calculate_rewards():
    st.set_page_config(page_title="Bilt 2.0: Full Year Comparison", layout="wide")
    st.title("💳 Bilt 2.0 Comprehensive Dashboard")
    st.write("Compare Monthly & Yearly yields including Bilt Cash conversion and Card Benefits.")
    
    # --- Sidebar Inputs ---
    st.sidebar.header("Monthly Spend Profile")
    rent = st.sidebar.number_input("Monthly Rent/Mortgage ($)", min_value=0, value=2500)
    dining = st.sidebar.number_input("Dining ($)", min_value=0, value=600)
    groceries = st.sidebar.number_input("Groceries ($)", min_value=0, value=500)
    travel = st.sidebar.number_input("Travel ($)", min_value=0, value=300)
    other = st.sidebar.number_input("Other Spend ($)", min_value=0, value=600)

    strategy = st.sidebar.selectbox(
        "Select Reward Strategy",
        ["Housing-only (Tiered Points)", "Flexible Bilt Cash (4% Back + Unlock)"]
    )

    total_everyday = dining + groceries + travel + other
    
    # Updated Card Specs with Credits and Signup Bonuses
    cards = {
        "Bilt Blue": {
            "fee": 0, "d": 1, "g": 1, "t": 1, "o": 1, 
            "signup_cash": 100, "annual_credits": 0,
            "perks": ["Cellphone Protection", "Secondary Rental Car Coverage"]
        },
        "Bilt Obsidian": {
            "fee": 95, "d": 3, "g": 3, "t": 2, "o": 1, 
            "signup_cash": 200, "annual_credits": 100,
            "perks": ["$100 Travel Credit ($50 semi-annually)", "Trip Delay Insurance"]
        },
        "Bilt Palladium": {
            "fee": 495, "d": 2, "g": 2, "t": 2, "o": 2, 
            "signup_cash": 300, "annual_credits": 600,
            "perks": ["Priority Pass (Unlimited)", "$400 Hotel Credit", "$200 Annual Bilt Cash"]
        }
    }

    cols = st.columns(3)

    for i, (name, s) in enumerate(cards.items()):
        with cols[i]:
            st.markdown(f"## {name}")
            
            # 1. PRE-CONVERSION (Points from Spending Only)
            if name == "Bilt Obsidian":
                # Cap 3x groceries at $25k/yr ($2,083/mo)
                g_pts = min(groceries, 2083) * s['g'] + max(0, groceries - 2083) * 1
                base_spend_pts = (dining * s['d']) + g_pts + (travel * s['t']) + (other * s['o'])
            else:
                base_spend_pts = (dining * s['d']) + (groceries * s['g']) + (travel * s['t']) + (other * s['o'])

            # 2. LOGIC CALCULATION
            if strategy == "Housing-only (Tiered Points)":
                ratio = total_everyday / rent if rent > 0 else 0
                h_mult = 1.25 if ratio >= 1.0 else 1.0 if ratio >= 0.75 else 0.75 if ratio >= 0.50 else 0.50 if ratio >= 0.25 else 0.0
                housing_pts = rent * h_mult
                monthly_cash_earned = 0
                cash_spent_on_rent = 0
            else:
                # Flexible Strategy
                monthly_cash_earned = total_everyday * 0.04
                cash_needed_for_max = (rent / 1000) * 30
                cash_spent_on_rent = min(monthly_cash_earned, cash_needed_for_max)
                housing_pts = (cash_spent_on_rent / 30) * 1000

            # 3. METRICS
            total_monthly_pts = base_spend_pts + housing_pts
            final_monthly_cash = monthly_cash_earned - cash_spent_on_rent
            
            st.metric("Total Monthly Points", f"{int(total_monthly_pts):,}", f"{int(housing_pts):,} from Housing")
            st.metric("Net Monthly Bilt Cash", f"${final_monthly_cash:,.2f}")

            with st.expander("Monthly 'Before & After' Detail"):
                st.write("**Point Breakdown:**")
                st.write(f"- Spending Points (Before Rent): {int(base_spend_pts):,}")
                st.write(f"- Housing Points Added: +{int(housing_pts):,}")
                st.write("**Cash Breakdown:**")
                st.write(f"- Bilt Cash Earned (4%): ${monthly_cash_earned:,.2f}")
                st.write(f"- Bilt Cash Burned for Rent: -${cash_spent_on_rent:,.2f}")

            st.divider()
            
            # 4. YEARLY PROJECTION
            st.write("### Yearly Projection")
            yearly_pts = total_monthly_pts * 12
            yearly_cash = (final_monthly_cash * 12) + s['annual_credits'] + s['signup_cash']
            net_value = (yearly_pts * 0.02) + yearly_cash - s['fee'] # Assumes 2cpp valuation
            
            y_data = {
                "Item": ["Annual Points", "Annual Bilt Cash", "Annual Fee", "Est. Net Value*"],
                "Value": [f"{int(yearly_pts):,}", f"${yearly_cash:,.2f}", f"-${s['fee']}", f"${net_value:,.2f}"]
            }
            st.table(pd.DataFrame(y_data))
            
            # 5. PERKS
            st.write("**Key Benefits:**")
            for perk in s['perks']:
                st.markdown(f"- {perk}")

    st.caption("*Net Value assumes Bilt Points are worth 2 cents per point (2.0 cpp).")

if __name__ == "__main__":
    calculate_rewards()
