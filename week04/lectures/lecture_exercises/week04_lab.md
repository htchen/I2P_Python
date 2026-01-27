# Week 4 Lab: HTTP Requests & API Keys

## Lab Overview

In this lab, you'll practice making HTTP requests using Python's `requests` library and interact with the Nominatim geocoding API.

**Time:** 90 minutes

### Prerequisites
- Completed Week 4 lecture
- Python environment with `requests` installed
- Internet connection

### Learning Objectives
1. Make HTTP GET requests with the `requests` library
2. Handle query parameters and headers properly
3. Parse JSON responses from APIs
4. Implement proper error handling
5. Respect rate limits when making API calls

---

## Setup

Before starting, ensure you have the `requests` library:

```bash
pip install requests
```

Create your working file:

```bash
cd week04/labs
touch week04_starter.py
```

---

## Exercise 1: HTTP Basics (15 minutes)

### Task
Make a GET request to `https://httpbin.org/get` and explore the response object.

### Requirements
1. Make a GET request to the endpoint
2. Print the following information:
   - Status code
   - Content type header
   - The 'origin' field from the JSON response (your IP address)
3. Check if the request was successful using `response.ok`

### Starter Code

```python
import requests

def explore_response():
    """
    Make a request to httpbin.org and explore the response object.
    """
    url = "https://httpbin.org/get"

    # TODO: Make the GET request

    # TODO: Print status code

    # TODO: Print Content-Type header

    # TODO: Parse JSON and print the 'origin' field

    # TODO: Print whether request was successful (response.ok)

    pass


if __name__ == "__main__":
    explore_response()
```

### Expected Output
```
Status Code: 200
Content-Type: application/json
Your IP: 123.45.67.89
Request successful: True
```

---

## Exercise 2: Query Parameters (15 minutes)

### Task
Make a request to `https://httpbin.org/get` with custom query parameters and verify they were received correctly.

### Requirements
1. Send these query parameters:
   - `city`: "Taipei"
   - `country`: "Taiwan"
   - `limit`: 5
2. Parse the response and verify the 'args' field contains your parameters
3. Print each parameter from the response

### Starter Code

```python
import requests

def test_query_params():
    """
    Send query parameters and verify they were received.
    """
    url = "https://httpbin.org/get"

    # TODO: Define parameters dict
    params = {
        # Your parameters here
    }

    # TODO: Make request with params

    # TODO: Parse response and print the 'args' field

    # TODO: Verify each parameter was received correctly

    pass


if __name__ == "__main__":
    test_query_params()
```

### Expected Output
```
Sent parameters:
  city: Taipei
  country: Taiwan
  limit: 5

Received parameters (from API):
  city: Taipei
  country: Taiwan
  limit: 5

✓ All parameters received correctly!
```

---

## Exercise 3: Custom Headers (15 minutes)

### Task
Make a request with custom headers and verify they were sent correctly.

### Requirements
1. Send these headers:
   - `User-Agent`: "CS101-Lab/1.0 (your-email@example.com)"
   - `Accept`: "application/json"
   - `X-Custom-Header`: "Hello from Python!"
2. Use the endpoint `https://httpbin.org/headers`
3. Verify your headers appear in the response

### Starter Code

```python
import requests

def test_headers():
    """
    Send custom headers and verify they were received.
    """
    url = "https://httpbin.org/headers"

    # TODO: Define headers dict
    headers = {
        # Your headers here
    }

    # TODO: Make request with headers

    # TODO: Parse response and find your headers

    # TODO: Print each custom header from response

    pass


if __name__ == "__main__":
    test_headers()
```

### Expected Output
```
Headers sent and received:
  User-Agent: CS101-Lab/1.0 (your-email@example.com)
  Accept: application/json
  X-Custom-Header: Hello from Python!

✓ Custom headers working correctly!
```

---

## Exercise 4: First Nominatim Request (20 minutes)

### Task
Make your first request to the Nominatim API and parse the response.

### Requirements
1. Search for "National Taiwan University" using Nominatim
2. Include proper User-Agent header (REQUIRED!)
3. Request JSON format
4. Print the display name, latitude, and longitude
5. Handle the case where no results are found

### API Endpoint
```
https://nominatim.openstreetmap.org/search
```

### Query Parameters
- `q`: The search query
- `format`: "json"
- `limit`: 1

### Starter Code

```python
import requests

def geocode_place(place_name: str) -> dict | None:
    """
    Geocode a place name using Nominatim.

    Args:
        place_name: Name of the place to search

    Returns:
        Dict with display_name, lat, lon or None if not found
    """
    url = "https://nominatim.openstreetmap.org/search"

    # TODO: Define query parameters

    # TODO: Define headers with User-Agent (REQUIRED!)

    # TODO: Make the request with timeout

    # TODO: Check status code

    # TODO: Parse JSON and return result

    pass


if __name__ == "__main__":
    result = geocode_place("National Taiwan University")

    if result:
        print(f"Name: {result['display_name']}")
        print(f"Latitude: {result['lat']}")
        print(f"Longitude: {result['lon']}")
    else:
        print("Place not found!")
```

### Expected Output
```
Name: National Taiwan University, Roosevelt Road, Da'an District, Taipei, Taiwan
Latitude: 25.0173405
Longitude: 121.5397518
```

---

## Exercise 5: Error Handling (15 minutes)

### Task
Implement robust error handling for HTTP requests.

### Requirements
1. Handle these error cases:
   - Network timeout
   - Connection error
   - HTTP error status (4xx, 5xx)
2. Use try/except blocks
3. Print meaningful error messages

### Starter Code

```python
import requests

def safe_request(url: str, params: dict = None, headers: dict = None) -> dict | None:
    """
    Make an HTTP request with comprehensive error handling.

    Args:
        url: The URL to request
        params: Optional query parameters
        headers: Optional headers

    Returns:
        Parsed JSON response or None if failed
    """
    try:
        # TODO: Make request with 10 second timeout

        # TODO: Check status code and handle errors

        # TODO: Return parsed JSON

        pass

    except requests.exceptions.Timeout:
        # TODO: Handle timeout
        pass

    except requests.exceptions.ConnectionError:
        # TODO: Handle connection error
        pass

    except requests.exceptions.RequestException as e:
        # TODO: Handle other errors
        pass

    return None


def test_error_handling():
    """Test various error scenarios."""

    print("Test 1: Successful request")
    result = safe_request("https://httpbin.org/get")
    print(f"Result: {'Success' if result else 'Failed'}\n")

    print("Test 2: Timeout (using httpbin delay)")
    result = safe_request("https://httpbin.org/delay/15", headers={}, params={})
    print(f"Result: {'Success' if result else 'Failed'}\n")

    print("Test 3: 404 Not Found")
    result = safe_request("https://httpbin.org/status/404")
    print(f"Result: {'Success' if result else 'Failed'}\n")

    print("Test 4: Invalid URL")
    result = safe_request("https://invalid.domain.example.com/test")
    print(f"Result: {'Success' if result else 'Failed'}\n")


if __name__ == "__main__":
    test_error_handling()
```

### Expected Output
```
Test 1: Successful request
Result: Success

Test 2: Timeout (using httpbin delay)
Error: Request timed out
Result: Failed

Test 3: 404 Not Found
Error: HTTP 404 - Not Found
Result: Failed

Test 4: Invalid URL
Error: Connection failed - check URL or network
Result: Failed
```

---

## Exercise 6: Geocoder with Rate Limiting (20 minutes)

### Task
Build a complete geocoder that handles multiple places with proper rate limiting.

### Requirements
1. Geocode a list of at least 3 places
2. Implement rate limiting (1 request per second)
3. Handle errors gracefully
4. Return results as a list of dictionaries
5. Print progress as you go

### Starter Code

```python
import requests
import time

def geocode_multiple(places: list[str]) -> list[dict]:
    """
    Geocode multiple places with rate limiting.

    Args:
        places: List of place names to geocode

    Returns:
        List of dicts with name, lat, lon for successfully geocoded places
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {
        "User-Agent": "CS101-Lab/1.0 (your-email@example.com)"
    }

    results = []

    for i, place in enumerate(places):
        print(f"[{i+1}/{len(places)}] Geocoding: {place}...")

        # TODO: Implement rate limiting (wait 1 second between requests)

        # TODO: Make API request

        # TODO: Parse response and add to results

        # TODO: Handle errors

        pass

    return results


def main():
    # Test places
    places = [
        "Taipei 101",
        "National Palace Museum",
        "Jiufen Old Street",
        "Sun Moon Lake",
        "Taroko National Park"
    ]

    print("=== Geocoding Multiple Places ===\n")

    results = geocode_multiple(places)

    print(f"\n=== Results ({len(results)}/{len(places)} found) ===\n")

    for place in results:
        print(f"{place['name'][:50]}...")
        print(f"  Coordinates: ({place['lat']:.6f}, {place['lon']:.6f})\n")


if __name__ == "__main__":
    main()
```

### Expected Output
```
=== Geocoding Multiple Places ===

[1/5] Geocoding: Taipei 101...
  ✓ Found!
[2/5] Geocoding: National Palace Museum...
  ✓ Found!
[3/5] Geocoding: Jiufen Old Street...
  ✓ Found!
[4/5] Geocoding: Sun Moon Lake...
  ✓ Found!
[5/5] Geocoding: Taroko National Park...
  ✓ Found!

=== Results (5/5 found) ===

Taipei 101, 7, Section 5, Xinyi Road, Xinyi District...
  Coordinates: (25.033964, 121.564472)

National Palace Museum, Section 2, Zhishan Road, Sh...
  Coordinates: (25.102279, 121.548464)

...
```

---

## Bonus Challenge: Reverse Geocoder

### Task
Create a reverse geocoder that converts coordinates to addresses.

### Requirements
1. Use the Nominatim reverse endpoint: `/reverse`
2. Take latitude and longitude as input
3. Return the formatted address
4. Handle errors properly

### API Endpoint
```
https://nominatim.openstreetmap.org/reverse?lat=25.033&lon=121.564&format=json
```

### Starter Code

```python
import requests

def reverse_geocode(lat: float, lon: float) -> str | None:
    """
    Convert coordinates to an address.

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        Address string or None if not found
    """
    # TODO: Implement reverse geocoding
    pass


def main():
    # Famous Taipei locations
    locations = [
        (25.0339, 121.5645),  # Taipei 101
        (25.0478, 121.5170),  # Taipei Main Station
        (25.1023, 121.5485),  # National Palace Museum
    ]

    print("=== Reverse Geocoding ===\n")

    for lat, lon in locations:
        print(f"Coordinates: ({lat}, {lon})")
        address = reverse_geocode(lat, lon)
        if address:
            print(f"Address: {address[:80]}...\n")
        else:
            print("Address not found\n")


if __name__ == "__main__":
    main()
```

---

## Submission Checklist

Before submitting, verify:

- [ ] All exercises run without errors
- [ ] Proper User-Agent header included in all Nominatim requests
- [ ] Rate limiting implemented (1 request/second)
- [ ] Error handling covers timeout, connection, and HTTP errors
- [ ] Code is well-commented and readable

## Grading Rubric

| Exercise | Points | Criteria |
|----------|--------|----------|
| Exercise 1 | 10 | Correct response parsing |
| Exercise 2 | 10 | Parameters sent correctly |
| Exercise 3 | 10 | Headers sent correctly |
| Exercise 4 | 20 | Nominatim geocoding works |
| Exercise 5 | 20 | All errors handled properly |
| Exercise 6 | 30 | Rate limiting + multiple geocodes |
| Bonus | +10 | Reverse geocoding works |

**Total: 100 points (+10 bonus)**

---

## Common Issues & Solutions

### Issue: 403 Forbidden from Nominatim
**Solution:** You forgot the User-Agent header!
```python
headers = {"User-Agent": "MyApp/1.0 (email@example.com)"}
```

### Issue: Requests timing out
**Solution:** Always set a timeout
```python
response = requests.get(url, timeout=10)
```

### Issue: Getting rate limited (429)
**Solution:** Add delays between requests
```python
import time
time.sleep(1)  # Wait 1 second
```

### Issue: JSON parsing fails
**Solution:** Check status code first
```python
if response.status_code == 200:
    data = response.json()
```

---

*End of Week 4 Lab*
