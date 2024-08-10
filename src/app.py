import requests
import json
import transformers
from transformers import ViTFeatureExtractor, ViTForImageClassification
import warnings
from PIL import Image
from io import BytesIO
warnings.filterwarnings('ignore')
api_key = 'Pg4KovXV5JCvaXooRRyxew==4SEE299nmZkw7xBI'
import gradio as gr

def food_identification(img_path):
    model_name = "google/vit-base-patch16-224"
    feature_extractor = ViTFeatureExtractor.from_pretrained(model_name)
    model = ViTForImageClassification.from_pretrained(model_name)
    try:
        image = Image.open(img_path)
    except FileNotFoundError as e:
        print('Got an error -> ', e)

    input = feature_extractor(images= image,return_tensors= 'pt' )   #pt means pytorch
    outputs = model(**input)
    logits = outputs.logits
    # model predicts one of the 1000 ImageNet classes
    pred_class_idx = logits.argmax(-1).item()
    ans = f"{model.config.id2label[pred_class_idx]}".split(',')[0]
    return ans
    

def cal_calculation(fruit_name):
    api_url = f'https://api.api-ninjas.com/v1/nutrition?query={fruit_name}'
    Headers = { 'X-Api-Key': api_key}
    response = requests.get(api_url, headers=Headers)
    # we are sending api_key through header because header is more secure as compare to body or api_url .
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return f"Error: {response.status_code}, Messages: {response.text}"


def json_to_html_table(json_data):
    # Start the HTML table
    html = '<table border="1" style="border-collapse: collapse; width: 50%;">'
    
    # Add table rows
    for item in json_data:
        for key, value in item.items():
            html += '<tr>'
            html += f'<th style="padding: 10px; background-color: #f2f2f2; color: blue; text-align: left;">{key}</th>'
            html += f'<td style="padding: 10px; text-align: left;">{value}</td>'
            html += '</tr>'
    
    # End the HTML table
    html += '</table>'
    return html

def display_table(json_input):
    json_data = json.loads(json_input)
    return json_to_html_table(json_data)


def main_function(image_path):
    food_identity = food_identification(image_path)
    neutrition_info = cal_calculation(food_identity)
    json_data = json.dumps(neutrition_info)   #convert list into json format by using json.dumps() method
    html_table_output = display_table(json_data)
    return html_table_output


def gradio_interface(img):
    return main_function(img)



import gradio as gr
iface = gr.Interface(
    fn= gradio_interface,
    inputs= gr.Image(type='filepath'),
    outputs= 'html',
    title= 'Food Identification and neutrition info',
    description= 'Upload the image of a food to get neutrition info',
    allow_flagging='never',
    
)

iface.launch(share= True)
