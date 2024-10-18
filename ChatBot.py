import openai
import os

# Set up the OpenAI API key securely
openai.api_key = q

# Define the Bot’s Goals, Guidelines, and Examples in the System Message
SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are a salesperson for a small group training gym called Full Circle Fitness. Your task is to interact with leads in a natural, conversational manner, ensuring they believe they are speaking to a real person. A templated message will be sent initially, which reads: "
        "'Hi Firstname, I hope you're well. I'm Harry from Full Circle Fitness. I understand that you previously looked at joining the gym. I just wanted to check in with you and see how your fitness goals are going so far and if there's anything you're struggling with that I could help with? Thanks.' "
        "Once the lead responds, your objective is to engage them in a friendly conversation, gathering information about their fitness goals. Use this information to explain why Full Circle Fitness would be a great fit for them. Your ultimate goal is to schedule them for a free session at the gym to see if it's the right fit. At all times, maintain a natural, personable tone, and ensure that the lead remains unaware they are interacting with a chatbot. "
        "Guidelines:\n"
        "1. Adapt responses based on the specific context and user input.\n"
        "2. If the user expresses confusion, offer clarification or additional information. If you are unsure of any answers state that you are not sure but that is a question that can be answered by one of the coaches in a session\n"
        "3. If the user seems uninterested or disengaged after a few messages end the conversation and don't say anything\n"
        "4. For gym specific information, refer to the company info section for your responses\n"
        "5. When trying to get someone booked into the gym, include this link as it is the booking link: https://go.full-circle-fitness.co.uk/info\n"
        "6. Strive to leave the user with a positive experience, regardless of the outcome.\n\n"

        "Examples:\n"
        "User: I'm not sure what I need.\n"
        "Assistant: That's okay! Can you tell me a bit about what you're trying to accomplish? I can help guide you to the right solution.\n\n"

        "User: I don't want to talk about this right now.\n"
        "Assistant: I understand. If you ever want to continue, I'm here to help. Have a great day!\n\n"

        "User: This is too expensive for me.\n"
        "Assistant: I understand that budget is a concern. Would you like to explore some other options that might better fit your budget?\n"
    )
}

# Company-Specific Information
COMPANY_INFO = {
    "name": "Full Circle Fitness",
    "about_services": (
        "Full Circle Fitness is a premium group training gym based in Cambridge. They offer a mix of small group training sessions "
        "such as circuit training, strength training, mobility, and cardio workouts to suit most people’s fitness needs. "
        "With 43 fully coached sessions every week, they also provide nutritional advice to cut through the confusion. "
        "The variety of sessions caters to various goals, including improving strength, muscle mass, general health and fitness, "
        "cardio, and mobility. The small group training format ensures personalized attention from coaches, helping members stay "
        "accountable and motivated."
    ),
    "owner_message": (
        "Message from the owner: I have nearly 20 years of experience helping regular people make fitness a part of their everyday "
        "life and finally put their health at the top of the pile. I have a straightforward perspective on fitness and can’t stand "
        "much of the fitness BS you read about. Like many reading this, I struggle to be consistent 100% of the time. This is why "
        "I built FCF. If I can help you do better than if you went it alone and help you achieve some AWESOME things (you never "
        "thought were possible), then I’ve done my job!"
    ),
    "tools_gadgets": (
        "They offer a number of tools and gadgets such as:\n\n"
        "TrueCoach: Helps track your exercise progress, nutrition, and stay in touch outside of the gym using the TrueCoach software and app.\n\n"
        "InBody: Provides a detailed breakdown of your body composition, including lean mass, body fat, and muscle, with a quick, "
        "accurate, and non-invasive process.\n\n"
        "MyZone: Rewards you based on the effort your heart is putting in during workouts, with Myzone Effort Points (MEPs) tailored "
        "to your heart rate, not your fitness level."
    ),
    "ethos": (
        "There is so much fitness noise out there, so we’ll help you cut through it all and get RESULTS! We only ever work with a limited "
        "number of people in small groups. You’ll get the guidance and accountability of having a Personal Trainer but without the price tag."
    ),
    "selling_points": [
        "Accountability and guidance without the high price of a personal trainer",
        "Focus on helping ordinary people achieve their fitness goals",
        "Nutritional advice",
        "Variety of many classes each week at different times"
    ],
    "faq": {
        "I have never trained before, is FCF for me?": (
            "YES! We cater to most abilities. Our job is to help you succeed with your training. We are always very happy to switch things "
            "up to help make your workout challenging but achievable."
        ),
        "What kind of training do you do?": (
            "We offer a blend of strength and conditioning designed to help people just like you get fitter, stronger, and leaner."
        ),
        "How long are sessions?": "Our sessions range from 45-60 minutes.",
        "Is there parking?": "Yes! Plenty.",
        "Is there a contract?": (
            "All we ask is for you to stick with us for 3 months so we can help show you just what you are capable of!"
        ),
        "Where are you based?": "Dry Drayton, CB23 8AT.",
        "What are your opening hours?": "6am till 7:30pm most days.",
        "Do you offer group classes?": "We specialize in small group coaching.",
        "How much does membership cost?": "Membership starts at just £85 per month and goes up to £149 per month.",
        "Do you offer any trial sessions?": (
            "YES! We insist you have a try first so you can check out what it’s all about and see if it’s a good fit for you."
        ),
        "Can I bring a friend to my session?": "Absolutely!",
        "What should I bring to my first session?": "A positive attitude, a water bottle, and gym wear.",
        "Are your coaches certified?": "Yes. All of our coaches are certified, fully insured, and first aid qualified.",
        "Do you offer nutritional advice?": "All of our members receive as much nutrition support as they need.",
        "Can I book sessions online?": "Yes. Our booking app is flexible and makes booking your sessions very easy.",
        "Do you have showers and changing facilities?": "Yes, we do.",
        "Is there a minimum age requirement to join?": "18 is the minimum age requirement.",
        "Do you offer corporate memberships?": (
            "We can tailor a bespoke membership package to suit you and your employees."
        ),
        "Can I freeze my membership if I go on holiday?": (
            "This is not something we offer, but we do not have long tie-in periods."
        ),
        "What are the differences between your different classes?": "No one does it like we do!"
    }
}


# Conversation Handling Logic with Dynamic Engagement Analysis
def generate_response(conversation):
    # Generate the response using OpenAI's GPT-4 API
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=conversation
    )

    return response.choices[0].message.content


# User Interaction
def chat():
    conversation = [SYSTEM_MESSAGE]  # Start the conversation with the system message
    print(
        "Hi Firstname, I hope you're well. I'm Harry from Full Circle Fitness. I understand that you previously looked at joining the gym. I just wanted to check in with you and see how your fitness goals are going so far and if there's anything you're struggling with that I could help with? Thanks")

    while True:
        user_input = input("You: ")

        # Add user input to the conversation history
        conversation.append({"role": "user", "content": user_input})

        # Generate response from GPT-4
        response = generate_response(conversation)
        print("Bot:", response)

        # Add the bot's response to the conversation history
        conversation.append({"role": "assistant", "content": response})

        # Ask GPT-4 to assess if the user wants to continue the conversation
        termination_check_prompt = {
            "role": "system",
            "content": (
                "Based on the conversation so far, determine whether the user is still engaged or interested. "
                "If the user seems uninterested or wishes to end the conversation after a couple messages, respond with 'terminate'. "
                "If the conversation should continue, continue the conversation."
            )
        }
        conversation.append(termination_check_prompt)
        termination_decision = generate_response(conversation)

        if 'terminate' in termination_decision.lower():
            print(
                "It seems you're not interested. I'll end our conversation here. If you need anything, feel free to reach out. Goodbye!")
            break

        # Remove the termination check prompt and decision from the conversation history to keep it clean
        conversation.pop()


if __name__ == "__main__":
    chat()
