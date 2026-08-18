from create_payments import add_payment


def test_add_payments():

    payments = [
        (1, "2026-08-16", 548, "Paid"),
        (2, "2026-08-16", 399, "Paid"),
        (3, "2026-08-16", 699, "Pending"),
        (4, "2026-08-16", 249, "Paid"),
        (5, "2026-08-16", 459, "Pending"),
        (6, "2026-08-16", 799, "Paid"),
        (7, "2026-08-16", 329, "Failed"),
        (8, "2026-08-16", 599, "Paid"),
        (9, "2026-08-16", 449, "Pending"),
        (10, "2026-08-16", 899, "Paid")
    ]

    for payment in payments:

        payment_id = add_payment(
            payment[0],
            payment[1],
            payment[2],
            payment[3]
        )

        print(
            f"Payment created: "
            f"Payment ID={payment_id}, "
            f"Order ID={payment[0]}, "
            f"Amount={payment[2]}, "
            f"Status={payment[3]}"
        )


if __name__ == "__main__":
    test_add_payments()
