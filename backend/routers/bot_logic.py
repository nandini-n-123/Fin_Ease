# backend/routers/bot_logic.py
import re
from typing import Dict, List

# Import the data from our bot_data.py file
from .bot_data import INTENT_KEYWORDS, INTENT_RESPONSES

def is_kannada(text: str) -> bool:
    """Checks if the text contains any Kannada characters."""
    # This regex checks for characters in the Kannada Unicode range.
    return bool(re.search("[\u0C80-\u0CFF]", text))

def get_intent_from_keywords(message_lower: str) -> str:
    """
    This is the corrected and final version of the intent matching logic.
    It checks for keywords for every intent in a prioritized order.
    """
    # By using a single if/elif chain, we enforce a strict priority
    # to prevent incorrect matches. More specific intents come first.

    if any(k in message_lower for k in INTENT_KEYWORDS["HealthInsurance"]):
        return "HealthInsurance"
    elif any(k in message_lower for k in INTENT_KEYWORDS["WhatIsSavings"]):
        return "WhatIsSavings"
    elif any(k in message_lower for k in INTENT_KEYWORDS["WhatIsInvestment"]):
        return "WhatIsInvestment"
    elif any(k in message_lower for k in INTENT_KEYWORDS["WhatIsFinease"]):
        return "WhatIsFinease"
    elif any(k in message_lower for k in INTENT_KEYWORDS["LifeInsurance"]):
        return "LifeInsurance"
    elif any(k in message_lower for k in INTENT_KEYWORDS["GeneralInsurance"]):
        return "GeneralInsurance"
    elif any(k in message_lower for k in INTENT_KEYWORDS["SaveIn20s"]):
        return "SaveIn20s"
    elif any(k in message_lower for k in INTENT_KEYWORDS["SaveIn40s"]):
        return "SaveIn40s"
    elif any(k in message_lower for k in INTENT_KEYWORDS["SaveIn60s"]):
        return "SaveIn60s"
    elif any(k in message_lower for k in INTENT_KEYWORDS["OpenBankAccount"]):
        return "OpenBankAccount"
    elif any(k in message_lower for k in INTENT_KEYWORDS["Budgeting"]):
        return "Budgeting"
    elif any(k in message_lower for k in INTENT_KEYWORDS["DebtManagement"]):
        return "DebtManagement"
    elif any(k in message_lower for k in INTENT_KEYWORDS["StudentFinance"]):
        return "StudentFinance"
    elif any(k in message_lower for k in INTENT_KEYWORDS["WomenInvestment"]):
        return "WomenInvestment" # Placed before WomenFinance to catch "investment" first
    elif any(k in message_lower for k in INTENT_KEYWORDS["WomenFinance"]):
        return "WomenFinance"
    elif any(k in message_lower for k in INTENT_KEYWORDS["SmartSavingTips"]):
        return "SmartSavingTips"
    elif any(k in message_lower for k in INTENT_KEYWORDS["FarmerSchemes"]):
        return "FarmerSchemes"
    elif any(k in message_lower for k in INTENT_KEYWORDS["ProtectFinance"]):
        return "ProtectFinance"
    elif any(k in message_lower for k in INTENT_KEYWORDS["Greeting"]):
        return "Greeting"
    else:
        return "Fallback" # Return "Fallback" if no keywords match

def get_final_response(user_message: str) -> str:
    """
    This is the main function that gets called from our API.
    It determines the language and finds the correct intent to give a final response.
    """
    # 1. Detect the language
    lang = "kn" if is_kannada(user_message) else "en"
    
    # 2. Find the correct intent based on keywords
    message_lower = user_message.lower()
    intent = get_intent_from_keywords(message_lower)
    
    # 3. Get the correct response from our data dictionary
    return INTENT_RESPONSES[intent][lang]
