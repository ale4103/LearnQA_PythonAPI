class TestExample:
    def test_check_length(self):
        phrase = input("Set a phrase: ")
        obtained_len = len(phrase)
        expected_len = 15
        assert obtained_len < expected_len, f"Obtained len >= {expected_len}"