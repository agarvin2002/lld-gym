"""Tests for LSP Payment Hierarchy exercise."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.modules.pop('starter', None)
from starter import CreditCard, DebitCard, GiftCard, PaymentMethod, RefundablePayment


class TestCreditCard:
    def test_process_returns_success(self):
        cc = CreditCard("1234", "Alice")
        result = cc.process(100.0)
        assert result.success is True
        assert result.amount == 100.0

    def test_refund_returns_true(self):
        cc = CreditCard("1234", "Alice")
        assert cc.refund("TX-001") is True

    def test_credit_card_is_payment_method(self):
        assert isinstance(CreditCard("1234", "Alice"), PaymentMethod)

    def test_credit_card_is_refundable(self):
        assert isinstance(CreditCard("1234", "Alice"), RefundablePayment)

    def test_get_payment_type(self):
        assert CreditCard("1234", "Alice").get_payment_type() == "CreditCard"


class TestDebitCard:
    def test_process_returns_success(self):
        dc = DebitCard("5678")
        result = dc.process(50.0)
        assert result.success is True

    def test_refund_returns_true(self):
        dc = DebitCard("5678")
        assert dc.refund("TX-002") is True

    def test_debit_card_is_refundable(self):
        assert isinstance(DebitCard("5678"), RefundablePayment)


class TestGiftCard:
    def test_process_with_sufficient_balance(self):
        gc = GiftCard("GIFT123", balance=100.0)
        result = gc.process(50.0)
        assert result.success is True

    def test_process_with_insufficient_balance(self):
        gc = GiftCard("GIFT123", balance=10.0)
        result = gc.process(50.0)
        assert result.success is False

    def test_gift_card_is_payment_method(self):
        assert isinstance(GiftCard("GIFT123", 100.0), PaymentMethod)

    def test_gift_card_is_not_refundable(self):
        """LSP-compliant design: GiftCard does NOT inherit RefundablePayment."""
        assert not isinstance(GiftCard("GIFT123", 100.0), RefundablePayment)


class TestSubstitution:
    def test_all_payment_methods_can_process(self):
        """Any PaymentMethod can be substituted in process_payment."""
        def process_payment(method: PaymentMethod, amount: float) -> bool:
            return method.process(amount).success

        methods: list[PaymentMethod] = [
            CreditCard("1234", "Alice"),
            DebitCard("5678"),
            GiftCard("GIFT", 1000.0),
        ]
        for method in methods:
            assert process_payment(method, 10.0) is True
