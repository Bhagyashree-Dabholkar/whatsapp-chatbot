import json
import os

STATE_FILE = "conversation_state.json"

# Load state from file
def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r") as file:
        return json.load(file)

# Save updated state to file
def save_state(state):
    with open(STATE_FILE, "w") as file:
        json.dump(state, file, indent=2)

# ✅ Get the current conversation step of the user
def get_user_step(user_id):
    state = load_state()
    return state.get(user_id, {}).get("step", "location")

# ✅ Update just the step (not answer values)
def update_user_step(user_id, step):
    state = load_state()
    user_state = state.get(user_id, {})
    user_state["step"] = step
    state[user_id] = user_state
    save_state(state)

# ✅ Save user's response (like location, company, etc.)
def save_user_response(user_id, key, value):
    state = load_state()
    user_state = state.get(user_id, {})
    user_state[key] = value
    state[user_id] = user_state
    save_state(state)
