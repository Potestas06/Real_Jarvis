from fastai.text.all import *

# replace it with the path to your dataset
path = '/path/to/dataset'


df = pd.read_csv(path, header=None, names=['label', 'text'])
df.head()

dls = TextDataLoaders.from_df(df, text_col='text', label_col='label', valid_pct=0.2, is_lm=False)

learn = text_classifier_learner(dls, AWD_LSTM, drop_mult=0.5, metrics=accuracy)

learn.fine_tune(4, 1e-2)

learn.show_results()

model_path = '/model'
learn.export(model_path)

loaded_model = load_learner(model_path)

test_text = "This is a test sentence."
prediction = loaded_model.predict(test_text)
print(f"Predicted label: {prediction[0]}, Confidence: {prediction[2][1].item()}")
