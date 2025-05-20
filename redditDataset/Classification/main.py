import click
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
from sentence_transformers import SentenceTransformer


def cli():
    comments = [
        {"id": 0, "parent_id": None, "body": "What do you think of Reddit?", "removed": 0},
        {"id": 1, "parent_id": 0, "body": "Reddit sucks, it's full of trolls", "removed": 1},
        {"id": 2, "parent_id": 0, "body": "I like Reddit for AMAs", "removed": 0},
        {"id": 3, "parent_id": 1, "body": "Shut up, you're dumb", "removed": 1},
        {"id": 4, "parent_id": 2, "body": "Agreed, some threads are great", "removed": 0}
    ]

    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [c["body"] for c in comments]
    x = torch.tensor(model.encode(texts), dtype=torch.float)

    edges = []
    for c in comments:
        if c["parent_id"] is not None:
            edges.append((c["parent_id"], c["id"]))
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()

    y = torch.tensor([c["removed"] for c in comments], dtype=torch.long)

    data = Data(x=x, edge_index=edge_index, y=y)

    class GNN(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = GCNConv(x.size(1), 64)
            self.conv2 = GCNConv(64, 2)

        def forward(self, data):
            x, edge_index = data.x, data.edge_index
            x = F.relu(self.conv1(x, edge_index))
            x = self.conv2(x, edge_index)
            return x
        
    model = GNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = torch.nn.CrossEntropyLoss()

    for epoch in range(100):
        model.train()
        optimizer.zero_grad()
        out = model(data)
        loss = loss_fn(out, data.y)
        loss.backward()
        optimizer.step()
    
    model.eval()
    pred = out.argmax(dim=1)
    print("Prédictions :", pred.tolist())
    print("Réels       :", data.y.tolist())

if __name__ == "__main__":
    cli()