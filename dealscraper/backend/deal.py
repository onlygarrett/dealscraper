from copy import deepcopy
from datetime import date, datetime
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from data.resources import HEADERS

class Deal():
    """
    This class represents base Deal object.
    """
    def __init__(self,
                 title: str,
                 sale_price: float,
                 sale_date: date,
                 vendor: Optional[str] = None,
                 discount: Optional[float] = None,
                 original_price: Optional[float] = None,
                 bundle_name: Optional[str] = None                 
                 ) -> None:
                
                self.title = title
                self.sale_price = sale_price
                self.sale_date = sale_date
                
                # not required
                self.vendor = vendor
                self.discount = discount
                self.original_price = original_price
                self.bundle_name = bundle_name  
                
    @property
    def update_current_sale_price(self, deal: 'Deal', sale_price: float) -> None:
        
        if (deal.post_date > self.post_date):
            self.sale_price = deepcopy(deal.sale_price)
            self.post_date = deepcopy(deal.post_date)
            self.sale_date = deepcopy(deal.sale_date)
            self.vendor = deepcopy(deal.vendor)
            self.discount = deepcopy(deal.discount)
            self.original_price = deepcopy(deal.original_price)
            self.bundle_name = deepcopy(deal.bundle_name)
            return True
        else:
            return False
        
    @property
    def write_to_csv(self, deal: 'Deal') -> None:
        
        return dict([
            (h, v) for h, v in zip(
                HEADERS,
                [
                    self.title,
                    self.sale_price,
                    self.original_price,
                    self.discount,
                    self.vendor,
                    self.bundle_name,
                    self.sale_date.strftime("%m/%d/%Y"),                    
                ]
            )
        ])
        
