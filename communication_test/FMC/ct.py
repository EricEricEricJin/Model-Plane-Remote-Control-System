from communications.receive_cmd import receiveCmd
RC = receiveCmd()
print("CONNECT:", RC.init())
RC.run()
