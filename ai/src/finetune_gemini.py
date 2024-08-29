import json
import time

import google.generativeai as genai

base_model = "models/gemini-1.5-flash-001-tuning"
# read training data from ft/gen/formatted_dataset.json
with open("ft/gen/formatted_dataset.json") as f:
  training_data = json.load(f)
print("training_data", len(training_data))
# raise Exception("Not implemented")
operation = genai.create_tuned_model(
  # You can use a tuned model here too. Set `source_model="tunedModels/..."`
  display_name="mesop-ft",
  source_model=base_model,
  #   epoch_count=20,
  #   batch_size=4,
  #   learning_rate=0.001,
  training_data=training_data,
)

for status in operation.wait_bar():
  time.sleep(10)

result = operation.result()
print(result)
# # You can plot the loss curve with:
# snapshots = pd.DataFrame(result.tuning_task.snapshots)
# sns.lineplot(data=snapshots, x='epoch', y='mean_loss')

model = genai.GenerativeModel(model_name=result.name)
result = model.generate_content("III")
print(result.text)  # IV
