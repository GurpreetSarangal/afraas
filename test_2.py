from afraas_client.Recognizer import Recognizer
from afraas_client.Camera import Camera

import afraas_client

# obj = Recognizer()
# obj.recompileDataSet()

# afraas_client.boot()
# afraas_client.removeFace("1_6_Yuvraj Singh")
# afraas_client.removeFace("2_2_Gurpreet Sarangal")
# afraas_client.removeFace("3_2_Gurpreet Sarangal")
# afraas_client.removeFace("5_1_Sandeep Kaur")


# afraas_client.addNewFace(1)
# afraas_client.addNewFace(7)
# afraas_client.mark_attendance("1_2_sandeep kaur")

obj=Camera(0)
obj.test_Cam()