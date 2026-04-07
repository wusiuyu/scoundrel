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

# Sidebar: Game Rules
st.sidebar.title("📜 Game Rules")

# Inject CSS that adapts to both light and dark mode
st.sidebar.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        color: inherit; /* use theme default */
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] h5, 
    [data-testid="stSidebar"] h6 {
        color: inherit; /* headings follow theme */
    }
    [data-testid="stSidebar"] p {
        color: rgba(255,255,255,0.85); /* light text in dark mode */
    }
    @media (prefers-color-scheme: light) {
        [data-testid="stSidebar"] p {
            color: rgba(0,0,0,0.85); /* dark text in light mode */
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("""
**Scoundrel Dungeon Rules**

- Each round you draw 3 or 4 cards  
- Choose 3 cards, leave 1 for next round  
- First Potion (♥️) heals, rest are discarded  
- Start with bare hand, Equip or Replace a weapon (♦️)  
- Monsters (♠️/♣️) deal damage, minus str of weapon  
- Weapon only deals damage if monster is weaker than last one  
- You can dump all 4 cards to the bottom, but not twice in a row  
- Survive until the deck runs out to win!
""")

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

if "last_round_skip" not in st.session_state:
    st.session_state.last_round_skip = False

if "draw_used" not in st.session_state:
    st.session_state.draw_used = False

# -----------------------------
# Player Status Panel (adaptive layout)
# -----------------------------
st.markdown("###### Player Status")

# Group status items into pairs
status_pairs = [
    ("❤️ Health", st.session_state.health, "⚔️ Weapon", st.session_state.weapon),
    ("📦 Deck", len(st.session_state.deck), "👹 Last Monster",
     st.session_state.last_monster_value if st.session_state.get("last_monster_value") else "None")
]

cols = st.columns(len(status_pairs))

for i, (label1, value1, label2, value2) in enumerate(status_pairs):
    with cols[i]:
        st.markdown(
            f"""
            <div style='background-color:var(--secondary-background-color);
                        color:var(--text-color);
                        padding:15px; text-align:center;
                        font-size:18px; border-radius:8px;'>
                <table style='width:100%; text-align:center;'>
                    <tr>
                        <td><b>{label1}</b> {value1}</td>
                        <td><b>{label2}</b> {value2}</td>
                    </tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )


# -----------------------------
# Action Buttons Row
# -----------------------------
st.markdown("###### Actions")

st.markdown("""
<style>
/* Force two items per row on small screens */
div[data-testid="stHorizontalBlock"] {
    flex-wrap: wrap;
}
div[data-testid="stHorizontalBlock"] > div {
    flex: 1 1 45%;   /* roughly half width */
    min-width: 120px;
}
</style>
""", unsafe_allow_html=True)


# First row: Draw + Confirm
row1 = st.columns(2)
with row1[0]:
    draw_pressed = st.button("🎴 **Draw**", key="draw_button",
                             disabled=st.session_state.draw_used)
with row1[1]:
    confirm_pressed = st.button("✅ **Confirm**", key="confirm_button")

# Second row: Skip + Restart
row2 = st.columns(2)
with row2[0]:
    skip_pressed = st.button("⏭️ **Skip**", key="skip_button")
with row2[1]:
    restart_pressed = st.button("🔄 **Restart**", key="restart_button")

if restart_pressed:
    st.session_state.deck = create_scoundrel_deck()
    st.session_state.health = 20
    st.session_state.weapon = 0
    st.session_state.log = []
    st.session_state.current_draw = []
    st.session_state.leftover = None
    st.session_state.round = 1
    st.session_state.round_potion_used = False
    st.session_state.chosen_cards = []
    st.session_state.draw_used = False
    st.session_state.last_round_skip = False


if draw_pressed:
    if st.session_state.health > 0 and st.session_state.deck:
        needed = 4 if st.session_state.round == 1 else (4 if st.session_state.last_round_skip else 3)
        draw_count = min(needed, len(st.session_state.deck))

        if len(st.session_state.deck) <= 2:
            st.session_state.current_draw = []
            st.success(f"🏆 You survived the dungeon! Final Health: {st.session_state.health}")
        else:
            draw = [st.session_state.deck.pop(0) for _ in range(draw_count)]
            if st.session_state.round > 1 and st.session_state.leftover:
                draw.insert(0, st.session_state.leftover)

            st.session_state.current_draw = draw
            st.session_state.chosen_cards = []
            st.session_state.round_potion_used = False

        # Mark draw as used
        st.session_state.draw_used = True
        st.rerun()
    else:
        st.session_state.log.append("No more cards or you are dead!")


# Define emoji mapping once
emoji_map = {
    "H": "❤️",  # Potion
    "D": "⚔️",  # Weapon
    "S": "👹",  # Monster (Spades)
    "C": "👹"   # Monster (Clubs)
}

if st.session_state.current_draw:
    st.markdown(f"###### Round {st.session_state.round} - Your Drawn Cards")
    cols = st.columns(len(st.session_state.current_draw))
    for i, card in enumerate(st.session_state.current_draw):
        with cols[i]:
            selected = card in st.session_state.chosen_cards
            suit = card[-1]
            emoji = emoji_map.get(suit, "")
            label = f"{emoji} {card}" + (" ✅" if selected else "")
            if st.button(label, key=f"card_{st.session_state.round}_{i}"):
                if selected:
                    st.session_state.chosen_cards.remove(card)
                else:
                    if len(st.session_state.chosen_cards) < 3:
                        st.session_state.chosen_cards.append(card)
    chosen_display = [f"{emoji_map.get(c[-1], '')} {c}" for c in st.session_state.chosen_cards]
    st.write("Chosen cards: " + ", ".join(chosen_display))

    # Normal confirm
    if confirm_pressed and len(st.session_state.chosen_cards) == 3:
        for card in st.session_state.chosen_cards:
            result = apply_card(card, st.session_state)
            st.session_state.log.append(result)
        leftover = [c for c in st.session_state.current_draw if c not in st.session_state.chosen_cards]
        st.session_state.leftover = leftover[0] if leftover else None
        st.session_state.current_draw = []
        st.session_state.round += 1
        st.session_state.chosen_cards = []
        st.session_state.last_round_skip = False  # reset skip flag when playing normally
        st.session_state.draw_used = False
        st.rerun()

    # New skip option
    if skip_pressed:
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
            st.session_state.draw_used = False
            st.rerun()
            st.info("All cards placed at the bottom of the deck.")

st.markdown("###### Adventure Log")
for entry in st.session_state.log[::-1]:
    st.write(entry)

if st.session_state.health <= 0:
    st.error("💀 You died in the dungeon!")
elif not st.session_state.deck and not st.session_state.current_draw:
    st.success(f"🏆 You survived the dungeon! Final Health: {st.session_state.health}")