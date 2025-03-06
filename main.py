import streamlit as st
import pandas as pd

st.set_page_config(page_title='Stock Average Down Calculator', page_icon='', layout='wide')
st.markdown('<h2 style="text-align:center">Stock Average Down Calculator for Day Traders</h2>',
            unsafe_allow_html=True)

# Session state to store trades
if 'trades' not in st.session_state:
    st.session_state.trades = []


# Function to calculate the average cost
def calculate_average(trades):
    total_cost = 0
    total_shares = 0

    for trade in trades:
        action, shares, price = trade
        if action == 'Buy':
            total_cost += shares * price
            total_shares += shares
        elif action == 'Sell':
            if total_shares > 0:
                avg_price = total_cost / total_shares if total_shares else 0
                cost_removed = min(shares, total_shares) * avg_price
                total_cost -= cost_removed
                total_shares -= shares

    avg_cost = (total_cost / total_shares) if total_shares > 0 else 0
    return avg_cost, total_shares


# Layout
layout1, layout2 = st.columns(2)

with layout1:
    action = st.selectbox('Trade Type', ['Buy', 'Sell'], help='The share type (Buy or Sell)')
    shares = st.number_input('\\# of Shares', min_value=1, step=1, help='The number of shares purchased')
    price = st.number_input('Price per Share',
                            min_value=0.01,
                            step=0.01,
                            format='%.2f',
                            help='The price of the bought share')

    add_trade_btn, remove_trade_btn, reverse_trades_btn, clear_trades_btn = st.columns(4)

    with add_trade_btn:
        if st.button('Add Trade'):
            st.session_state.trades.append((action, shares, price))

    with remove_trade_btn:
        if st.button('Remove Last Trade') and st.session_state.trades:
            st.session_state.trades.pop()

    with reverse_trades_btn:
        if st.button('Reverse Trades') and st.session_state.trades:
            st.session_state.trades.reverse()

    with clear_trades_btn:
        if st.button('Clear All Trades') and st.session_state.trades:
            st.session_state.trades.clear()

with layout2:
    if st.session_state.trades:
        df = pd.DataFrame(st.session_state.trades, columns=['Action', 'Shares', 'Price'])

        # Make DataFrame editable
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            num_rows='dynamic',
            column_config={
                'Action': st.column_config.SelectboxColumn(
                    'Action',
                    options=['Buy', 'Sell'],
                    required=True
                ),
                'Shares': st.column_config.NumberColumn(
                    'Shares',
                    min_value=1,
                    step=1,
                    required=True
                ),
                'Price': st.column_config.NumberColumn(
                    'Price',
                    min_value=0.01,
                    step=0.01,
                    format='$ %.2f',
                    required=True
                )
            }
        )

        # Save the edited DataFrame back to session state
        st.session_state.trades = edited_df.values.tolist()

        # Calculate and display average cost
        avg_price, remaining_shares = calculate_average(st.session_state.trades)
        st.markdown(f'**Remaining Shares:** {int(remaining_shares)}')
        st.markdown(f'**Average Cost per Share:** ${avg_price:.2f}')

    else:
        st.write('No trades entered yet.')

st.markdown('''_Copyright (©) Keller Hydle_ 
###### Warning: this calculator cannot guarantee perfect results''')
