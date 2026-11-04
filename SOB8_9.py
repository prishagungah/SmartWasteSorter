import random  
'''Python checks sys.modules cache first; if not cached, it searches sys.path,
loads and runs the module, then binds the name "random" in this program.'''

def read_ultrasonic(min_dist=0.2, max_dist=2.0):
    """Purpose: emulate an ultrasonic sensor reading.
    Parameters: min_dist (float, metres), max_dist (float, metres).
    Returns: float - random distance in metres, rounded to 1 d.p.
    Raises ValueError if min_dist < 0 or min_dist > max_dist."""
    if min_dist < 0 or min_dist > max_dist:
        raise ValueError("min_dist must be >= 0 and <= max_dist")                # Pick a random float in the range and round it to 1 decimal place
    return round(random.uniform(min_dist, max_dist), 1)


def calculate_drive_time(distance, speed=0.5, stop_margin=0.8):
    """Purpose: work out how far and how long the robot drives before stopping.
    Parameters: distance (float, m to obstacle), speed (float, m/s),
                stop_margin (float, m).
    Returns: tuple (distance_driven, time_taken) as floats.
    Raises ValueError if distance < 0 or speed <= 0.""" 
    if distance < 0 or speed <= 0:
        raise ValueError("distance must be >= 0 and speed must be > 0")          # Raises ValueError if distance is negative or speed is zero or negative
    distance_driven = max(0, distance - stop_margin)                             # Drive until stop_margin away; max(0, ...) stops it reversing if already too close
    time_taken = distance_driven / speed
    return distance_driven, time_taken


def choose_turn(left_clearance, right_clearance, heading):
    """Purpose: turn 90 degrees towards the clearer side (right if equal).
    Parameters: left_clearance (float), right_clearance (float),
                heading (int, 0-359 compass degrees).
    Returns: int - new heading (0-359)."""
    if left_clearance > right_clearance:                                         # Left turn only if left is larger 
        return (heading - 90) % 360
    return (heading + 90) % 360                                                  # Otherwise, turn right 


def run_mission(total_distance, speed):
    """Purpose: run the full robot mission and print each leg.
    Parameters: total_distance (float, m to drive), speed (float, m/s).
    Returns: float - total distance driven in metres."""
    heading = 0
    total = 0.0
    while total < total_distance:
        forward = read_ultrasonic()
        driven, time_taken = calculate_drive_time(forward, speed)
        driven = min(driven, total_distance - total)  # cap final leg
        total += driven
        left = read_ultrasonic()
        right = read_ultrasonic()
        heading = choose_turn(left, right, heading)
        print(f"Forward: {forward} m | Driven: {driven:.1f} m | "
              f"Total: {total:.1f} m | Heading: {heading}")
    return total


def test_table():
    """Purpose: run fixed test cases and print a results table.
    Parameters: none.
    Returns: None."""
    tests = []

    # (name, function name, arguments, expected, actual)
    r = read_ultrasonic(0.5, 1.0)
    tests.append(("Sensor in range", "read_ultrasonic", "(0.5, 1.0)",
                  "0.5 <= x <= 1.0", str(r), 0.5 <= r <= 1.0))
    r = read_ultrasonic(1.0, 1.0)
    tests.append(("Sensor min = max", "read_ultrasonic", "(1.0, 1.0)",
                  "1.0", str(r), r == 1.0))
    try:
        read_ultrasonic(-1, 2)
        res = "no error"
    except ValueError:
        res = "ValueError"
    tests.append(("Negative min", "read_ultrasonic", "(-1, 2)",
                  "ValueError", res, res == "ValueError"))
    try:
        read_ultrasonic(3, 2)
        res = "no error"
    except ValueError:
        res = "ValueError"
    tests.append(("Min > max", "read_ultrasonic", "(3, 2)",
                  "ValueError", res, res == "ValueError"))

    r = calculate_drive_time(2.0, 0.5)
    tests.append(("Normal drive", "calculate_drive_time", "(2.0, 0.5)",
                  "(1.2, 2.4)", str((round(r[0], 1), round(r[1], 1))),
                  (round(r[0], 1), round(r[1], 1)) == (1.2, 2.4)))
    r = calculate_drive_time(0.5, 0.5)
    tests.append(("Inside margin", "calculate_drive_time", "(0.5, 0.5)",
                  "(0, 0)", str(r), r == (0, 0)))
    try:
        calculate_drive_time(1.0, 0)
        res = "no error"
    except ValueError:
        res = "ValueError"
    tests.append(("Zero speed", "calculate_drive_time", "(1.0, 0)",
                  "ValueError", res, res == "ValueError"))

    r = choose_turn(1.5, 0.5, 270)
    tests.append(("Turn left", "choose_turn", "(1.5, 0.5, 270)",
                  "180", str(r), r == 180))
    r = choose_turn(1.5, 0.5, 0)
    tests.append(("Left wraps", "choose_turn", "(1.5, 0.5, 0)",
                  "270", str(r), r == 270))
    r = choose_turn(1.0, 1.0, 270)
    tests.append(("Equal -> right", "choose_turn", "(1.0, 1.0, 270)",
                  "0", str(r), r == 0))

    print("\nTest | Function | Arguments | Expected | Actual | Pass/Fail")
    for name, func, args, exp, act, ok in tests:
        print(f"{name} | {func} | {args} | {exp} | {act} | "
              f"{'Pass' if ok else 'Fail'}")


if __name__ == "__main__":
    run_mission(10, 0.5)
    test_table()