import pandas as pd
import scipy.io


def to_csv(output_path, concatenate_tables=False):
    for i in range(1, 16):
        subject = f"SBJ{i:02d}"
        print(f'STARTED {subject}')
        for j in range(1, 4):
            session = f"S0{j}"
            print(f'SESSION -> {session} STARTED')
            train_session = f"{session}/Train"
            path = subject + '/' + train_session

            data = scipy.io.loadmat(path + '/trainData.mat')['trainData']
            events = pd.read_csv(path + '/trainEvents.txt', header=None)
            targets = pd.read_csv(path + '/trainTargets.txt', header=None)

            if concatenate_tables:
                df = concat_tables(data, events, targets)
                df.to_csv(f'{output_path}/{subject}/{session}.csv', index=False)
            else:
                for channel in range(0, 8):
                    df = pd.DataFrame(data[channel, :, :]).transpose()
                    df['target'] = targets
                    df['event'] = events

                    df.to_csv(f'{output_path}/{subject}/{session}_{channel:02d}.csv', index=False)
            print(f'SESSION -> {session} FINISHED')
        print(f'FINISHED {subject}')


def concat_tables(data, events, targets):
    dfs = []
    for channel in range(0, 8):
        dfs.append(pd.DataFrame(data[channel, :, :]).transpose())

    df = pd.concat(dfs, axis=1, ignore_index=True)
    df['target'] = targets
    df['event'] = events

    return df


to_csv('./concatenated', concatenate_tables=True)
to_csv('./individual')
