# A tiny smart-car assistant for beginner Python practice.
# Type commands and watch the vehicle state change.

assistant_name = "ADA Vehicle Assistant"

battery_percent = 80
readiness = "parked"
speed_mode = "safe"

print(f"{assistant_name} online.")
print("Type one command: start, drive, park, charge, horn, status, or quit.")

while True:
    command = input("> ").strip().lower()

    if command == "quit":
        print("Assistant shutting down. See you at ADA camp!")
        break

    elif command == "start":
        readiness = "ready"
        print("Vehicle systems ready.")
        print("Action: START")

    elif command == "drive":
        if readiness == "ready":
            speed_mode = "campus cruise"
            battery_percent = battery_percent - 5
            print("Rolling forward carefully.")
            print("Action: MOVE")
        else:
            print("Please use start before drive.")
            print("Action: PARK")

    elif command == "park":
        readiness = "parked"
        speed_mode = "safe"
        print("Parking mode on.")
        print("Action: PARK")

    elif command == "charge":
        battery_percent = min(100, battery_percent + 10)
        print("Charging the vehicle battery.")
        print("Action: CHARGE")

    elif command == "horn":
        print("Beep beep from the ADA vehicle!")
        print("Action: HONK")

    elif command == "status":
        print(f"Readiness: {readiness}")
        print(f"Battery: {battery_percent}%")
        print(f"Speed mode: {speed_mode}")

    else:
        print("I do not know that command yet.")
        print("Try: start, drive, park, charge, horn, status, or quit.")

