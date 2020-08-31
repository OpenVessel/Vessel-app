##
## After step 25th we are intergrating into existing medical software platforms 
##Epic's APi 
## 



#### API query for HL7 
## ingestion framework 
message = 'MSH|^~\&|GHH LAB|ELAB-3|GHH OE|BLDG4|200202150930||ORU^R01|CNTRL-3456|P|2.4\r'
import hl7 
test = hl7.parse(message)