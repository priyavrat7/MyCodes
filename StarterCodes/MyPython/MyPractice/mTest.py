port = 22
ip = "192.168.1.1"

print("-" * 30)
print(f"Device IP: {ip}, port: {port}")
print("-" * 30)

# write tuple, since they are immutable and preferred for the network conditions
network_end_point = ('192.168.1.1', 22, 'ssh') # (ip, port, protocol)


# devices is a list
devices = ["Router-1", "Switch-1", "Firewall-1"] 
print(f"Network devices: {devices}")
print(f"Last device: {devices[-1]}")

devices.append("Access-Point-10")
print(f"Number of devices: {len(devices)}")

print("-" * 30)

# device_info is a dictionary
device_info = {
    "name": "Core-Switch-01",
    "ip": "192.168.1.10",
    "type": "switch",
    "ports": 52
}
print("-" * 30)


# Function with Error Handling
def safe_divide(a, b):
    try:
        result = a / b
        return f"{a} ÷ {b} = {result}"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except Exception as e:
        return f"Unexpected error: {e}"
    
print(safe_divide(10, 2)) # Normal case
print(safe_divide(10, 0)) # Error case


# Writing to a file using multiline string
config_data = """
interface GigabitEthernet0/1
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/2
 ip address 192.168.2.1 255.255.255.0
 no shutdown
"""

lines = config_data.strip().split('\n')
print(type(lines))
print(lines)

for line_number, line in enumerate(lines, 1):
    print(f"Line {line_number}: {line}")

# or alternatively
# for i in range(len(lines)):
#     line_number = i + 1
#     line = lines[i]
#     print(f"Line: {line_number}: {line}")

# or
# line_number = 1
# for line in lines:
#     print(f"Line {line_number}: {line}")
#     line_number += 1
#     line.strip()

# Function and decorators for test automation
# *args collects any number of positional arguments into a tuple
# **kwargs collects any number of keyword arguments into a dictionary
def wrapper(*args, **kwargs):
    print(f"Received {len(args)} arguments by args as {type(args)}")
    print(f"Arguments: {args}")

    print(f"Received {len(kwargs)} arguments by kwargs as {type(kwargs)}")
    print(f"Arguments: {kwargs}")

wrapper("192.168.1.1", count = 7)

print("-" *46)

def network_test_decorator(func):
    print(func)
    print(f"{func.__name__} function will be executed by wrapper")

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper

@network_test_decorator
def ping_test(host, count = 3): #if count is not passed, default is 3
    pingSuccess = f"ping test passed with count = {count}"
    print(pingSuccess)
    return pingSuccess

ping_test("192.168.1.1", count = 11)
ping_test("192.168.1.7")

print("-" *46)