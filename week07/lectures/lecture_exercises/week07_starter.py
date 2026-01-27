#!/usr/bin/env python3
"""
Week 7 Lab: Smart City Navigator - Starter Code

Complete the TODO sections to build a fully functional navigation system
that combines geocoding and routing services.

Usage:
    python week07_starter.py --test       # Run tests
    python week07_starter.py -i           # Interactive mode
    python week07_starter.py -s "Start" -e "End"  # Direct navigation
"""

import argparse
import requests
import time
import re
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Any


# =============================================================================
# EXERCISE 1: Location Data Model
# =============================================================================

@dataclass
class Location:
    """
    Represents a geographic location.

    Attributes:
        name: Short name of the location
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        display_name: Full address from geocoder
    """
    # TODO: Define the four fields: name, latitude, longitude, display_name
    name: str
    latitude: float
    longitude: float
    display_name: str

    @property
    def coords(self) -> Tuple[float, float]:
        """Return (lat, lon) tuple."""
        # TODO: Return a tuple of (latitude, longitude)
        return (self.latitude, self.longitude)

    def __str__(self) -> str:
        """Return readable string representation."""
        # TODO: Return string like "Name (lat, lon)" with 4 decimal places
        return f"{self.name} ({self.latitude:.4f}, {self.longitude:.4f})"


# =============================================================================
# EXERCISE 2: Route Data Model
# =============================================================================

@dataclass
class RouteStep:
    """A single step in the route instructions."""
    instruction: str
    distance: float  # meters
    duration: float  # seconds

    @property
    def distance_km(self) -> float:
        """Distance in kilometers."""
        return self.distance / 1000

    @property
    def duration_min(self) -> float:
        """Duration in minutes."""
        return self.duration / 60


@dataclass
class Route:
    """
    Represents a complete route between locations.

    Attributes:
        distance: Total distance in meters
        duration: Total duration in seconds
        geometry: List of (lat, lon) coordinate tuples
        steps: List of RouteStep objects (optional)
    """
    # TODO: Define the fields
    distance: float
    duration: float
    geometry: List[Tuple[float, float]]
    steps: List[RouteStep] = field(default_factory=list)

    @property
    def distance_km(self) -> float:
        """Total distance in kilometers."""
        # TODO: Convert meters to kilometers
        return self.distance / 1000

    @property
    def duration_min(self) -> float:
        """Total duration in minutes."""
        # TODO: Convert seconds to minutes
        return self.duration / 60

    def summary(self) -> str:
        """Return a human-readable summary."""
        # TODO: Return string like "5.2 km, ~12 minutes"
        return f"{self.distance_km:.1f} km, ~{self.duration_min:.0f} minutes"


# =============================================================================
# EXERCISE 3: Geocoding Service
# =============================================================================

class GeocodingService:
    """
    Service for converting addresses to coordinates using Nominatim.

    Attributes:
        user_agent: Identifier for API requests (required by Nominatim)
        base_url: Nominatim API base URL
    """

    def __init__(self, user_agent: str = "SmartCityNavigator/1.0"):
        """Initialize the geocoding service."""
        self.user_agent = user_agent
        self.base_url = "https://nominatim.openstreetmap.org"
        # TODO: Add instance variables for rate limiting
        self._last_request_time = 0
        self._min_request_interval = 1.0  # Nominatim requires 1 second

    def _wait_for_rate_limit(self):
        """Ensure we don't exceed API rate limits."""
        # TODO: Calculate time since last request
        # TODO: If less than 1 second, sleep for the remaining time
        # TODO: Update last request time
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_request_interval:
            time.sleep(self._min_request_interval - elapsed)
        self._last_request_time = time.time()

    def geocode(self, address: str) -> Optional[Location]:
        """
        Convert an address to coordinates.

        Args:
            address: The address or place name to geocode

        Returns:
            Location object if found, None otherwise
        """
        # TODO: Wait for rate limit
        self._wait_for_rate_limit()

        # TODO: Build request parameters
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }

        # TODO: Make request with error handling
        headers = {"User-Agent": self.user_agent}

        try:
            response = requests.get(
                f"{self.base_url}/search",
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.Timeout:
            print("Error: Request timed out.")
            return None
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to geocoding service.")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"Error: HTTP error occurred: {e}")
            return None
        except ValueError:
            print("Error: Invalid response from geocoding service.")
            return None

        # TODO: Check if results were found
        if not data or len(data) == 0:
            return None

        # TODO: Create and return Location object
        result = data[0]
        return Location(
            name=address,
            latitude=float(result["lat"]),
            longitude=float(result["lon"]),
            display_name=result.get("display_name", address)
        )

    def reverse_geocode(self, lat: float, lon: float) -> Optional[Location]:
        """
        Convert coordinates to an address.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Location object if found, None otherwise
        """
        # TODO: Wait for rate limit
        self._wait_for_rate_limit()

        # TODO: Build request parameters
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json"
        }

        # TODO: Make request with error handling
        headers = {"User-Agent": self.user_agent}

        try:
            response = requests.get(
                f"{self.base_url}/reverse",
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException:
            return None
        except ValueError:
            return None

        # TODO: Check for errors
        if not data or "error" in data:
            return None

        # TODO: Create and return Location object
        return Location(
            name=data.get("name", "Unknown"),
            latitude=float(data["lat"]),
            longitude=float(data["lon"]),
            display_name=data.get("display_name", "Unknown location")
        )


# =============================================================================
# EXERCISE 4: Routing Service
# =============================================================================

class RoutingService:
    """
    Service for calculating routes using OSRM.

    Attributes:
        profile: Travel mode (driving, walking, cycling)
        base_url: OSRM API base URL
    """

    PROFILES = ["driving", "walking", "cycling"]

    def __init__(self, profile: str = "driving"):
        """
        Initialize the routing service.

        Args:
            profile: Travel mode - "driving", "walking", or "cycling"
        """
        # TODO: Validate profile is in PROFILES list
        if profile not in self.PROFILES:
            raise ValueError(f"Profile must be one of: {self.PROFILES}")

        self.profile = profile
        self.base_url = "https://router.project-osrm.org"

    def _format_coordinates(self, coords: List[Tuple[float, float]]) -> str:
        """
        Format coordinates for OSRM API.

        IMPORTANT: OSRM uses longitude,latitude order (not lat,lon)!

        Args:
            coords: List of (latitude, longitude) tuples

        Returns:
            String formatted as "lon1,lat1;lon2,lat2;..."
        """
        # TODO: Format each coordinate as "lon,lat" (note the order!)
        # TODO: Join with semicolons
        return ";".join(f"{lon},{lat}" for lat, lon in coords)

    def _parse_geometry(self, geometry: dict) -> List[Tuple[float, float]]:
        """
        Parse GeoJSON geometry to list of (lat, lon) tuples.

        Args:
            geometry: GeoJSON geometry object

        Returns:
            List of (latitude, longitude) tuples
        """
        # TODO: Check that geometry type is "LineString"
        if geometry.get("type") != "LineString":
            return []

        # TODO: Extract coordinates and convert from [lon,lat] to (lat,lon)
        return [(coord[1], coord[0]) for coord in geometry.get("coordinates", [])]

    def _parse_steps(self, legs: List[dict]) -> List[RouteStep]:
        """Parse route steps from OSRM response."""
        steps = []
        for leg in legs:
            for step in leg.get("steps", []):
                maneuver = step.get("maneuver", {})
                instruction = maneuver.get("type", "continue")
                modifier = maneuver.get("modifier", "")

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
        # TODO: Validate we have at least 2 waypoints
        if len(waypoints) < 2:
            print("Error: Need at least 2 waypoints for a route.")
            return None

        # TODO: Format coordinates for OSRM
        coords_str = self._format_coordinates(waypoints)

        # TODO: Build URL (use "foot" for walking profile)
        profile = "foot" if self.profile == "walking" else self.profile
        url = f"{self.base_url}/route/v1/{profile}/{coords_str}"

        # TODO: Build request parameters
        params = {
            "overview": "full",
            "geometries": "geojson"
        }
        if include_steps:
            params["steps"] = "true"

        # TODO: Make request with error handling
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

        # TODO: Check response code
        if data.get("code") != "Ok":
            message = data.get("message", "Unknown error")
            print(f"Error: Routing failed - {message}")
            return None

        # TODO: Extract route data and create Route object
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


# =============================================================================
# EXERCISE 5: Navigator Class
# =============================================================================

class Navigator:
    """
    Smart City Navigator - combines geocoding and routing services.

    This class coordinates between the geocoding and routing services
    to provide complete navigation functionality.
    """

    def __init__(self, profile: str = "driving"):
        """
        Initialize the Navigator.

        Args:
            profile: Travel mode - "driving", "walking", or "cycling"
        """
        # TODO: Create GeocodingService and RoutingService instances
        self.geocoder = GeocodingService(user_agent="SmartCityNavigator/1.0")
        self.router = RoutingService(profile=profile)
        self.profile = profile

    def _parse_location(self, location: str) -> Optional[Location]:
        """
        Parse a location string - could be coordinates or an address.

        Accepts:
            - Coordinates: "25.0330, 121.5654" or "(25.0330, 121.5654)"
            - Address: "Taipei 101"

        Args:
            location: Location string to parse

        Returns:
            Location object if successful, None otherwise
        """
        # TODO: Define regex pattern for coordinates
        coord_pattern = r'^\(?\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\)?$'
        match = re.match(coord_pattern, location.strip())

        if match:
            # TODO: Extract lat and lon from match groups
            lat, lon = float(match.group(1)), float(match.group(2))

            # TODO: Validate coordinate ranges
            if not (-90 <= lat <= 90):
                print(f"Error: Invalid latitude {lat}. Must be between -90 and 90.")
                return None
            if not (-180 <= lon <= 180):
                print(f"Error: Invalid longitude {lon}. Must be between -180 and 180.")
                return None

            # TODO: Try to reverse geocode for a better name
            location_obj = self.geocoder.reverse_geocode(lat, lon)
            if location_obj:
                return location_obj

            # If reverse geocoding fails, create basic Location
            return Location(
                name=f"({lat}, {lon})",
                latitude=lat,
                longitude=lon,
                display_name=f"Coordinates: {lat}, {lon}"
            )

        # TODO: It's an address - geocode it
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

        # TODO: Parse and geocode start location
        print("Finding start location...")
        start_loc = self._parse_location(start)
        if not start_loc:
            print(f"Error: Could not find location: {start}")
            return None
        print(f"  Found: {start_loc.display_name[:60]}...")

        # TODO: Parse and geocode end location
        print("Finding destination...")
        end_loc = self._parse_location(end)
        if not end_loc:
            print(f"Error: Could not find location: {end}")
            return None
        print(f"  Found: {end_loc.display_name[:60]}...")

        # TODO: Get route between locations
        print("Calculating route...")
        route = self.router.get_route(
            [start_loc.coords, end_loc.coords],
            include_steps=show_steps
        )

        if not route:
            print("Error: Could not calculate route.")
            return None

        # TODO: Return result dictionary
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
        # TODO: Validate we have at least 2 locations
        if len(locations) < 2:
            print("Error: Need at least 2 locations for navigation.")
            return None

        print(f"\nPlanning {self.profile} route through {len(locations)} stops...")
        print("-" * 40)

        # TODO: Geocode all locations
        waypoints = []
        for i, loc_str in enumerate(locations):
            print(f"Finding stop {i + 1}: {loc_str[:30]}...")
            location = self._parse_location(loc_str)
            if not location:
                print(f"Error: Could not find location: {loc_str}")
                return None
            waypoints.append(location)
            print(f"  Found: {location.display_name[:50]}...")

        # TODO: Get route through all waypoints
        print("Calculating route...")
        coords = [wp.coords for wp in waypoints]
        route = self.router.get_route(coords, include_steps=show_steps)

        if not route:
            print("Error: Could not calculate route.")
            return None

        # TODO: Return result dictionary
        return {
            "waypoints": waypoints,
            "route": route,
            "profile": self.profile
        }


# =============================================================================
# EXERCISE 6: Navigation Formatter and CLI
# =============================================================================

class NavigationFormatter:
    """Formats navigation results for display."""

    @staticmethod
    def format_duration(minutes: float) -> str:
        """Format duration in a human-readable way."""
        if minutes < 1:
            return "less than a minute"
        elif minutes < 60:
            return f"{minutes:.0f} minute{'s' if minutes >= 2 else ''}"
        else:
            hours = int(minutes // 60)
            mins = int(minutes % 60)
            parts = []
            if hours > 0:
                parts.append(f"{hours} hour{'s' if hours >= 2 else ''}")
            if mins > 0:
                parts.append(f"{mins} minute{'s' if mins >= 2 else ''}")
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
            "Stops:",
        ]

        for i, wp in enumerate(waypoints, 1):
            if i == 1:
                marker = "Start"
            elif i == len(waypoints):
                marker = "End"
            else:
                marker = f"Stop {i}"
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
  %(prog)s --test
        """
    )

    # Mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    mode_group.add_argument(
        "--test",
        action="store_true",
        help="Run tests"
    )

    # Navigation arguments
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
    print("  Type 'quit' to exit")
    print("=" * 50 + "\n")

    while True:
        try:
            print("\nOptions:")
            print(f"  1. Navigate between two locations")
            print(f"  2. Multi-stop route")
            print(f"  3. Change travel mode (current: {navigator.profile})")
            print(f"  4. Quit")

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


# =============================================================================
# BONUS: Simple Cache (Optional)
# =============================================================================

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

            cached_time = datetime.fromisoformat(data["timestamp"])
            if datetime.now() - cached_time > self.ttl:
                path.unlink()
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


# =============================================================================
# TESTS
# =============================================================================

def run_tests():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("  RUNNING TESTS")
    print("=" * 50)

    passed = 0
    failed = 0

    # Test 1: Location dataclass
    print("\nTest 1: Location dataclass")
    try:
        loc = Location("Test", 25.0330, 121.5654, "Test Location")
        assert loc.coords == (25.0330, 121.5654), "coords property failed"
        assert "25.0330" in str(loc), "str representation failed"
        print("  PASSED")
        passed += 1
    except AssertionError as e:
        print(f"  FAILED: {e}")
        failed += 1

    # Test 2: Route dataclass
    print("\nTest 2: Route dataclass")
    try:
        route = Route(distance=5000, duration=600, geometry=[])
        assert route.distance_km == 5.0, "distance_km failed"
        assert route.duration_min == 10.0, "duration_min failed"
        assert "5.0 km" in route.summary(), "summary failed"
        print("  PASSED")
        passed += 1
    except AssertionError as e:
        print(f"  FAILED: {e}")
        failed += 1

    # Test 3: RouteStep
    print("\nTest 3: RouteStep dataclass")
    try:
        step = RouteStep("Turn Right", 1500, 180)
        assert step.distance_km == 1.5, "distance_km failed"
        assert step.duration_min == 3.0, "duration_min failed"
        print("  PASSED")
        passed += 1
    except AssertionError as e:
        print(f"  FAILED: {e}")
        failed += 1

    # Test 4: RoutingService coordinate formatting
    print("\nTest 4: RoutingService coordinate formatting")
    try:
        router = RoutingService()
        coords = [(25.0330, 121.5654), (25.0478, 121.5170)]
        result = router._format_coordinates(coords)
        # Should be lon,lat order (Python may drop trailing zeros)
        assert "121.5654,25.033" in result, "Coordinate order wrong"
        assert "121.517,25.0478" in result, "Second coordinate wrong"
        print("  PASSED")
        passed += 1
    except AssertionError as e:
        print(f"  FAILED: {e}")
        failed += 1

    # Test 5: RoutingService geometry parsing
    print("\nTest 5: RoutingService geometry parsing")
    try:
        router = RoutingService()
        geometry = {
            "type": "LineString",
            "coordinates": [[121.5654, 25.0330], [121.5170, 25.0478]]
        }
        result = router._parse_geometry(geometry)
        # Should convert to (lat, lon) order
        assert result[0] == (25.0330, 121.5654), "First point wrong"
        assert result[1] == (25.0478, 121.5170), "Second point wrong"
        print("  PASSED")
        passed += 1
    except AssertionError as e:
        print(f"  FAILED: {e}")
        failed += 1

    # Test 6: RoutingService invalid profile
    print("\nTest 6: RoutingService invalid profile")
    try:
        try:
            router = RoutingService(profile="flying")
            print("  FAILED: Should have raised ValueError")
            failed += 1
        except ValueError:
            print("  PASSED")
            passed += 1
    except Exception as e:
        print(f"  FAILED: {e}")
        failed += 1

    # Test 7: Navigator coordinate parsing
    print("\nTest 7: Navigator coordinate parsing")
    try:
        nav = Navigator()
        # Test coordinate pattern matching
        pattern = r'^\(?\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\)?$'

        test_cases = [
            ("25.0330, 121.5654", True),
            ("(25.0330, 121.5654)", True),
            ("  25.0330,121.5654  ", True),
            ("Taipei 101", False),
            ("abc, def", False),
        ]

        for test_input, should_match in test_cases:
            match = re.match(pattern, test_input.strip())
            is_match = match is not None
            assert is_match == should_match, f"Pattern failed for: {test_input}"

        print("  PASSED")
        passed += 1
    except AssertionError as e:
        print(f"  FAILED: {e}")
        failed += 1

    # Test 8: NavigationFormatter duration
    print("\nTest 8: NavigationFormatter duration")
    try:
        assert NavigationFormatter.format_duration(0.5) == "less than a minute"
        assert "5 minute" in NavigationFormatter.format_duration(5)
        assert "1 hour" in NavigationFormatter.format_duration(65)
        print("  PASSED")
        passed += 1
    except AssertionError as e:
        print(f"  FAILED: {e}")
        failed += 1

    # Test 9: NavigationFormatter distance
    print("\nTest 9: NavigationFormatter distance")
    try:
        assert "500 meters" in NavigationFormatter.format_distance(0.5)
        assert "5.5 km" in NavigationFormatter.format_distance(5.5)
        print("  PASSED")
        passed += 1
    except AssertionError as e:
        print(f"  FAILED: {e}")
        failed += 1

    # Test 10: SimpleCache
    print("\nTest 10: SimpleCache")
    try:
        cache = SimpleCache(cache_dir=".test_cache", ttl_hours=1)
        cache.set({"test": "value"}, "key1", "key2")
        result = cache.get("key1", "key2")
        assert result == {"test": "value"}, "Cache get failed"

        result = cache.get("nonexistent")
        assert result is None, "Cache should return None for miss"

        cache.clear()
        print("  PASSED")
        passed += 1
    except AssertionError as e:
        print(f"  FAILED: {e}")
        failed += 1
    finally:
        # Cleanup
        import shutil
        if Path(".test_cache").exists():
            shutil.rmtree(".test_cache")

    # Summary
    print("\n" + "=" * 50)
    print(f"  RESULTS: {passed} passed, {failed} failed")
    print("=" * 50)

    return failed == 0


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Run tests if requested
    if args.test:
        success = run_tests()
        sys.exit(0 if success else 1)

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
