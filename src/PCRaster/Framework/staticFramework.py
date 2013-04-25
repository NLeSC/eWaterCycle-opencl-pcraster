#!/usr/bin/env python
# -*- coding: utf-8 -*-

import frameworkBase
import sys

# # \brief Framework for static models
#
class StaticFramework(frameworkBase.FrameworkBase):
    # # \brief Constructor
    #
    # \param userModel object containing the user model class
    def __init__(self, userModel):
        frameworkBase.FrameworkBase.__init__(self)
        self._d_model = userModel
        self._testRequirements()

        self._addMethodToClass(self._readmapNew)
        self._addMethodToClass(self._reportNew)


    # # \brief Re-implemented from ShellScript.
    #
    # Runs the execute or initial section of the user model.
    def run(self):
        self._atStartOfScript()
        # Execute initial section.
        self._runInitial()

        return 0


    # # \brief Returns the class provided by the user
    def _userModel(self):
        return self._d_model



    # # \brief Testing the requirements for the static framework
    #
    # To use the static framework the user must implement:
    # - either a run or an initial method
    def _testRequirements(self):
        if hasattr(self._userModel(), "_userModel"):
            msg = "The _userModel method is deprecated and obsolete"
            self.showWarning(msg)

        if not hasattr(self._userModel(), "initial")\
          and not hasattr(self._userModel(), "run"):
            msg = "Cannot run static framework: Implement either an initial or a run method in the user class"
            raise frameworkBase.FrameworkError(msg)
