import xbox_gamepad as gp

gamepad = gp.DroneGamepad(5)
gamepad.start_thread()

while True:
    print([gamepad.ud, gamepad.fb, gamepad.lr, gamepad.yv])
