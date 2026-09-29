import torch
import torch.nn as nn

from app.core.config import INPUT_DIM, ENCODER_DIMS, LATENT_DIM


class Autoencoder(nn.Module):
    def __init__(self, input_dim=INPUT_DIM, encoder_dims=ENCODER_DIMS, latent_dim=LATENT_DIM):
        super().__init__()

        enc_layers = []
        dims = [input_dim] + encoder_dims
        for i in range(len(dims) - 1):
            enc_layers += [nn.Linear(dims[i], dims[i+1]), nn.ReLU(), nn.Dropout(0.1)]
        enc_layers.append(nn.Linear(dims[-1], latent_dim))
        self.encoder = nn.Sequential(*enc_layers)

        dec_dims = [latent_dim] + encoder_dims[::-1]
        dec_layers = []
        for i in range(len(dec_dims) - 1):
            dec_layers += [nn.Linear(dec_dims[i], dec_dims[i+1]), nn.ReLU(), nn.Dropout(0.1)]
        dec_layers += [nn.Linear(dec_dims[-1], input_dim), nn.Sigmoid()]
        self.decoder = nn.Sequential(*dec_layers)

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)
    