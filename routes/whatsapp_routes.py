from flask import Blueprint, Response, request
from services.twilio_service import send_whatsapp_message
from utils.conversation_state import (
    get_user_step,
    update_user_step,
    save_user_response
)

whatsapp_bp = Blueprint('whatsapp_bp', __name__)

@whatsapp_bp.route('/webhook', methods=['POST'])
def receive_message():
    incoming_data = request.form
    incoming_msg = incoming_data.get("Body", "").strip()
    from_number = incoming_data.get("From")

    step = get_user_step(from_number)

    # ✅ Block messages after completion
    if step == "complete":
        return Response(send_whatsapp_message(
            "✅ Your details have already been submitted. Our team will get in touch with you soon.",
            from_number
        ), status=200)

    # 🏁 Step 1: Ask for Location
    if step == "location":
        save_user_response(from_number, "location", incoming_msg)
        update_user_step(from_number, "location", incoming_msg)
        return Response(send_whatsapp_message(
            "Got it! 🗺️ Which company would you prefer?",
            from_number
        ), status=200)

    # 🏢 Step 2: Ask for Company
    elif step == "company":
        save_user_response(from_number, "company", incoming_msg)
        update_user_step(from_number, "company", incoming_msg)
        return Response(send_whatsapp_message(
            "Nice! 🏢 What type of role are you interested in?",
            from_number
        ), status=200)

    # 👩‍💼 Step 3: Ask for Role
    elif step == "role":
        save_user_response(from_number, "role", incoming_msg)
        update_user_step(from_number, "role", incoming_msg)
        return Response(send_whatsapp_message(
            "Great! 📄 Please upload your CV as a file (PDF or DOC).",
            from_number
        ), status=200)

    # 📎 Step 4: Receive CV File
    elif step == "cv":
        if "MediaUrl0" in incoming_data:
            media_url = incoming_data.get("MediaUrl0")
            save_user_response(from_number, "cv_url", media_url)
            update_user_step(from_number, "cv", media_url)
            return Response(send_whatsapp_message(
                "Thanks! 🎤 Now please send a short voice note introducing yourself.",
                from_number
            ), status=200)
        else:
            return Response(send_whatsapp_message(
                "❗ Please upload your CV as a file (PDF or DOC).",
                from_number
            ), status=200)

    # 🎤 Step 5: Receive Voice Note
    elif step == "audio":
        if "MediaUrl0" in incoming_data:
            voice_url = incoming_data.get("MediaUrl0")
            save_user_response(from_number, "voice_note_url", voice_url)
            update_user_step(from_number, "audio", voice_url)
            return Response(send_whatsapp_message(
                "✅ Thank you! We’ve received all your details. Our team will get in touch with you shortly.\n– HumanHire HR Team",
                from_number
            ), status=200)
        else:
            return Response(send_whatsapp_message(
                "🎤 Please send a voice note using WhatsApp's mic feature.",
                from_number
            ), status=200)

    # 🔄 Fallback if no step is set
    else:
        update_user_step(from_number, "location", "")
        return Response(send_whatsapp_message(
            "Hi! 👋 Let's get started. Which location are you looking for a job in?",
            from_number
        ), status=200)
