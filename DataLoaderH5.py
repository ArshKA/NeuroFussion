import torch
import h5py
import random


class DatasetH5(torch.utils.data.Dataset):
    def __init__(self, scan_path, stimuli_path, subject, scan_type, sessions, device='cpu'):
        self.device = device
        self.sessions = sessions
        self.scans = h5py.File(scan_path, 'r')[f'CSI{subject}/type{scan_type}']
        self.stimuli = h5py.File(stimuli_path, 'r')[f'CSI{subject}']

        self.order = [(s, r) for s in self.sessions for r in range(self.stimuli[f'sess{s:02}'].shape[0])]
        random.shuffle(self.order)

    def __len__(self):
        return len(self.order)

    def __getitem__(self, idx):
        ses, run = self.order[idx]
        X = torch.tensor(self.scans[f'sess{ses:02}'][run])
        X = torch.nan_to_num(X)
        X = X.unsqueeze(0)
        X = X.float().to(self.device)
        y = torch.tensor(self.stimuli[f'sess{ses:02}'][run]).float().to(self.device)
        return X, y
