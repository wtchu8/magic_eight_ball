#!/usr/bin/env python3

import streamlit as st
import random
import json

def main():
    run_streamlit()

def run_streamlit():
    first_roll=False

    st.title("The Magic Eight Ball")

    dr = DiceRoller()

    dr.mode = st.selectbox("Pick a Mode", dr.get_mode_dict())

    dr.set_options_from_mode()

    opt_str = f"These are your options: "
    for name in dr.options:
        opt_str += f"{name}, "
    st.write(opt_str)

    if st.button("Roll"):
        first_roll=True
        dr.roll_dice()

    if first_roll:
        st.write(f"You all shall play: {dr.result}")


class DiceRoller:
    def __init__(self, mode="yn"):
        self.mode=mode
        self.set_options_from_mode()
        self.result = None

    def roll_dice(self):
        self.result = random.choice(self.options)
        return self.result

    def set_options_from_mode(self):
        if self.mode in self.get_mode_dict():
            self.options=self.get_mode_dict()[self.mode]
        else:
            self.options=[]

    def get_mode_dict(self):
        vgame_modes = {f"{n}+ Player Games":self.get_vgame_options(n) for n in range(6,1,-1)}
        dice_modes = {f"{n}-sided Dice": list(range(1,n+1)) for n in range(3,21)}
        mode_dict = {
            **vgame_modes,
            "Yes or No": ["Yes", "No"],
            **dice_modes
        }
        return mode_dict

    def get_modes(self):
        return list(self.get_mode_dict().keys())

    def append_to_options(self, item):
        self.options.append(item)

    def get_options(self):
        return self.options

    def get_vgame_options(self, n, custom_games=False):
        vgame_max_players = self.get_vgame_max_players_dict()
        return [name for name,data in  vgame_max_players.items() if data['Max'] >= n]

    def get_vgame_max_players_dict(self):
        with open('game_max.json','rt', encoding='utf-8') as f:
            out_dict = json.load(f)
        return out_dict

if __name__ == "__main__":
    main()