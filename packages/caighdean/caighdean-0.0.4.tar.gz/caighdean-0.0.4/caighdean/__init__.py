#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib


_translator = importlib.import_module('caighdean.translator')
Translator = _translator.Translator


__all__ = ["Translator"]
