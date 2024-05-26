from copy import deepcopy
from datetime import date
from typing import Any, Dict, Optional

from data.resources import HEADERS


class Deal:
    """
    This class represents base Deal object.
    """

    def __init__(
        self,
        id: int,
        title: str,
        sale_price: str,
        sale_date: date,
        vendor: Optional[str] = None,
        discount: Optional[str] = None,
        original_price: Optional[str] = None,
        bundle_name: Optional[str] = None,
    ) -> None:
        """
        Initialize a Deal object.

        Parameters:
        id (int): The unique identifier of the deal.
        title (str): The title of the deal.
        sale_price (str): The sale price of the deal.
        sale_date (date): The date when the deal is on sale.
        vendor (str, optional): The vendor of the deal. Defaults to None.
        discount (str, optional): The discount offered by the deal. Defaults to None.
        original_price (str, optional): The original price of the deal. Defaults to None.
        bundle_name (str, optional): The name of the bundle if the deal is part of a bundle. Defaults to None.

        Returns:
        None
        """

        self.id = id
        self.title = title
        self.sale_price = sale_price
        self.sale_date = sale_date

        # not required
        self.vendor = vendor
        self.discount = discount
        self.original_price = original_price
        self.bundle_name = bundle_name

    def update_current_sale_price(self, deal: "Deal") -> bool:
        """
            Not yet used
        """
        if deal.sale_date > self.sale_date:
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
    def row_output(self) -> Dict[str, Any]:
        """
        Returns a dictionary representing the Deal object's attributes,
        formatted for output in a table.

        The dictionary keys correspond to the column headers defined in the HEADERS constant.
        The values are obtained from the Deal object's attributes.

        Returns:
        dict: A dictionary containing the Deal object's attributes formatted for output.
        """

        return dict(
            [
                (h, v)
                for h, v in zip(
                    HEADERS,
                    [
                        self.id,
                        self.title,
                        self.sale_price,
                        self.original_price,
                        self.discount,
                        self.vendor,
                        self.bundle_name,
                        self.sale_date.strftime("%m/%d/%Y"),
                    ],
                )
            ]
        )
