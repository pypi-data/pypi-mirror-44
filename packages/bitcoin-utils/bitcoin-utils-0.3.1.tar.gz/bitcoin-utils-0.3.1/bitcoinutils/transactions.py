# Copyright (C) 2018 The python-bitcoin-utils developers
#
# This file is part of python-bitcoin-utils
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoin-utils, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

import hashlib
import struct
from binascii import unhexlify, hexlify

from bitcoinutils.constants import DEFAULT_TX_SEQUENCE, DEFAULT_TX_LOCKTIME, \
                    DEFAULT_TX_VERSION, SATOSHIS_PER_BITCOIN, NEGATIVE_SATOSHI, \
                    EMPTY_TX_SEQUENCE, SIGHASH_ALL, SIGHASH_NONE, \
                    SIGHASH_SINGLE, SIGHASH_ANYONECANPAY, \
                    ABSOLUTE_TIMELOCK_SEQUENCE, REPLACE_BY_FEE_SEQUENCE, \
                    TYPE_ABSOLUTE_TIMELOCK, TYPE_RELATIVE_TIMELOCK, \
                    TYPE_REPLACE_BY_FEE
from bitcoinutils.script import Script



class TxInput:
    """Represents a transaction input.

    A transaction input requires a transaction id of a UTXO and the index of
    that UTXO.

    Attributes
    ----------
    txid : str
        the transaction id as a hex string (little-endian as displayed by
        tools)
    txout_index : int
        the index of the UTXO that we want to spend
    script_sig : list (strings)
        the op code and data of the script as string
    sequence : bytes
        the input sequence (for timelocks, RBF, etc.)

    Methods
    -------
    stream()
        converts TxInput to bytes
    copy()
        creates a copy of the object (classmethod)
    """

    def __init__(self, txid, txout_index, script_sig=Script([]),
                 sequence=DEFAULT_TX_SEQUENCE):
        """See TxInput description"""

        # expected in the format used for displaying Bitcoin hashes
        self.txid = txid
        self.txout_index = txout_index
        self.script_sig = script_sig
        # if user provided a sequence it would be as string (for now...)
        if type(sequence) is str:
            self.sequence = unhexlify(sequence)
        else:
            self.sequence = sequence


    def stream(self):
        """Converts to bytes"""

        # Internally Bitcoin uses little-endian byte order as it improves
        # speed. Hashes are defined and implemented as big-endian thus
        # those are transmitted in big-endian order. However, when hashes are
        # displayed Bitcoin uses little-endian order because it is sometimes
        # convenient to consider hashes as little-endian integers (and not
        # strings)
        # - note that we reverse the byte order for the tx hash since the string
        #   was displayed in little-endian!
        # - note that python's struct uses little-endian by default
        txid_bytes = unhexlify(self.txid)[::-1]
        txout_bytes = struct.pack('<L', self.txout_index)
        script_sig_bytes = self.script_sig.to_bytes()
        data = txid_bytes + txout_bytes + \
                struct.pack('B', len(script_sig_bytes)) + \
                script_sig_bytes + self.sequence
        return data

    @classmethod
    def copy(cls, txin):
        """Deep copy of TxInput"""

        return cls(txin.txid, txin.txout_index, txin.script_sig,
                       txin.sequence)



class TxOutput:
    """Represents a transaction output

    Attributes
    ----------
    amount : float
        the value we want to send to this output (in BTC)
    script_pubkey : list (string)
        the script that will lock this amount

    Methods
    -------
    stream()
        converts TxInput to bytes
    copy()
        creates a copy of the object (classmethod)
    """


    def __init__(self, amount, script_pubkey):
        """See TxOutput description"""

        self.amount = amount
        self.script_pubkey = script_pubkey


    def stream(self):
        """Converts to bytes"""

        # internally all little-endian except hashes
        # note struct uses little-endian by default

        # 0.29*100000000 results in 28999999.999999996 so we round to the
        # closest integer -- this is because the result is represented as
        # fractions
        amount_bytes = struct.pack('<q', round(self.amount * SATOSHIS_PER_BITCOIN))
        script_bytes = self.script_pubkey.to_bytes()
        data = amount_bytes + struct.pack('B', len(script_bytes)) + script_bytes
        return data


    @classmethod
    def copy(cls, txout):
        """Deep copy of TxOutput"""

        return cls(txout.amount, txout.script_pubkey)


class Sequence:
    """Helps setting up appropriate sequence. Used to provide the sequence to
    transaction inputs and to scripts.

    Attributes
    ----------
    value : int
        The value of the block height or the 512 seconds increments
    seq_type : int
        Specifies the type of sequence (TYPE_RELATIVE_SEQUNCE |
        TYPE_ABSOLUTE_SEQUENCE | TYPE_REPLACE_BY_FEE
    is_type_block : bool
        If type is TYPE_RELATIVE_SEQUENCE then this specifies its type 
        (block height or 512 secs increments)

    Methods
    -------
    for_input_sequence()
        Serializes the relative sequence as required in a transaction
    for_script()
        Returns the appropriate integer for a script; e.g. for relative timelocks

    Raises
    ------
    ValueError
        if the value is not within range of 2 bytes.
    """

    def __init__(self, seq_type, value=None, is_type_block=True):
        self.seq_type = seq_type
        self.value = value
        if self.seq_type == TYPE_RELATIVE_TIMELOCK and (self.value < 1 or self.value > 0xffff):
            raise ValueError('Sequence should be between 1 and 65535')
        self.is_type_block = is_type_block

    def for_input_sequence(self):
        """Creates a relative timelock sequence value as expected from 
        TxInput sequence attribute"""
        if self.seq_type == TYPE_ABSOLUTE_TIMELOCK:
            return ABSOLUTE_TIMELOCK_SEQUENCE

        if self.seq_type == TYPE_REPLACE_BY_FEE:
            return REPLACE_BY_FEE_SEQUENCE

        if self.seq_type == TYPE_RELATIVE_TIMELOCK:
            # most significant bit is already 0 so relative timelocks are enabled
            seq = 0
            # if not block height type set 23 bit
            if not self.is_type_block:
                seq |= 1 << 22
            # set the value
            seq |= self.value
            seq_bytes = seq.to_bytes(4, byteorder='little')
            return seq_bytes



    def for_script(self):
        """Creates a relative/absolute timelock sequence value as expected in scripts"""
        if self.seq_type == TYPE_REPLACE_BY_FEE:
            raise ValueError('RBF is not to be included in a script.')

        script_integer = self.value

        # if not block-height type then set 23 bit
        if self.seq_type == TYPE_RELATIVE_TIMELOCK and not self.is_type_block:
            script_integer |= 1 << 22

        return script_integer


class Locktime:
    """Helps setting up appropriate locktime.

    Attributes
    ----------
    value : int
        The value of the block height or the 512 seconds increments

    Methods
    -------
    for_transaction()
        Serializes the locktime as required in a transaction

    Raises
    ------
    ValueError
        if the value is not within range of 2 bytes.
    """

    def __init__(self, value):
        self.value = value

    def for_transaction(self):
        """Creates a timelock as expected from Transaction"""

        locktime_bytes = self.value.to_bytes(4, byteorder='little')
        return locktime_bytes



class Transaction:
    """Represents a Bitcoin transaction

    Attributes
    ----------
    inputs : list (TxInput)
        A list of all the transaction inputs
    outputs : list (TxOutput)
        A list of all the transaction outputs
    locktime : bytes
        The transaction's locktime parameter
    version : bytes
        The transaction version

    Methods
    -------
    stream()
        Converts Transaction to bytes
    serialize()
        Converts Transaction to hex string
    get_txid()
        Calculates txid and returns it
    copy()
        creates a copy of the object (classmethod)
    get_transaction_digest(txin_index, script, sighash)
        returns the transaction input's digest that is to be signed according
        to sighash
    """

    def __init__(self, inputs=[], outputs=[], locktime=DEFAULT_TX_LOCKTIME,
                 version=DEFAULT_TX_VERSION):
        """See Transaction description"""
        self.inputs = inputs
        self.outputs = outputs

        # if user provided a locktime it would be as string (for now...)
        if type(locktime) is str:
            self.locktime = unhexlify(locktime)
        else:
            self.locktime = locktime

        self.version = version


    @classmethod
    def copy(cls, tx):
        """Deep copy of Transaction"""

        ins = [TxInput.copy(txin) for txin in tx.inputs]
        outs = [TxOutput.copy(txout) for txout in tx.outputs]
        return cls(ins, outs, tx.locktime, tx.version)


    def get_transaction_digest(self, txin_index, script, sighash=SIGHASH_ALL):
        """Returns the transaction's digest for signing.

        |  SIGHASH types (see constants.py):
        |      SIGHASH_ALL - signs all inputs and outputs (default)
        |      SIGHASH_NONE - signs all of the inputs
        |      SIGHASH_SINGLE - signs all inputs but only txin_index output
        |      SIGHASH_ANYONECANPAY (only combined with one of the above)
        |      - with ALL - signs all outputs but only txin_index input
        |      - with NONE - signs only the txin_index input
        |      - with SINGLE - signs txin_index input and output

        Attributes
        ----------
        txin_index : int
            The index of the input that we wish to sign
        script : list (string)
            The scriptPubKey of the UTXO that we want to spend
        sighash : int
            The type of the signature hash to be created
        """

        # clone transaction to modify without messing up the real transaction
        tmp_tx = Transaction.copy(self)

        # make sure all input scriptSigs are empty
        for txin in tmp_tx.inputs:
            txin.script_sig = Script([])

        #
        # TODO Deal with (delete?) script's OP_CODESEPARATORs, if any
        # Very early versions of Bitcoin were using a different design for
        # scripts that were flawed. OP_CODESEPARATOR has no purpose currently
        # but we could not delete it for compatibility purposes. If it exists
        # in a script it needs to be removed.
        #

        # the temporary transaction's scriptSig needs to be set to the
        # scriptPubKey of the UTXO we are trying to spend - this is required to
        # get the correct transaction digest (which is then signed)
        tmp_tx.inputs[txin_index].script_sig = script

        #
        # by default we sign all inputs/outputs (SIGHASH_ALL is used)
        #

        # whether 0x0n or 0x8n, bitwise AND'ing will result to n
        if (sighash & 0x1f) == SIGHASH_NONE:
            # do not include outputs in digest (i.e. do not sign outputs)
            tmp_tx.outputs = []

            # do not include sequence of other inputs (zero them for digest)
            # which means that they can be replaced
            for i in range(len(tmp_tx.inputs)):
                if i != txin_index:
                    tmp_tx.inputs[i].sequence = EMPTY_TX_SEQUENCE

        elif (sighash & 0x1f) == SIGHASH_SINGLE:
            # only sign the output that corresponds to txin_index

            if txin_index >= len(tmp_tx.outputs):
                raise ValueError('Transaction index is greater than the \
                                 available outputs')

            # keep only output that corresponds to txin_index -- delete all outputs
            # after txin_index and zero out all outputs upto txin_index
            txout = tmp_tx.outputs[txin_index]
            tmp_tx.outputs = []
            for i in range(txin_index):
                tmp_tx.outputs.append( TxOutput(NEGATIVE_SATOSHI, Script([])) )
            tmp_tx.outputs.append(txout)

            # do not include sequence of other inputs (zero them for digest)
            # which means that they can be replaced
            for i in range(len(tmp_tx.inputs)):
                if i != txin_index:
                    tmp_tx.inputs[i].sequence = EMPTY_TX_SEQUENCE

        # bitwise AND'ing 0x8n to 0x80 will result to true
        if sighash & SIGHASH_ANYONECANPAY:
            # ignore all other inputs from the signature which means that
            # anyone can add new inputs
            tmp_tx.inputs = [tmp_tx.inputs[txin_index]]

        # get the byte stream of the temporary transaction
        tx_for_signing = tmp_tx.stream()

        # add sighash bytes to be hashed
        # Note that although sighash is one byte it is hashed as a 4 byte value.
        # There is no real reason for this other than that the original implementation
        # of Bitcoin stored sighash as an integer (which serializes as a 4
        # bytes), i.e. it should be converted to one byte before serialization.
        # It is converted to 1 byte before serializing to send to the network
        tx_for_signing += struct.pack('<i', sighash)

        # create transaction digest -- note double hashing
        tx_digest = hashlib.sha256( hashlib.sha256(tx_for_signing).digest()).digest()

        return tx_digest


    def stream(self):
        """Converts to bytes"""

        data = self.version
        txin_count_bytes = chr(len(self.inputs)).encode()
        txout_count_bytes = chr(len(self.outputs)).encode()
        data += txin_count_bytes
        for txin in self.inputs:
            data += txin.stream()
        data += txout_count_bytes
        for txout in self.outputs:
            data += txout.stream()
        data += self.locktime
        return data


    def get_txid(self):
        """Hashes the serialized tx to get a unique id"""

        data = self.stream()
        hash = hashlib.sha256( hashlib.sha256(data).digest() ).digest()
        # note that we reverse the hash for display purposes
        return hexlify(hash[::-1]).decode('utf-8')


    def serialize(self):
        """Converts to hex string"""

        return hexlify(self.stream()).decode('utf-8')


def main():
    # READ SEGWIT BIPs
    # READ EXAMPLE SERIALIZATION OF SEGWIT TX:
    # https://medium.com/coinmonks/how-to-create-a-raw-bitcoin-transaction-step-by-step-239b888e87f2
    pass

if __name__ == "__main__":
    main()

