# backend/routers/bot_data.py
from typing import List, Dict

# This file stores the "knowledge" of the chatbot.
# This version includes more comprehensive keywords for better accuracy.

# 1. Define all keywords for each intent with more variations.
INTENT_KEYWORDS: Dict[str, List[str]] = {

    "WhatIsSavings": ["what is saving", "about savings", "ಉಳಿತಾಯ ಎಂದರೇನು", "ಉಳಿತಾಯ ಬಗ್ಗೆ ತಿಳಿಸಿ"],
    "WhatIsInvestment": ["what is investment", "investing", "ಹೂಡಿಕೆ ಎಂದರೇನು", "ಹೂಡಿಕೆ ಬಗ್ಗೆ"],
    "WhatIsFinease": ["who are you", "what is finease", "ಫಿನೀಸ್ ಎಂದರೇನು", "ನೀವು ಯಾರು"],
    "SaveIn20s": ["in my 20s", "when i'm young", "20ರ ಹರೆಯದಲ್ಲಿ", "ಉಳಿತಾಯ ಏಕೆ ಮುಖ್ಯ", "ಈಗಲೇ ಉಳಿತಾಯ"],
    "SaveIn40s": ["in 40s", "is 40 too late", "strategies for 40s", "40ರ ವಯಸ್ಸಿನಲ್ಲಿ", "ತಡವಾಯಿತೇ"],
    "SaveIn60s": ["at 60", "for elders", "60 ವರ್ಷ", "ಖಾತೆ ತ್ಯಾಜ್ಯವಲ್ಲವೇ"],
    "OpenBankAccount": ["open a bank account", "zero balance account", "kyc", "ಕೆವೈಸಿ", "ನಗದು ಇಲ್ಲದೆ", "ಖಾತೆ ತೆರೆಯಬಹುದಾ"],
    "Budgeting": ["budget", "plan my spending", "ಬಜೆಟ್", "ರೂಪಿಸಬೇಕು", "ಕಡಿಮೆ ಆದಾಯದಿಂದ"],
    "DebtManagement": ["loan burden", "emi", "manage multiple loans", "ಸಾಲ", "ಹಿಂತೆಗೆದುಕೊಳ್ಳುವುದು"],
    "HealthInsurance": ["health insurance", "ayushman bharat", "ಆರೋಗ್ಯ ವಿಮೆ", "government health"],
    "LifeInsurance": ["lic", "term life insurance", "ಜೀವನ ವಿಮೆ"],
    "StudentFinance": ["students save", "ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ", "plan for students", "saving as a student"],
    "WomenFinance": ["schemes for women", "ಮಹಿಳೆಯರು ಯಾವ ಯೋಜನೆಗಳನ್ನು", "women get loans", "women investment plans"],
    "GeneralInsurance": ["general insurance", "insure my scooter", "insure my mobile", "ವಿಮೆ ಎಲ್ಲರಿಗೂ", "ಸೈಕಲ್"],
    "SmartSavingTips": ["save money at home","save money", "save daily", "ಪ್ರತಿ ದಿನ ಹಣ ಉಳಿಸಬಹುದೆ", "ಹಚ್ಚಳಿಕೆ"],
    "FarmerSchemes": ["schemes for farmers", "ರೈತರಿಗಾಗಿ", "farmers get loans", "insurance for crops", "ಬೆಳೆ"],
    "WomenInvestment": ["fd or rd", "ಮಹಿಳೆಯರು ಎಲ್ಲಿ ಹೂಡಿಕೆ", "sip", "safe investment", "investment for salary"],
    "ProtectFinance": ["online banking fraud", "otp", "upi safe", "ಹಣ ಕಳವೇ"],
    "Greeting": ["hello", "hi", "ನಮಸ್ಕಾರ", "hey"],
}

# 2. The detailed, bilingual responses remain the same.
# (I've truncated them here for brevity, the full text is in your existing file)
INTENT_RESPONSES: Dict[str, Dict[str, str]] = {
    "WhatIsSavings": {
        "en": "Saving is the process of setting aside a portion of your current income for future use, rather than spending it immediately. It's the first step towards financial security. Common ways to save include putting money in a bank savings account, a recurring deposit (RD), or simply keeping cash aside for emergencies. The main goal of saving is to have funds available for future needs and to build a safety net.",
        "kn": "ಉಳಿತಾಯ ಎಂದರೆ ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಆದಾಯದ ಒಂದು ಭಾಗವನ್ನು ತಕ್ಷಣವೇ ಖರ್ಚು ಮಾಡುವ ಬದಲು ಭವಿಷ್ಯದ ಬಳಕೆಗಾಗಿ ಮೀಸಲಿಡುವ ಪ್ರಕ್ರಿಯೆ. ಇದು ಆರ್ಥಿಕ ಭದ್ರತೆಯತ್ತ ಮೊದಲ ಹೆಜ್ಜೆ. ಬ್ಯಾಂಕ್ ಉಳಿತಾಯ ಖಾತೆಯಲ್ಲಿ ಹಣ ಇಡುವುದು, ಮರುಕಳಿಸುವ ಠೇವಣಿ (ಆರ್‌ಡಿ), ಅಥವಾ ತುರ್ತು ಪರಿಸ್ಥಿತಿಗಳಿಗಾಗಿ ನಗದನ್ನು ಮೀಸಲಿಡುವುದು ಉಳಿತಾಯದ ಸಾಮಾನ್ಯ ವಿಧಾನಗಳಾಗಿವೆ. ಉಳಿತಾಯದ ಮುಖ್ಯ ಗುರಿ ಭವಿಷ್ಯದ ಅಗತ್ಯಗಳಿಗಾಗಿ ನಿಧಿಗಳನ್ನು ಲಭ್ಯವಾಗಿಸುವುದು ಮತ್ತು ಸುರಕ್ಷತಾ ಜಾಲವನ್ನು ನಿರ್ಮಿಸುವುದು."
    },
    "WhatIsInvestment": {
        "en": "Investment is the act of allocating money with the expectation of generating a profit or income in the future. Unlike saving, investing involves taking on some level of risk with the goal of making your money grow. Popular investment options in India include stocks, mutual funds (like SIPs), real estate, and fixed deposits (FDs). The goal of investing is to build wealth over time.",
        "kn": "ಹೂಡಿಕೆ ಎಂದರೆ ಭವಿಷ್ಯದಲ್ಲಿ ಲಾಭ ಅಥವಾ ಆದಾಯವನ್ನು ಗಳಿಸುವ ನಿರೀಕ್ಷೆಯೊಂದಿಗೆ ಹಣವನ್ನು ಮೀಸಲಿಡುವ ಕ್ರಿಯೆ. ಉಳಿತಾಯಕ್ಕಿಂತ ಭಿನ್ನವಾಗಿ, ಹೂಡಿಕೆಯು ನಿಮ್ಮ ಹಣವನ್ನು ಬೆಳೆಸುವ ಗುರಿಯೊಂದಿಗೆ ಸ್ವಲ್ಪ ಮಟ್ಟಿಗೆ ಅಪಾಯವನ್ನು ತೆಗೆದುಕೊಳ್ಳುವುದನ್ನು ಒಳಗೊಂಡಿರುತ್ತದೆ. ಭಾರತದಲ್ಲಿ ಜನಪ್ರಿಯ ಹೂಡಿಕೆ ಆಯ್ಕೆಗಳಲ್ಲಿ ಷೇರುಗಳು, ಮ್ಯೂಚುಯಲ್ ಫಂಡ್‌ಗಳು (ಎಸ್‌ಐಪಿಗಳಂತಹ), ರಿಯಲ್ ಎಸ್ಟೇಟ್, ಮತ್ತು ಸ್ಥಿರ ಠೇವಣಿಗಳು (ಎಫ್‌ಡಿಗಳು) ಸೇರಿವೆ. ಕಾಲಾನಂತರದಲ್ಲಿ ಸಂಪತ್ತನ್ನು ನಿರ್ಮಿಸುವುದು ಹೂಡಿಕೆಯ ಗುರಿಯಾಗಿದೆ."
    },
    "WhatIsFinease": {
        "en": "I am Finease, a bilingual financial assistant created to help answer your basic questions about finance in both English and Kannada. I can provide information on topics like savings, investment, insurance, and government schemes. My goal is to make financial knowledge more accessible to everyone.",
        "kn": "ನಾನು ಫಿನೀಸ್, ಇಂಗ್ಲಿಷ್ ಮತ್ತು ಕನ್ನಡ ಎರಡರಲ್ಲೂ ಹಣಕಾಸಿನ ಬಗ್ಗೆ ನಿಮ್ಮ ಮೂಲಭೂತ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಲು ಸಹಾಯ ಮಾಡಲು ರಚಿಸಲಾದ ದ್ವಿಭಾಷಾ ಆರ್ಥಿಕ ಸಹಾಯಕ. ಉಳಿತಾಯ, ಹೂಡಿಕೆ, ವಿಮೆ, ಮತ್ತು ಸರ್ಕಾರಿ ಯೋಜನೆಗಳಂತಹ ವಿಷಯಗಳ ಬಗ್ಗೆ ನಾನು ಮಾಹಿತಿ ನೀಡಬಲ್ಲೆ. ಹಣಕಾಸಿನ ಜ್ಞಾನವನ್ನು ಎಲ್ಲರಿಗೂ ಹೆಚ್ಚು ಸುಲಭವಾಗಿ ತಲುಪಿಸುವುದು ನನ್ನ ಗುರಿಯಾಗಿದೆ."
    },
    "SaveIn20s": {
        "en": "Saving in your 20s is crucial as it lays the foundation for your financial future. The power of compounding is strongest when you start early, allowing even small, regular investments to grow into a substantial amount over time. This helps you build an emergency fund, save for major life goals like buying a house, and achieve financial independence sooner.",
        "kn": "ನಿಮ್ಮ 20ನೇ ವಯಸ್ಸಿನಲ್ಲಿ ಉಳಿತಾಯ ಮಾಡುವುದು ನಿಮ್ಮ ಆರ್ಥಿಕ ಭವಿಷ್ಯಕ್ಕೆ ಅಡಿಪಾಯ ಹಾಕುತ್ತದೆ. ನೀವು ಬೇಗನೆ ಪ್ರಾರಂಭಿಸಿದಾಗ, ಚಕ್ರಬಡ್ಡಿಯ ಶಕ್ತಿಯು ಅತ್ಯಂತ ಪ್ರಬಲವಾಗಿರುತ್ತದೆ, ಇದು ಸಣ್ಣ, ನಿಯಮಿತ ಹೂಡಿಕೆಗಳು ಸಹ ಕಾಲಾನಂತರದಲ್ಲಿ ಗಣನೀಯ ಮೊತ್ತವಾಗಿ ಬೆಳೆಯಲು ಅನುವು ಮಾಡಿಕೊಡುತ್ತದೆ. ಇದು ತುರ್ತು ನಿಧಿಯನ್ನು ನಿರ್ಮಿಸಲು, ಮನೆ ಖರೀದಿಸುವಂತಹ ಪ್ರಮುಖ ಜೀವನ ಗುರಿಗಳಿಗಾಗಿ ಉಳಿಸಲು ಮತ್ತು ಬೇಗನೆ ಆರ್ಥಿಕ ಸ್ವಾತಂತ್ರ್ಯವನ್ನು ಸಾಧಿಸಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ."
    },
    "SaveIn40s": {
        "en": "It is absolutely not too late to save in your 40s. This is often a peak earning period, making it an ideal time to accelerate your savings for retirement, children's education, and other goals. Focus on increasing your investment contributions, rebalancing your portfolio, and planning for your post-retirement life. Every rupee saved now makes a significant difference.",
        "kn": "ನಿಮ್ಮ 40ನೇ ವಯಸ್ಸಿನಲ್ಲಿ ಉಳಿತಾಯ ಮಾಡಲು ಖಂಡಿತವಾಗಿಯೂ ತಡವಾಗಿಲ್ಲ. ಇದು ಸಾಮಾನ್ಯವಾಗಿ ಗರಿಷ್ಠ ಆದಾಯ ಗಳಿಸುವ ಅವಧಿಯಾಗಿದ್ದು, ನಿವೃತ್ತಿ, ಮಕ್ಕಳ ಶಿಕ್ಷಣ ಮತ್ತು ಇತರ ಗುರಿಗಳಿಗಾಗಿ ನಿಮ್ಮ ಉಳಿತಾಯವನ್ನು ಹೆಚ್ಚಿಸಲು ಇದು ಸೂಕ್ತ ಸಮಯ. ನಿಮ್ಮ ಹೂಡಿಕೆ ಕೊಡುಗೆಗಳನ್ನು ಹೆಚ್ಚಿಸುವುದು, ನಿಮ್ಮ ಪೋರ್ಟ್‌ಫೋಲಿಯೊವನ್ನು ಮರುಸಮತೋಲನಗೊಳಿಸುವುದು ಮತ್ತು ನಿಮ್ಮ ನಿವೃತ್ತಿಯ ನಂತರದ ಜೀವನಕ್ಕಾಗಿ ಯೋಜಿಸುವುದರ ಮೇಲೆ ಗಮನಹರಿಸಿ. ಈಗ ಉಳಿಸಿದ ಪ್ರತಿಯೊಂದು ರೂಪಾಯಿ ಗಣನೀಯ ವ್ಯತ್ಯಾಸವನ್ನು ಮಾಡುತ್ತದೆ."
    },
    "SaveIn60s": {
        "en": "Yes, you can absolutely save and open new accounts in your 60s. Banks offer special Senior Citizen Savings Schemes with higher interest rates and guaranteed returns. These are very safe options for your retirement funds. Furthermore, all bank deposits are insured by the RBI's Deposit Insurance and Credit Guarantee Corporation (DICGC) for up to ₹5 lakhs per depositor.",
        "kn": "ಹೌದು, ನಿಮ್ಮ 60ನೇ ವಯಸ್ಸಿನಲ್ಲಿ ನೀವು ಖಂಡಿತವಾಗಿಯೂ ಉಳಿತಾಯ ಮಾಡಬಹುದು ಮತ್ತು ಹೊಸ ಖಾತೆಗಳನ್ನು ತೆರೆಯಬಹುದು. ಬ್ಯಾಂಕುಗಳು ಹೆಚ್ಚಿನ ಬಡ್ಡಿ ದರಗಳು ಮತ್ತು ಖಾತರಿಯ ಆದಾಯದೊಂದಿಗೆ ವಿಶೇಷ ಹಿರಿಯ ನಾಗರಿಕರ ಉಳಿತಾಯ ಯೋಜನೆಗಳನ್ನು ನೀಡುತ್ತವೆ. ನಿಮ್ಮ ನಿವೃತ್ತಿ ನಿಧಿಗಳಿಗೆ ಇವು ಬಹಳ ಸುರಕ್ಷಿತ ಆಯ್ಕೆಗಳಾಗಿವೆ. ಇದಲ್ಲದೆ, ಎಲ್ಲಾ ಬ್ಯಾಂಕ್ ಠೇವಣಿಗಳನ್ನು ಆರ್‌ಬಿಐನ ಠೇವಣಿ ವಿಮೆ ಮತ್ತು ಕ್ರೆಡಿಟ್ ಗ್ಯಾರಂಟಿ ಕಾರ್ಪೊರೇಷನ್ (ಡಿಐಸಿಜಿಸಿ) ಅಡಿಯಲ್ಲಿ ಪ್ರತಿ ಠೇವಣಿದಾರರಿಗೆ ₹5 ಲಕ್ಷದವರೆಗೆ ವಿಮೆ ಮಾಡಲಾಗುತ್ತದೆ."
    },
    "OpenBankAccount": {
        "en": "To open a bank account, you generally need Proof of Identity (like Aadhaar card, PAN card, or Passport) and Proof of Address. 'KYC' stands for 'Know Your Customer', which is a mandatory process for banks to verify your identity. This helps prevent financial fraud and ensures the security of the banking system. Many banks offer zero-balance accounts like those under the Pradhan Mantri Jan Dhan Yojana.",
        "kn": "ಬ್ಯಾಂಕ್ ಖಾತೆ ತೆರೆಯಲು, ನಿಮಗೆ ಸಾಮಾನ್ಯವಾಗಿ ಗುರುತಿನ ಪುರಾವೆ (ಆಧಾರ್ ಕಾರ್ಡ್, ಪ್ಯಾನ್ ಕಾರ್ಡ್, ಅಥವಾ ಪಾಸ್‌ಪೋರ್ಟ್‌ನಂತಹ) ಮತ್ತು ವಿಳಾಸದ ಪುರಾವೆ ಬೇಕಾಗುತ್ತದೆ. 'ಕೆವೈಸಿ' ಎಂದರೆ 'ನಿಮ್ಮ ಗ್ರಾಹಕರನ್ನು ತಿಳಿಯಿರಿ', ಇದು ನಿಮ್ಮ ಗುರುತನ್ನು ಪರಿಶೀಲಿಸಲು ಬ್ಯಾಂಕುಗಳಿಗೆ ಕಡ್ಡಾಯ ಪ್ರಕ್ರಿಯೆಯಾಗಿದೆ. ಇದು ಆರ್ಥಿಕ ವಂಚನೆಯನ್ನು ತಡೆಯಲು ಮತ್ತು ಬ್ಯಾಂಕಿಂಗ್ ವ್ಯವಸ್ಥೆಯ ಸುರಕ್ಷತೆಯನ್ನು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ. ಪ್ರಧಾನ ಮಂತ್ರಿ ಜನ್ ಧನ್ ಯೋಜನೆಯಡಿಯಲ್ಲಿರುವಂತಹ ಶೂನ್ಯ-ಬ್ಯಾಲೆನ್ಸ್ ಖಾತೆಗಳನ್ನು ಅನೇಕ ಬ್ಯಾಂಕುಗಳು ನೀಡುತ್ತವೆ."
    },
    "Budgeting": {
        "en": "A budget is a plan for how you will spend your money each month. To create one, start by tracking all your income sources. Then, list all your fixed expenses (like rent and bills) and variable expenses (like food and entertainment). A popular method is the 50/30/20 rule: 50% of your income for needs, 30% for wants, and 20% for savings and debt repayment.",
        "kn": "ಬಜೆಟ್ ಎಂದರೆ ನೀವು ಪ್ರತಿ ತಿಂಗಳು ನಿಮ್ಮ ಹಣವನ್ನು ಹೇಗೆ ಖರ್ಚು ಮಾಡುತ್ತೀರಿ ಎಂಬುದರ ಯೋಜನೆ. ಒಂದನ್ನು ರಚಿಸಲು, ನಿಮ್ಮ ಎಲ್ಲಾ ಆದಾಯದ ಮೂಲಗಳನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡುವುದರೊಂದಿಗೆ ಪ್ರಾರಂಭಿಸಿ. ನಂತರ, ನಿಮ್ಮ ಎಲ್ಲಾ ಸ್ಥಿರ ವೆಚ್ಚಗಳನ್ನು (ಬಾಡಿಗೆ ಮತ್ತು ಬಿಲ್‌ಗಳಂತಹ) ಮತ್ತು ಬದಲಾಗುವ ವೆಚ್ಚಗಳನ್ನು (ಆಹಾರ ಮತ್ತು ಮನರಂಜನೆಯಂತಹ) ಪಟ್ಟಿ ಮಾಡಿ. 50/30/20 ನಿಯಮವು ಒಂದು ಜನಪ್ರಿಯ ವಿಧಾನವಾಗಿದೆ: ನಿಮ್ಮ ಆದಾಯದ 50% ಅಗತ್ಯಗಳಿಗಾಗಿ, 30% ಬಯಕೆಗಳಿಗಾಗಿ, ಮತ್ತು 20% ಉಳಿತಾಯ ಮತ್ತು ಸಾಲ ಮರುಪಾವತಿಗಾಗಿ."
    },
    "DebtManagement": {
        "en": "Managing debt effectively is key to financial health. Always prioritize paying your EMIs on time to avoid penalties and maintain a good credit score. If you have multiple high-interest loans, consider a 'debt consolidation' loan to combine them into one with a lower interest rate. It's wise to avoid taking new loans until existing ones are cleared.",
        "kn": "ಸಾಲವನ್ನು ಪರಿಣಾಮಕಾರಿಯಾಗಿ ನಿರ್ವಹಿಸುವುದು ಆರ್ಥಿಕ ಆರೋಗ್ಯಕ್ಕೆ ಪ್ರಮುಖವಾಗಿದೆ. ದಂಡಗಳನ್ನು ತಪ್ಪಿಸಲು ಮತ್ತು ಉತ್ತಮ ಕ್ರೆಡಿಟ್ ಸ್ಕೋರ್ ಅನ್ನು ನಿರ್ವಹಿಸಲು ಯಾವಾಗಲೂ ನಿಮ್ಮ ಇಎಂಐಗಳನ್ನು ಸಮಯಕ್ಕೆ ಸರಿಯಾಗಿ ಪಾವತಿಸಲು ಆದ್ಯತೆ ನೀಡಿ. ನೀವು ಅನೇಕ ಅಧಿಕ-ಬಡ್ಡಿ ಸಾಲಗಳನ್ನು ಹೊಂದಿದ್ದರೆ, ಅವುಗಳನ್ನು ಕಡಿಮೆ ಬಡ್ಡಿ ದರದಲ್ಲಿ ಒಂದಾಗಿ ಸಂಯೋಜಿಸಲು 'ಸಾಲ ಕ್ರೋಢೀಕರಣ' ಸಾಲವನ್ನು ಪರಿಗಣಿಸಿ. ಅಸ್ತಿತ್ವದಲ್ಲಿರುವ ಸಾಲಗಳನ್ನು ತೀರಿಸುವವರೆಗೆ ಹೊಸ ಸಾಲಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳುವುದನ್ನು ತಪ್ಪಿಸುವುದು ಬುದ್ಧಿವಂತಿಕೆ."
    },
    "HealthInsurance": {
        "en": "Health insurance is a policy that covers your medical and surgical expenses. It protects your savings from being depleted by unexpected hospital bills. Ayushman Bharat, or Pradhan Mantri Jan Arogya Yojana (PM-JAY), is a Government of India scheme that provides free health coverage up to ₹5 lakh per family per year for secondary and tertiary care hospitalization to poor and vulnerable families.",
        "kn": "ಆರೋಗ್ಯ ವಿಮೆ ಎನ್ನುವುದು ನಿಮ್ಮ ವೈದ್ಯಕೀಯ ಮತ್ತು ಶಸ್ತ್ರಚಿಕಿತ್ಸಾ ವೆಚ್ಚಗಳನ್ನು ಒಳಗೊಂಡಿರುವ ಪಾಲಿಸಿಯಾಗಿದೆ. ಇದು ಅನಿರೀಕ್ಷಿತ ಆಸ್ಪತ್ರೆ ಬಿಲ್‌ಗಳಿಂದ ನಿಮ್ಮ ಉಳಿತಾಯವನ್ನು ಖಾಲಿಯಾಗದಂತೆ ರಕ್ಷಿಸುತ್ತದೆ. ಆಯುಷ್ಮಾನ್ ಭಾರತ್, ಅಥವಾ ಪ್ರಧಾನ ಮಂತ್ರಿ ಜನ ಆರೋಗ್ಯ ಯೋಜನೆ (ಪಿಎಂ-ಜೆಎವೈ), ಭಾರತ ಸರ್ಕಾರದ ಒಂದು ಯೋಜನೆಯಾಗಿದ್ದು, ಬಡ ಮತ್ತು ದುರ್ಬಲ ಕುಟುಂಬಗಳಿಗೆ ದ್ವಿತೀಯ ಮತ್ತು ತೃತೀಯ ಆರೈಕೆ ಆಸ್ಪತ್ರೆಗೆ ದಾಖಲಾಗಲು ಪ್ರತಿ ಕುಟುಂಬಕ್ಕೆ ವಾರ್ಷಿಕ ₹5 ಲಕ್ಷದವರೆಗೆ ಉಚಿತ ಆರೋಗ್ಯ ರಕ್ಷಣೆಯನ್ನು ಒದಗಿಸುತ್ತದೆ."
    },
    "LifeInsurance": {
        "en": "Life insurance provides a financial payout (called a sum assured) to your family or beneficiaries upon your death. This ensures they are financially secure and can manage expenses in your absence. LIC (Life Insurance Corporation of India) is a government-owned insurer and is one of the most trusted and oldest insurance companies in India, offering a wide range of policies.",
        "kn": "ಜೀವ ವಿಮೆಯು ನಿಮ್ಮ ಮರಣದ ನಂತರ ನಿಮ್ಮ ಕುಟುಂಬ ಅಥವಾ ಫಲಾನುಭವಿಗಳಿಗೆ ಆರ್ಥಿಕ ಪಾವತಿಯನ್ನು (ವಿಮಾ ಮೊತ್ತ ಎಂದು ಕರೆಯಲಾಗುತ್ತದೆ) ಒದಗಿಸುತ್ತದೆ. ಇದು ನಿಮ್ಮ ಅನುಪಸ್ಥಿತಿಯಲ್ಲಿ ಅವರು ಆರ್ಥಿಕವಾಗಿ ಸುರಕ್ಷಿತವಾಗಿರಲು ಮತ್ತು ವೆಚ್ಚಗಳನ್ನು ನಿರ್ವಹಿಸಲು ಖಚಿತಪಡಿಸುತ್ತದೆ. ಎಲ್ಐಸಿ (ಭಾರತೀಯ ಜೀವ ವಿಮಾ ನಿಗಮ) ಸರ್ಕಾರಿ ಸ್ವಾಮ್ಯದ ವಿಮಾದಾರನಾಗಿದ್ದು, ಭಾರತದ ಅತ್ಯಂತ ವಿಶ್ವಾಸಾರ್ಹ ಮತ್ತು ಹಳೆಯ ವಿಮಾ ಕಂಪನಿಗಳಲ್ಲಿ ಒಂದಾಗಿದೆ, ಇದು ವ್ಯಾಪಕ ಶ್ರೇಣಿಯ ಪಾಲಿಸಿಗಳನ್ನು ನೀಡುತ್ತದೆ."
    },
    "GeneralInsurance": {
        "en": "General insurance covers non-life assets against loss or damage. This includes vehicle insurance for your car or scooter, home insurance against fire or theft, and travel insurance. The premium you pay depends on the value of the asset and the level of risk involved. It provides financial protection against unforeseen events, ensuring you don't have to bear the entire financial burden yourself.",
        "kn": "ಸಾಮಾನ್ಯ ವಿಮೆಯು ನಷ್ಟ ಅಥವಾ ಹಾನಿಯ ವಿರುದ್ಧ ಜೀವವಲ್ಲದ ಆಸ್ತಿಗಳನ್ನು ಒಳಗೊಂಡಿದೆ. ಇದು ನಿಮ್ಮ ಕಾರು ಅಥವಾ ಸ್ಕೂಟರ್‌ಗೆ ವಾಹನ ವಿಮೆ, ಬೆಂಕಿ ಅಥವಾ ಕಳ್ಳತನದ ವಿರುದ್ಧ ಗೃಹ ವಿಮೆ, ಮತ್ತು ಪ್ರಯಾಣ ವಿಮೆಯನ್ನು ಒಳಗೊಂಡಿದೆ. ನೀವು ಪಾವತಿಸುವ ಪ್ರೀಮಿಯಂ ಆಸ್ತಿಯ ಮೌಲ್ಯ ಮತ್ತು ಅದರಲ್ಲಿರುವ ಅಪಾಯದ ಮಟ್ಟವನ್ನು ಅವಲಂಬಿಸಿರುತ್ತದೆ. ಇದು ಅನಿರೀಕ್ಷಿತ ಘಟನೆಗಳ ವಿರುದ್ಧ ಆರ್ಥಿಕ ರಕ್ಷಣೆಯನ್ನು ಒದಗಿಸುತ್ತದೆ, ನೀವು ಸಂಪೂರ್ಣ ಆರ್ಥಿಕ ಹೊರೆಯನ್ನು ನೀವೇ ಹೊರಬೇಕಾಗಿಲ್ಲ ಎಂದು ಖಚಿತಪಡಿಸುತ್ತದೆ."
    },
    "StudentFinance": {
        "en": "Students can start their financial journey by opening a savings account, many of which have zero balance requirements for students. A Recurring Deposit (RD) is an excellent tool to save small amounts every month. For long-term goals, government schemes like the Sukanya Samriddhi Yojana offer high, tax-free interest rates for the financial security of a girl child.",
        "kn": "ವಿದ್ಯಾರ್ಥಿಗಳು ಉಳಿತಾಯ ಖಾತೆಯನ್ನು ತೆರೆಯುವ ಮೂಲಕ ತಮ್ಮ ಆರ್ಥಿಕ ಪ್ರಯಾಣವನ್ನು ಪ್ರಾರಂಭಿಸಬಹುದು, ಇವುಗಳಲ್ಲಿ ಹಲವು ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ ಶೂನ್ಯ ಬ್ಯಾಲೆನ್ಸ್ ಅವಶ್ಯಕತೆಗಳನ್ನು ಹೊಂದಿವೆ. ಮರುಕಳಿಸುವ ಠೇವಣಿ (ಆರ್‌ಡಿ) ಪ್ರತಿ ತಿಂಗಳು ಸಣ್ಣ ಮೊತ್ತವನ್ನು ಉಳಿಸಲು ಒಂದು ಅತ್ಯುತ್ತಮ ಸಾಧನವಾಗಿದೆ. ದೀರ್ಘಕಾಲೀನ ಗುರಿಗಳಿಗಾಗಿ, ಸುಕನ್ಯಾ ಸಮೃದ್ಧಿ ಯೋಜನೆಯಂತಹ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಹೆಣ್ಣು ಮಗುವಿನ ಆರ್ಥಿಕ ಭದ್ರತೆಗಾಗಿ ಹೆಚ್ಚಿನ, ತೆರಿಗೆ-ಮುಕ್ತ ಬಡ್ಡಿ ದರಗಳನ್ನು ನೀಡುತ್ತವೆ."
    },
    "WomenFinance": {
        "en": "There are several financial schemes designed specifically for women in India to promote their financial independence. The Mahila Samman Saving Certificate offers an attractive interest rate for a two-year deposit. The MUDRA Yojana provides loans to women entrepreneurs to start small businesses. Additionally, the Sukanya Samriddhi Yojana is a great saving scheme for the future of a daughter.",
        "kn": "ಭಾರತದಲ್ಲಿ ಮಹಿಳೆಯರ ಆರ್ಥಿಕ ಸ್ವಾತಂತ್ರ್ಯವನ್ನು ಉತ್ತೇಜಿಸಲು ವಿಶೇಷವಾಗಿ ವಿನ್ಯಾಸಗೊಳಿಸಲಾದ ಹಲವಾರು ಆರ್ಥಿಕ ಯೋಜನೆಗಳಿವೆ. ಮಹಿಳಾ ಸಮ್ಮಾನ್ ಉಳಿತಾಯ ಪ್ರಮಾಣಪತ್ರವು ಎರಡು ವರ್ಷಗಳ ಠೇವಣಿಗೆ ಆಕರ್ಷಕ ಬಡ್ಡಿ ದರವನ್ನು ನೀಡುತ್ತದೆ. ಮುದ್ರಾ ಯೋಜನೆಯು ಮಹಿಳಾ ಉದ್ಯಮಿಗಳಿಗೆ ಸಣ್ಣ ವ್ಯಾಪಾರಗಳನ್ನು ಪ್ರಾರಂಭಿಸಲು ಸಾಲವನ್ನು ಒದಗಿಸುತ್ತದೆ. ಹೆಚ್ಚುವರಿಯಾಗಿ, ಸುಕನ್ಯಾ ಸಮೃದ್ಧಿ ಯೋಜನೆಯು ಮಗಳ ಭವಿಷ್ಯಕ್ಕಾಗಿ ಒಂದು ಉತ್ತಮ ಉಳಿತಾಯ ಯೋಜನೆಯಾಗಿದೆ."
    },
    "SmartSavingTips": {
        "en": "Developing smart saving habits can significantly boost your finances. Start by setting a small, achievable daily saving goal, like saving your change. Track all your expenses for a month to see where your money goes. Consciously avoid impulse buying by waiting 24 hours before making a non-essential purchase. Automating your savings by setting up a monthly transfer to a savings account is also a very effective strategy.",
        "kn": "ಬುದ್ಧಿವಂತ ಉಳಿತಾಯ ಅಭ್ಯಾಸಗಳನ್ನು ಬೆಳೆಸಿಕೊಳ್ಳುವುದು ನಿಮ್ಮ ಹಣಕಾಸನ್ನು ಗಮನಾರ್ಹವಾಗಿ ಹೆಚ್ಚಿಸುತ್ತದೆ. ನಿಮ್ಮ ಚಿಲ್ಲರೆಯನ್ನು ಉಳಿಸುವಂತಹ ಸಣ್ಣ, ಸಾಧಿಸಬಹುದಾದ ದೈನಂದಿನ ಉಳಿತಾಯ ಗುರಿಯನ್ನು ಹೊಂದುವುದರೊಂದಿಗೆ ಪ್ರಾರಂಭಿಸಿ. ನಿಮ್ಮ ಹಣ ಎಲ್ಲಿಗೆ ಹೋಗುತ್ತದೆ ಎಂಬುದನ್ನು ನೋಡಲು ಒಂದು ತಿಂಗಳ ಕಾಲ ನಿಮ್ಮ ಎಲ್ಲಾ ಖರ್ಚುಗಳನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಿ. ಅನಗತ್ಯ ಖರೀದಿಯನ್ನು ಮಾಡುವ ಮೊದಲು 24 ಗಂಟೆಗಳ ಕಾಲ ಕಾಯುವ ಮೂಲಕ ಹಠಾತ್ ಖರೀದಿಯನ್ನು ಪ್ರಜ್ಞಾಪೂರ್ವಕವಾಗಿ ತಪ್ಪಿಸಿ. ಉಳಿತಾಯ ಖಾತೆಗೆ ಮಾಸಿಕ ವರ್ಗಾವಣೆಯನ್ನು ಸ್ಥಾಪಿಸುವ ಮೂಲಕ ನಿಮ್ಮ ಉಳಿತಾಯವನ್ನು ಸ್ವಯಂಚಾಲಿತಗೊಳಿಸುವುದು ಸಹ ಬಹಳ ಪರಿಣಾಮಕಾರಿ ತಂತ್ರವಾಗಿದೆ."
    },
    "FarmerSchemes": {
        "en": "The government offers several schemes to support farmers. PM-Kisan provides direct income support of ₹6,000 per year to small and marginal farmer families. The Pradhan Mantri Fasal Bima Yojana (PMFBY) is a crop insurance scheme that protects against crop failure. Additionally, banks provide agricultural loans at subsidized interest rates for various farming needs. Farmers can visit their local bank or Raitha Samparka Kendra for more details.",
        "kn": "ರೈತರನ್ನು ಬೆಂಬಲಿಸಲು ಸರ್ಕಾರವು ಹಲವಾರು ಯೋಜನೆಗಳನ್ನು ನೀಡುತ್ತದೆ. ಪಿಎಂ-ಕಿಸಾನ್ ಸಣ್ಣ ಮತ್ತು ಅತಿಸಣ್ಣ ರೈತ ಕುಟುಂಬಗಳಿಗೆ ವಾರ್ಷಿಕ ₹6,000 ನೇರ ಆದಾಯ ಬೆಂಬಲವನ್ನು ಒದಗಿಸುತ್ತದೆ. ಪ್ರಧಾನ ಮಂತ್ರಿ ಫಸಲ್ ಬಿಮಾ ಯೋಜನೆ (ಪಿಎಂಎಫ್‌ಬಿವೈ) ಬೆಳೆ ವೈಫಲ್ಯದ ವಿರುದ್ಧ ರಕ್ಷಣೆ ನೀಡುವ ಬೆಳೆ ವಿಮಾ ಯೋಜನೆಯಾಗಿದೆ. ಹೆಚ್ಚುವರಿಯಾಗಿ, ಬ್ಯಾಂಕುಗಳು ವಿವಿಧ ಕೃಷಿ ಅಗತ್ಯಗಳಿಗಾಗಿ ಸಬ್ಸಿಡಿ ಬಡ್ಡಿ ದರಗಳಲ್ಲಿ ಕೃಷಿ ಸಾಲಗಳನ್ನು ಒದಗಿಸುತ್ತವೆ. ಹೆಚ್ಚಿನ ವಿವರಗಳಿಗಾಗಿ ರೈತರು ತಮ್ಮ ಸ್ಥಳೀಯ ಬ್ಯಾಂಕ್ ಅಥವಾ ರೈತ ಸಂಪರ್ಕ ಕೇಂದ್ರಕ್ಕೆ ಭೇಟಿ ನೀಡಬಹುದು."
    },
    "WomenInvestment": {
        "en": "Women have many excellent investment options based on their financial goals. For low-risk, steady returns, Recurring Deposits (RD) and Public Provident Fund (PPF) are great choices. For potentially higher returns with market risks, Systematic Investment Plans (SIPs) in mutual funds are very popular. Gold bonds offer a way to invest in gold digitally. The best choice depends on your risk appetite, investment horizon, and financial objectives.",
        "kn": "ಮಹಿಳೆಯರಿಗೆ ಅವರ ಆರ್ಥಿಕ ಗುರಿಗಳನ್ನು ಆಧರಿಸಿ ಅನೇಕ ಅತ್ಯುತ್ತಮ ಹೂಡಿಕೆ ಆಯ್ಕೆಗಳಿವೆ. ಕಡಿಮೆ-ಅಪಾಯ, ಸ್ಥಿರ ಆದಾಯಕ್ಕಾಗಿ, ಮರುಕಳಿಸುವ ಠೇವಣಿಗಳು (ಆರ್‌ಡಿ) ಮತ್ತು ಸಾರ್ವಜನಿಕ ಭವಿಷ್ಯ ನಿಧಿ (ಪಿಪಿಎಫ್) ಉತ್ತಮ ಆಯ್ಕೆಗಳಾಗಿವೆ. ಮಾರುಕಟ್ಟೆ ಅಪಾಯಗಳೊಂದಿಗೆ ಸಂಭಾವ್ಯ ಹೆಚ್ಚಿನ ಆದಾಯಕ್ಕಾಗಿ, ಮ್ಯೂಚುಯಲ್ ಫಂಡ್‌ಗಳಲ್ಲಿನ ವ್ಯವಸ್ಥಿತ ಹೂಡಿಕೆ ಯೋಜನೆಗಳು (ಎಸ್‌ಐಪಿಗಳು) ಬಹಳ ಜನಪ್ರಿಯವಾಗಿವೆ. ಚಿನ್ನದ ಬಾಂಡ್‌ಗಳು ಡಿಜಿಟಲ್ ರೂಪದಲ್ಲಿ ಚಿನ್ನದಲ್ಲಿ ಹೂಡಿಕೆ ಮಾಡಲು ಒಂದು ಮಾರ್ಗವನ್ನು ನೀಡುತ್ತವೆ. ಅತ್ಯುತ್ತಮ ಆಯ್ಕೆಯು ನಿಮ್ಮ ಅಪಾಯ ಸಹಿಷ್ಣುತೆ, ಹೂಡಿಕೆ ಅವಧಿ, ಮತ್ತು ಆರ್ಥಿಕ ಉದ್ದೇಶಗಳನ್ನು ಅವಲಂಬಿಸಿರುತ್ತದೆ."
    },
    "ProtectFinance": {
        "en": "Protecting your finances in the digital age is crucial. Never share your OTP (One-Time Password), CVV, or PIN with anyone. Be cautious of clicking on unknown links or downloading suspicious attachments from emails or messages. Always use a secure UPI PIN for transactions and review your bank statements regularly to spot any unauthorized activity. Remember, your bank will never ask for your secret information over the phone.",
        "kn": "ಡಿಜಿಟಲ್ ಯುಗದಲ್ಲಿ ನಿಮ್ಮ ಹಣಕಾಸನ್ನು ರಕ್ಷಿಸುವುದು ಬಹಳ ಮುಖ್ಯ. ನಿಮ್ಮ ಒಟಿಪಿ (ಒಂದು-ಬಾರಿ ಪಾಸ್‌ವರ್ಡ್), ಸಿವಿವಿ, ಅಥವಾ ಪಿನ್ ಅನ್ನು ಯಾರೊಂದಿಗೂ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ. ಇಮೇಲ್‌ಗಳು ಅಥವಾ ಸಂದೇಶಗಳಿಂದ ಅಪರಿಚಿತ ಲಿಂಕ್‌ಗಳನ್ನು ಕ್ಲಿಕ್ ಮಾಡುವಾಗ ಅಥವಾ ಅನುಮಾನಾಸ್ಪದ ಲಗತ್ತುಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡುವಾಗ ಜಾಗರೂಕರಾಗಿರಿ. ವಹಿವಾಟುಗಳಿಗಾಗಿ ಯಾವಾಗಲೂ ಸುರಕ್ಷಿತ ಯುಪಿಐ ಪಿನ್ ಬಳಸಿ ಮತ್ತು ಯಾವುದೇ ಅನಧಿಕೃತ ಚಟುವಟಿಕೆಯನ್ನು ಪತ್ತೆಹಚ್ಚಲು ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಸ್ಟೇಟ್‌ಮೆಂಟ್‌ಗಳನ್ನು ನಿಯಮಿತವಾಗಿ ಪರಿಶೀಲಿಸಿ. ನೆನಪಿಡಿ, ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಫೋನ್ ಮೂಲಕ ನಿಮ್ಮ ರಹಸ್ಯ ಮಾಹಿತಿಯನ್ನು ಎಂದಿಗೂ ಕೇಳುವುದಿಲ್ಲ."
    },
    "Greeting": {
        "en": "Hello! I am Finease, your financial assistant. How can I help you today?",
        "kn": "ನಮಸ್ಕಾರ! ನಾನು ಫಿನೀಸ್, ನಿಮ್ಮ ಆರ್ಥಿಕ ಸಹಾಯಕ. ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?"
    },
    "Fallback": {
        "en": "I'm sorry, I don't have information on that topic. Please ask me about budgeting, saving, or insurance.",
        "kn": "ಕ್ಷಮಿಸಿ, ಆ ವಿಷಯದ ಬಗ್ಗೆ ನನ್ನ ಬಳಿ ಮಾಹಿತಿ ಇಲ್ಲ. ದಯವಿಟ್ಟು ಬಜೆಟ್, ಉಳಿತಾಯ, ಅಥವಾ ವಿಮೆಯ ಬಗ್ಗೆ ಕೇಳಿ."
    }
}
