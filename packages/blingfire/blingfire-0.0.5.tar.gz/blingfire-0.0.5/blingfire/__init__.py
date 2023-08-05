import os
from ctypes import *
import inspect
import os.path
import numpy as np
from sys import platform

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))

# load the DLL
blingfiretokdll = None

if platform == "linux" or platform == "linux2":
    # linux
    blingfiretokdll = cdll.LoadLibrary(os.path.join(path, "libblingfiretokdll.so"))
elif platform == "win32":
    blingfiretokdll = cdll.LoadLibrary(os.path.join(path, "blingfiretokdll.dll"))


def text_to_sentences(s):

    # get the UTF-8 bytes
    s_bytes = s.encode("utf-8")

    # allocate the output buffer
    o_bytes = create_string_buffer(len(s_bytes) * 2)
    o_bytes_count = len(o_bytes)

    # identify paragraphs
    o_len = blingfiretokdll.TextToSentences(c_char_p(s_bytes), c_int(len(s_bytes)), byref(o_bytes), c_int(o_bytes_count))

    # check if no error has happened
    if -1 == o_len or o_len > o_bytes_count:
        return ''

    # compute the unicode string from the UTF-8 bytes
    return o_bytes.value.decode('utf-8')


def text_to_words(s):

    # get the UTF-8 bytes
    s_bytes = s.encode("utf-8")

    # allocate the output buffer
    o_bytes = create_string_buffer(len(s_bytes) * 2)
    o_bytes_count = len(o_bytes)

    # identify paragraphs
    o_len = blingfiretokdll.TextToWords(c_char_p(s_bytes), c_int(len(s_bytes)), byref(o_bytes), c_int(o_bytes_count))

    # check if no error has happened
    if -1 == o_len or o_len > o_bytes_count:
        return ''

    # compute the unicode string from the UTF-8 bytes
    return o_bytes.value.decode('utf-8')


# returns the current version of the DLL's algo
def get_blingfiretok_version():
    return blingfiretokdll.GetBlingFireTokVersion()


# Returns numpy array with data type unsigned int32 array
def text_to_hashes(s, word_n_grams, bucketSize):
    # get the UTF-8 bytes
    s_bytes = s.encode("utf-8")

    # allocate the output buffer
    o_bytes = (c_uint32 * (2 * len(s_bytes)))()
    o_bytes_count = len(o_bytes)

    # identify paragraphs
    o_len = blingfiretokdll.TextToHashes(c_char_p(s_bytes), c_int(len(s_bytes)), byref(o_bytes), c_int(o_bytes_count), c_int(word_n_grams), c_int(bucketSize))

    # check if no error has happened
    if -1 == o_len or o_len > o_bytes_count:
        return ''

    # return numpy array without copying
    return np.frombuffer(o_bytes, dtype=c_uint32, count = o_len)

