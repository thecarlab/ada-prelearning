# A tiny driving decision script.
# It combines fake distance and fake lane status into one action.

distance_meters = 8
lane_status = "center"

stop_distance = 2
slow_distance = 5

driver_message = "Nice focus, ADA driver!"

print("ADA drive decision check")
print(f"Distance: {distance_meters} meters")
print(f"Lane: {lane_status}")

# Safety comes first: distance rules are checked before lane rules.
if distance_meters <= stop_distance:
    decision = "STOP"
elif distance_meters <= slow_distance:
    decision = "SLOW"
elif lane_status == "left":
    decision = "TURN RIGHT"
elif lane_status == "right":
    decision = "TURN LEFT"
elif lane_status == "center":
    decision = "MOVE"
else:
    decision = "SLOW"

print(f"Decision: {decision}")
print(driver_message)

