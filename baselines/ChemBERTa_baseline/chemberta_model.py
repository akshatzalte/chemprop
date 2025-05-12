from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel
import torch
import torch.nn as nn
from sklearn.base import BaseEstimator
import numpy as np
from torch.utils.data import TensorDataset, DataLoader

class ChemBERTaModel(BaseEstimator):
    def __init__(self, task_type="regression", model_name="DeepChem/ChemBERTa-77M-MTR", max_length=128, random_seed=42, batch_size=32, num_epochs=10, learning_rate=1e-5):
        self.task_type = task_type
        self.model_name = model_name
        self.max_length = max_length
        self.random_seed = random_seed
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.learning_rate = learning_rate
        self.tokenizer = None
        self.model = None
        self.regression_head = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def fit(self, X, y):
        # Set seeds for reproducibility
        torch.manual_seed(self.random_seed)
        np.random.seed(self.random_seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(self.random_seed)
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # For regression, we use the base model and add our own regression head
        if self.task_type == "regression":
            self.model = AutoModel.from_pretrained(self.model_name)
            hidden_size = self.model.config.hidden_size
            self.regression_head = nn.Sequential(
                nn.Linear(hidden_size, 512),
                nn.ReLU(),
                nn.Dropout(0.1),
                nn.Linear(512, 256),
                nn.ReLU(),
                nn.Dropout(0.1),
                nn.Linear(256, 1)
            )
        else:
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=2)

        # Move models to device
        self.model.to(self.device)
        if self.regression_head is not None:
            self.regression_head.to(self.device)

        # Tokenize inputs
        encodings = self.tokenizer(list(X), truncation=True, padding=True, max_length=self.max_length, return_tensors="pt")
        labels = torch.tensor(y, dtype=torch.float if self.task_type == "regression" else torch.long)
        dataset = TensorDataset(encodings['input_ids'], encodings['attention_mask'], labels)
        dataloader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

        # Training setup
        parameters = list(self.model.parameters()) 
        if self.regression_head is not None:
            parameters += list(self.regression_head.parameters())
        
        optimizer = torch.optim.AdamW(parameters, lr=self.learning_rate)
        criterion = nn.MSELoss() if self.task_type == "regression" else nn.CrossEntropyLoss()
        
        # Training loop
        for epoch in range(self.num_epochs):
            self.model.train()
            if self.regression_head is not None:
                self.regression_head.train()
                
            total_loss = 0
            for batch in dataloader:
                input_ids, attention_mask, labels = [b.to(self.device) for b in batch]
                optimizer.zero_grad()
                
                if self.task_type == "regression":
                    outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                    pooled_output = outputs.pooler_output
                    predictions = self.regression_head(pooled_output).squeeze()
                    loss = criterion(predictions, labels)
                else:
                    outputs = self.model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
                    loss = outputs.loss
                
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                
            print(f"Epoch {epoch+1}/{self.num_epochs} | Loss: {total_loss/len(dataloader):.4f}")
        
        return self

    def predict_proba(self, X):
        if self.task_type != "classification":
            raise ValueError("predict_proba is only for classification")
        
        self.model.eval()
        encodings = self.tokenizer(list(X), truncation=True, padding=True, max_length=self.max_length, return_tensors="pt")
        dataset = TensorDataset(encodings['input_ids'], encodings['attention_mask'])
        dataloader = DataLoader(dataset, batch_size=self.batch_size, shuffle=False)
        
        probs = []
        with torch.no_grad():
            for batch in dataloader:
                input_ids, attention_mask = [b.to(self.device) for b in batch]
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                prob = torch.softmax(outputs.logits, dim=1)[:, 1]
                probs.append(prob.cpu().numpy())
        
        return np.concatenate(probs)

    def predict(self, X):
        self.model.eval()
        if self.regression_head is not None:
            self.regression_head.eval()
        
        encodings = self.tokenizer(list(X), truncation=True, padding=True, max_length=self.max_length, return_tensors="pt")
        dataset = TensorDataset(encodings['input_ids'], encodings['attention_mask'])
        dataloader = DataLoader(dataset, batch_size=self.batch_size, shuffle=False)
        
        predictions = []
        with torch.no_grad():
            for batch in dataloader:
                input_ids, attention_mask = [b.to(self.device) for b in batch]
                
                if self.task_type == "regression":
                    outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                    pooled_output = outputs.pooler_output
                    preds = self.regression_head(pooled_output).squeeze()
                else:
                    outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                    preds = torch.argmax(outputs.logits, dim=1)
                
                predictions.append(preds.cpu().numpy())
        
        return np.concatenate(predictions).reshape(-1)