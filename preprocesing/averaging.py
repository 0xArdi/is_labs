import pandas as pd

folder = 'individual/'

for subject in range(1, 16):
    subject_folder = f'{folder}/SBJ{subject:02d}'
    for session in range(1, 4):
        session_file = f'{subject_folder}/S{session:02d}'
        channels = []

        for channel in range(0, 8):
            channels.append(pd.read_csv(f'{session_file}_{channel:02d}.csv'))

        df = pd.read_csv(f'{session_file}_00.csv') # read first channel
        for i in range(0, 1600):
            for j in range(0, 352):
                sum = 0
                for channel in channels:
                    sum += channel.iloc[i, j]
                df.iloc[i, j] = sum / 8
        df.to_csv(f'average/SBJ{subject:02d}/S{session:02d}_avg.csv', index=False)
