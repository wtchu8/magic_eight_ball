#!/usr/bin/env python3

import streamlit as st
import random
import json

def main():
    run_streamlit()

def run_streamlit():
    # first_roll=False

    st.title("The Magic Eight Ball")

    dr = DiceRoller()

    dr.mode = st.selectbox("Pick a Mode", dr.get_mode_list())

    dr.set_options_from_mode()

    if len(dr.options) > 0:
        opt_str = dr.get_option_list_string()

        st.write(opt_str)

        if st.button("Roll"):
            # first_roll=True
            dr.roll_dice()

        # if first_roll:
            st.write(f"This is your fate: {dr.result}")


class DiceRoller:
    def __init__(self, mode="yn"):
        # custom is not ready yet
        self.mode_list = ["Yes or No", "Games", "Dice"]#, "Custom"]
        self.mode=mode
        self.options=[]
        # self.set_options_from_mode()
        self.result = None

    def roll_dice(self):
        self.result = random.choice(self.options)
        return self.result

    def set_options_from_mode(self):
        if self.mode == "Yes or No":
            self.options = ["Yes", "No"]
        elif self.mode == "Games":
            n_players = st.slider("Number of Players", min_value=1, max_value=14, value=5)
            self.options = self.get_vgame_options(n_players)
        elif self.mode == "Dice":
            n_sided_dice = st.slider("Number of sides of die", 1, 20)
            self.options = list(range(1,n_sided_dice+1))
        elif self.mode == "Custom":
            self.options = self.get_custom_options()
        else:
            raise ValueError(f"Invalid mode: {self.mode}")

    def get_mode_list(self):
        return self.mode_list

    def append_to_options(self, item):
        self.options.append(item)

    def get_options(self):
        return self.options
    
    def get_option_list_string(self):
        opt_str = f"These are your options: {self.options[0]}"

        for name in self.options[1:-1]:
            opt_str += f", {name}"
        
        if len(self.options) > 2:
            opt_str += ","

        if len(self.options) > 1:
            opt_str += f" or {self.options[-1]}"

        return opt_str

    def get_vgame_options(self, n, custom_games=False):
        vgame_max_players = self.get_vgame_max_players_dict()
        return [name for name,data in  vgame_max_players.items() if data['Max'] >= n]

    def get_vgame_max_players_dict(self):
        with open('game_max.json','rt', encoding='utf-8') as f:
            out_dict = json.load(f)
        return out_dict

    def get_custom_options(self):

        # Initialize the list in session state if not present
        if "option_list" not in st.session_state:
            st.session_state["option_list"] = []

        # Text input to add a new option, with an `on_change` callback
        st.text_input("Add an option", key="new_option", on_change=self.add_option)

        # Display options with a remove button next to each
        st.write("Options:")
        for i, option in enumerate(st.session_state["option_list"]):
            col1, col2 = st.columns([2, 8])
            with col1:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state["option_list"].pop(i)
                    st.experimental_rerun()  # Rerun to update the list immediately after removal
            with col2:
                st.write(option)

        return st.session_state["option_list"]

    def add_option(self):
        # Append the new option to the list and clear the input field
        if st.session_state["new_option"] and st.session_state["new_option"] not in st.session_state["option_list"]:
            st.session_state["option_list"].append(st.session_state["new_option"])
        st.session_state["new_option"] = ""  # Clear the input field after adding

if __name__ == "__main__":
    main()