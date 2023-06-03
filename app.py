from flask import Flask, render_template, request
from flask_weasyprint import HTML, render_pdf

app = Flask(__name__)

class Party:
    def __init__(self, name, address, proof_document=None, signature=None):
        self.name = name
        self.address = address
        self.proof_document = proof_document
        self.signature = signature

class RentalAgreement:
    def __init__(self, party1, party2):
        self.party1 = party1
        self.party2 = party2

    def generate_agreement(self):
        agreement = f"""RENTAL AGREEMENT

This Rental Agreement (the "Agreement") is made and entered into this day between:

Party 1:
Name: {self.party1.name}
Address: {self.party1.address}

Party 2:
Name: {self.party2.name}
Address: {self.party2.address}

Hereby both parties agree to the following terms and conditions:

...

Please sign below:

Party 1 Signature: {self.party1.signature}

Party 2 Signature: {self.party2.signature}
"""

        return agreement

@app.route('/', methods=['GET', 'POST'])
def rental_agreement():
    if request.method == 'POST':
        # Get form data
        party1_name = request.form['party1_name']
        party1_address = request.form['party1_address']
        party1_proof_document = request.files['party1_proof_document']
        party1_signature = request.form['party1_signature']
        party2_name = request.form['party2_name']
        party2_address = request.form['party2_address']
        party2_proof_document = request.files['party2_proof_document']
        party2_signature = request.form['party2_signature']

        # Save uploaded files
        party1_proof_document.save(party1_proof_document.filename)
        party2_proof_document.save(party2_proof_document.filename)

        # Create Party objects
        party1 = Party(party1_name, party1_address, 
                       party1_proof_document.filename, party1_signature)
        party2 = Party(party2_name, party2_address, 
                       party2_proof_document.filename, party2_signature)

        # Create RentalAgreement object
        agreement = RentalAgreement(party1, party2)

        # Generate the rental agreement
        agreement_text = agreement.generate_agreement()

        # Generate PDF
        pdf = render_pdf(HTML(string=agreement_text))

        # Render the template with the generated agreement and PDF
        return render_template('agreement.html', 
                               agreement=agreement_text, pdf=pdf)
    
    # Render the form template
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
