## EmoNet Server

The EmoNet Server is the central server used to store and updated the models trained at each client in the federated system. The server is a pure Flask API that is hosted at https://api.emonet.xyz.

 - Backend API

 The backend API consists of a Flask app that runs the api.emonet.xyz server. The API has four endpoints `/receive-update`, `/send-model`, `/test-model`, and `/predict`. 

 `/receive-update` receives the model updates from each client, stores them temporarily in memory, and then updates the base model every 10 updates from the client. This is the core logic for the federation of the model.

 `/send-model` sends the most up-to-date base model to the requesting client. This allows the client to train on the most recent model when training at the edge.

 `/test-model` uses a dataset to test the base model as it stands at the moment. Users can use RAVDESS or SAVEE to test the current base model.

 `/predict` uses the base model and an input of MFCCs to run an inference.