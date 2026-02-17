import streamlit as st
import pandas as pd

def calculate_rewards():
    st.set_page_config(page_title="Bilt 2.0 Conversion Dashboard", layout="wide")
    st.title("💳 Bilt 2.0: Before vs. After Conversion")
    
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
    cards = {
        "Bilt Blue": {"fee": 0, "d": 1, "g": 1, "t": 1, "o": 1},
        "Bilt Obsidian": {"fee": 95, "d": 3, "g": 3, "t": 2, "o": 1},
        "Bilt Palladium": {"fee": 495, "d": 2, "g": 2, "t": 2, "o": 2}
    }

    cols = st.columns(3)

    for i, (name, specs) in enumerate(cards.items()):
        with cols[i]:
            st.markdown(f"### {name}")
            
            # 1. PRE-CONVERSION: Points from Spending Only
            if name == "Bilt Obsidian":
                g_pts = min(groceries, 2083) * specs['g'] + max(0, groceries - 2083) * 1
                base_spend_pts = (dining * specs['d']) + g_pts + (travel * specs['t']) + (other * specs['o'])
            else:
                base_spend_pts = (dining * specs['d']) + (groceries * specs['g']) + (travel * specs['t']) + (other * specs['o'])

            # 2. CONVERSION LOGIC
            if strategy == "Housing-only (Tiered Points)":
                ratio = total_everyday / rent if rent > 0 else 0
                h_mult = 1.25 if ratio >= 1.0 else 1.0 if ratio >= 0.75 else 0.75 if ratio >= 0.50 else 0.50 if ratio >= 0.25 else 0.0
                housing_pts = rent * h_mult
                final_cash = 0
                total_pts = base_spend_pts + housing_pts
                
                # Show Base vs Total
                st.metric("Total Monthly Points", f"{int(total_pts):,}", f"+{int(housing_pts):,} from Rent")
                st.write(f"**Strategy:** Tiered {h_mult}x applied")

            else:
                # Flexible Strategy: 4% Cash earned first
                gross_cash = total_everyday * 0.04
                
                # Conversion: $30 Cash = 1000 Pts
                cash_needed_for_max = (rent / 1000) * 30
                cash_spent = min(gross_cash, cash_needed_for_max)
                housing_pts = (cash_spent / 30) * 1000
                final_cash = gross_cash - cash_spent
                total_pts = base_spend_pts + housing_pts

                # Dashboard Display
                st.metric("Total Monthly Points", f"{int(total_pts):,}", f"+{int(housing_pts):,} unlocked")
                st.metric("Remaining Bilt Cash", f"${final_cash:,.2f}")

                # EXPLICIT BEFORE/AFTER TABLE
                st.write("**Conversion Breakdown:**")
                df_data = {
                    "Stage": ["1. Base Spending", "2. Bilt Cash Earned", "3. Bilt Cash Used", "4. FINAL TOTAL"],
                    "Points": [f"{int(base_spend_pts):,}", "-", "-", f"{int(total_pts):,}"],
                    "Bilt Cash": ["-", f"${gross_cash:,.2f}", f"-${cash_spent:,.2f}", f"${final_cash:,.2f}"]
                }
                st.table(pd.DataFrame(df_data))
            
            st.divider()

if __name__ == "__main__":
    calculate_rewards()
