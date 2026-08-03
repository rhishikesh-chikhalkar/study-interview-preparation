"""
Coding Interview Problems - Study Guide

This file contains commonly asked interview problems with multiple solution approaches.
Organized for easy reference and learning.
"""

# --------------------------------------------------------------------------------
# 1. API FRAMEWORKS SETUP
# --------------------------------------------------------------------------------

from collections import Counter
from fastapi import FastAPI, Query, Request
from flask import Flask, jsonify

# FastAPI setup
fastapi_app = FastAPI(title="Demo API", version="1.0")


@fastapi_app.get("/health")
async def check_health():
    """FastAPI health check endpoint"""
    return {"Status": "healthy!"}


# Flask setup
flask_app = Flask(__name__)


@flask_app.route("/health", methods=["GET"])
def flask_check_health():
    """Flask health check endpoint"""
    return jsonify({"Status": "healthy!"})


pagination_api = FastAPI()
items = [{"id": i, "name": f"item-{i}"} for i in range(1, 100)]


@pagination_api.get("/items")
def get_items(
    request: Request,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    total = len(items)
    paginated_items = items[offset : offset + limit]

    base_url = str(request.url).split("?")[0]

    next_url = (
        f"{base_url}?limit={limit}&offset={offset + limit}"
        if offset + limit < total
        else None
    )
    prev_url = (
        f"{base_url}?limit={limit}&offset={max(0, offset - limit)}"
        if offset > 0
        else None
    )

    return {
        "count": total,
        "next": next_url,
        "previous": prev_url,
        "results": paginated_items,
    }


# --------------------------------------------------------------------------------
# Problem 1: Reverse a String
# --------------------------------------------------------------------------------


def reverse_string_simple(data):
    """Approach 1: Using Python slicing (simplest)"""
    return data[::-1]


def reverse_using_two_pointer(data):
    """Approach 2: Using two-pointer technique (manual)

    Time Complexity: O(n)
    Space Complexity: O(n) for the list
    """
    data_list = list(data)
    left = 0
    right = len(data_list) - 1

    while left < right:
        # Swap using tuple unpacking
        data_list[left], data_list[right] = data_list[right], data_list[left]
        left += 1
        right -= 1

    return "".join(data_list) if isinstance(data, str) else data_list


# Test cases
data = "Rhishikesh"
print(f"Original: {data}")
print(f"Reversed (slicing): {reverse_string_simple(data)}")
print(f"Reversed (two-pointer): {reverse_using_two_pointer(data)}")


# --------------------------------------------------------------------------------
# Problem 2: Check Palindrome
# --------------------------------------------------------------------------------


def palindrome_simple(sample_text):
    """Approach 1: Using string slicing

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    clean_text = sample_text.lower()
    return clean_text == clean_text[::-1]


def palindrome_using_two_pointer(sample_text):
    """Approach 2: Using two-pointer technique

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    text = sample_text.lower()
    left, right = 0, len(text) - 1

    while left < right:
        if text[left] != text[right]:
            return False
        left += 1
        right -= 1

    return True


# Test cases
sample_text_1 = "rhishikesh"
sample_text_2 = "radar"

print(f"\nString 1: '{sample_text_1}'")
print(f"  Is palindrome (slicing): {palindrome_simple(sample_text_1)}")
print(f"  Is palindrome (two-pointer): {palindrome_using_two_pointer(sample_text_1)}")

print(f"\nString 2: '{sample_text_2}'")
print(f"  Is palindrome (slicing): {palindrome_simple(sample_text_2)}")
print(f"  Is palindrome (two-pointer): {palindrome_using_two_pointer(sample_text_2)}")


# --------------------------------------------------------------------------------
# Problem 3: Count Character Frequency
# --------------------------------------------------------------------------------


def count_char_simple(sample_text):
    """Approach 1: Using dictionary iteration

    Time Complexity: O(n)
    Space Complexity: O(k) where k is number of unique characters
    """
    freq = {}
    for char in sample_text:
        freq[char] = freq.get(char, 0) + 1
    return freq


def count_char_using_counter(sample_text):
    """Approach 2: Using collections.Counter (optimized)

    Time Complexity: O(n)
    Space Complexity: O(k) where k is number of unique characters
    """
    return dict(Counter(sample_text))


# Test cases
print(f"\nString 1: '{sample_text_1}'")
print(f"  Frequency (dict): {count_char_simple(sample_text_1)}")
print(f"  Frequency (Counter): {count_char_using_counter(sample_text_1)}")

print(f"\nString 2: '{sample_text_2}'")
print(f"  Frequency (dict): {count_char_simple(sample_text_2)}")
print(f"  Frequency (Counter): {count_char_using_counter(sample_text_2)}")


# --------------------------------------------------------------------------------
# Problem 4: Check Unique Elements
# --------------------------------------------------------------------------------


def is_unique_using_set(sample_list):
    """Approach 1: Using set length comparison

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    return len(sample_list) == len(set(sample_list))


def is_unique_using_seen_tracking(sample_list):
    """Approach 2: Using seen set with early exit

    Time Complexity: O(n)
    Space Complexity: O(n)
    Best Case: O(1) - exits early if duplicate found at start
    """
    seen = set()
    for item in sample_list:
        if item in seen:
            return False
        seen.add(item)
    return True


# Test cases
sample_list_1 = [1, 2, 3, 4]
sample_list_2 = [1, 2, 3, 2, 4]

print(f"\nList 1: {sample_list_1}")
print(f"  All unique (set): {is_unique_using_set(sample_list_1)}")
print(f"  All unique (tracking): {is_unique_using_seen_tracking(sample_list_1)}")

print(f"\nList 2: {sample_list_2}")
print(f"  All unique (set): {is_unique_using_set(sample_list_2)}")
print(f"  All unique (tracking): {is_unique_using_seen_tracking(sample_list_2)}")


# --------------------------------------------------------------------------------
# Problem 5: Find Second Largest Number
# --------------------------------------------------------------------------------


def find_second_largest_sorting(sample_list):
    """Approach 1: Using sorting

    Time Complexity: O(n log n)
    Space Complexity: O(1) or O(n) depending on sort algorithm
    """
    if len(sample_list) < 2:
        return None
    return sorted(sample_list)[-2]


def find_second_largest_iterative(sample_list):
    """Approach 2: Using single pass iteration (optimal)

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if len(sample_list) < 2:
        return None

    first = second = float("-inf")

    for number in sample_list:
        if number > first:
            second = first
            first = number
        elif number > second and number != first:
            second = number

    return second if second != float("-inf") else None


# Test cases
print(f"\nList 1: {sample_list_1}")
print(f"  Second largest (sorting): {find_second_largest_sorting(sample_list_1)}")
print(f"  Second largest (iterative): {find_second_largest_iterative(sample_list_1)}")

print(f"\nList 2: {sample_list_2}")
print(f"  Second largest (sorting): {find_second_largest_sorting(sample_list_2)}")
print(f"  Second largest (iterative): {find_second_largest_iterative(sample_list_2)}")


# --------------------------------------------------------------------------------
