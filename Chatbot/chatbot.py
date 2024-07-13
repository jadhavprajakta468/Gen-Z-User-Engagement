from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

app = Flask(__name__)
CORS(app)

nltk.download('punkt')
nltk.download('stopwords')

responses = {
    "greetings": ["Hi there! How can I assist you with your fashion needs today?",
                  "Hello! How can I help you today?",
                  "Hi! What can I do for you?",
                  "Hey! How can I assist you with fashion today?",
                  "Hi! Need some style advice?"],
    "recommendation": ["Sure! I can recommend outfits based on your style preferences. What are you looking for?",
                       "I'd be happy to recommend something. Do you have a specific style or occasion in mind?",
                       "Tell me more about what you like, and I'll find something perfect for you.",
                       "I can help with recommendations. What’s your style preference or occasion?",
                       "Looking for a new outfit? Let me know your style and I'll suggest something great."],
    "discount": ["We have great discounts available! What type of products are you interested in?",
                 "Looking for discounts? Let me know the product type, and I'll find the best deals for you.",
                 "Discounts are available on many items! What are you looking to buy?",
                 "I can help you find the best discounts. What are you shopping for?",
                 "There are discounts on various items. Tell me what you’re looking for, and I'll find the best deals."],
    "availability": ["I can check the availability for you. Which product are you interested in?",
                     "Let me find out if we have that in stock. What’s the item?",
                     "I can look up availability. Please provide the product details.",
                     "Which product are you looking for? I’ll check if it's available.",
                     "Tell me the product name or category, and I'll check the availability for you."],
    "shipping": ["We offer various shipping options. Where do you need the item shipped?",
                 "I can help with shipping information. Where is your delivery location?",
                 "Let me provide you with shipping details. What’s your delivery address?",
                 "We have several shipping methods. Where should the item be delivered?",
                 "I can check the shipping options for you. Where do you need the item shipped to?"],
    "returns": ["Our return policy allows returns within 30 days of purchase. Please ensure the item is unused and in its original packaging.",
                "Returns are accepted within 30 days of purchase. You’ll need to provide proof of purchase for a full refund.",
                "You can return items within 30 days for a refund or exchange. Make sure the product is in its original condition.",
                "Our return policy is straightforward: returns are accepted within 30 days of purchase.",
                "We have a flexible return policy. You can return items within 30 days as long as they are unused and in their original packaging."],
    "trendy": ["Right now, oversized blazers and wide-leg pants are very trendy!",
               "Trendy fashion at the moment includes pastel colors and chunky sneakers.",
               "Fashion trends currently include vintage-inspired dresses and sustainable fabrics.",
               "Street style trends right now are all about graphic tees and distressed jeans.",
               "Trendy accessories include statement earrings and mini bags."],
    "new_arrivals": ["Check out our latest collection! We have new arrivals in every category.",
                     "Our new arrivals section is updated weekly. Take a look!",
                     "New styles just dropped! Visit our new arrivals to see the latest trends.",
                     "We have exciting new arrivals! Explore the freshest additions to our collection.",
                     "Discover our new arrivals for the latest in fashion."],
    "style_suggestions": {
        "casual": "For a casual look, you might like our selection of comfortable jeans, t-shirts, and sneakers.",
        "formal": "For a formal occasion, consider our range of tailored suits, elegant dresses, and classic shoes.",
        "sporty": "For a sporty style, check out our collection of activewear, including leggings, sports bras, and running shoes.",
        "bohemian": "For a bohemian vibe, you might enjoy our flowy dresses, floral prints, and wide-brim hats.",
        "streetwear": "For a streetwear look, explore our hoodies, joggers, and trendy sneakers."
    },
    "summer_trends": ["Summer trends this season include lightweight fabrics, floral prints, and bright colors.",
                      "For summer, consider outfits like sundresses, shorts, and breathable tops.",
                      "Popular summer styles include linen shirts, maxi dresses, and sandals.",
                      "Stay cool in summer with breezy outfits like tank tops, skirts, and flip flops.",
                      "Accessorize for summer with sunglasses, hats, and beach bags."],
    "winter_trends": ["Winter fashion trends feature cozy sweaters, wool coats, and layered outfits.",
                      "For winter, try outfits like trench coats, boots, and knit scarves.",
                      "Stylish winter options include pea coats, cashmere sweaters, and thermal leggings.",
                      "Stay warm in winter with essentials like gloves, earmuffs, and insulated jackets.",
                      "Accessorize for winter with beanies, scarves, and stylish boots."],
    "monsoon_trends": ["Monsoon trends include waterproof jackets, umbrellas, and rain boots.",
                       "For monsoon fashion, consider outfits like raincoats, waterproof pants, and quick-dry tops.",
                       "Stay dry in monsoon with essentials like ponchos, umbrellas, and waterproof bags.",
                       "Stylish monsoon options include trench coats, ankle boots, and moisture-wicking fabrics.",
                       "Accessorize for monsoon with water-resistant watches, hats, and rainproof backpacks."],
    "size_guide": ["You can find our size guide on the product page under the 'Size Chart' tab.",
                   "Our size guide is available on each product page. Look for the 'Size Chart' tab.",
                   "To find your size, check the 'Size Chart' tab on the product page.",
                   "Look for the 'Size Chart' tab on the product page to view our size guide.",
                   "The size guide can be found under the 'Size Chart' tab on our product pages."],
    "sales": ["We currently have new sales running! Check out our website for the latest discounts.",
              "New sales are now live! Visit our website to see the great deals available.",
              "Don't miss out on our latest sales! Head over to our website to explore the discounts.",
              "Exciting sales are happening now! Browse our website for incredible offers.",
              "Discover amazing deals in our new sales! Visit our website to find your favorites."],
    "try_on_clothes": ["You can try on clothes using our virtual try-on feature! Just select the item and use your phone camera for a virtual fitting.",
                       "Try on clothes virtually with our AR feature! Choose an item and see how it looks on you using your smartphone.",
                       "Experience our virtual try-on for clothes! Simply pick an item and use AR to see how it fits you without trying it on physically.",
                       "Explore our virtual try-on option to see how clothes look on you before buying! Use AR on your smartphone for a fitting experience.",
                       "Try clothes virtually with our AR technology! Select an item and use your phone to see how it suits you without visiting the store."],
    "affordable_brands": ["We offer a range of affordable brands that combine style and value. Check out our budget-friendly options!",
                          "Discover our selection of affordable brands that cater to your fashion needs without breaking the bank.",
                          "Explore our affordable brands for stylish options that fit your budget!",
                          "We have several affordable brands that offer trendy styles at reasonable prices.",
                          "Shop from our affordable brands for great fashion at wallet-friendly prices!"],
    "competitions": ["We regularly host exciting competitions! Visit our website or app to participate and win amazing prizes.",
                     "Check out our ongoing competitions! Join now for a chance to win exclusive rewards.",
                     "Explore our competitions section for opportunities to win prizes and more!",
                     "Participate in our competitions for a chance to win exciting rewards!",
                     "Join our competitions to win fabulous prizes and enjoy great experiences."],
    "trendy_brands": ["Discover trendy brands that set the fashion trends! Explore our collection of brands known for their stylish offerings.",
                      "Explore our trendy brands section for the latest in fashion and style.",
                      "Shop from our curated list of trendy brands for the latest fashion statements.",
                      "Check out our trendy brands known for their cutting-edge designs and popular styles.",
                      "Browse through our trendy brands collection to stay ahead in fashion."],
    "accessories_available": ["We have a wide range of accessories available, including bags, shoes, jewelry, and more! Explore our accessories collection.",
                              "Discover a variety of accessories to complement your style. Shop bags, shoes, and jewelry from our collection.",
                              "Explore our selection of accessories, including bags, shoes, and jewelry, to complete your look.",
                              "Check out our accessories section for stylish bags, shoes, and jewelry.",
                              "Find the perfect accessories to enhance your outfit. Shop bags, shoes, and jewelry from our collection."],
    "fallback": ["I'm here to help with all your fashion queries. Can you please elaborate on what you need?",
                 "I'm not sure I understand. Could you please provide more details?",
                 "Let's try that again. What exactly are you looking for?",
                 "I didn’t quite catch that. Could you please rephrase or provide more information?",
                 "I'm here to assist you. Could you give me more details about what you're looking for?"],
    "goodbye": ["Have a great day!",
                "Thanks for chatting with me. Have a wonderful day!",
                "Goodbye! Take care.",
                "Until next time! Have a good one.",
                "See you later!"]
}

def preprocess_input(user_message):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(user_message)
    filtered_sentence = [w.lower() for w in word_tokens if w.lower() not in stop_words and w not in string.punctuation]
    return filtered_sentence


import random

def get_response(user_message):
    processed_message = preprocess_input(user_message)

    if any(word in processed_message for word in ["hello", "hi", "hey"]):
        return {"response": random.choice(responses["greetings"])}
    elif any(word in processed_message for word in ["recommend", "suggest", "advice"]):
        return {"response": random.choice(responses["recommendation"])}
    elif any(word in processed_message for word in ["discount", "sale", "offer"]):
        return {"response": random.choice(responses["discount"])}
    elif any(word in processed_message for word in ["shipping", "delivery"]):
        return {"response": random.choice(responses["shipping"])}
    elif any(word in processed_message for word in ["returns", "return policy"]):
        return {"response": random.choice(responses["returns"])}
    elif any(word in processed_message for word in ["new arrivals", "new"]):
        return {"response": random.choice(responses["new_arrivals"])}
    elif any(word in processed_message for word in ["style suggestions", "style advice", "outfit ideas"]):
        if "casual" in processed_message:
            return {"response": responses["style_suggestions"]["casual"]}
        elif "formal" in processed_message:
            return {"response": responses["style_suggestions"]["formal"]}
        elif "sporty" in processed_message:
            return {"response": responses["style_suggestions"]["sporty"]}
        elif "bohemian" in processed_message:
            return {"response": responses["style_suggestions"]["bohemian"]}
        elif "streetwear" in processed_message:
            return {"response": responses["style_suggestions"]["streetwear"]}
        else:
            return {"response": "Can you specify the style you're looking for? (casual, formal, sporty, bohemian, streetwear)"}
    elif any(word in processed_message for word in ["summer trends", "summer fashion"]):
        return {"response": random.choice(responses["summer_trends"])}
    elif any(word in processed_message for word in ["winter trends", "winter fashion"]):
        return {"response": random.choice(responses["winter_trends"])}
    elif any(word in processed_message for word in ["sales", "deals"]):
        return {"response": random.choice(responses["sales"])}
    elif any(word in processed_message for word in ["try on", "virtual try on", "try clothes"]):
        return {"response": random.choice(responses["try_on_clothes"])}
    elif any(word in processed_message for word in ["affordable brands", "cheap brands", "budget brands"]):
        return {"response": random.choice(responses["affordable_brands"])}
    elif any(word in processed_message for word in ["competitions", "contests"]):
        return {"response": random.choice(responses["competitions"])}
    elif any(word in processed_message for word in ["trendy brands", "popular brands"]):
        return {"response": random.choice(responses["trendy_brands"])}
    elif any(word in processed_message for word in ["accessories", "must-have accessories"]):
        return {"response": random.choice(responses["accessories_available"])}
    elif any(word in processed_message for word in ["goodbye", "bye"]):
        return {"response": random.choice(responses["goodbye"])}
    elif any(word in processed_message for word in ["size", "guide"]):
        return {"response": random.choice(responses["size_guide"])}
    else:
        return {"response": random.choice(responses["fallback"])}



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get("message")
    response = get_response(user_message)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
