from lwpcms.moduling.moduling import LWPCMSModule
from lwpcms.api.constants import hooks


class SampleModule(LWPCMSModule):

    def event(self, event, data):
        if event == hooks['post_publish']:
            data['post'].content += '\r\n ~ sample_module'

        elif event == hooks['layout_head']:
            return '<script type="text/javascript">console.log("head from SampleModule");</script>'

        elif event == hooks['layout_body']:
            return '<div style="display:none;">body from SampleModule></div>'

        elif event == hooks['layout_footer']:
            return '<div style="display:none;">footer from SampleModule></div>'

        
module = SampleModule()
