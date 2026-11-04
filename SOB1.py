import time

floor = 0            # lift starts at floor 0
target = 0
doors = "closed"     # doors start closed
state = "IDLE"       # FSM states: IDLE, MOVING, DOOR_OPEN
event = None

def move_lift():
    global floor
    while floor != target:
        if floor < target:
            floor += 1
        else:
            floor -= 1
        print("Lift at floor", floor)
        time.sleep(1)


print("Lift at floor 0, doors closed")

while True:
    if state == "IDLE":
        choice = input("Select floor (0, 1, 2, 3): ")
        if choice in ["0", "1", "2", "3"]:
            target = int(choice)
            event = "floor_selected"
    elif state == "MOVING":
        move_lift()
        event = "floor_reached"
    elif state == "DOOR_OPEN":
        time.sleep(3)
        print("Doors will close in 3 seconds...")
        event = "door_timer_expired"

    if event == "floor_selected":
        if target == floor:
            doors = "open"
            print("Doors open")
            state = "DOOR_OPEN"
        else:
            state = "MOVING"
    elif event == "floor_reached":
        doors = "open"
        print("Arrived at floor", floor, "- doors open")
        state = "DOOR_OPEN"
    elif event == "door_timer_expired":
        doors = "closed"
        print("Doors closed")
        state = "IDLE"

    event = None     # event has been handled