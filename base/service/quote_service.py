from openai import OpenAI
import json

API_CALL = True

client = OpenAI(organization='org-fg5NeKWBmc0tpExrrvfzBMNC')

class QuoteService:
  @staticmethod
  def generate(language = 'English'):
    if not API_CALL:
      return QuoteService.__get_fallback_quote()
    
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"You are a quote assistant, skilled in generating quote in the language {language}."},
        {"role": "user", "content": "Generate a quote with the author name, generate a JSON without any whitespaces with properties 'message' which has the actual quote and a property 'quotee' which has quotee's name"}
      ],
    )

    return json.loads(completion.choices[0].message.content)
  
  @staticmethod
  def __get_fallback_quote():
    return { 'message': 'The best way to predict the future is to create it.', 'quotee': 'Peter Drucker' }
