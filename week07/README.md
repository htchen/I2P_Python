# Week 7: The Smart City Navigator (Capstone Project)

**Phase 2: The API & The Cloud** — "Fetching the World"

---

## Overview

This is our capstone week! We combine everything learned to build a complete **Smart City Navigator** - a command-line application that helps users navigate between locations using real addresses, coordinates, and optimal routing.

---

## Concepts

- System architecture and separation of concerns
- Data models with dataclasses (Location, Route, RouteStep)
- Integrating multiple APIs (Nominatim + OSRM)
- Command-line interface design with argparse
- Error handling strategies
- Caching for performance

---

## What We'll Build

A fully-functional navigation system that:
- Converts addresses to coordinates (Nominatim)
- Calculates optimal routes (OSRM)
- Handles multiple waypoints efficiently
- Provides clear, user-friendly output
- Handles errors gracefully
- Supports different transportation modes

---

## Project Structure

```python
# Key classes in our navigator
class Location:
    """Represents a geographic location."""
    name: str
    latitude: float
    longitude: float
    display_name: str

class Route:
    """Represents a complete route."""
    distance: float
    duration: float
    geometry: List[Tuple[float, float]]

class GeocodingService:
    """Handles address → coordinates conversion."""
    def geocode(self, address: str) -> Optional[Location]: ...

class RoutingService:
    """Handles route calculation."""
    def get_route(self, waypoints: List) -> Optional[Route]: ...

class Navigator:
    """Coordinates the services."""
    def navigate(self, start: str, end: str) -> Optional[dict]: ...
```

---

## Lab Exercises

See the `lectures/lecture_exercises/` folder for this week's exercises.

## Lecture Materials

See the `lectures/` folder for slides and examples.
