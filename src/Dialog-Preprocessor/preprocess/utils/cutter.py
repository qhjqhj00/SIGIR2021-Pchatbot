import json
import pkuseg

class Cutter():
    def __init__(self, method='pkuseg'):
        if method == 'pkuseg':
            self.cutter = pkuseg.pkuseg(model_name='web')

    def cut_text(self, text):
        return self.cutter.cut(text)

    def cut_data_line(self, line_json):
        for item in line_json:
            item[0] = ' '.join(self.cut_text(item[0]))
        return line_json
