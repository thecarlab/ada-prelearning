# A fake lane checker for beginner autonomous-driving logic.
# Try changing lane_status to "center", "left", or "right".

lane_status = "center"

print("Fake lane checker online.")
print(f"Lane status: {lane_status}")

if lane_status == "center":
    print("Decision: KEEP GOING")
elif lane_status == "left":
    print("Decision: TURN RIGHT")
elif lane_status == "right":
    print("Decision: TURN LEFT")
else:
    print("Decision: SLOW")

