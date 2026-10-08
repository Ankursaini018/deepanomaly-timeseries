import torch
import torch.nn as nn


class LSTMAutoencoder(nn.Module):
    """
    Sequence-to-sequence LSTM autoencoder.

    Unlike the dense autoencoder, this treats the input as an ordered
    sequence of scalars rather than a flat feature vector. The encoder LSTM
    compresses the sequence into a fixed-size hidden state (the bottleneck);
    the decoder LSTM reconstructs the sequence from that state, repeated at
    every timestep since the decoder has no other input to condition on.
    """

    def __init__(self, seq_len=140, hidden_dim=64, latent_dim=16, num_layers=1):
        super().__init__()
        self.seq_len = seq_len
        self.latent_dim = latent_dim

        self.encoder_lstm = nn.LSTM(
            input_size=1, hidden_size=hidden_dim,
            num_layers=num_layers, batch_first=True
        )
        self.encoder_fc = nn.Linear(hidden_dim, latent_dim)

        self.decoder_fc = nn.Linear(latent_dim, hidden_dim)
        self.decoder_lstm = nn.LSTM(
            input_size=hidden_dim, hidden_size=hidden_dim,
            num_layers=num_layers, batch_first=True
        )
        self.output_fc = nn.Linear(hidden_dim, 1)

    def forward(self, x):
        # x: (batch, seq_len) -> (batch, seq_len, 1) for LSTM input
        x = x.unsqueeze(-1)

        _, (hidden, _) = self.encoder_lstm(x)
        latent = self.encoder_fc(hidden[-1])  # (batch, latent_dim)

        # Repeat the latent vector across every output timestep — the
        # decoder has no other signal to drive reconstruction from.
        decoder_input = self.decoder_fc(latent).unsqueeze(1)
        decoder_input = decoder_input.repeat(1, self.seq_len, 1)

        decoded, _ = self.decoder_lstm(decoder_input)
        output = self.output_fc(decoded).squeeze(-1)  # back to (batch, seq_len)

        return torch.sigmoid(output)


if __name__ == "__main__":
    model = LSTMAutoencoder()
    x = torch.randn(8, 140)
    out = model(x)
    print(f"Input: {x.shape} | Output: {out.shape}")
    print(f"Params: {sum(p.numel() for p in model.parameters()):,}")