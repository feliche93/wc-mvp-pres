from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)
example = """
Advising regulated financial firms regarding internal investigations in relation to failures in systems and controls regarding money laundering.
Advising a financial institution regarding a criminal investigation into customers and associated money laundering reporting obligations and injunctive proceedings.
Investigating and reporting on the source of wealth of corporates and high-net-worth individuals.
Advising an SPV regarding an internal investigation into allegations of fraud and corruption in relation to an LNG to power project.
Advising a corporate regarding an internal investigation, a self-report to the Serious Fraud Office and the deferred prosecution agreement process.
Advising a global tech company regarding an internal investigation into allegations of fraud and corruption in relation to a business critical infrastructure project.
Advising senior executives under investigation regarding allegations of bribery, fraud, accounting irregularities and/or money laundering.
Advising individuals under investigation by the Financial Conduct Authority, the U.S. Department of Justice and other agencies in relation to trading activity.
Advising corporates and individuals regarding investigations by HM Revenue & Customs into allegations of tax fraud, sanctions busting and money laundering.
    """

ner_results = nlp(example)
print(ner_results)

df = pd.DataFrame(ner_results)
df[df['entity'] == 'B-ORG']