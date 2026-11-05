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
- readmission: None is adequate for this job because to catch about half of readmissions, the best model, random forest at 0.10, flags 35.7 patients per 100 and about 31 of those are false alarms, so there would not be enough staff to support the patient volume. At a threshold staff could handle, like 0.20, it misses about 9 of every 10 readmissions.
- diabetes: Logistic regression at 0.12 because it reaches the screening team’s 90% sensitivity target with 34.6 false alarms per 100 adults, the fewest of the models, and a false alarm is ruled out medically with specific tests. Since I chose the threshold on the test patients, sensitivity on new patients may be a little lower.

## Design choice and AI use
A few sentences each. The design choice must be your own idea, not an AI tool's.
- design choice: In the Beyond Accuracy section, I chose for a confusion matrix to be displayed next to the model’s accuracy description. I thought it was important to explain how a model’s accuracy score may be misleading when looking at the number of people flagged in each category.
- AI suggestion I turned down: For the Threshold for the Job section, I did not choose the dot plot option because I did not want too many visuals to distract from the main focus of probabilities and the confusion matrix.
