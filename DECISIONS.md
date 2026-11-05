# Decisions

<!-- Fill in each section at the step the activity website gives, then commit and push.
     Write each answer after its label. Keep the headings and labels exactly as they are:
     `python -m analysis` reads them. Limit: 150 words for Before results.
     Fill in Recommendations and Design choice and AI use last, once your app is built. -->

## Before results
For each dataset: positive class; which error matters more for the job (missed positive or false alarm) and why.
- readmission:
Positive class: Positive class is readmitted patients within 30 days. A missed positive matters more because the patient is not getting the care or preventative care they need. A false alarm only costs a follow-up call from a provider talking about lab results and symptoms, and a medical professional uses their medical training to make the ultimate decision. But if the model predicts positive for too many patients, there may not be enough staff to support the patient volume.

- diabetes: Positive class is a patient having diabetes. A missed positive matters more because there could be potential fatal results or long-term health effects. A false alarm would be ruled out medically with specific tests and become a confirmed no, though too many flags could cause capacity and budget issues.

## Recommendations
- readmission: <model and threshold, or "none is adequate for this job"> because ...
- diabetes: ...

## Design choice and AI use
A few sentences each. The design choice must be your own idea, not an AI tool's.
- design choice: <one thing you chose to show, or leave out, for your clinical lead> because ...
- AI suggestion I turned down: <what an AI tool suggested, and why you didn't use it, or "no AI tools used">
