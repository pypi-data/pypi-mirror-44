#!/usr/bin/env python

# Copyright (c) 2019, IRIS-HEP
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import importlib

# uses numpy, not awkward.numpy, because it operates on TFile data, not TTree data
import numpy
        
def towriteable(obj):
    def identity(x):
        return x

    def resolve(obj):
        def types(cls, obj):
            if cls is numpy.ndarray:
                yield ("numpy", "ndarray", len(obj.shape), str(obj.dtype))
            elif cls.__module__ == "pandas.core.frame" and cls.__name__ == "DataFrame":
                yield ("pandas.core.frame", "DataFrame", obj.index.__class__.__name__, set(obj.columns))
            else:
                yield (cls.__module__, cls.__name__)
            for x in cls.__bases__:
                for y in types(x, obj):
                    yield y

        if any(x == ("builtins", "bytes") or x == ("builtins", "str") or x == ("__builtin__", "str") or x == ("__builtin__", "unicode") for x in types(obj.__class__, obj)):
            return (None, None, "uproot.write.objects.TObjString", "TObjString")

        elif isinstance(obj, tuple) and any(x[:2] == ("numpy", "ndarray") for x in types(obj[0].__class__, obj[0])) and any(x[:2] == ("numpy", "ndarray") for x in types(obj[1].__class__, obj[1])) and len(obj[0]) + 1 == len(obj[1]):
            return ("uproot_methods.classes.TH1", "from_numpy", "uproot.write.objects.TH1", "TH1")

        elif any(x[:3] == ("pandas.core.frame", "DataFrame", "IntervalIndex") and "count" in x[3] for x in types(obj.__class__, obj)):
            return ("uproot_methods.classes.TH1", "from_pandas", "uproot.write.objects.TH1", "TH1")

        elif any(x == ("physt.histogram1d", "Histogram1D") for x in types(obj.__class__, obj)):
            return ("uproot_methods.classes.TH1", "from_physt", "uproot.write.objects.TH1", "TH1")

        elif any(x == ("uproot_methods.classes.TH1", "Methods") or x == ("TH1", "Methods") for x in types(obj.__class__, obj)):
            return (None, None, "uproot.write.objects.TH1", "TH1")

        else:
            raise TypeError("type {0} from module {1} is not writeable by uproot".format(obj.__class__.__name__, obj.__class__.__module__))

    convertmod, convertfcn, mod, cls = resolve(obj)

    if convertfcn is not None:
        convert = getattr(importlib.import_module(convertmod), convertfcn)
        obj = convert(obj)

    cls = getattr(importlib.import_module(mod), cls)
    return cls(obj)
