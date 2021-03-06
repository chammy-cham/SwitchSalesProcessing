import logging
import pandas as pd

from sale import Sale

class MessageProcessor:
   
    OPERATIONS = set(["add", "subtract", "multiply"])
    UNUSED_WORDS = ['of', 'at', 'each']

    def __init__(self, sales_list):
      self.sales_list = sales_list

    def process_message(self, message): 
        """ Determine message type and process into sales """
        try:
            word_list = message.lower().split()
            if self.OPERATIONS.intersection(word_list):
                self._apply_adjustments(word_list) #  message three being the one with adjustments                                 
            elif word_list[0].isdigit():
                sale = self._parse_message_two(word_list) # message two is amount of product message
                self.sales_list.append(sale)
            elif(self._check_float(word_list[-1], message)): # message one is basic type and value
                sale = self._parse_message_one(word_list)
                self.sales_list.append(sale)
        except Exception as e:              
            logging.info("Could not parse message {}.\n{}".format(message, e))

    def _check_float(self, value, message):
        """ Check if item returns a float or not """
        try:
            float(value)
            return True
        except ValueError:
            logging.warning("Float required for product value: {}".format(message))
            return False

    def _apply_adjustments(self, word_list): 
        """ Parse message that shows adjustments for product. """
        try:
            operation = word_list[0]
            amount = float(word_list[1])
            product = " ".join(word_list[2:]).title() # allowing for spaces in product namne           
            for sale in self.sales_list: 
                if sale.product.lower() == product.lower(): 
                    sale.add_adjustment(operation, amount)
        except Exception as e:
            logging.warning("Cannot parse adjustment message: {}".format(e))

    def _parse_message_one(self, word_list): 
        """ Parse messages showing product and value, assuming amount is one per sale. """ 
        try:
            word_list = [word for word in word_list if word not in self.UNUSED_WORDS]
            value = float(word_list[-1])
            product = " ".join(word_list[:-1]).title()
            sale = Sale(product, value=value)
            return sale
        except Exception as e:
            logging.warning("Cannot parse message type one: {}. Expected format <product> at <value>".format(e))

    def _parse_message_two(self, word_list): 
        """ Parse messages showing product, value and amount of products in sale. """ 
        try:
            word_list = [word for word in word_list if word not in self.UNUSED_WORDS]
            amount = int(word_list[0])
            value = float(word_list[-1])
            product = " ".join(word_list[1: -1]).title()
            sale = Sale(product, amount=amount, value=value)
            return sale
        except Exception as e:
            logging.warning("Cannot parse message type two: {}. Expected format <amount> of <product> at <value> each".format(e))

    

                
        