import os


class Config:
    copter_id = os.environ.get('COPTER_ID')
    host = os.environ.get('HOST')
    animation_file_path = 'drone{}.csv'.format(copter_id)
