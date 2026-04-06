# A tiny smart-car assistant for beginner Python practice.
# Type commands and watch the vehicle state change.

assistant_name = "ADA Vehicle Assistant"

# A dictionary keeps related vehicle information together.
vehicle_state = {
    "battery_percent": 80,
    "readiness": "parked",
    "speed_mode": "safe",
    "last_action": "PARK",
}

# A list remembers what commands the driver tried.
command_history = []


def print_status(state, history):
    """Show the current vehicle state."""
    print(f"Readiness: {state['readiness']}")
    print(f"Battery: {state['battery_percent']}%")
    print(f"Speed mode: {state['speed_mode']}")
    print(f"Last action: {state['last_action']}")
    print(f"Commands tried: {len(history)}")


def set_action(state, action):
    """Save and print the newest vehicle action."""
    state["last_action"] = action
    print(f"Action: {action}")


def charge_battery(state, amount):
    """Charge the battery without going above 100 percent."""
    state["battery_percent"] = min(100, state["battery_percent"] + amount)


print(f"{assistant_name} online.")
print("Type one command: start, drive, park, charge, horn, status, or quit.")

while True:
    command = input("> ").strip().lower()
    command_history.append(command)

    if command == "quit":
        print("Assistant shutting down. See you at ADA camp!")
        break

    elif command == "start":
        vehicle_state["readiness"] = "ready"
        print("Vehicle systems ready.")
        set_action(vehicle_state, "START")

    elif command == "drive":
        if vehicle_state["readiness"] == "ready":
            vehicle_state["speed_mode"] = "campus cruise"
            vehicle_state["battery_percent"] = vehicle_state["battery_percent"] - 5
            print("Rolling forward carefully.")
            set_action(vehicle_state, "MOVE")
        else:
            print("Please use start before drive.")
            set_action(vehicle_state, "PARK")

    elif command == "park":
        vehicle_state["readiness"] = "parked"
        vehicle_state["speed_mode"] = "safe"
        print("Parking mode on.")
        set_action(vehicle_state, "PARK")

    elif command == "charge":
        charge_battery(vehicle_state, 10)
        print("Charging the vehicle battery.")
        set_action(vehicle_state, "CHARGE")

    elif command == "horn":
        print("Beep beep from the ADA vehicle!")
        set_action(vehicle_state, "HONK")

    elif command == "status":
        print_status(vehicle_state, command_history)

    else:
        print("I do not know that command yet.")
        print("Try: start, drive, park, charge, horn, status, or quit.")
