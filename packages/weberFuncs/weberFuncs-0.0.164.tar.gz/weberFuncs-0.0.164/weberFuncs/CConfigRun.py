#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__createTime__ = "2017/11/7 11:40"
__author__ = "WeiYanfeng"
__email__ = "weber.juche@gmail.com"
__version__ = "0.0.1"
        
~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述
记录一些运行参数，用于下次运行时加载。
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from .WyfPublicFuncs import PrintTimeMsg, ReadTailLines, GetCurrentTime
# from .PrettyPrint import PrettyPrintStr


class CConfigRun:
    def __init__(self, sConfigFN='Config.Run', bVerbose=True):
        self.sConfigFN = sConfigFN
        self.bVerbose = bVerbose
        if self.bVerbose:
            PrintTimeMsg('CConfigRun.sConfigFN=%s=' % self.sConfigFN)

    def SaveInfo(self, sInfo):
        with open(self.sConfigFN, 'a') as f:
            sLine = '%s  # %s\n' % (sInfo, GetCurrentTime())
            f.write(sLine)

    def LoadTail(self, iTailNum=1):
        # 返回 [(info, YYYYMMDD-hhnnss)]
        lsResult = []
        for sLine in ReadTailLines(self.sConfigFN, iTailNum):
            sTm = sLine[-15:]
            sV = sLine[:-19]
            lsResult.append((sV, sTm),)
        return lsResult

    def LoadLast(self):
        # 存在返回对应信息，否则返回空串
        try:
            lsTails = self.LoadTail(1)
            if len(lsTails) >= 1:
                lsInfo = lsTails[-1]  # WeiYF.20181112 [0]==[-1] 但后者更符合逻辑
                if len(lsInfo) >= 1:
                    return lsInfo[0]
        except Exception as e:
            pass
        return ''

    def SaveDiff(self, sDiffInfo):
        # 保存与最后一行不同的信息
        sLastLine = self.LoadLast()
        if sDiffInfo != sLastLine:
            self.SaveInfo(sDiffInfo)
            return True
        return False

    def SaveCmp(self, sNewInfo, cbCmp):
        # 保存与最后一行不同的信息
        sLastLine = self.LoadLast()
        if cbCmp(sNewInfo, sLastLine) > 0:
            self.SaveInfo(sNewInfo)
            return True
        return False


def mainCConfigRun():
    o = CConfigRun()
    o.SaveInfo('Test Info')
    sTail = o.LoadTail(2)
    # sTail = o.LoadLast()
    PrintTimeMsg('mainCConfigRun.sTail=%s=' % sTail)


# --------------------------------------
if __name__ == '__main__':
    mainCConfigRun()
