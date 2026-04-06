# A fake distance sensor for beginner autonomous-driving logic.
# Change the number below to test different decisions.

distance_meters = 8

print("Fake distance sensor online.")
print(f"Distance reading: {distance_meters} meters")

if distance_meters <= 2:
    print("Decision: STOP")
elif distance_meters <= 5:
    print("Decision: SLOW")
else:
    print("Decision: MOVE")

