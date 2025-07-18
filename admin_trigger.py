from services.twilio_service import send_whatsapp_message
from utils.conversation_state import update_user_step
import time

# Sample candidate list
candidates = [
    # {"name": "Manoj", "phone": "whatsapp:+917058617355"},
    {"name": "Shree", "phone": "whatsapp:+919156347655"},
]

# Message template
trigger_template = """
Hi {name}, 
We have shortlisted your profile for a position in one of the top MNCs.
Please find the details below:

Companies: TCS, WNS, Concentrix, Teleperformance  
Role: Voice & Chat Process  
Locations: Mumbai, Pune, Chennai, Delhi, Jaipur  
Timings: Rotational Shifts  
Salary: Up to ₹6 LPA  
🗕 Immediate Joiners Only

To proceed, please share:  
Your updated **CV**  
A 30-40 sec **voice note** introducing yourself  
– HumanHire HR Team
"""

# Send message + initialize state
for person in candidates:
    message = trigger_template.format(name=person["name"])
    send_whatsapp_message(message, person["phone"])
    
    # Set initial state
    update_user_step(person["phone"], "step", "location")
    
    print(f"✅ Message sent to {person['name']} at {person['phone']}")
    time.sleep(2)
