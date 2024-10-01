import numpy as np
import pandas as pd
import random
import itertools 
import os
from collections import defaultdict
import json
import random
import numpy as np
from time import time
from tqdm import tqdm


def load_process_simulations(path): 
    simulations = np.load(path)
    def int_to_bit(n):
        binary = bin(n)[2:] 
        return binary.zfill(52)
    binary_simulations = [int_to_bit(sim) for sim in simulations]             
    return binary_simulations

def variation1(deck, player1_sequence, player2_sequence):
    player1_cards = 0
    player2_cards = 0
    pile = 0
    i = 0
    
    while i < len(deck) - 2:
        current_sequence = deck[i:i+3]
        pile += 1
        if current_sequence == player1_sequence:
            player1_cards += pile
            pile = 0
            i += 3
        elif current_sequence == player2_sequence:
            player2_cards += pile
            pile = 0 
            i += 3
        else:
            i += 1
    return player1_cards, player2_cards


def variation2(deck, player1_sequence, player2_sequence):
    player1_tricks = 0
    player2_tricks = 0
    i = 0
    
    while i < len(deck) - 2:
        current_sequence = deck[i:i+3]
        if current_sequence == player1_sequence:
            player1_tricks += 1
            i += 3
        elif current_sequence == player2_sequence:
            player2_tricks += 1
            i += 3
        else:
            i += 1
    return player1_tricks, player2_tricks


def analyze_all_combinations(simulations):
    all_sequences = ['{:03b}'.format(i) for i in range(8)]  # Generate sequences as '000', '001', etc.
    results_v1 = []
    results_v2 = []

    total_iterations = len(all_sequences) * (len(all_sequences) - 1)  # Total number of (p1, p2) pairs

    with tqdm(total=total_iterations, desc="Processing Pairs") as pbar:
        for p1 in all_sequences:
            for p2 in all_sequences:

                if p1 != p2:
                    p1_wins_v1, p2_wins_v1 = 0, 0
                    p1_wins_v2, p2_wins_v2 = 0, 0

                    for game in simulations:
                        p1_cards_v1, p2_cards_v1 = variation1(game, p1, p2)
                        if p1_cards_v1 > p2_cards_v1:
                            p1_wins_v1 += 1
                        elif p2_cards_v1 > p1_cards_v1:
                            p2_wins_v1 += 1
                    
                        p1_cards_v2, p2_cards_v2 = variation2(game, p1, p2)
                        if p1_cards_v2 > p2_cards_v2:
                            p1_wins_v2 += 1
                        elif p2_cards_v2 > p1_cards_v2:
                            p2_wins_v2 += 1
                    
                    results_v1.append({
                        'Sequence 1': p1, 
                        'Sequence 2': p2, 
                        'Player 1 Wins': p1_wins_v1, 
                        'Player 2 Wins': p2_wins_v1, 
                        'Player 1 Win %': round((p1_wins_v1/(p1_wins_v1 + p2_wins_v1))*100, 2)
                    })
                    results_v2.append({
                        'Sequence 1': p1, 
                        'Sequence 2': p2, 
                        'Player 1 Wins': p1_wins_v2, 
                        'Player 2 Wins': p2_wins_v2, 
                        'Player 1 Win %': round((p1_wins_v2/(p1_wins_v2 + p2_wins_v2))*100, 2) 
                    })

                    pbar.update(1)

    aggreg_df1 = pd.DataFrame(results_v1)
    aggreg_df2 = pd.DataFrame(results_v2)

    # Ensure 'Sequence 1' and 'Sequence 2' are treated as strings
    aggreg_df1['Sequence 1'] = aggreg_df1['Sequence 1'].astype(str)
    aggreg_df1['Sequence 2'] = aggreg_df1['Sequence 2'].astype(str)
    aggreg_df2['Sequence 1'] = aggreg_df2['Sequence 1'].astype(str)
    aggreg_df2['Sequence 2'] = aggreg_df2['Sequence 2'].astype(str)

    return aggreg_df1, aggreg_df2


def combine_past_data(new_var1, new_var2, var1_existing_filename, var2_existing_filename, folder='data'):
    var1_existing_path = os.path.join(folder, var1_existing_filename)
    var2_existing_path = os.path.join(folder, var2_existing_filename)
    
    if os.path.exists(var1_existing_path):
        existing_var1 = pd.read_csv(var1_existing_path, dtype={'Sequence 1': str, 'Sequence 2': str})
    else:
        existing_var1 = pd.DataFrame(columns=['Sequence 1', 'Sequence 2', 'Player 1 Wins', 'Player 2 Wins', 'Player 1 Win %'])
        
    if os.path.exists(var2_existing_path):
        existing_var2 = pd.read_csv(var2_existing_path, dtype={'Sequence 1': str, 'Sequence 2': str})
    else:
        existing_var2 = pd.DataFrame(columns=['Sequence 1', 'Sequence 2', 'Player 1 Wins', 'Player 2 Wins', 'Player 1 Win %'])

    # Ensure all sequences are 3 digits for both new and existing data
    for df in [new_var1, new_var2, existing_var1, existing_var2]:
        if not df.empty:
            df['Sequence 1'] = df['Sequence 1'].apply(lambda x: x.zfill(3))
            df['Sequence 2'] = df['Sequence 2'].apply(lambda x: x.zfill(3))
    
    # Combine existing and new data for v 1
    variation1_combined = update_dataframe(existing_var1, new_var1)

    # Combine existing and new data for v 2
    variation2_combined = update_dataframe(existing_var2, new_var2)

    # Save the combined data back to csv
    variation1_combined.to_csv(var1_existing_path, index=False)
    variation2_combined.to_csv(var2_existing_path, index=False)

    return variation1_combined, variation2_combined

def update_dataframe(existing_df, new_df):
    # If there is no existing data, return the new data
    if existing_df.empty:
        return new_df

    # Ensure that Sequence 1 and Sequence 2 have the same identifiers
    new_df = new_df.copy()
    new_df['Sequence 1'] = new_df['Sequence 1'].apply(lambda x: x.zfill(3))
    new_df['Sequence 2'] = new_df['Sequence 2'].apply(lambda x: x.zfill(3))

    existing_df['Sequence 1'] = existing_df['Sequence 1'].apply(lambda x: x.zfill(3))
    existing_df['Sequence 2'] = existing_df['Sequence 2'].apply(lambda x: x.zfill(3))

    # Add the values for Player 1 Wins and Player 2 Wins without changing row order
    existing_df['Player 1 Wins'] = existing_df['Player 1 Wins'] + new_df['Player 1 Wins']
    existing_df['Player 2 Wins'] = existing_df['Player 2 Wins'] + new_df['Player 2 Wins']

    # Recalculate Player 1 Win Percentage based on updated totals
    total_games = existing_df['Player 1 Wins'] + existing_df['Player 2 Wins']
    existing_df['Player 1 Win %'] = (existing_df['Player 1 Wins'] / total_games * 100).fillna(0).round(2)

    return existing_df






    

    
