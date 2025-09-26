#I have a feeling this is better off as its own thing so it doesn't clutter 
#up other modules
import sys
from colorama import Fore, Style

def throw_error(exception, errorMessage):
	exc_type, exc_obj, tb = sys.exc_info()
	k = tb
	while k.tb_next is not None:
		k = k.tb_next
		#print(f"{k.tb_frame.f_lineno} @ {k.tb_frame.f_code.co_filename}")
	k = k.tb_frame
	print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {errorMessage}\n\t{exc_type.__name__}: {str(exception)} (line {tb.tb_lineno})\n\terror traces to `{k.f_code.co_name}` (line {k.f_lineno}),\n\t{k.f_code.co_filename}")
	