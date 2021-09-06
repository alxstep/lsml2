import torch
from torch import nn
from torchvision import models, transforms
from flask import current_app
from pathlib import Path
from PIL import Image


transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def get_model():
	model = models.vgg16()
	model.classifier[6] = nn.Sequential(nn.Linear(model.classifier[6].in_features, 256), nn.ReLU(), nn.Dropout(0.4),
                                    	nn.Linear(256, 2), nn.LogSoftmax(dim=1))

	model_path = Path('vgg16_pneumonia.pth')
	if model_path.is_file():
		weights = torch.load(model_path, map_location=torch.device('cpu'))
		model.load_state_dict(weights)

	for param in model.features.parameters():
	    param.required_grad = False

	model.eval()

	return model

def predict(fname, model):
	img_path = Path(current_app.config['UPLOAD_FOLDER'])/fname
	if img_path.is_file():		
		img = Image.open(img_path).convert('RGB')
		img = transform(img).unsqueeze(0)
		with torch.no_grad():
		    outputs = model(img)
		    _, pred = torch.max(outputs.data, 1)

		return pred.item()		
	return -1
