#!/usr/bin/env python3
"""
Week 7: Smart City Navigator - Complete Examples

This module contains all the code examples from Week 7 lecture,
demonstrating a complete navigation system that combines geocoding
and routing services.

Run this file to see interactive demonstrations of each concept.
"""

import requests
import time
import json
import hashlib
import re
import math
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Any


# =============================================================================
# PART 1: Data Models
# =============================================================================

@dataclass
class Location:
    """Represents a geographic location."""
    name: str
    latitude: float
    longitude: float
    display_name: str

    @property
    def coords(self) -> Tuple[float, float]:
        """Return (lat, lon) tuple."""
        return (self.latitude, self.longitude)

    def __str__(self) -> str:
        return f"{self.name} ({self.latitude:.4f}, {self.longitude:.4f})"


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


# =============================================================================
# PART 2: Simple Cache Implementation
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
        print("Cache cleared.")


# =============================================================================
# PART 3: Geocoding Service
# =============================================================================

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


# =============================================================================
# PART 4: Routing Service
# =============================================================================

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


# =============================================================================
# PART 5: Navigation Formatter
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


# =============================================================================
# PART 6: Navigator (Main Coordinator)
# =============================================================================

class Navigator:
    """
    Smart City Navigator - combines geocoding and routing services.

    Usage:
        nav = Navigator()
        result = nav.navigate("Taipei 101", "Taipei Main Station")
        print(NavigationFormatter.format_simple_result(result))
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


# =============================================================================
# INTERACTIVE EXAMPLES
# =============================================================================

def example_1_location_dataclass():
    """Example 1: Using the Location dataclass."""
    print("\n" + "=" * 60)
    print("Example 1: Location Dataclass")
    print("=" * 60)

    # Create a location
    loc = Location(
        name="Taipei 101",
        latitude=25.0330,
        longitude=121.5654,
        display_name="Taipei 101, Xinyi District, Taipei, Taiwan"
    )

    print(f"\nLocation: {loc}")
    print(f"Coordinates tuple: {loc.coords}")
    print(f"Display name: {loc.display_name}")

    # Create another location
    loc2 = Location(
        name="Taipei Main Station",
        latitude=25.0478,
        longitude=121.5170,
        display_name="Taipei Main Station, Zhongzheng District, Taipei"
    )

    print(f"\nSecond location: {loc2}")

    # Calculate straight-line distance (Haversine)
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat/2)**2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon/2)**2)
        return 2 * R * math.asin(math.sqrt(a))

    distance = haversine(
        loc.latitude, loc.longitude,
        loc2.latitude, loc2.longitude
    )
    print(f"\nStraight-line distance: {distance:.2f} km")


def example_2_route_dataclass():
    """Example 2: Using the Route dataclass."""
    print("\n" + "=" * 60)
    print("Example 2: Route Dataclass")
    print("=" * 60)

    # Create a route
    route = Route(
        distance=5200,  # 5.2 km in meters
        duration=720,   # 12 minutes in seconds
        geometry=[
            (25.0330, 121.5654),
            (25.0350, 121.5500),
            (25.0400, 121.5300),
            (25.0478, 121.5170)
        ],
        steps=[
            RouteStep("Depart", 0, 0),
            RouteStep("Turn Right", 1500, 180),
            RouteStep("Continue Straight", 2500, 360),
            RouteStep("Turn Left", 1200, 180),
            RouteStep("Arrive", 0, 0)
        ]
    )

    print(f"\nRoute Summary: {route.summary()}")
    print(f"Distance: {route.distance_km:.1f} km ({route.distance} meters)")
    print(f"Duration: {route.duration_min:.0f} minutes ({route.duration} seconds)")
    print(f"Waypoints: {len(route.geometry)} points")
    print(f"\nSteps:")
    for i, step in enumerate(route.steps, 1):
        print(f"  {i}. {step.instruction} - {step.distance_km:.1f} km")


def example_3_simple_cache():
    """Example 3: Using the SimpleCache."""
    print("\n" + "=" * 60)
    print("Example 3: Simple Cache")
    print("=" * 60)

    cache = SimpleCache(cache_dir=".example_cache", ttl_hours=1)

    # Cache some data
    print("\nCaching geocoding result...")
    cache.set(
        {"lat": 25.0330, "lon": 121.5654, "name": "Taipei 101"},
        "geocode", "Taipei 101"
    )
    print("  Cached!")

    # Retrieve from cache
    print("\nRetrieving from cache...")
    result = cache.get("geocode", "Taipei 101")
    if result:
        print(f"  Found: {result}")
    else:
        print("  Not found (cache miss)")

    # Try to get non-existent key
    print("\nTrying non-existent key...")
    result = cache.get("geocode", "Unknown Location")
    if result:
        print(f"  Found: {result}")
    else:
        print("  Not found (cache miss) - expected!")

    # Clear cache
    cache.clear()


def example_4_geocoding_service():
    """Example 4: Using the GeocodingService."""
    print("\n" + "=" * 60)
    print("Example 4: Geocoding Service")
    print("=" * 60)

    geocoder = GeocodingService(user_agent="Week7Example/1.0")

    print("\nGeocoding 'Taipei 101'...")
    location = geocoder.geocode("Taipei 101")

    if location:
        print(f"  Name: {location.name}")
        print(f"  Coordinates: {location.coords}")
        print(f"  Full address: {location.display_name}")
    else:
        print("  Could not geocode (network may be unavailable)")

    print("\nReverse geocoding (25.0330, 121.5654)...")
    location = geocoder.reverse_geocode(25.0330, 121.5654)

    if location:
        print(f"  Name: {location.name}")
        print(f"  Full address: {location.display_name}")
    else:
        print("  Could not reverse geocode (network may be unavailable)")


def example_5_routing_service():
    """Example 5: Using the RoutingService."""
    print("\n" + "=" * 60)
    print("Example 5: Routing Service")
    print("=" * 60)

    router = RoutingService(profile="driving")

    # Define waypoints
    waypoints = [
        (25.0330, 121.5654),  # Taipei 101
        (25.0478, 121.5170)   # Taipei Main Station
    ]

    print(f"\nCalculating driving route...")
    print(f"  From: {waypoints[0]}")
    print(f"  To: {waypoints[1]}")

    route = router.get_route(waypoints, include_steps=True)

    if route:
        print(f"\nRoute found!")
        print(f"  Distance: {route.distance_km:.1f} km")
        print(f"  Duration: {route.duration_min:.0f} minutes")
        print(f"  Path points: {len(route.geometry)}")

        if route.steps:
            print(f"\nTurn-by-turn ({len(route.steps)} steps):")
            for i, step in enumerate(route.steps[:5], 1):  # Show first 5
                print(f"    {i}. {step.instruction}")
            if len(route.steps) > 5:
                print(f"    ... and {len(route.steps) - 5} more steps")
    else:
        print("  Could not calculate route (network may be unavailable)")


def example_6_navigator_simple():
    """Example 6: Simple navigation with Navigator."""
    print("\n" + "=" * 60)
    print("Example 6: Simple Navigation")
    print("=" * 60)

    nav = Navigator(profile="driving")
    formatter = NavigationFormatter()

    result = nav.navigate(
        "Taipei 101, Taiwan",
        "Taipei Main Station, Taiwan"
    )

    if result:
        print(formatter.format_simple_result(result))
    else:
        print("\nNavigation failed (network may be unavailable)")


def example_7_navigator_with_coords():
    """Example 7: Navigation with coordinates."""
    print("\n" + "=" * 60)
    print("Example 7: Navigation with Coordinates")
    print("=" * 60)

    nav = Navigator(profile="driving")
    formatter = NavigationFormatter()

    # Using coordinates instead of addresses
    result = nav.navigate(
        "25.0330, 121.5654",  # Taipei 101 coordinates
        "National Palace Museum, Taiwan"
    )

    if result:
        print(formatter.format_simple_result(result))
    else:
        print("\nNavigation failed (network may be unavailable)")


def example_8_multi_stop():
    """Example 8: Multi-stop navigation."""
    print("\n" + "=" * 60)
    print("Example 8: Multi-Stop Navigation")
    print("=" * 60)

    nav = Navigator(profile="driving")
    formatter = NavigationFormatter()

    stops = [
        "Taipei 101, Taiwan",
        "Taipei City Hall, Taiwan",
        "Sun Yat-sen Memorial Hall, Taiwan"
    ]

    result = nav.navigate_multi(stops)

    if result:
        print(formatter.format_multi_result(result))
    else:
        print("\nNavigation failed (network may be unavailable)")


def example_9_walking_route():
    """Example 9: Walking route comparison."""
    print("\n" + "=" * 60)
    print("Example 9: Walking vs Driving Comparison")
    print("=" * 60)

    formatter = NavigationFormatter()

    start = "Taipei City Hall, Taiwan"
    end = "Sun Yat-sen Memorial Hall, Taiwan"

    # Driving route
    print("\n--- DRIVING ---")
    nav_drive = Navigator(profile="driving")
    result_drive = nav_drive.navigate(start, end)

    # Walking route
    print("\n--- WALKING ---")
    nav_walk = Navigator(profile="walking")
    result_walk = nav_walk.navigate(start, end)

    # Compare
    print("\n" + "=" * 50)
    print("  COMPARISON")
    print("=" * 50)

    if result_drive and result_walk:
        drive_route = result_drive["route"]
        walk_route = result_walk["route"]

        print(f"\nDriving:")
        print(f"  Distance: {formatter.format_distance(drive_route.distance_km)}")
        print(f"  Time: {formatter.format_duration(drive_route.duration_min)}")

        print(f"\nWalking:")
        print(f"  Distance: {formatter.format_distance(walk_route.distance_km)}")
        print(f"  Time: {formatter.format_duration(walk_route.duration_min)}")

        # Calculate differences
        time_diff = walk_route.duration_min - drive_route.duration_min
        print(f"\nWalking takes {time_diff:.0f} minutes longer")
    else:
        print("\nCould not compare (network may be unavailable)")


def example_10_formatter_demo():
    """Example 10: Navigation Formatter demonstration."""
    print("\n" + "=" * 60)
    print("Example 10: Formatter Demonstration")
    print("=" * 60)

    # Test duration formatting
    print("\nDuration formatting:")
    for minutes in [0.5, 1, 5, 30, 60, 90, 125]:
        formatted = NavigationFormatter.format_duration(minutes)
        print(f"  {minutes} min -> {formatted}")

    # Test distance formatting
    print("\nDistance formatting:")
    for km in [0.1, 0.5, 1.0, 5.5, 10.0, 100.0]:
        formatted = NavigationFormatter.format_distance(km)
        print(f"  {km} km -> {formatted}")


def run_all_examples():
    """Run all examples in sequence."""
    examples = [
        ("Location Dataclass", example_1_location_dataclass),
        ("Route Dataclass", example_2_route_dataclass),
        ("Simple Cache", example_3_simple_cache),
        ("Geocoding Service", example_4_geocoding_service),
        ("Routing Service", example_5_routing_service),
        ("Simple Navigation", example_6_navigator_simple),
        ("Navigation with Coordinates", example_7_navigator_with_coords),
        ("Multi-Stop Navigation", example_8_multi_stop),
        ("Walking vs Driving", example_9_walking_route),
        ("Formatter Demo", example_10_formatter_demo),
    ]

    print("\n" + "=" * 60)
    print("  WEEK 7: SMART CITY NAVIGATOR EXAMPLES")
    print("=" * 60)
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  {len(examples) + 1}. Run all (non-network examples only)")
    print("  0. Exit")

    while True:
        try:
            choice = input("\nEnter choice: ").strip()

            if choice == "0":
                print("Goodbye!")
                break
            elif choice == str(len(examples) + 1):
                # Run non-network examples
                for name, func in examples[:3]:  # First 3 don't need network
                    func()
                example_10_formatter_demo()  # This one also doesn't need network
            elif choice.isdigit() and 1 <= int(choice) <= len(examples):
                _, func = examples[int(choice) - 1]
                func()
            else:
                print("Invalid choice. Please enter a number from the menu.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            break


if __name__ == "__main__":
    run_all_examples()
