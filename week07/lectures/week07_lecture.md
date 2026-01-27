# Week 7: The Smart City Navigator (Capstone Project)

**Phase 2: The API & The Cloud** — "Fetching the World"

---

## Overview

This is our capstone week! We'll combine everything we've learned to build a complete **Smart City Navigator** - a command-line application that helps users navigate between locations using real addresses, coordinates, and optimal routing.

### What We'll Build

A fully-functional navigation system that:
- Converts addresses to coordinates (Nominatim - Week 5)
- Calculates optimal routes (OSRM - Week 7)
- Handles multiple waypoints efficiently
- Provides clear, user-friendly output
- Handles errors gracefully
- Supports different transportation modes

### Learning Objectives

By the end of this lecture, you will be able to:
1. Design and implement a multi-component Python application
2. Integrate multiple external APIs into a cohesive system
3. Implement robust error handling strategies
4. Create user-friendly command-line interfaces
5. Apply software design patterns (separation of concerns)
6. Build testable, maintainable code

---

## Hour 1: System Architecture and Design (60 minutes)

### 1.1 Understanding System Design (20 minutes)

Before writing code, good programmers plan their systems. Let's think about what our Smart City Navigator needs to do.

#### The User's Perspective

Imagine a user wants to:
1. Enter a starting address: "Taipei 101"
2. Enter a destination: "Taipei Main Station"
3. Get directions with distance and time estimates

What happens behind the scenes?

```
User Input: "Taipei 101"
     ↓
[Geocoding Service] → Convert to coordinates (25.0330, 121.5654)
     ↓
[Routing Service] → Calculate route to destination
     ↓
[Formatting Service] → Present results to user
     ↓
User Output: "Distance: 5.2 km, Time: 12 minutes"
```

#### Separation of Concerns

**Key Principle**: Each part of our program should do ONE thing well.

```python
# BAD: Everything mixed together
def navigate(start, end):
    # Geocoding code...
    # Routing code...
    # Formatting code...
    # Error handling code...
    # 200 lines of tangled code!
    pass

# GOOD: Separate responsibilities
class GeocodingService:
    """Handles address → coordinates conversion"""
    pass

class RoutingService:
    """Handles route calculation"""
    pass

class Navigator:
    """Coordinates the services and handles user interaction"""
    pass
```

**Benefits of separation:**
- Easier to test each component
- Easier to fix bugs (they're isolated)
- Easier to replace components (swap Nominatim for Google Maps)
- Code is more readable

### 1.2 Designing the GeocodingService (20 minutes)

Let's design our first component. We need to convert addresses to coordinates.

#### Requirements

1. Accept an address string
2. Return coordinates (latitude, longitude)
3. Handle cases where address isn't found
4. Handle network errors
5. Respect API rate limits

#### Interface Design

```python
from typing import Optional, Tuple
from dataclasses import dataclass

@dataclass
class Location:
    """Represents a geographic location."""
    name: str
    latitude: float
    longitude: float
    display_name: str  # Full address from geocoder

    @property
    def coords(self) -> Tuple[float, float]:
        """Return (lat, lon) tuple."""
        return (self.latitude, self.longitude)

    def __str__(self) -> str:
        return f"{self.name} ({self.latitude:.4f}, {self.longitude:.4f})"


class GeocodingService:
    """Service for converting addresses to coordinates."""

    def __init__(self, user_agent: str = "SmartCityNavigator/1.0"):
        """
        Initialize the geocoding service.

        Args:
            user_agent: Identifier for API requests (required by Nominatim)
        """
        self.user_agent = user_agent
        self.base_url = "https://nominatim.openstreetmap.org/search"

    def geocode(self, address: str) -> Optional[Location]:
        """
        Convert an address to a Location.

        Args:
            address: The address or place name to geocode

        Returns:
            Location object if found, None otherwise
        """
        pass  # We'll implement this

    def reverse_geocode(self, lat: float, lon: float) -> Optional[Location]:
        """
        Convert coordinates to an address.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Location object if found, None otherwise
        """
        pass  # We'll implement this
```

#### Implementation

```python
import requests
import time
from typing import Optional

class GeocodingService:
    """Service for converting addresses to coordinates using Nominatim."""

    def __init__(self, user_agent: str = "SmartCityNavigator/1.0"):
        self.user_agent = user_agent
        self.base_url = "https://nominatim.openstreetmap.org"
        self._last_request_time = 0
        self._min_request_interval = 1.0  # Nominatim requires 1 second between requests

    def _wait_for_rate_limit(self):
        """Ensure we don't exceed API rate limits."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_request_interval:
            time.sleep(self._min_request_interval - elapsed)
        self._last_request_time = time.time()

    def _make_request(self, endpoint: str, params: dict) -> Optional[dict]:
        """Make a request to Nominatim with error handling."""
        self._wait_for_rate_limit()

        headers = {"User-Agent": self.user_agent}
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print("Error: Request timed out. Please try again.")
            return None
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to geocoding service.")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"Error: HTTP error occurred: {e}")
            return None
        except ValueError:  # JSON decode error
            print("Error: Invalid response from geocoding service.")
            return None

    def geocode(self, address: str) -> Optional[Location]:
        """Convert an address to coordinates."""
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }

        data = self._make_request("search", params)

        if not data or len(data) == 0:
            return None

        result = data[0]
        return Location(
            name=address,
            latitude=float(result["lat"]),
            longitude=float(result["lon"]),
            display_name=result.get("display_name", address)
        )

    def reverse_geocode(self, lat: float, lon: float) -> Optional[Location]:
        """Convert coordinates to an address."""
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json"
        }

        data = self._make_request("reverse", params)

        if not data or "error" in data:
            return None

        return Location(
            name=data.get("name", "Unknown"),
            latitude=float(data["lat"]),
            longitude=float(data["lon"]),
            display_name=data.get("display_name", "Unknown location")
        )
```

#### Understanding the Design

**Why use a class?**
- Encapsulates configuration (user_agent, base_url)
- Manages state (rate limiting with `_last_request_time`)
- Groups related functions together
- Easy to test and mock

**Why use `@dataclass` for Location?**
- Automatically generates `__init__`, `__repr__`, `__eq__`
- Clean, readable way to define data containers
- Supports type hints

### 1.3 Designing the RoutingService (20 minutes)

Now let's design the routing component using OSRM.

#### Requirements

1. Accept start and end coordinates
2. Return route information (distance, duration, path)
3. Support different travel profiles (driving, walking, cycling)
4. Handle multiple waypoints
5. Handle errors gracefully

#### Data Classes for Routes

```python
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

@dataclass
class RouteStep:
    """A single step in the route instructions."""
    instruction: str
    distance: float  # meters
    duration: float  # seconds

    @property
    def distance_km(self) -> float:
        return self.distance / 1000

    @property
    def duration_min(self) -> float:
        return self.duration / 60


@dataclass
class Route:
    """Represents a complete route between locations."""
    distance: float  # Total distance in meters
    duration: float  # Total duration in seconds
    geometry: List[Tuple[float, float]]  # List of (lat, lon) points
    steps: List[RouteStep] = field(default_factory=list)

    @property
    def distance_km(self) -> float:
        """Total distance in kilometers."""
        return self.distance / 1000

    @property
    def duration_min(self) -> float:
        """Total duration in minutes."""
        return self.duration / 60

    def summary(self) -> str:
        """Return a human-readable summary."""
        return f"{self.distance_km:.1f} km, ~{self.duration_min:.0f} minutes"
```

#### RoutingService Implementation

```python
class RoutingService:
    """Service for calculating routes using OSRM."""

    PROFILES = ["driving", "walking", "cycling"]

    def __init__(self, profile: str = "driving"):
        """
        Initialize the routing service.

        Args:
            profile: Travel mode - "driving", "walking", or "cycling"
        """
        if profile not in self.PROFILES:
            raise ValueError(f"Profile must be one of: {self.PROFILES}")

        self.profile = profile
        self.base_url = "https://router.project-osrm.org"

    def _format_coordinates(self, coords: List[Tuple[float, float]]) -> str:
        """
        Format coordinates for OSRM API.

        IMPORTANT: OSRM uses longitude,latitude order!
        """
        return ";".join(f"{lon},{lat}" for lat, lon in coords)

    def _parse_geometry(self, geometry: dict) -> List[Tuple[float, float]]:
        """Parse GeoJSON geometry to list of (lat, lon) tuples."""
        if geometry["type"] != "LineString":
            return []

        # GeoJSON uses [lon, lat], we convert to (lat, lon)
        return [(coord[1], coord[0]) for coord in geometry["coordinates"]]

    def _parse_steps(self, legs: List[dict]) -> List[RouteStep]:
        """Parse route steps from OSRM response."""
        steps = []
        for leg in legs:
            for step in leg.get("steps", []):
                maneuver = step.get("maneuver", {})
                instruction = maneuver.get("type", "continue")
                modifier = maneuver.get("modifier", "")

                # Build readable instruction
                if modifier:
                    instruction = f"{instruction} {modifier}"

                steps.append(RouteStep(
                    instruction=instruction.replace("_", " ").title(),
                    distance=step.get("distance", 0),
                    duration=step.get("duration", 0)
                ))
        return steps

    def get_route(self,
                  waypoints: List[Tuple[float, float]],
                  include_steps: bool = False) -> Optional[Route]:
        """
        Calculate a route through the given waypoints.

        Args:
            waypoints: List of (latitude, longitude) tuples
            include_steps: Whether to include turn-by-turn directions

        Returns:
            Route object if successful, None otherwise
        """
        if len(waypoints) < 2:
            print("Error: Need at least 2 waypoints for a route.")
            return None

        coords_str = self._format_coordinates(waypoints)

        # Use 'foot' for walking profile (OSRM naming)
        profile = "foot" if self.profile == "walking" else self.profile
        url = f"{self.base_url}/route/v1/{profile}/{coords_str}"

        params = {
            "overview": "full",
            "geometries": "geojson"
        }

        if include_steps:
            params["steps"] = "true"

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: Could not get route: {e}")
            return None
        except ValueError:
            print("Error: Invalid response from routing service.")
            return None

        if data.get("code") != "Ok":
            message = data.get("message", "Unknown error")
            print(f"Error: Routing failed - {message}")
            return None

        route_data = data["routes"][0]

        steps = []
        if include_steps:
            steps = self._parse_steps(route_data.get("legs", []))

        return Route(
            distance=route_data["distance"],
            duration=route_data["duration"],
            geometry=self._parse_geometry(route_data["geometry"]),
            steps=steps
        )
```

---

## Hour 2: Building the Navigator (60 minutes)

### 2.1 The Navigator Class (25 minutes)

Now we'll create the main Navigator class that coordinates our services.

#### Design Philosophy

The Navigator should:
- Accept user-friendly inputs (addresses OR coordinates)
- Coordinate between services
- Format output nicely
- Handle all errors gracefully

```python
from typing import Union, List, Optional
import re

class Navigator:
    """
    Smart City Navigator - combines geocoding and routing services.

    Usage:
        nav = Navigator()
        result = nav.navigate("Taipei 101", "Taipei Main Station")
        print(result)
    """

    def __init__(self, profile: str = "driving"):
        """
        Initialize the Navigator.

        Args:
            profile: Travel mode - "driving", "walking", or "cycling"
        """
        self.geocoder = GeocodingService(user_agent="SmartCityNavigator/1.0")
        self.router = RoutingService(profile=profile)
        self.profile = profile

    def _parse_location(self, location: str) -> Optional[Location]:
        """
        Parse a location string - could be coordinates or an address.

        Accepts:
            - Coordinates: "25.0330, 121.5654" or "(25.0330, 121.5654)"
            - Address: "Taipei 101"
        """
        # Try to parse as coordinates first
        coord_pattern = r'^\(?\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\)?$'
        match = re.match(coord_pattern, location.strip())

        if match:
            lat, lon = float(match.group(1)), float(match.group(2))

            # Validate coordinate ranges
            if not (-90 <= lat <= 90):
                print(f"Error: Invalid latitude {lat}. Must be between -90 and 90.")
                return None
            if not (-180 <= lon <= 180):
                print(f"Error: Invalid longitude {lon}. Must be between -180 and 180.")
                return None

            # Reverse geocode to get address
            location_obj = self.geocoder.reverse_geocode(lat, lon)
            if location_obj:
                return location_obj

            # If reverse geocoding fails, create a basic Location
            return Location(
                name=f"({lat}, {lon})",
                latitude=lat,
                longitude=lon,
                display_name=f"Coordinates: {lat}, {lon}"
            )

        # It's an address - geocode it
        return self.geocoder.geocode(location)

    def navigate(self,
                 start: str,
                 end: str,
                 show_steps: bool = False) -> Optional[dict]:
        """
        Get navigation from start to end.

        Args:
            start: Starting location (address or coordinates)
            end: Ending location (address or coordinates)
            show_steps: Whether to include turn-by-turn directions

        Returns:
            Dictionary with navigation results, or None if failed
        """
        print(f"\nPlanning {self.profile} route...")
        print(f"From: {start}")
        print(f"To:   {end}")
        print("-" * 40)

        # Geocode start location
        print("Finding start location...")
        start_loc = self._parse_location(start)
        if not start_loc:
            print(f"Error: Could not find location: {start}")
            return None
        print(f"  Found: {start_loc.display_name[:60]}...")

        # Geocode end location
        print("Finding destination...")
        end_loc = self._parse_location(end)
        if not end_loc:
            print(f"Error: Could not find location: {end}")
            return None
        print(f"  Found: {end_loc.display_name[:60]}...")

        # Get route
        print("Calculating route...")
        route = self.router.get_route(
            [start_loc.coords, end_loc.coords],
            include_steps=show_steps
        )

        if not route:
            print("Error: Could not calculate route.")
            return None

        return {
            "start": start_loc,
            "end": end_loc,
            "route": route,
            "profile": self.profile
        }

    def navigate_multi(self,
                       locations: List[str],
                       show_steps: bool = False) -> Optional[dict]:
        """
        Navigate through multiple waypoints.

        Args:
            locations: List of locations to visit in order
            show_steps: Whether to include turn-by-turn directions

        Returns:
            Dictionary with navigation results, or None if failed
        """
        if len(locations) < 2:
            print("Error: Need at least 2 locations for navigation.")
            return None

        print(f"\nPlanning {self.profile} route through {len(locations)} stops...")
        print("-" * 40)

        # Geocode all locations
        waypoints = []
        for i, loc_str in enumerate(locations):
            print(f"Finding stop {i + 1}: {loc_str[:30]}...")
            location = self._parse_location(loc_str)
            if not location:
                print(f"Error: Could not find location: {loc_str}")
                return None
            waypoints.append(location)
            print(f"  Found: {location.display_name[:50]}...")

        # Get route through all waypoints
        print("Calculating route...")
        coords = [wp.coords for wp in waypoints]
        route = self.router.get_route(coords, include_steps=show_steps)

        if not route:
            print("Error: Could not calculate route.")
            return None

        return {
            "waypoints": waypoints,
            "route": route,
            "profile": self.profile
        }
```

### 2.2 Formatting Output (20 minutes)

Good software isn't just functional - it's user-friendly. Let's create a formatter for our results.

```python
class NavigationFormatter:
    """Formats navigation results for display."""

    @staticmethod
    def format_duration(minutes: float) -> str:
        """Format duration in a human-readable way."""
        if minutes < 1:
            return "less than a minute"
        elif minutes < 60:
            return f"{minutes:.0f} minute{'s' if minutes != 1 else ''}"
        else:
            hours = int(minutes // 60)
            mins = int(minutes % 60)
            parts = []
            if hours > 0:
                parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
            if mins > 0:
                parts.append(f"{mins} minute{'s' if mins != 1 else ''}")
            return " ".join(parts)

    @staticmethod
    def format_distance(km: float) -> str:
        """Format distance in a human-readable way."""
        if km < 1:
            return f"{km * 1000:.0f} meters"
        else:
            return f"{km:.1f} km"

    @staticmethod
    def format_simple_result(result: dict) -> str:
        """Format a simple A-to-B navigation result."""
        if not result:
            return "No route found."

        route = result["route"]
        start = result["start"]
        end = result["end"]
        profile = result["profile"]

        lines = [
            "",
            "=" * 50,
            f"  {profile.upper()} DIRECTIONS",
            "=" * 50,
            "",
            f"From: {start.display_name}",
            f"To:   {end.display_name}",
            "",
            "-" * 50,
            f"Total Distance: {NavigationFormatter.format_distance(route.distance_km)}",
            f"Estimated Time: {NavigationFormatter.format_duration(route.duration_min)}",
            "-" * 50,
        ]

        # Add turn-by-turn if available
        if route.steps:
            lines.append("")
            lines.append("Turn-by-Turn Directions:")
            lines.append("")
            for i, step in enumerate(route.steps, 1):
                dist = NavigationFormatter.format_distance(step.distance_km)
                lines.append(f"  {i}. {step.instruction} ({dist})")

        lines.append("")
        lines.append("=" * 50)

        return "\n".join(lines)

    @staticmethod
    def format_multi_result(result: dict) -> str:
        """Format a multi-stop navigation result."""
        if not result:
            return "No route found."

        route = result["route"]
        waypoints = result["waypoints"]
        profile = result["profile"]

        lines = [
            "",
            "=" * 50,
            f"  {profile.upper()} ROUTE - {len(waypoints)} STOPS",
            "=" * 50,
            "",
        ]

        # List all stops
        lines.append("Stops:")
        for i, wp in enumerate(waypoints, 1):
            marker = "Start" if i == 1 else ("End" if i == len(waypoints) else f"Stop {i}")
            lines.append(f"  {marker}: {wp.name}")

        lines.extend([
            "",
            "-" * 50,
            f"Total Distance: {NavigationFormatter.format_distance(route.distance_km)}",
            f"Estimated Time: {NavigationFormatter.format_duration(route.duration_min)}",
            "-" * 50,
            "",
            "=" * 50,
        ])

        return "\n".join(lines)
```

### 2.3 Error Handling Strategies (15 minutes)

Robust applications handle errors gracefully. Let's look at different strategies.

#### Strategy 1: Return None on Error

```python
def geocode(self, address: str) -> Optional[Location]:
    """Returns None if geocoding fails."""
    try:
        # ... API call ...
        return location
    except Exception:
        return None

# Usage
location = geocoder.geocode("Invalid Address xyz123")
if location is None:
    print("Location not found")
```

**Pros**: Simple, caller decides what to do
**Cons**: No information about what went wrong

#### Strategy 2: Raise Custom Exceptions

```python
class GeocodingError(Exception):
    """Base exception for geocoding errors."""
    pass

class LocationNotFoundError(GeocodingError):
    """Raised when a location cannot be found."""
    pass

class RateLimitError(GeocodingError):
    """Raised when API rate limit is exceeded."""
    pass

def geocode(self, address: str) -> Location:
    """Raises exception if geocoding fails."""
    # ... API call ...
    if response.status_code == 429:
        raise RateLimitError("Too many requests. Please wait.")
    if not results:
        raise LocationNotFoundError(f"Could not find: {address}")
    return location

# Usage
try:
    location = geocoder.geocode(address)
except LocationNotFoundError:
    print("Sorry, couldn't find that location.")
except RateLimitError:
    print("Too many requests. Waiting...")
    time.sleep(60)
```

**Pros**: Detailed error information, forces caller to handle errors
**Cons**: More complex, need to define exception hierarchy

#### Strategy 3: Result Objects

```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Union

T = TypeVar('T')

@dataclass
class Result(Generic[T]):
    """Represents either a success or failure."""
    success: bool
    value: Optional[T] = None
    error: Optional[str] = None

    @classmethod
    def ok(cls, value: T) -> 'Result[T]':
        return cls(success=True, value=value)

    @classmethod
    def fail(cls, error: str) -> 'Result[T]':
        return cls(success=False, error=error)

def geocode(self, address: str) -> Result[Location]:
    """Returns a Result object."""
    try:
        # ... API call ...
        return Result.ok(location)
    except Exception as e:
        return Result.fail(str(e))

# Usage
result = geocoder.geocode(address)
if result.success:
    print(f"Found: {result.value}")
else:
    print(f"Error: {result.error}")
```

**Pros**: Explicit success/failure, includes error info, no exceptions
**Cons**: More verbose, need to always check success

---

## Hour 3: Complete Application and Testing (60 minutes)

### 3.1 Building the CLI Application (25 minutes)

Let's create a complete command-line interface for our navigator.

```python
#!/usr/bin/env python3
"""
Smart City Navigator - A command-line navigation tool.

Usage:
    python navigator.py                    # Interactive mode
    python navigator.py -s "Start" -e "End"  # Direct navigation
    python navigator.py --multi "A" "B" "C"  # Multi-stop route
"""

import argparse
import sys


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Smart City Navigator - Navigate between locations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -s "Taipei 101" -e "Taipei Main Station"
  %(prog)s -s "25.0330, 121.5654" -e "National Palace Museum"
  %(prog)s --multi "Taipei 101" "Shilin Night Market" "Taipei Zoo"
  %(prog)s -s "Central Park" -e "Times Square" -p walking --steps
        """
    )

    # Navigation mode
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )

    # Direct navigation
    parser.add_argument(
        "-s", "--start",
        type=str,
        help="Starting location (address or coordinates)"
    )
    parser.add_argument(
        "-e", "--end",
        type=str,
        help="Destination (address or coordinates)"
    )

    # Multi-stop
    parser.add_argument(
        "--multi",
        nargs="+",
        metavar="STOP",
        help="Multiple stops for a route"
    )

    # Options
    parser.add_argument(
        "-p", "--profile",
        choices=["driving", "walking", "cycling"],
        default="driving",
        help="Travel mode (default: driving)"
    )
    parser.add_argument(
        "--steps",
        action="store_true",
        help="Include turn-by-turn directions"
    )

    return parser


def interactive_mode(navigator: Navigator, formatter: NavigationFormatter):
    """Run the navigator in interactive mode."""
    print("\n" + "=" * 50)
    print("  SMART CITY NAVIGATOR")
    print("  Type 'quit' to exit, 'help' for commands")
    print("=" * 50 + "\n")

    while True:
        try:
            print("\nOptions:")
            print("  1. Navigate between two locations")
            print("  2. Multi-stop route")
            print("  3. Change travel mode (current: {})".format(navigator.profile))
            print("  4. Quit")

            choice = input("\nEnter choice (1-4): ").strip()

            if choice == "1":
                start = input("Enter starting location: ").strip()
                if not start:
                    print("Start location is required.")
                    continue

                end = input("Enter destination: ").strip()
                if not end:
                    print("Destination is required.")
                    continue

                show_steps = input("Show turn-by-turn? (y/n): ").strip().lower() == 'y'

                result = navigator.navigate(start, end, show_steps=show_steps)
                if result:
                    print(formatter.format_simple_result(result))

            elif choice == "2":
                print("Enter locations one per line (empty line when done):")
                stops = []
                while True:
                    stop = input(f"  Stop {len(stops) + 1}: ").strip()
                    if not stop:
                        break
                    stops.append(stop)

                if len(stops) < 2:
                    print("Need at least 2 stops.")
                    continue

                result = navigator.navigate_multi(stops)
                if result:
                    print(formatter.format_multi_result(result))

            elif choice == "3":
                print("Travel modes: driving, walking, cycling")
                mode = input("Enter mode: ").strip().lower()
                if mode in ["driving", "walking", "cycling"]:
                    navigator = Navigator(profile=mode)
                    print(f"Changed to {mode} mode.")
                else:
                    print("Invalid mode.")

            elif choice == "4" or choice.lower() == "quit":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please enter 1-4.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    navigator = Navigator(profile=args.profile)
    formatter = NavigationFormatter()

    # Determine mode
    if args.interactive:
        interactive_mode(navigator, formatter)

    elif args.multi:
        if len(args.multi) < 2:
            print("Error: Need at least 2 stops for multi-stop route.")
            sys.exit(1)

        result = navigator.navigate_multi(args.multi, show_steps=args.steps)
        if result:
            print(formatter.format_multi_result(result))
        else:
            sys.exit(1)

    elif args.start and args.end:
        result = navigator.navigate(args.start, args.end, show_steps=args.steps)
        if result:
            print(formatter.format_simple_result(result))
        else:
            sys.exit(1)

    else:
        # Default to interactive mode
        interactive_mode(navigator, formatter)


if __name__ == "__main__":
    main()
```

### 3.2 Adding Caching (15 minutes)

API calls are slow. Let's add caching to speed up repeated lookups.

```python
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Any


class SimpleCache:
    """A simple file-based cache for API responses."""

    def __init__(self, cache_dir: str = ".navigator_cache", ttl_hours: int = 24):
        """
        Initialize the cache.

        Args:
            cache_dir: Directory to store cache files
            ttl_hours: Time-to-live in hours for cached entries
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)

    def _get_key(self, *args) -> str:
        """Generate a cache key from arguments."""
        key_string = json.dumps(args, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()

    def _get_path(self, key: str) -> Path:
        """Get the file path for a cache key."""
        return self.cache_dir / f"{key}.json"

    def get(self, *args) -> Optional[Any]:
        """
        Get a cached value.

        Returns:
            Cached value if exists and not expired, None otherwise
        """
        key = self._get_key(*args)
        path = self._get_path(key)

        if not path.exists():
            return None

        try:
            with open(path, 'r') as f:
                data = json.load(f)

            # Check if expired
            cached_time = datetime.fromisoformat(data["timestamp"])
            if datetime.now() - cached_time > self.ttl:
                path.unlink()  # Delete expired cache
                return None

            return data["value"]
        except (json.JSONDecodeError, KeyError, ValueError):
            return None

    def set(self, value: Any, *args):
        """Cache a value."""
        key = self._get_key(*args)
        path = self._get_path(key)

        data = {
            "timestamp": datetime.now().isoformat(),
            "value": value
        }

        with open(path, 'w') as f:
            json.dump(data, f)

    def clear(self):
        """Clear all cached entries."""
        for path in self.cache_dir.glob("*.json"):
            path.unlink()


class CachedGeocodingService(GeocodingService):
    """Geocoding service with caching."""

    def __init__(self, user_agent: str = "SmartCityNavigator/1.0"):
        super().__init__(user_agent)
        self.cache = SimpleCache(cache_dir=".geocode_cache")

    def geocode(self, address: str) -> Optional[Location]:
        """Geocode with caching."""
        # Check cache first
        cached = self.cache.get("geocode", address)
        if cached:
            return Location(**cached)

        # Call API
        result = super().geocode(address)

        # Cache the result
        if result:
            self.cache.set({
                "name": result.name,
                "latitude": result.latitude,
                "longitude": result.longitude,
                "display_name": result.display_name
            }, "geocode", address)

        return result
```

### 3.3 Testing Your Application (20 minutes)

Good code needs good tests. Let's write tests for our navigator.

#### Unit Tests

```python
import unittest
from unittest.mock import Mock, patch

class TestLocation(unittest.TestCase):
    """Tests for the Location dataclass."""

    def test_coords_property(self):
        """Test that coords returns (lat, lon) tuple."""
        loc = Location(
            name="Test",
            latitude=25.0330,
            longitude=121.5654,
            display_name="Test Location"
        )
        self.assertEqual(loc.coords, (25.0330, 121.5654))

    def test_str_representation(self):
        """Test string representation."""
        loc = Location(
            name="Test",
            latitude=25.0330,
            longitude=121.5654,
            display_name="Test Location"
        )
        self.assertIn("25.0330", str(loc))
        self.assertIn("121.5654", str(loc))


class TestRoute(unittest.TestCase):
    """Tests for the Route dataclass."""

    def test_distance_km(self):
        """Test distance conversion to kilometers."""
        route = Route(distance=5000, duration=600, geometry=[])
        self.assertEqual(route.distance_km, 5.0)

    def test_duration_min(self):
        """Test duration conversion to minutes."""
        route = Route(distance=5000, duration=600, geometry=[])
        self.assertEqual(route.duration_min, 10.0)

    def test_summary(self):
        """Test summary string."""
        route = Route(distance=5000, duration=600, geometry=[])
        summary = route.summary()
        self.assertIn("5.0 km", summary)
        self.assertIn("10 minutes", summary)


class TestNavigator(unittest.TestCase):
    """Tests for the Navigator class."""

    def test_parse_coordinates(self):
        """Test parsing coordinate strings."""
        nav = Navigator()

        # Mock the reverse_geocode to avoid API calls
        nav.geocoder.reverse_geocode = Mock(return_value=Location(
            name="Test",
            latitude=25.0330,
            longitude=121.5654,
            display_name="Test"
        ))

        # Test various coordinate formats
        result = nav._parse_location("25.0330, 121.5654")
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.latitude, 25.0330)

        result = nav._parse_location("(25.0330, 121.5654)")
        self.assertIsNotNone(result)

    def test_parse_invalid_coordinates(self):
        """Test parsing invalid coordinates."""
        nav = Navigator()

        # Invalid latitude (> 90)
        result = nav._parse_location("95.0, 121.0")
        self.assertIsNone(result)

        # Invalid longitude (> 180)
        result = nav._parse_location("25.0, 200.0")
        self.assertIsNone(result)


class TestNavigationFormatter(unittest.TestCase):
    """Tests for the NavigationFormatter class."""

    def test_format_duration_minutes(self):
        """Test duration formatting for minutes."""
        self.assertEqual(
            NavigationFormatter.format_duration(5),
            "5 minutes"
        )
        self.assertEqual(
            NavigationFormatter.format_duration(1),
            "1 minute"
        )

    def test_format_duration_hours(self):
        """Test duration formatting for hours."""
        result = NavigationFormatter.format_duration(90)
        self.assertIn("1 hour", result)
        self.assertIn("30 minutes", result)

    def test_format_distance_meters(self):
        """Test distance formatting for short distances."""
        self.assertEqual(
            NavigationFormatter.format_distance(0.5),
            "500 meters"
        )

    def test_format_distance_km(self):
        """Test distance formatting for longer distances."""
        self.assertEqual(
            NavigationFormatter.format_distance(5.5),
            "5.5 km"
        )


if __name__ == "__main__":
    unittest.main()
```

#### Integration Tests (with real API calls)

```python
import unittest
import os

@unittest.skipIf(
    os.environ.get("SKIP_INTEGRATION_TESTS"),
    "Skipping integration tests"
)
class TestIntegration(unittest.TestCase):
    """Integration tests that make real API calls."""

    def test_full_navigation_flow(self):
        """Test complete navigation from address to route."""
        nav = Navigator(profile="driving")

        result = nav.navigate(
            "Taipei 101, Taiwan",
            "Taipei Main Station, Taiwan"
        )

        self.assertIsNotNone(result)
        self.assertIn("start", result)
        self.assertIn("end", result)
        self.assertIn("route", result)

        # Verify route has reasonable values
        route = result["route"]
        self.assertGreater(route.distance_km, 0)
        self.assertGreater(route.duration_min, 0)

    def test_multi_stop_navigation(self):
        """Test multi-stop route planning."""
        nav = Navigator(profile="walking")

        result = nav.navigate_multi([
            "Taipei 101",
            "Taipei City Hall",
            "Sun Yat-sen Memorial Hall"
        ])

        self.assertIsNotNone(result)
        self.assertEqual(len(result["waypoints"]), 3)


if __name__ == "__main__":
    unittest.main()
```

---

## Complete Code Summary

Here's the structure of our complete Smart City Navigator:

```
smart_navigator/
├── __init__.py
├── models.py          # Location, Route, RouteStep dataclasses
├── services/
│   ├── __init__.py
│   ├── geocoding.py   # GeocodingService
│   └── routing.py     # RoutingService
├── cache.py           # SimpleCache
├── navigator.py       # Navigator class
├── formatter.py       # NavigationFormatter
├── cli.py             # Command-line interface
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    └── test_navigator.py
```

---

## Key Takeaways

### 1. System Design Principles

- **Separation of Concerns**: Each class has one responsibility
- **Dependency Injection**: Navigator receives services, doesn't create them
- **Interface Design**: Think about how classes will be used before implementing

### 2. API Integration Best Practices

- Always handle errors gracefully
- Respect rate limits
- Cache responses when possible
- Use timeouts to prevent hanging

### 3. User Experience

- Provide clear, helpful error messages
- Format output for readability
- Support multiple input formats
- Include help and documentation

### 4. Code Quality

- Write tests for critical functionality
- Use type hints for clarity
- Document public interfaces
- Keep functions small and focused

---

## Challenge Exercises

### Challenge 1: Offline Mode
Implement an offline mode that works with cached data only.

### Challenge 2: Route Comparison
Add a feature to compare routes with different profiles (driving vs walking).

### Challenge 3: ETA Calculation
Add departure time support and calculate estimated arrival time.

### Challenge 4: Route Export
Export routes to various formats (GPX, KML) for use with GPS devices.

---

## References

- [OSRM API Documentation](http://project-osrm.org/docs/v5.24.0/api/)
- [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/)
- [Python argparse Tutorial](https://docs.python.org/3/library/argparse.html)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [GeoJSON Specification](https://geojson.org/)

---

## Next Steps

Congratulations! You've built a complete navigation application. In future weeks, you could extend this with:
- Web interface using Flask
- Database storage for routes
- User accounts and saved locations
- Real-time traffic data integration
