from pitop import LED

led_left = LED("D2")
led_right = LED("D6")

led_left.on()
if led_left.is_active is True:
    print("LED_left ok")
elif led_left.is_active is False:
    print("LED left not ok")
led_right.off()

led_right.on()
if led_right.is_active is True:
    print("LED right ok")
elif led_right.is_active is False:
    print("LED right not ok")
led_right.off()

