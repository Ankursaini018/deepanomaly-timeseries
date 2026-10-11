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


class LSTMAutoencoder(nn.Module):
    def __init__(self, seq_len=INPUT_DIM, hidden_dim=64, latent_dim=LATENT_DIM, num_layers=1):
        super().__init__()
        self.seq_len = seq_len

        self.encoder_lstm = nn.LSTM(1, hidden_dim, num_layers, batch_first=True)
        self.encoder_fc = nn.Linear(hidden_dim, latent_dim)

        self.decoder_fc = nn.Linear(latent_dim, hidden_dim)
        self.decoder_lstm = nn.LSTM(hidden_dim, hidden_dim, num_layers, batch_first=True)
        self.output_fc = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        x = x.unsqueeze(-1)
        _, (hidden, _) = self.encoder_lstm(x)
        latent = self.encoder_fc(hidden[-1])

        decoder_input = self.decoder_fc(latent).unsqueeze(1).repeat(1, self.seq_len, 1)
        decoded, _ = self.decoder_lstm(decoder_input)
        output = self.output_fc(decoded).squeeze(-1)
        return torch.sigmoid(output)