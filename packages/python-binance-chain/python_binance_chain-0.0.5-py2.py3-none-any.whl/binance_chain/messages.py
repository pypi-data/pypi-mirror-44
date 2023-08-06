import json
import binascii
from typing import Dict, Union
from decimal import Decimal
from collections import OrderedDict

from binance_chain.wallet import Wallet
from binance_chain.constants import TimeInForce, OrderSide, OrderType
from binance_chain.dex_pb2 import NewOrder, CancelOrder, TokenFreeze, TokenUnfreeze, StdTx, StdSignature
from binance_chain.utils import encode_number, varint_encode

# An identifier for tools triggering broadcast transactions, set to zero if unwilling to disclose.
BROADCAST_SOURCE = 1


class Msg:

    AMINO_MESSAGE_TYPE = ""
    INCLUDE_AMINO_LENGTH_PREFIX = False

    def __init__(self, wallet: Wallet):
        self._wallet = wallet

    def to_dict(self) -> Dict:
        return {}

    def to_protobuf(self):
        pass

    def to_amino(self):
        proto = self.to_protobuf()
        if type(proto) != bytes:
            proto = proto.SerializeToString()

        # wrap with type
        type_bytes = b""
        if self.AMINO_MESSAGE_TYPE:
            type_bytes = binascii.unhexlify(self.AMINO_MESSAGE_TYPE)
            varint_length = varint_encode(len(proto) + len(type_bytes))
        else:
            varint_length = varint_encode(len(proto))

        msg = b""
        if self.INCLUDE_AMINO_LENGTH_PREFIX:
            msg += varint_length
        msg += type_bytes + proto

        return msg

    @property
    def wallet(self):
        return self._wallet

    def to_hex_data(self):
        """Wrap in a Standard Transaction Message and convert to hex string

        """
        return binascii.hexlify(StdTxMsg(self).to_amino())

    def increment_sequence(self):
        self._wallet.increment_account_sequence()


class Signature:

    def __init__(self, msg: Msg, data=None, memo=''):
        self._msg = msg
        self._chain_id = msg.wallet.chain_id
        self._data = data
        self._memo = memo
        self._source = BROADCAST_SOURCE

    def to_json(self):
        return json.dumps(OrderedDict([
            ('account_number', str(self._msg.wallet.account_number)),
            ('chain_id', self._chain_id),
            ('data', self._data),
            ('memo', self._memo),
            ('msgs', [self._msg.to_dict()]),
            ('sequence', str(self._msg.wallet.sequence)),
            ('source', str(self._source))
        ]), separators=(',', ':'), ensure_ascii=False)

    def to_bytes_json(self):
        return self.to_json().encode()

    def sign(self, wallet):
        # sign string
        json_bytes = self.to_bytes_json()

        signed = wallet.sign_message(json_bytes)
        return signed[-64:]


class NewOrderMsg(Msg):

    ORDER_SIDE_INT = {
        OrderSide.BUY: 1,
        OrderSide.SELL: 2
    }

    ORDER_TYPE_INT = {
        OrderType.LIMIT: 2
    }

    TIME_IN_FORCE_INT = {
        TimeInForce.GOOD_TILL_EXPIRE: 1,
        TimeInForce.IMMEDIATE_OR_CANCEL: 3
    }

    AMINO_MESSAGE_TYPE = b"CE6DC043"

    def __init__(self, wallet: Wallet, symbol: str, time_in_force: TimeInForce, order_type: OrderType, side: OrderSide,
                 price: Union[int, float, Decimal], quantity: Union[int, float, Decimal]):
        """NewOrder transaction creates a new order to buy and sell tokens on Binance DEX.

        :param symbol: symbol for trading pair in full name of the tokens e.g. 'ANN-457_BNB'
        :param time_in_force: TimeInForce type (GOOD_TILL_EXPIRE, IMMEDIATE_OR_CANCEL)
        :param order_type: OrderType (LIMIT, MARKET)
        :param side: OrderSide (BUY, SELL)
        :param price: price of the order e.g. Decimal(0.000396000) or 0.002384
        :param quantity: quantity of the order Decimal(12) or 12

        """
        super().__init__(wallet)
        self._symbol = symbol
        self._time_in_force = NewOrderMsg.TIME_IN_FORCE_INT[time_in_force]
        self._order_type = NewOrderMsg.ORDER_TYPE_INT[order_type]
        self._side = NewOrderMsg.ORDER_SIDE_INT[side]
        self._price = encode_number(price)
        self._quantity = encode_number(quantity)

    def to_dict(self) -> Dict:
        return OrderedDict([
            ('id', self._wallet.generate_order_id()),
            ('ordertype', self._order_type),
            ('price', self._price),
            ('quantity', self._quantity),
            ('sender', self._wallet.address),
            ('side', self._side),
            ('symbol', self._symbol),
            ('timeinforce', self._time_in_force),
        ])

    def to_protobuf(self) -> NewOrder:
        pb = NewOrder()
        pb.sender = self._wallet.address_decoded
        pb.id = self._wallet.generate_order_id()
        pb.symbol = self._symbol.encode()
        pb.timeinforce = self._time_in_force
        pb.ordertype = self._order_type
        pb.side = self._side
        pb.price = self._price
        pb.quantity = self._quantity
        return pb


class LimitOrderMsg(NewOrderMsg):

    def __init__(self, wallet: Wallet, symbol: str, side: OrderSide,
                 price: Union[int, float, Decimal], quantity: Union[int, float, Decimal],
                 time_in_force: TimeInForce = TimeInForce.GOOD_TILL_EXPIRE):
        """NewOrder transaction creates a new order to buy and sell tokens on Binance DEX.

        :param symbol: symbol for trading pair in full name of the tokens e.g. 'ANN-457_BNB'
        :param side: OrderSide (BUY, SELL)
        :param price: price of the order e.g. Decimal(0.000396000) or 0.002384
        :param quantity: quantity of the order Decimal(12) or 12
        :param time_in_force: TimeInForce type (GOOD_TILL_EXPIRE, IMMEDIATE_OR_CANCEL) default GOOD_TILL_EXPIRE

        """
        super().__init__(
            wallet=wallet,
            symbol=symbol,
            time_in_force=time_in_force,
            order_type=OrderType.LIMIT,
            side=side,
            price=price,
            quantity=quantity
        )


class LimitOrderBuyMsg(LimitOrderMsg):

    def __init__(self, wallet: Wallet, symbol: str,
                 price: Union[int, float, Decimal], quantity: Union[int, float, Decimal],
                 time_in_force: TimeInForce = TimeInForce.GOOD_TILL_EXPIRE):
        """LimitOrderBuyMsg transaction creates a new limit order buy message on Binance DEX.

        :param symbol: symbol for trading pair in full name of the tokens e.g. 'ANN-457_BNB'
        :param price: price of the order e.g. Decimal(0.000396000) or 0.002384
        :param quantity: quantity of the order Decimal(12) or 12
        :param time_in_force: TimeInForce type (GOOD_TILL_EXPIRE, IMMEDIATE_OR_CANCEL) default GOOD_TILL_EXPIRE

        """
        super().__init__(
            wallet=wallet,
            symbol=symbol,
            time_in_force=time_in_force,
            side=OrderSide.BUY,
            price=price,
            quantity=quantity
        )


class LimitOrderSellMsg(LimitOrderMsg):

    def __init__(self, wallet: Wallet, symbol: str,
                 price: Union[int, float, Decimal], quantity: Union[int, float, Decimal],
                 time_in_force: TimeInForce = TimeInForce.GOOD_TILL_EXPIRE):
        """LimitOrderSellMsg transaction creates a new limit order sell message on Binance DEX.

        :param symbol: symbol for trading pair in full name of the tokens e.g. 'ANN-457_BNB'
        :param time_in_force: TimeInForce type (GOOD_TILL_EXPIRE, IMMEDIATE_OR_CANCEL)
        :param price: price of the order e.g. Decimal(0.000396000) or 0.002384
        :param quantity: quantity of the order Decimal(12) or 12
        :param time_in_force: TimeInForce type (GOOD_TILL_EXPIRE, IMMEDIATE_OR_CANCEL) default GOOD_TILL_EXPIRE

        """
        super().__init__(
            wallet=wallet,
            symbol=symbol,
            time_in_force=time_in_force,
            side=OrderSide.SELL,
            price=price,
            quantity=quantity
        )


class CancelOrderMsg(Msg):

    AMINO_MESSAGE_TYPE = b"166E681B"

    def __init__(self, wallet: Wallet, symbol: str, order_id: str):
        """Cancel transactions cancel the outstanding (unfilled) orders from the Binance DEX. After cancel success,
        the locked quantity on the orders would return back to the address' balance and become free to use,
        i.e. transfer or send new orders.

        :param symbol: symbol for trading pair in full name of the tokens
        :param order_id: order id of the one to cancel
        """
        super().__init__(wallet)

        self._symbol = symbol
        self._order_id = order_id

    def to_dict(self):
        return OrderedDict([
            ('refid', self._order_id),
            ('sender', self._wallet.address),
            ('symbol', self._symbol),
        ])

    def to_protobuf(self) -> CancelOrder:
        pb = CancelOrder()
        pb.sender = self._wallet.address_decoded
        pb.refid = self._order_id
        pb.symbol = self._symbol.encode()
        return pb


class FreezeMsg(Msg):

    AMINO_MESSAGE_TYPE = b"E774B32D"

    def __init__(self, wallet: Wallet, symbol: str, amount: Union[int, float, Decimal]):
        """Freeze transaction moves the amount of the tokens into a frozen state,
        in which it cannot be used to transfer or send new orders.

        :param symbol: token symbol, in full name with "-" suffix
        :param amount: amount of token to freeze
        """
        super().__init__(wallet)
        self._symbol = symbol
        self._amount = encode_number(amount)

    def to_dict(self):
        return OrderedDict([
            ('amount', self._amount),
            ('from', self._wallet.address),
            ('symbol', self._symbol),
        ])

    def to_protobuf(self) -> TokenFreeze:
        pb = TokenFreeze()
        setattr(pb, 'from', self._wallet.address_decoded)
        pb.symbol = self._symbol.encode()
        pb.amount = self._amount
        return pb


class UnFreezeMsg(Msg):

    AMINO_MESSAGE_TYPE = b"6515FF0D"

    def __init__(self, wallet: Wallet, symbol: str, amount: Union[int, float, Decimal]):
        """Turn the amount of frozen tokens back to free state.

        :param symbol: token symbol, in full name with "-" suffix
        :param amount: amount of token to unfreeze
        """
        super().__init__(wallet)
        self._symbol = symbol
        self._amount = encode_number(amount)

    def to_dict(self):
        return OrderedDict([
            ('amount', self._amount),
            ('from', self._wallet.address),
            ('symbol', self._symbol),
        ])

    def to_protobuf(self) -> TokenUnfreeze:
        pb = TokenUnfreeze()
        setattr(pb, 'from', self._wallet.address_decoded)
        pb.symbol = self._symbol.encode()
        pb.amount = self._amount
        return pb


class SignatureMsg(Msg):

    AMINO_MESSAGE_TYPE = None

    def __init__(self, msg: Msg):
        super().__init__(msg.wallet)
        self._signature = Signature(msg)

    def to_protobuf(self) -> NewOrder:
        pub_key_msg = PubKeyMsg(self._wallet)
        std_sig = StdSignature()
        std_sig.sequence = self._wallet.sequence
        std_sig.account_number = self._wallet.account_number
        std_sig.pub_key = pub_key_msg.to_amino()
        std_sig.signature = self._signature.sign(self._wallet)
        return std_sig


class StdTxMsg(Msg):

    AMINO_MESSAGE_TYPE = b"F0625DEE"
    INCLUDE_AMINO_LENGTH_PREFIX = True

    def __init__(self, msg: Msg, data='', memo=''):
        super().__init__(msg.wallet)

        self._msg = msg
        self._signature = SignatureMsg(msg)
        self._data = data
        self._memo = memo
        self._source = BROADCAST_SOURCE

    def to_protobuf(self) -> NewOrder:
        stdtx = StdTx()
        stdtx.msgs.extend([self._msg.to_amino()])
        stdtx.signatures.extend([self._signature.to_amino()])
        stdtx.data = self._data.encode()
        stdtx.memo = self._memo
        stdtx.source = self._source
        return stdtx


class PubKeyMsg(Msg):

    AMINO_MESSAGE_TYPE = b"EB5AE987"

    def __init__(self, wallet: Wallet):
        super().__init__(wallet)

    def to_protobuf(self):
        return self._wallet.public_key

    def to_amino(self):
        proto = self.to_protobuf()

        type_bytes = binascii.unhexlify(self.AMINO_MESSAGE_TYPE)

        varint_length = varint_encode(len(proto))

        msg = type_bytes + varint_length + proto

        return msg
