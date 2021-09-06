
## Final project: Pneumonia checker 

This app helps identify pneumonia using a trained model to predict pneumonia on the provided chest X-ray. It has web gui and performes all tasks asynchronously.


![alt text](https://testdriven.io/static/images/blog/flask-celery/flask-celery-flow.png)

Images:
web: flask web app
worker: celery
model: flask restful web service, trained model. 
redis: message broker

Container orchestration tool is used for managing containers.

## Model

Model: VGG16, loss: CrossEntropyLoss, metric: Accuracy

VGG16 is a convolutional neural network model.
The architecture of VGG16: 
![alt text](https://neurohive.io/wp-content/uploads/2018/11/vgg16-neural-network.jpg)

Trained model is already included into model image.
To generate a new model:
1. run `model/model_train.ipynb` 
2. rebuild docker images after that.

## Dataset

The dataset consists of chest X-ray images (anterior-posterior) that were selected from retrospective cohorts of pediatric patients of one to five years old from Guangzhou Women and Children’s Medical Center, Guangzhou. For the analysis of chest x-ray images, all chest radiographs were initially screened for quality control by removing all low quality or unreadable scans. The diagnoses for the images were then graded by two expert physicians before being cleared for training the AI system. In order to account for any grading errors, the evaluation set was also checked by a third expert.

```bash
wget https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia/download
unzip archive.zip
```

## Usage instructions

Run the app:

```sh
$ sudo docker-compose up --build
```

Open browser to view web gui 
[http://localhost:5000](http://localhost:5000)

Get prediction:
1. upload new X-ray (or use uploaded one)
2. click 'Check' (it may take a time to get a prediction at the first time)

POSSIBLE RESULT: 0 - NORMAL, 1 - PNEUMONIA, -1 - ERROR
