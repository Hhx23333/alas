import os

from module.campaign.run import CampaignRun
from module.logger import logger

RECORD_SINCE = (0,)
CAMPAIGN_NAME = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3']


class CampaignAB(CampaignRun):
    def run(self, name, folder='campaign_main', total=0):
        name = name.lower()
        option = ('EventABRecord', name)
        if not self.config.record_executed_since(option=option, since=RECORD_SINCE):
            super().run(name=name, folder=folder, total=1)
            self.config.record_save(option=option)

    def run_event_daily(self):
        existing = [file[:-3] for file in os.listdir(f'./campaign/{self.config.EVENT_NAME_AB}') if file[-3:] == '.py']

        for name in existing:
            if name.lower().startswith('sp'):
                logger.warning(f'{self.config.EVENT_NAME_AB} seems to be a SP event, skip daily_ab')
                logger.warning(f'Existing map files: {existing}')
                return False

        for name in CAMPAIGN_NAME:
            if name not in existing:
                continue
            self.run(name=name, folder=self.config.EVENT_NAME_AB)
