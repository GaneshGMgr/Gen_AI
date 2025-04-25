import sys
import logging

class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()
        self.lineno = exc_tb.tb_lineno 
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in Python script [{self.file_name}] line number [{self.lineno}] error message [{self.error_message}]"

if __name__ == "__main__":
    try:
        a = 1 / 0
    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")
        raise CustomException(str(e), sys)
