extern int spSetAudioCallbackFunc_(spAudio audio, spAudioCallbackType call_type, PyObject *obj);

extern long spReadAudioDoubleBufferWeighted_(spAudio audio, char *buffer, long buf_size, double weight);

extern long spWriteAudioDoubleBufferWeighted_(spAudio audio, char *buffer, long buf_size, double weight);
