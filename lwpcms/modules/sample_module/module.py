from lwpcms.moduling.moduling import LWPCMSModule
from lwpcms.api.constants import hooks


class SampleModule(LWPCMSModule):

    def event(self, event, data):
        if event == hooks['post_publish']:
            data['post'].content += '\r\n ~ sample_module'


module = SampleModule()
