from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType 
from langchain_community.llms import Ollama
from langchain.tools import tool
import requests
import re
from langchain.agents import AgentExecutor

llm=Ollama(model="llama3")

symptom_to_drug={
    "headche":["Paracetamol","Aspirin","Ibuprofen"],
    "fever":["Paracetamol","Aspirin","Ibuprofen"],
    "cough":["Dextromethronphan","Codeine","Guaifenesin"],
    "cold": ["Antihistamines", "Decongestants"],
    "pain": ["Ibuprofen", "Aspirin", "Paracetamol"]
}
@tool
def fetch_drug_info(drug_name:str)->str:
    """
    Fetches drug info
    """
    api_url = f"https://api.fda.gov/drug/label.json?search=generic_name:\"{drug_name}"
    response=requests.get(api_url)
    data=response.json()
    result=data["results"][0]
    description=result.get("indications_and_usage",["No description available"])[0]
    side_effects = result.get("side_effects", ["No side effects reported"])[0]
    dosage = result.get("dosage_and_administration", ["No dosage information available"])[0]
    return f"""Drug:{drug_name}
    -**Description**:{description}
    -**Side effects**:{side_effects}
    -**Dosage**:{dosage}
    """
@tool
def suggest_drugs(symptoms:str)->str:
    """
    Suggest drugs
    """
    clean_q=re.sub(r"[^a-zA-Z\s]","",symptoms).strip().lower()
    suggested_drugs=[]
    for symptom,drugs in symptom_to_drug.items():
        if symptom in clean_q:
            suggested_drugs.extend(drugs)
    drug_info=""
    for drug in set(suggested_drugs):
        drug_info=drug_info+fetch_drug_info(drug)+"\n"
    return drug_info 


@tool
def drug_info_func(query:str)->str:
    """
    This tool fetches drug-related info from an api.
    Example:"What is aspirin?"
    """
    clean_query = re.sub(r"[^a-zA-Z\s]", "", query).strip().lower()
    clean_query = re.sub(r"^what\s+is\s+", "", clean_query)
    api_url=url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{clean_query}"
    response=requests.get(api_url)
    if response.status_code==200:
        data=response.json()
        result = data["results"][0]
        openfda = result.get("openfda", {})
        name = openfda.get("generic_name", ["Unknown"])[0].capitalize()
        brand = openfda.get("brand_name", ["Unknown"])[0]
        purpose = result.get("purpose", ["Not specified"])[0]
        usage = result.get("indications_and_usage", ["Not specified"])[0]
        warnings = result.get("warnings", ["Not specified"])[0]
        dosage = result.get("dosage_and_administration", ["Not specified"])[0]
        pregnancy = result.get("pregnancy_or_breast_feeding", ["Not specified"])[0]
        side_effects = result.get("adverse_reactions", ["Not reported"])[0]
        manufacturer = openfda.get("manufacturer_name", ["Unknown"])[0]
        route = openfda.get("route", ["Unknown"])[0]
        ndc = openfda.get("product_ndc", ["Unknown"])[0]
        return f"""🧾 Drug: {name} ({brand})
         - **Purpose**: {purpose}
         - **Indications/Usage**: {usage}
         - **Dosage**: {dosage}
         - **Warnings**: {warnings[:500]}...  \n(Truncated for length)
         - **Pregnancy Warning**: {pregnancy}
         - **Manufacturer**: {manufacturer}
         - **Route**: {route}
         - **NDC Code**: {ndc}
        """
    else:
        return "Soryy,I can't find any information"

@tool
def bmi_calculator(info:str)->str:
    """
   Calculate BMI from 'height=170,weight=73'.
    """
    cleaned = info.strip().replace("'", "").replace('"', '')
    parts={}
    for part in cleaned.split(','):
        if '=' in part:
            key,value=part.strip().split('=',1)
            parts[key.strip()]=float(value.strip())
    height=parts.get('height')
    weight=parts.get('weight')
    height_in_meters=height/100
    bmi=weight/(height_in_meters**2)
    return f"Your BMI is {bmi:.2f}"
@tool
def health_risk_calculator(age:int,cholesterol:int,blood_pressure:int)->str:
    """
    It will calculate the risk calculator and give the conclusion
    """
    risk_score=0
    if age>=45:
        risk_score+=1
    if cholesterol>=200:
        risk_score+=1
    if blood_pressure>=145:
        risk_score+=1

    if risk_score>=3:
        return "High risk please consult doctor"
    if risk_score>=2:
        return "Moderate risk please follow some suggesstions from doctor"
    if risk_score<=1:
        return "No need to worry You have less risk"

@tool
def extract_health_data(query):
    """
    Calculates the heart disease risk based on age, cholesterol level, and blood pressure.
    Returns a risk category (e.g., Low, Medium, High).
    """
    # query = "age=52,cholesterol=230,blood_pressure=145"
    parts = {}
    for part in query.split(','):
        if '=' in part:
            key, value = part.split('=')
            parts[key.strip()] = float(value.strip())
    age = parts.get("age")
    cholesterol = parts.get("cholesterol")
    blood_pressure = parts.get("blood_pressure")
    result = health_risk_calculator(age=age, cholesterol=cholesterol, blood_pressure=bp)
    return result

@tool
def recommend_lifestyle_changes(condition:str)->str:
    """
    Recommends for lifestyle
    """
    condition=condition.lower().strip()
    recommendation={
        "high blood pressure": [
            "Reduce salt intake",
            "Exercise regularly (30 minutes daily)",
            "Limit alcohol and caffeine",
            "Maintain a healthy weight",
            "Quit smoking"
        ],
        "diabetes": [
            "Eat a low-sugar, high-fiber diet",
            "Exercise regularly",
            "Monitor blood sugar levels",
            "Maintain healthy weight",
            "Avoid sugary drinks"
        ],
        "obesity": [
            "Follow a calorie-controlled diet",
            "Increase daily physical activity",
            "Reduce portion sizes",
            "Limit processed and high-fat foods",
            "Drink plenty of water"
        ],
    }
    if condition in recommendation:
        advice = "\n- " + "\n- ".join(recommendation[condition])
        return f"Life Style advice for *{condition.title()}*:\n{advice}"

    
tools=[drug_info_func,bmi_calculator,suggest_drugs,recommend_lifestyle_changes,extract_health_data]
agent=initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent.agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True 
)
question=input("Ask your healthcare question: ")
response = agent_executor.run(question)
print("Agent:",response)
