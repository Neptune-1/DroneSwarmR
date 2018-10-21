import os


class Config:
    copter_id = 1  # os.environ.get('COPTER_ID')
    host = "192.168.43.19"  # os.environ.get('HOST')
    animation_file_path = 'drone{}.csv'.format(copter_id)
