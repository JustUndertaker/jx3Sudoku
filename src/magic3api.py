# -*- coding: utf-8 -*-
class magic3():
    def __init__(self):
        self.__magiclist = [[2, 7, 6, 9, 5, 1, 4, 3, 8],
                            [2, 9, 4, 7, 5, 3, 6, 1, 8],
                            [4, 3, 8, 9, 5, 1, 2, 7, 6],
                            [4, 9, 2, 3, 5, 7, 8, 1, 6],
                            [6, 1, 8, 7, 5, 3, 2, 9, 4],
                            [6, 7, 2, 1, 5, 9, 8, 3, 4],
                            [8, 3, 4, 1, 5, 9, 6, 7, 2],
                            [8, 1, 6, 3, 5, 7, 4, 9, 2]]

    def getlist(self, datalist) -> dict:
        '''
        接口：获取结果列表
        datalist:参数列表，0表示无数据
        '''

        indexlist = []
        indexreq = []
        indexnum = -1
        code = '0'
        for i in range(0, 9):
            if datalist[i] != 0:
                indexlist.append(i)
            else:
                indexreq.append(i)

        if not indexlist:
            getdata = [0, 0, 0, 0, 0, 0, 0, 0]
            code = '1'
            datareq = {'index': indexreq, 'data': getdata, 'code': code}
            return datareq

        for i in range(0, 8):
            flag = True
            data = self.__magiclist[i]
            for index in indexlist:
                if datalist[index] != data[index]:
                    flag = False
            if flag:
                indexnum = i
                break
        if indexnum != -1:
            getdata = self.__magiclist[indexnum]
        else:
            getdata = [0, 0, 0, 0, 0, 0, 0, 0]
            code = '1'
        datareq = {'index': indexreq, 'data': getdata, 'code': code}

        return datareq
