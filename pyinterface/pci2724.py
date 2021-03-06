
"""
PCI/CPZ-2724 DIO ボードのドライバです。概ね公式ドライバ GPG-2000 に対応する機能を提供します。


メソッド一覧
----------

.. list-table:: 
  :header-rows: 1

  * - メソッド
    - 公式ドライバの対応する関数
    - 機能
  
  * - `initialize() <#pyinterface.pci2724.pci2724_driver.initialize>`_
    - DioOpen
    - ボードを初期化します

  * - `input_point(start, num) <#pyinterface.pci2724.pci2724_driver.input_point>`_
    - DioInputPoint
    - デジタル入力を任意点数取得します

  * - `input_byte(range_) <#pyinterface.pci2724.pci2724_driver.input_byte>`_
    - DioInputByte
    - デジタル入力を1byte単位で取得します

  * - `input_word(range_) <#pyinterface.pci2724.pci2724_driver.input_word>`_
    - DioInputWord
    - デジタル入力を2byte単位で取得します

  * - `input_dword() <#pyinterface.pci2724.pci2724_driver.input_dword>`_
    - DioInputDword
    - デジタル入力を4byte単位で取得します

  * - `output_point(data, start) <#pyinterface.pci2724.pci2724_driver.output_point>`_
    - DioOutputPoint
    - デジタル出力を任意点数設定します

  * - `output_byte(range_) <#pyinterface.pci2724.pci2724_driver.output_byte>`_
    - DioOutputByte
    - デジタル出力を1byte単位で設定します

  * - `output_word(range_) <#pyinterface.pci2724.pci2724_driver.output_word>`_
    - DioOutputWord
    - デジタル出力を2byte単位で設定します

  * - `output_dword() <#pyinterface.pci2724.pci2724_driver.output_dword>`_
    - DioOutputDword
    - デジタル出力を4byte単位で設定します
 
  * - `set_latch_status(enable) <#pyinterface.pci2724.pci2724_driver.set_latch_status>`_
    - DioSetLatchStatus
    - ラッチ回路の接続を設定します

  * - `get_latch_status() <#pyinterface.pci2724.pci2724_driver.get_latch_status>`_
    - DioGetLatchStatus
    - ラッチ回路の接続状態を取得します

  * - `get_ack_status() <#pyinterface.pci2724.pci2724_driver.get_ack_status>`_
    - DioGetAckStatus
    - ACK2, STB2 端子の接続状態を取得します

  * - `set_ack_pulse_command(ack, pulse) <#pyinterface.pci2724.pci2724_driver.set_ack_pulse_command>`_
    - DioSetAckPulseCommand
    - ACK1, PULS.OUT1 の出力制御を設定します

  * - `get_stb_status() <#pyinterface.pci2724.pci2724_driver.get_stb_status>`_
    - DioGetStbStatus
    - STB1, ACK1 端子の接続状態を取得します

  * - `set_stb_pulse_command(stb, pulse) <#pyinterface.pci2724.pci2724_driver.set_stb_pulse_command>`_
    - DioSetStbPulseCommand
    - STB2, PULS.OUT2 の出力制御を設定します

"""

import struct
from . import core


class InvalidIoNumberError(Exception):
    pass

class InvalidListLengthError(Exception):
    pass

    
class pci2724_driver(core.interface_driver):
    bit_flags_in = (
        (
            ('IN1', 'IN2', 'IN3', 'IN4', 'IN5', 'IN6', 'IN7', 'IN8'),
            ('IN9', 'IN10', 'IN11', 'IN12', 'IN13', 'IN14', 'IN15', 'IN16'),
            ('IN17', 'IN18', 'IN19', 'IN20', 'IN21', 'IN22', 'IN23', 'IN24'),
            ('IN25', 'IN26', 'IN27', 'IN28', 'IN29', 'IN30', 'IN31', 'IN32'),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('IRIN2', '', '', '', '', 'STB2', 'ACKR2', 'ACK2'),
            ('IRIN1', '', '', '', 'LF', 'ACK1', 'STBR1', 'STB1'),
            ('TD1', 'TD2', 'TD3', 'TD4', '', '', '', ''),
            ('PORT0', 'PORT1', 'PORT2', 'PORT3', '', '', '', ''),
            ('SIG1', 'SIG2', 'SIG3', 'SIG4', 'SIGT', 'SIGR', 'SIGRR', ''),
            ('SIG1', 'SIG2', 'SIG3', 'SIG4', 'SIGT', 'SIGR', '', ''),
            ('SIG1', 'SIG2', 'SIG3', 'SIG4', 'EDS1', 'EDS2', 'EDS3', 'EDS4'),
            ('BID0', 'BID1', 'BID2', 'BID3', '', '', '', ''),
        ),
    )
    
    bit_flags_out = (
        (
            ('OUT1', 'OUT2', 'OUT3', 'OUT4', 'OUT5', 'OUT6', 'OUT7', 'OUT8'),
            ('OUT9', 'OUT10', 'OUT11', 'OUT12', 'OUT13', 'OUT14', 'OUT15', 'OUT16'),
            ('OUT17', 'OUT18', 'OUT19', 'OUT20', 'OUT21', 'OUT22', 'OUT23', 'OUT24'),
            ('OUT25', 'OUT26', 'OUT27', 'OUT28', 'OUT29', 'OUT30', 'OUT31', 'OUT32'),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', '', '', '', '', ''),
            ('', '', '', 'PO10', 'PO11', 'PO12', 'ACK10', 'ACK11'),
            ('', '', '', 'PO20', 'PO21', 'PO22', 'STB20', 'STB21'),
            ('TCTRL1', 'TCTRL2', 'TCTRL3', 'TCTRL4', 'SCK1', 'SCK2', 'SCK3', ''),
            ('PORT0', 'PORT1', 'PORT2', 'PORT3', '', '', '', ''),
            ('SIG1', 'SIG2', 'SIG3', 'SIG4', 'SIGT', 'SIGR', '', ''),
            ('SIG1', 'SIG2', 'SIG3', 'SIG4', 'SIGT', 'SIGR', '', ''),
            ('SIG1', 'SIG2', 'SIG3', 'SIG4', 'EDS1', 'EDS2', 'EDS3', 'EDS4'),
            ('', '', '', '', '', '', '', ''),
        ),
    )
    
    io_number = 32
    
    def get_board_id(self):
        bar = 0
        offset = 0x0f
        size = 1
        
        ret = self.read(bar, offset, size)
        bid = ret.to_hex()[1]
        return bid
    
    
    def initialize(self):
        """ボードを初期化します
        
        Notes
        -----
        - 以下の処理を実行します:
        
            - デジタル出力を全て 0 に
            - ラッチ設定の初期化
            - ACK 設定の初期化
            - STB 設定の初期化
        
        - DioOpen 関数に概ね対応しますが、pyinterface には open の概念がありませんので
          initialize() を実行しなくともドライバへアクセス可能です。
        - initialize() を実行しない場合、直前のボード状況が反映されています。
        """
        self.output_dword(0)
        self.set_latch_status()
        self.set_ack_pulse_command()
        self.set_stb_pulse_command()
        return
    
    
    def _verify_io_number_access(self, start, num):
        if (start < 1) or (start+num > self.io_number+1):
            msg = 'I/O number must be in 1-{0},'.format(self.io_number)
            msg += ' while {0}-{1} is given.'.format(start, start+num-1)
            raise InvalidIoNumberError(msg)
        return
    
    
    def input_point(self, start, num):
        """デジタル入力を任意点数取得します
        
        Notes
        -----
        GPG-2000ドライバのDioInputPoint関数に対応します
        
        Parameters
        ----------
        start : int
            取得する最初のチャンネルを指定します (範囲: 1 -- 32)
        num : int
            取得する個数を指定します (`start` + `num` が 33 を超えてはいけません) 
        
        Returns
        -------
        list
            指定したチャンネルのデジタル入力状況のリスト
        
        Examples
        --------
        IN2 - IN6 のデジタル入力状況を取得します
        
        >>> pci2724.input_point(2, 5)
        [1, 0, 1, 0, 1]
        """
        self._verify_io_number_access(start, num)
        inp = self.input_dword()
        bits = inp.to_list()[start-1:start+num-1]
        return bits
    
    
    def output_point(self, data, start):
        """デジタル出力を任意点数設定します
        
        Notes
        -----
        GPG-2000ドライバのDioOutputPoint関数に対応します
        
        Parameters
        ----------
        data : list
            設定するデジタル出力状況のリストです (1:ON, 0:OFF)
        start : int
            設定する最初のチャンネルを指定します (範囲: 1 -- 32)
                
        Examples
        --------
        OUT3 より 4 チャンネルのデジタル出力を ON にします
        
        >>> pci2724.output_point([1,1,1,1], 3)
        3C000000
        """
        bar = 0
        offset = 0x00
        
        num = len(data)
        self._verify_io_number_access(start, num)
        new_d = self.log_bytes_out[0][0:4]
        new_d = core.bytes2list(new_d)
        new_d[start-1:start+num-1] = data
        new_d = core.list2bytes(new_d)
        self.write(bar, offset, new_d)
        return 
    
    
    def input_byte(self, range_):
        """デジタル入力を1byte単位で取得します
        
        Notes
        -----
        GPG-2000ドライバのDioInputByte関数に対応します
        
        Parameters
        ----------
        range_ : str
            デジタル入力状況を取得する範囲を指定します
            
            .. list-table:: 
                :header-rows: 1
        
                * - `range_`
                  - 取得するチャンネル
  
                * - 'IN1_8' 
                  - IN1 から IN8 まで
        
                * - 'IN9_16' 
                  - IN9 から IN16 まで
        
                * - 'IN17_24' 
                  - IN17 から IN24 まで
        
                * - 'IN25_32' 
                  - IN25 から IN32 まで
        
        Returns
        -------
        list
            指定したチャンネルのデジタル入力状況のリスト (length=8)
        
        Examples
        --------
        IN9 - IN16 のデジタル入力状況を取得します
        
        >>> pci2724.input_byte('IN9_16')
        [1, 1, 0, 0, 1, 0, 1, 0]
        """
        bar = 0
        size = 1
        
        if range_ == 'IN1_8': offset = 0x00
        elif range_ == 'IN9_16': offset = 0x01            
        elif range_ == 'IN17_24': offset = 0x02
        elif range_ == 'IN25_32': offset = 0x03
        else: return
        
        d = self.read(bar, offset, size)
        return d
        
    
    def input_word(self, range_):
        """デジタル入力を2byte単位で取得します
        
        Notes
        -----
        GPG-2000ドライバのDioInputWord関数に対応します
        
        Parameters
        ----------
        range_ : str
            デジタル入力状況を取得する範囲を指定します
            
            .. list-table:: 
                :header-rows: 1
        
                * - `range`
                  - 取得するチャンネル
  
                * - 'IN1_16' 
                  - IN1 から IN16 まで
        
                * - 'IN17_32' 
                  - IN17 から IN32 まで
        
        Returns
        -------
        list
            指定したチャンネルのデジタル入力状況のリスト (length=16)
        
        Examples
        --------
        IN1 - IN16 のデジタル入力状況を取得します
        
        >>> pci2724.input_word('IN1_16')
        [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
        """
        bar = 0
        size = 2
        
        if range_ == 'IN1_16': offset = 0x00
        elif range_ == 'IN17_32': offset = 0x02
        else: return
        
        d = self.read(bar, offset, size)
        return d
        
    
    def input_dword(self):
        """デジタル入力を4byte取得します
        
        Notes
        -----
        GPG-2000ドライバのDioInputDword関数に対応します
        
        Returns
        -------
        list
            デジタル入力状況のリスト (length=32)
        
        Examples
        --------
        IN1 - IN32 のデジタル入力状況を取得します
        
        >>> pci2724.input_dword()
        [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0,
         1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
        """
        bar = 0
        size = 4
        offset = 0x00
        
        d = self.read(bar, offset, size)
        return d

        
    def output_byte(self, range_, data, fmt=''):
        """デジタル出力を1byte単位で設定します
        
        Notes
        -----
        GPG-2000ドライバのDioOutputByte関数に対応します
        
        Parameters
        ----------
        range_ : str
            デジタル出力状況を設定する範囲を指定します
            
            .. list-table:: 
                :header-rows: 1
        
                * - `range_`
                  - 設定するチャンネル
  
                * - 'OUT1_8' 
                  - OUT1 から OUT8 まで
        
                * - 'OUT9_16' 
                  - OUT9 から OUT16 まで
        
                * - 'OUT17_24' 
                  - OUT17 から OUT24 まで
        
                * - 'OUT25_32' 
                  - OUT25 から OUT32 まで
        
        data : list or int
            list の場合
                設定するデジタル出力状況のリストです (1:ON, 0:OFF)。
                length は 8 にしてください。
            int の場合
                signed char の bytes に変換して設定されます。
            unsigned int を設定したい場合
                data に正の int を代入し、fmt に '<B' を指定してください。
        
        fmt : str (option)
            fmt を指定した場合、data を fmt に従って pack しようとします。
            fmt に使用する文字列は、struct モジュールの書式です。
        
        
        Examples
        --------
        OUT1 より 1 byte 分のチャンネルのデジタル出力を設定します
        
        >>> pci2724.output_byte([1,0,1,0,1,0,1,0], 'OUT1_8')
        55000000
        """
        bar = 0
        
        if fmt != '':
            d = struct.pack(fmt, data)
        
        elif type(data) in [list, tuple]: 
            if len(data) != 8:
                msg = 'data length should be 8, not {0}'.format(len(data))
                raise InvalidListLengthError(msg)
            d = core.list2bytes(data)
        
        elif type(data) == int:
            d = struct.pack('<b', data)
            
        else:
            return
        
        if range_ == 'OUT1_8': offset = 0x00
        elif range_ == 'OUT9_16': offset = 0x01
        elif range_ == 'OUT17_24': offset = 0x02
        elif range_ == 'OUT25_32': offset = 0x03
        else: return
        
        self.write(bar, offset, d)
        return 


    def output_word(self, range_, data, fmt=''):
        """デジタル出力を2byte単位で設定します
        
        Notes
        -----
        GPG-2000ドライバのDioOutputWord関数に対応します
        
        Parameters
        ----------
        range_ : str
            デジタル出力状況を設定する範囲を指定します
            
            .. list-table:: 
                :header-rows: 1
        
                * - `range_`
                  - 設定するチャンネル
  
                * - 'OUT1_16'
                  - OUT1 から OUT16 まで
        
                * - 'OUT17_32'
                  - OUT17 から OUT32 まで

        data : list or int
            list の場合
                設定するデジタル出力状況のリストです (1:ON, 0:OFF)。
                length は 16 にしてください。
            int の場合
                signed short の bytes に変換して設定されます。
            unsigned int を設定したい場合
                data に正の int を代入し、fmt に '<H' を指定してください。
        
        fmt : str (option)
            fmt を指定した場合、data を fmt に従って pack しようとします。
            fmt に使用する文字列は、struct モジュールの書式です。
        
        Examples
        --------
        OUT17 より 2 byte 分のチャンネルのデジタル出力を設定します
        
        >>> pci2724.output_word([1,0,1,0,1,0,1,0,1,1,1,1,0,0,0,0], 'OUT17_32')

        """
        bar = 0
        
        if fmt != '':
            d = struct.pack(fmt, data)
        
        elif type(data) in [list, tuple]: 
            if len(data) != 16:
                msg = 'data length must be 16, not {0}'.format(len(data))
                raise InvalidListLengthError(msg)
            d = core.list2bytes(data)
        
        elif type(data) == int:
            d = struct.pack('<h', data)
            
        else:
            return
        
        if range_ == 'OUT1_16': offset = 0x00
        elif range_ == 'OUT17_32': offset = 0x02
        else: return
        
        self.write(bar, offset, d)
        return 


    def output_dword(self, data, fmt=''):
        """デジタル出力を4byte設定します
        
        Notes
        -----
        GPG-2000ドライバのDioOutputDword関数に対応します
        
        Parameters
        ----------
        data : list or int or float
            list の場合
                設定するデジタル出力状況のリストです (1:ON, 0:OFF)。
                length は 32 にしてください。
            int の場合
                signed int の bytes に変換して設定されます。
            unsigned int を設定したい場合
                data に正の int を代入し、fmt に '<I' を指定してください。
        
        fmt : str (option)
            fmt を指定した場合、data を fmt に従って pack しようとします。
            fmt に使用する文字列は、struct モジュールの書式です。

        Examples
        --------
        OUT1 より 4byte 分のチャンネルのデジタル出力を設定します
        
        >>> d = [1,0,1,0,1,0,1,0,1,1,1,1,0,0,0,0,1,0,1,0,1,0,1,0,1,1,1,1,0,0,0,0]
        >>> pci2724.output_dword(d)
        """
        bar = 0
        offset = 0x00
        
        if fmt != '':
            d = struct.pack(fmt, data)
        
        elif type(data) in [list, tuple]: 
            if len(data) != 32:
                msg = 'data length must be 32, not {0}'.format(len(data))
                raise InvalidListLengthError(msg)
            d = core.list2bytes(data)
        
        elif type(data) == int:
            d = struct.pack('<i', data)
            
        elif type(data) == float:
            d = struct.pack('<f', data)
            
        else:
            return

        self.write(bar, offset, d)
        return 
    

    def set_latch_status(self, enable=''):
        """ラッチ回路の接続を設定します
        
        Notes
        -----
        Compatibility: DioSetLatchStatus function in GPG-2000 driver
        
        Parameters
        ----------
        enable : str
            ラッチ回路接続を有効にするポートを指定します。
            複数指定する場合、スペースで区切って指定してください。
            指定されなかったポートは、ラッチ回路接続 "無効" になります。
        
            .. list-table:: 
                :header-rows: 1
                
                * - `enable`
                  - 有効にするチャンネル
                
                * - 'PORT0'
                  - IN1 - IN8
            
                * - 'PORT1'
                  - IN9 - IN16
            
                * - 'PORT2'
                  - IN17 - IN24 
        
                * - 'PORT3'
                  - IN25 - IN32
        
        Examples
        --------
        pci2724.set_latch_status('PORT0 PORT3')
        """
        bar = 0
        offset = 0x0b
        
        self.set_flag(bar, offset, enable)
        return
    

    def get_latch_status(self):
        """ラッチ回路の接続を取得します
        
        Notes
        -----
        Compatibility: DioGetLatchStatus function in GPG-2000 driver
        """
        bar = 0
        offset = 0x0b
        size = 1
        
        return self.read(bar, offset, size)
    
    
    def get_ack_status(self):
        """ACK2, STB2 端子の接続状態を取得します

        Notes
        -----
        Compatibility: DioGetAckStatus function in GPG-2000 driver
        """
        bar = 0
        offset = 0x08
        size = 1
        
        return self.read(bar, offset, size)
    
    def set_ack_pulse_command(self, ack='', pulse=''):
        """ACK1, PULS.OUT1 の出力制御を設定します

        Notes
        -----
        Compatibility : DioSetAckPulseCommand function in GPG-2000 driver
        
        Parameters
        ----------
        ack : str 
            ACK 出力制御
        
            .. list-table:: 
                :header-rows: 1
         
                * - `ack`
                  - 動作
        
                * - ''
                  - 何もしません
        
                * - 'ACK10'
                  - clear ACK1 terminal (Low -> High)
        
                * - 'ACK11'
                  - set ACK1 terminal (High -> Low)
        
        pulse : str
            PULSE.OUT1 出力制御
        
            .. list-table:: 
                :header-rows: 1
         
                * - `pulse`
                  - 動作
        
                * - ''
                  - 何もしません
        
                * - 'PO10'
                  - set PULS.OUT1 terminal High
        
                * - 'PO11'
                  - set PULS.OUT1 terminal Low
        
                * - 'PO12'
                  - output Low pulse from PULS.OUT1 terminal
        """
        bar = 0
        offset = 0x08
        flags = ack + ' ' + pulse
        
        return self.set_flag(bar, offset, flags)
    

    def get_stb_status(self):
        """STB1, ACK1 端子の接続状態を取得します
        
        Notes
        -----
        Compatibility: DioGetStbStatus function in GPG-2000 driver
        """
        bar = 0
        offset = 0x09
        size = 1
        
        return self.read(bar, offset, size)
        
    
    def set_stb_pulse_command(self, stb='', pulse=''):
        """STB2, PULS.OUT2 の出力制御を設定します
        
        Notes
        -----
        Compatibility : DioSetStbPulseCommand function in GPG-2000 driver
        
        Parameters
        ----------
        stb : str
            STB 出力制御
        
            .. list-table:: 
                :header-rows: 1
         
                * - `stb`
                  - 動作
        
                * - ''
                  - 何もしません
        
                * - 'STB20'
                  - clear STB2 terminal (Low -> High)

                * - 'STB21'
                  - set STB2 terminal (High -> Low)
        
        pulse : str
            PULSE.OUT2 出力制御
        
            .. list-table:: 
                :header-rows: 1
         
                * - `pulse`
                  - 動作
        
                * - ''
                  - 何もしません
        
                * - 'PO20'
                  - set PULS.OUT2 terminal High
        
                * - 'PO21'
                  - set PULS.OUT2 terminal Low

                * - 'PO22'
                  - output Low pulse from PULS.OUT2 terminal
        """
        bar = 0
        offset = 0x09
        flags = stb + ' ' + pulse
        
        return self.set_flag(bar, offset, flags)
    



    
