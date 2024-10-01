import numpy as np
import pandas as pd
import os
import itertools

def score_deck(deck: str,
               seq1: str,
               seq2: str) -> tuple[int]:
    return p1_cards, p2_cards, p1_tricks, p2_tricks

def calculate_winner(p1_cards: int,
                     p2_cards: int,
                     p1_tricks: int,
                     p2_tricks: int):
    cards_winner = 0
    cards_draw = 0
    tricks_winner = 0
    tricks_draw = 0

    # if p2 wins set winner to 1, otherwise it is 0 (including draws).
    # if there is a draw, set draw counter to 1
    if p1_cards < p2_cards:
        cards_winner = 1
    elif p1_cards == p2_cards:
        cards_draw = 1
    if p1_tricks < p2_tricks:
        tricks_winner = 1
    elif p1_cards == p2_cards:
        tricks_draw = 1
    return cards_winner, cards_draw, tricks_winner, tricks_draw

def play_one_deck(deck: str,
                  data: str):
    sequences = ['000', '001', '010', '011', '100', '101', '110', '111']
    combinations = itertools.product(sequences, repeat=2)
    p2_wins_cards = pd.DataFrame(columns=sequences, index=sequences)
    p2_wins_tricks = pd.DataFrame(columns=sequences, index=sequences)
    draws_cards = pd.DataFrame(columns=sequences, index=sequences)
    draws_tricks = pd.DataFrame(columns=sequences, index=sequences)

    for seq1, seq2 in combinations:
        cards_winner, cards_draw, tricks_winner, tricks_draw = calculate_winner(score_deck(deck, seq1, seq2))
        p2_wins_cards.at[seq1, seq2] = cards_winner
        draws_cards.at[seq1, seq2] = cards_draw
        p2_wins_tricks.at[seq1, seq2] = tricks_winner
        draws_tricks.at[seq1, seq2] = tricks_draw
    
    deck_name = str(int(deck, 2))
    np.save(f'{data}cards_win/{deck_name}.npy', p2_wins_cards, allow_pickle = True)
    np.save(f'{data}tricks_win/{deck_name}.npy', p2_wins_tricks, allow_pickle = True)
    np.save(f'{data}cards_draw/{deck_name}.npy', draws_cards, allow_pickle = True)
    np.save(f'{data}tricks_draw/{deck_name}.npy', draws_tricks, allow_pickle = True)

def sum_games(data: str, average: bool):
    '''Take all of the arrays in the /data folder, and add them together/divide by number of files to get the average'''
    files = [file for file in os.listdir(data) if os.path.isfile(os.path.join(data, file))] # iterate through /data directory, only process files
    games_total = None # where the sum of the games is going
    for file in files:
        file_path = os.path.join(data,file) # get file name and directory
        game = np.load(file_path, allow_pickle=True) # load the file
        if games_total is None:
            games_total = game # initialize games_total sum array
        else:
            games_total += game
    num_games = len(files)
    if average:
        return np.divide(games_total, num_games)
    return games_total # divide each individual element by the number of games played

def iterate (deck: ):
    pass

    return
# take in a deck and iterate through all possible combos of 

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
