# EEG-Filtering
This is an attempt at filtering and plotting live EEG signals. LSL is used for streaming while Python's http.server and Chart.js are used for graphing file contents. SciPy is used to filter the raw data.

![2022_07_11_14_44_44](https://user-images.githubusercontent.com/14152830/178349035-91a3f55c-9a67-4ff5-a08c-a04117af479b.gif)

- [This script](https://github.com/openbci-archive/OpenBCI_LSL) is used to start the stream
- receivedata.bat is then run to start the web server and data recording

ReceiveData.py was modified from [this example](https://github.com/labstreaminglayer/liblsl-Python/blob/master/pylsl/examples/ReceiveData.py).


[Forum Post](https://openbci.com/forum/index.php?p=/discussion/3376/)
[Reddit Post](https://www.reddit.com/r/neuro/comments/vw59g8/scipy_eeg_filtering_advice/)
