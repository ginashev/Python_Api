def test_phrase():
    phrase = input("Set a phrase less then 15 characters : ")
    phrase_length = len(phrase)
    assert phrase_length < 15, f"Phrase '{phrase}' is more than 15 characters, current length {phrase_length}'"
