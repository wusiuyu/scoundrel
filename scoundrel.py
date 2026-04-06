# Leisure Project to play scoundrel on webapp
# streamlit run "C:\Projects\Project 038 Scoundrel\src\scoundrel.py"

import random
import streamlit as st

# -----------------------------
# Deck Setup
# -----------------------------
suits = ["S", "H", "D", "C"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def create_scoundrel_deck():
    deck = []
    for suit in suits:
        for rank in ranks:
            if suit in ["H", "D"] and rank in ["J", "Q", "K", "A"]:
                continue
            deck.append(f"{rank}{suit}")
    random.shuffle(deck)
    return deck

def card_value(card):
    rank = card[:-1]
    return ranks.index(rank) + 2

# -----------------------------
# Card Effects
# -----------------------------
def apply_card(card, state):
    suit = card[-1]
    value = card_value(card)

    if suit == "H":  # Potion
        if not state["round_potion_used"]:  # only first potion in this round works
            state["round_potion_used"] = True
            last_round = len(state["deck"]) == 0 and not state["current_draw"]
            if last_round:
                state["health"] += value
                return f"{card}: Final potion heals +{value} HP (health can exceed 20)"
            else:
                heal_amount = min(value, 20 - state["health"])
                state["health"] += heal_amount
                return f"{card}: Potion heals +{heal_amount} HP (max 20)"
        else:
            return f"{card}: Extra potion discarded (only first potion in round is effective)"

    elif suit == "D":  # Weapon
        old_weapon = state["weapon"]
        state["weapon"] = value
        state["last_monster_value"] = None  # reset monster memory when weapon changes
        if old_weapon == 0:
            return f"{card}: Equipped weapon (strength {value})"
        else:
            return f"{card}: Replaced weapon {old_weapon} → {value}"

    else:  # Monster (S or C)
        # Check weapon effectiveness based on last monster value
        if state["weapon"] > 0:
            if state["last_monster_value"] is None or value < state["last_monster_value"]:
                damage = max(0, value - state["weapon"])
                state["health"] -= damage
                state["last_monster_value"] = value  # remember this monster’s strength
                if damage == 0:
                    return f"{card}: Monster (strength {value}) defeated with weapon!"
                else:
                    return f"{card}: Monster (strength {value}) dealt {damage} damage (weapon reduced)"
            else:
                # Weapon ineffective against equal/stronger monster
                state["health"] -= value
                return f"{card}: Monster (strength {value}) ignored weapon (too strong), full {value} damage!"
        else:
            # No weapon equipped
            state["health"] -= value
            return f"{card}: Monster (strength {value}) dealt {value} damage (no weapon)"

# -----------------------------
# Helper: Card Display
# -----------------------------
def card_display(card):
    suit = card[-1]
    if suit == "H":
        return f"<div style='background-color:#ffcccc; padding:20px; text-align:center; font-size:24px; border-radius:10px;'>❤️ {card}</div>"
    elif suit == "D":
        return f"<div style='background-color:#fff3cd; padding:20px; text-align:center; font-size:24px; border-radius:10px;'>⚔️ {card}</div>"
    else:
        return f"<div style='background-color:#cce5ff; padding:20px; text-align:center; font-size:24px; border-radius:10px;'>👹 {card}</div>"

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🃏 Scoundrel Dungeon Game")

if "deck" not in st.session_state:
    st.session_state.deck = create_scoundrel_deck()
    st.session_state.health = 20
    st.session_state.weapon = 0
    st.session_state.log = []
    st.session_state.current_draw = []
    st.session_state.leftover = None
    st.session_state.round = 1
    st.session_state.round_potion_used = False
    st.session_state.chosen_cards = []

# Initialize new flag
if "last_round_skip" not in st.session_state:
    st.session_state.last_round_skip = False


if st.button("Restart Game"):
    st.session_state.deck = create_scoundrel_deck()
    st.session_state.health = 20
    st.session_state.weapon = 0
    st.session_state.log = []
    st.session_state.current_draw = []
    st.session_state.leftover = None
    st.session_state.round = 1
    st.session_state.round_potion_used = False
    st.session_state.chosen_cards = []

if st.session_state.leftover and not st.session_state.current_draw:
    st.info(f"Carried over from last round: {st.session_state.leftover}")

draw_pressed = st.button("Draw Cards")

if draw_pressed:
    if st.session_state.health > 0 and st.session_state.deck:
        needed = 4 if st.session_state.round == 1 else (4 if st.session_state.last_round_skip else 3)
        draw_count = min(needed, len(st.session_state.deck))

        if len(st.session_state.deck) <= 2:
            st.session_state.current_draw = []
            st.success(f"🏆 You survived the dungeon! Final Health: {st.session_state.health}")
        else:
            # Draw from the front of the deck
            draw = [st.session_state.deck.pop(0) for _ in range(draw_count)]
            if st.session_state.round > 1 and st.session_state.leftover:
                draw.insert(0, st.session_state.leftover)

            st.session_state.current_draw = draw
            st.session_state.chosen_cards = []
            st.session_state.round_potion_used = False
    else:
        st.session_state.log.append("No more cards or you are dead!")


if st.session_state.current_draw:
    st.subheader(f"Round {st.session_state.round} - Your Drawn Cards")
    cols = st.columns(len(st.session_state.current_draw))

    for i, card in enumerate(st.session_state.current_draw):
        with cols[i]:
            st.markdown(card_display(card), unsafe_allow_html=True)

            label = "Deselect" if card in st.session_state.chosen_cards else "Select"
            if st.button(label, key=f"toggle_{st.session_state.round}_{i}"):
                if card in st.session_state.chosen_cards:
                    st.session_state.chosen_cards.remove(card)
                else:
                    if len(st.session_state.chosen_cards) < 3:
                        st.session_state.chosen_cards.append(card)

    st.write(f"Chosen cards: {', '.join(st.session_state.chosen_cards)}")


    # Normal confirm
    if len(st.session_state.chosen_cards) == 3 and st.button("Confirm Choices"):
        for card in st.session_state.chosen_cards:
            result = apply_card(card, st.session_state)
            st.session_state.log.append(result)
        leftover = [c for c in st.session_state.current_draw if c not in st.session_state.chosen_cards]
        st.session_state.leftover = leftover[0] if leftover else None
        st.session_state.current_draw = []
        st.session_state.round += 1
        st.session_state.chosen_cards = []
        st.session_state.last_round_skip = False  # reset skip flag when playing normally

    # New skip option
    if st.button("Put All Cards to Bottom"):
        if st.session_state.last_round_skip:
            st.warning("You cannot skip two rounds in a row!")
        else:
            # Move all current cards to bottom of deck
            st.session_state.deck = st.session_state.deck + st.session_state.current_draw
            # Clear state so leftover doesn’t persist
            st.session_state.current_draw = []
            st.session_state.chosen_cards = []
            st.session_state.leftover = None
            st.session_state.round += 1
            st.session_state.last_round_skip = True
            st.info("All cards placed at the bottom of the deck.")

# -----------------------------
# Player Status Panel
# -----------------------------
st.subheader("Player Status")
st.write(f"Health: {st.session_state.health}")
st.write(f"Weapon Strength: {st.session_state.weapon}")
st.write(f"Remaining Cards in Deck: {len(st.session_state.deck)}")

# Show remembered monster value
if "last_monster_value" in st.session_state and st.session_state.last_monster_value is not None:
    st.write(f"Last Monster Blocked: {st.session_state.last_monster_value}")
else:
    st.write("Last Monster Blocked: None")

st.subheader("Adventure Log")
for entry in st.session_state.log[::-1]:
    st.write(entry)

if st.session_state.health <= 0:
    st.error("💀 You died in the dungeon!")
elif not st.session_state.deck and not st.session_state.current_draw:
    st.success(f"🏆 You survived the dungeon! Final Health: {st.session_state.health}")