import torch
import torch.nn as nn

from ml.utils.config import INPUT_DIM, ENCODER_DIMS, LATENT_DIM, DROPOUT


class Autoencoder(nn.Module):
    def __init__(self, input_dim=INPUT_DIM, encoder_dims=ENCODER_DIMS,
                 latent_dim=LATENT_DIM, dropout=DROPOUT):
        super().__init__()

        # Encoder: input_dim -> ... -> latent_dim
        enc_layers = []
        dims = [input_dim] + encoder_dims
        for i in range(len(dims) - 1):
            enc_layers += [nn.Linear(dims[i], dims[i+1]), nn.ReLU(), nn.Dropout(dropout)]
        enc_layers.append(nn.Linear(dims[-1], latent_dim))
        self.encoder = nn.Sequential(*enc_layers)

        # Decoder: mirror of encoder
        dec_dims = [latent_dim] + encoder_dims[::-1]
        dec_layers = []
        for i in range(len(dec_dims) - 1):
            dec_layers += [nn.Linear(dec_dims[i], dec_dims[i+1]), nn.ReLU(), nn.Dropout(dropout)]
        dec_layers += [nn.Linear(dec_dims[-1], input_dim), nn.Sigmoid()]
        self.decoder = nn.Sequential(*dec_layers)

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)


if __name__ == "__main__":
    model = Autoencoder()
    x = torch.randn(8, INPUT_DIM)
    out = model(x)
    print(f"Input: {x.shape} | Output: {out.shape}")
    print(f"Params: {sum(p.numel() for p in model.parameters()):,}")