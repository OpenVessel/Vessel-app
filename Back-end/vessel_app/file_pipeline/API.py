##
## After step 25th we are intergrating into existing medical software platforms 
##Epic's APi 
## #https://fhir.epic.com/Documentation?docId=developerguidelines



#### API query for HL7 
## ingestion framework 
message = 'MSH|^~\&|GHH LAB|ELAB-3|GHH OE|BLDG4|200202150930||ORU^R01|CNTRL-3456|P|2.4\r'
message += 'PID|||555-44-4444||EVERYWOMAN^EVE^E^^^^L|JONES|196203520|F|||153 FERNWOOD DR.^^STATESVILLE^OH^35292||(206)3345232|(206)752-121||||AC555444444||67-A4335^OH^20030520\r'
message += 'OBR|1|845439^GHH OE|1045813^GHH LAB|1554-5^GLUCOSE|||200202150730||||||||555-55-5555^PRIMARY^PATRICIA P^^^^MD^^LEVEL SEVEN HEALTHCARE, INC.|||||||||F||||||444-44-4444^HIPPOCRATES^HOWARD H^^^^MD\r'
message += 'OBX|1|SN|1554-5^GLUCOSE^POST 12H CFST:MCNC:PT:SER/PLAS:QN||^182|mg/dl|70_105|H|||F'
import hl7 
test = hl7.parse(message)
print(test)
print(type(test))
print(test[1])
#https://help.interfaceware.com/getting-sample-hl7-data.html
#http://www.ringholm.com/docs/04300_en.htm
#https://blog.interfaceware.com/components-of-an-hl7-message/
#http://www.ringholm.com/training/FHIR_training_course.htm
#https://www.ihe.net/
#https://www.dicomstandard.org/
#https://github.com/firelyteam/fhir-net-api
#http://docs.simplifier.net/fhirnetapi/
#https://github.com/firelyteam/fhir-net-api
#