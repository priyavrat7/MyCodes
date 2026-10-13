#!/usr/bin/env python3
"""
Python Basics for Complete Beginners
Start here if you're new to Python programming!

This file covers:
1. What is Python and why use it?
2. Basic syntax and concepts
3. Variables and data types
4. Basic operations
5. Control structures (if, loops)
6. Functions
7. Simple examples
8. Next steps

Run this file: python3 prebasicspython.py
"""

print("🐍 Welcome to Python Programming! 🐍")
print("=" * 50)

# ============================================================================
# 1. WHAT IS PYTHON?
# ============================================================================

print("\n1. WHAT IS PYTHON?")
print("-" * 20)

"""
Python is a programming language that is:
- Easy to read and write (looks almost like English!)
- Powerful (can do complex tasks)
- Versatile (web development, data analysis, automation, AI, etc.)
- Popular (used by Google, Netflix, Instagram, etc.)

Why Python for Network Testing?
- Simple syntax = less bugs
- Great libraries for networking
- Easy automation of repetitive tasks
- Excellent for parsing device outputs
"""

print("Python is like giving instructions to a computer in simple English!")
print("Example: Instead of complex code, you can write:")
print("  if temperature > 30:")
print("    print('It's hot!')")

# ============================================================================
# 2. BASIC SYNTAX - YOUR FIRST PYTHON CODE
# ============================================================================

print("\n\n2. BASIC SYNTAX - YOUR FIRST CODE")
print("-" * 35)

# This is a comment - Python ignores this line
# Comments help explain what your code does

# Print statement - displays text on screen
print("Hello, World!")  # This is your first Python program!

# Python is case-sensitive: 'Print' is different from 'print'
# print("This works")
# Print("This would cause an error")

print("Python reads code from top to bottom, line by line")

# ============================================================================
# 3. VARIABLES - STORING INFORMATION
# ============================================================================

print("\n\n3. VARIABLES - STORING INFORMATION")
print("-" * 35)

# Variables are like boxes that store information
# Think of them as labels for your data

# Creating variables (no need to declare type!)
name = "Alice"              # Text (string)
age = 25                    # Number (integer)
height = 5.6               # Decimal number (float)
is_student = True          # True/False (boolean)

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height} feet")
print(f"Is student: {is_student}")

# Variable names rules:
# ✅ Good: name, age, user_name, device_ip
# ❌ Bad: 2name, user-name, class (reserved word)

# You can change variable values
age = 26
print(f"Updated age: {age}")

# ============================================================================
# 4. DATA TYPES - DIFFERENT KINDS OF INFORMATION
# ============================================================================

print("\n\n4. DATA TYPES - KINDS OF INFORMATION")
print("-" * 40)

# String (text) - always in quotes
device_name = "Router-01"
ip_address = "192.168.1.1"
print(f"Device: {device_name}, IP: {ip_address}")

# Numbers
port_number = 22        # Integer (whole number)
cpu_usage = 85.5       # Float (decimal number)
print(f"SSH Port: {port_number}, CPU Usage: {cpu_usage}%")

# Boolean (True/False)
is_online = True
is_configured = False
print(f"Device online: {is_online}, Configured: {is_configured}")

# You can check the type of any variable
print(f"Type of device_name: {type(device_name)}")
print(f"Type of port_number: {type(port_number)}")
print(f"Type of is_online: {type(is_online)}")

# ============================================================================
# 5. BASIC OPERATIONS
# ============================================================================

print("\n\n5. BASIC OPERATIONS")
print("-" * 20)

# Math operations
a = 10
b = 3

print(f"Addition: {a} + {b} = {a + b}")
print(f"Subtraction: {a} - {b} = {a - b}")
print(f"Multiplication: {a} * {b} = {a * b}")
print(f"Division: {a} / {b} = {a / b}")
print(f"Integer Division: {a} // {b} = {a // b}")
print(f"Remainder: {a} % {b} = {a % b}")
print(f"Power: {a} ** {b} = {a ** b}")

# String operations
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name  # Concatenation
print(f"Full name: {full_name}")

# String repetition
separator = "-" * 20
print(separator)

# String methods (functions that work on strings)
message = "hello world"
print(f"Original: {message}")
print(f"Uppercase: {message.upper()}")
print(f"Capitalized: {message.capitalize()}")
print(f"Length: {len(message)} characters")

# ============================================================================
# 6. GETTING INPUT FROM USER
# ============================================================================

print("\n\n6. GETTING INPUT FROM USER")
print("-" * 30)

# Note: In this demo, we'll simulate user input
# In real programs, you'd use: user_input = input("Enter something: ")

print("Simulating user input...")
simulated_input = "Router-Core-01"
print(f"User entered: {simulated_input}")

# Converting input to numbers
simulated_number = "25"
age_number = int(simulated_number)  # Convert string to integer
print(f"String '{simulated_number}' converted to number: {age_number}")

# ============================================================================
# 7. LISTS - STORING MULTIPLE ITEMS
# ============================================================================

print("\n\n7. LISTS - STORING MULTIPLE ITEMS")
print("-" * 35)

# Lists are like containers that hold multiple items
devices = ["Router-01", "Switch-01", "Firewall-01"]
print(f"Network devices: {devices}")

# Accessing list items (starts from 0!)
print(f"First device: {devices[0]}")
print(f"Second device: {devices[1]}")
print(f"Last device: {devices[-1]}")  # -1 means last item

# Adding items to list
devices.append("Access-Point-01")
print(f"After adding AP: {devices}")

# List length
print(f"Number of devices: {len(devices)}")

# Checking if item exists in list
if "Router-01" in devices:
    print("Router-01 is in our device list")

# ============================================================================
# 8. DICTIONARIES - STORING KEY-VALUE PAIRS
# ============================================================================

print("\n\n8. DICTIONARIES - KEY-VALUE PAIRS")
print("-" * 38)

# Dictionaries store information in key-value pairs
# Like a real dictionary: word -> definition
device_info = {
    "name": "Core-Switch-01",
    "ip": "192.168.1.10",
    "type": "switch",
    "ports": 48
}

print(f"Device info: {device_info}")
print(f"Device name: {device_info['name']}")
print(f"Device IP: {device_info['ip']}")

# Adding new information
device_info["location"] = "Data Center"
print(f"Updated info: {device_info}")

# ============================================================================
# 9. CONDITIONAL STATEMENTS - MAKING DECISIONS
# ============================================================================

print("\n\n9. CONDITIONAL STATEMENTS - MAKING DECISIONS")
print("-" * 48)

# if statements help your program make decisions
temperature = 75

if temperature > 80:
    print("It's hot! Turn on AC")
elif temperature > 60:
    print("Nice temperature")
else:
    print("It's cold! Turn on heater")

# Network example
device_status = "online"
cpu_usage = 90

if device_status == "offline":
    print("❌ Device is offline - check connection")
elif cpu_usage > 85:
    print("⚠️  High CPU usage - investigate")
else:
    print("✅ Device is healthy")

# Comparison operators
print(f"5 > 3: {5 > 3}")        # Greater than
print(f"5 < 3: {5 < 3}")        # Less than
print(f"5 == 5: {5 == 5}")      # Equal to
print(f"5 != 3: {5 != 3}")      # Not equal to

# ============================================================================
# 10. LOOPS - REPEATING ACTIONS
# ============================================================================

print("\n\n10. LOOPS - REPEATING ACTIONS")
print("-" * 32)

# For loop - repeat for each item in a list
print("Checking all devices:")
devices = ["Router-01", "Switch-01", "Firewall-01"]

for device in devices:
    print(f"  Pinging {device}...")

# For loop with numbers
print("\nCountdown:")
for i in range(5, 0, -1):  # 5, 4, 3, 2, 1
    print(f"  {i}...")
print("  Blast off! 🚀")

# While loop - repeat while condition is true
print("\nWaiting for device to come online:")
attempts = 0
max_attempts = 3

while attempts < max_attempts:
    attempts += 1  # Same as: attempts = attempts + 1
    print(f"  Attempt {attempts}: Checking device...")
    if attempts == 2:  # Simulate device coming online
        print("  Device is online! ✅")
        break  # Exit the loop
else:
    print("  Device failed to come online ❌")

# ============================================================================
# 11. FUNCTIONS - REUSABLE CODE BLOCKS
# ============================================================================

print("\n\n11. FUNCTIONS - REUSABLE CODE BLOCKS")
print("-" * 40)

# Functions are like recipes - you define them once, use them many times
def greet_user(name):
    """This function greets a user by name"""
    return f"Hello, {name}! Welcome to network automation!"

# Using the function
message = greet_user("Alice")
print(message)

# Function with multiple parameters
def check_device_health(device_name, cpu_usage, memory_usage):
    """Check if a device is healthy based on CPU and memory usage"""
    print(f"Checking {device_name}:")
    
    if cpu_usage > 90 or memory_usage > 90:
        return "❌ Unhealthy - High resource usage"
    elif cpu_usage > 70 or memory_usage > 70:
        return "⚠️  Warning - Monitor closely"
    else:
        return "✅ Healthy"

# Using the function
result = check_device_health("Router-01", 65, 45)
print(result)

result = check_device_health("Switch-01", 95, 80)
print(result)

# Function with default parameters
def ping_device(ip_address, count=4):
    """Simulate pinging a device"""
    return f"Pinging {ip_address} with {count} packets... Success!"

print(ping_device("192.168.1.1"))        # Uses default count=4
print(ping_device("192.168.1.2", 10))    # Uses count=10

# ============================================================================
# 12. ERROR HANDLING - DEALING WITH PROBLEMS
# ============================================================================

print("\n\n12. ERROR HANDLING - DEALING WITH PROBLEMS")
print("-" * 46)

# Sometimes things go wrong - Python helps you handle errors gracefully
def safe_divide(a, b):
    """Safely divide two numbers"""
    try:
        result = a / b
        return f"{a} ÷ {b} = {result}"
    except ZeroDivisionError:
        return "Error: Cannot divide by zero!"
    except Exception as e:
        return f"Unexpected error: {e}"

print(safe_divide(10, 2))   # Normal case
print(safe_divide(10, 0))   # Error case

# Network example
def connect_to_device(ip_address):
    """Simulate connecting to a network device"""
    try:
        # Simulate connection logic
        if ip_address == "192.168.1.999":  # Invalid IP
            raise Exception("Invalid IP address")
        return f"✅ Connected to {ip_address}"
    except Exception as e:
        return f"❌ Connection failed: {e}"

print(connect_to_device("192.168.1.1"))
print(connect_to_device("192.168.1.999"))

# ============================================================================
# 13. WORKING WITH FILES
# ============================================================================

print("\n\n13. WORKING WITH FILES")
print("-" * 25)

# Python can read and write files
# This is very useful for network configurations!

# Writing to a file
config_data = """
interface GigabitEthernet0/1
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/2
 ip address 192.168.2.1 255.255.255.0
 no shutdown
"""

# Simulate writing to file (we'll just print what would be written)
print("Writing configuration to file:")
print(config_data)

# Reading from a file (simulated)
print("Reading configuration from file:")
lines = config_data.strip().split('\n')
for line_number, line in enumerate(lines, 1):
    print(f"Line {line_number}: {line}")

# ============================================================================
# 14. PRACTICAL NETWORK EXAMPLES
# ============================================================================

print("\n\n14. PRACTICAL NETWORK EXAMPLES")
print("-" * 35)

# Example 1: IP Address validation
def is_valid_ip(ip):
    """Simple IP address validation"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    
    for part in parts:
        try:
            num = int(part)
            if num < 0 or num > 255:
                return False
        except ValueError:
            return False
    
    return True

# Test IP validation
test_ips = ["192.168.1.1", "256.1.1.1", "192.168.1", "10.0.0.1"]
for ip in test_ips:
    status = "✅ Valid" if is_valid_ip(ip) else "❌ Invalid"
    print(f"IP {ip}: {status}")

# Example 2: Parse device output
def parse_interface_status(output):
    """Parse interface status from device output"""
    interfaces = []
    lines = output.strip().split('\n')
    
    for line in lines:
        if 'GigabitEthernet' in line:
            parts = line.split()
            if len(parts) >= 3:
                interface = {
                    'name': parts[0],
                    'status': parts[1],
                    'protocol': parts[2]
                }
                interfaces.append(interface)
    
    return interfaces

# Test parsing
sample_output = """
GigabitEthernet0/1    up    up
GigabitEthernet0/2    down  down
GigabitEthernet0/3    up    up
"""

interfaces = parse_interface_status(sample_output)
print("\nParsed interfaces:")
for interface in interfaces:
    print(f"  {interface['name']}: {interface['status']}/{interface['protocol']}")

# ============================================================================
# 15. NEXT STEPS IN YOUR PYTHON JOURNEY
# ============================================================================

print("\n\n15. NEXT STEPS IN YOUR PYTHON JOURNEY")
print("-" * 40)

print("""
🎉 Congratulations! You've learned Python basics!

What you now know:
✅ Variables and data types
✅ Basic operations
✅ Lists and dictionaries
✅ Conditional statements (if/else)
✅ Loops (for/while)
✅ Functions
✅ Error handling
✅ File operations
✅ Basic network examples

Next steps for network automation:
1. Practice with basics.py - OSPF concepts
2. Study 01_python_fundamentals.py - Advanced concepts
3. Learn networking libraries (requests, socket, etc.)
4. Master regular expressions for parsing
5. Understand testing frameworks (pytest)
6. Explore Cisco pyATS framework

Practice exercises:
- Write a function to check if a port is open
- Create a script to parse router configurations
- Build a simple network inventory system
- Practice with different data formats (JSON, CSV)

Remember: Programming is like learning a language - practice makes perfect!
""")

# ============================================================================
# 16. QUICK REFERENCE
# ============================================================================

print("\n\n16. QUICK REFERENCE")
print("-" * 20)

print("""
Common Python Syntax:

# Variables
name = "value"
number = 42

# Lists
my_list = [1, 2, 3]
my_list.append(4)

# Dictionaries
my_dict = {"key": "value"}
my_dict["new_key"] = "new_value"

# Conditions
if condition:
    do_something()
elif other_condition:
    do_something_else()
else:
    do_default()

# Loops
for item in list:
    process(item)

while condition:
    do_something()

# Functions
def my_function(parameter):
    return result

# Error handling
try:
    risky_operation()
except Exception as e:
    handle_error(e)
""")

# ============================================================================
# FINAL MESSAGE
# ============================================================================

print("\n" + "=" * 60)
print("🎯 YOU'RE READY FOR THE NEXT LEVEL!")
print("=" * 60)
print("""
Now that you understand Python basics, you can:

1. Move to basics.py for OSPF concepts
2. Explore 01_python_fundamentals.py for advanced topics
3. Start building network automation scripts
4. Practice with real network scenarios

Remember: Every expert was once a beginner!
Keep practicing and you'll master Python for network automation! 🚀
""")

# Run a simple interactive demo
print("\n🎮 INTERACTIVE DEMO:")
print("Let's simulate a simple network check...")

devices_to_check = ["Router-01", "Switch-01", "Firewall-01"]
for i, device in enumerate(devices_to_check, 1):
    print(f"Step {i}: Checking {device}... ✅ Online")

print("All devices are healthy! Network automation with Python works! 🎉")

if __name__ == "__main__":
    print("\n💡 TIP: You just ran your first complete Python program!")
    print("Try modifying some values and run it again to see what changes!")
