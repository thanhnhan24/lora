error log:
15-march-2025
Traceback (most recent call last):
  File "/usr/lib/python3.11/threading.py", line 1038, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.11/threading.py", line 975, in run
    self._target(*self._args, **self._kwargs)
  File "/home/nckh_lora/sx126x_lorawan_hat_code/python/lora/examples/SX126x/receiver.py", line 50, in lora_handler
    LoRa.write(data_to_send.encode())
  File "/home/nckh_lora/sx126x_lorawan_hat_code/python/lora/LoRaRF/SX126x.py", line 688, in write
    raise TypeError("input data must be list, tuple, integer or float")
TypeError: input data must be list, tuple, integer or float

