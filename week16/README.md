# Week 16: Final Demo Day

**Final Project Presentation** — 期末專題 (25%)

---

## Demo Requirements

Your Smart City Navigator should demonstrate:

### Core Features (Required)

1. **Location Input**
   - User enters a starting location (address or place name)
   - App successfully geocodes it to coordinates

2. **Category Search**
   - User selects what they're looking for (pizza, cafe, etc.)
   - App finds relevant places using Nominatim

3. **Constraint Filtering**
   - User sets a walking time limit
   - App filters out places that are too far (using OSRM)

4. **Smart Sorting**
   - Results sorted by rating (highest first)
   - User can see top options clearly

5. **Route Optimization**
   - If visiting multiple places, route is optimized
   - Shortest walking path calculated

6. **Interactive Map**
   - Folium-generated map displayed in browser
   - Markers for all found places
   - Route line connecting selected places

### Bonus Features (Extra Credit)

- Custom icons for different categories
- Turn-by-turn directions
- Save favorite places
- Share route via URL
- Mobile-responsive design

---

## Grading Rubric

| Criteria | Points |
|----------|--------|
| Core functionality works | 50% |
| Code quality (OOP, decorators, clean structure) | 5% |
| User interface (clear, usable) | 15% |
| Demo presentation | 10% |
| Bonus features | 20% |

---

## Demo Format

1. **Introduction (1 min)**
   - What does your app do?
   - Any unique features?

2. **Live Demo (3-4 min)**
   - Show the full workflow
   - Handle at least one search
   - Display the map with results

3. **Q&A (1-2 min)**
   - Be ready to explain your code
   - Be ready to show specific features

---

## Submission

- Push final code to your repository
- Ensure `README.md` has setup instructions
- Include `requirements.txt`
- Test that it runs on a fresh environment

---

## Good Luck! 🎉

You've learned:
- Python fundamentals
- Working with APIs
- Data structures and algorithms
- Web development with Flask
- Interactive visualization with Folium

These are real, industry-relevant skills. Be proud of what you've built!
