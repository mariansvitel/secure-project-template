from secure_starter.redaction import redact_text


def test_redacts_common_high_risk_patterns() -> None:
    source = (
        "email=builder@example.com token:super-secret-token Authorization Bearer abcdefghijklmnop"
    )
    result = redact_text(source)

    assert result.count == 3
    assert "builder@example.com" not in result.text
    assert "super-secret-token" not in result.text
    assert "abcdefghijklmnop" not in result.text


def test_keeps_normal_product_text() -> None:
    result = redact_text("Compare a private beta with a public waitlist.")

    assert result.text == "Compare a private beta with a public waitlist."
    assert result.count == 0
