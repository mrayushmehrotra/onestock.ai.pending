from datetime import datetime
from typing import List, Dict, Any

class SeasonalEngine:
    """
    Maps Indian seasons and weather trends to specific market sectors.
    """
    
    SEASONS = {
        "SUMMER": {
            "months": [3, 4, 5, 6],
            "sectors": ["Solar Energy", "Cooling/Appliances", "Beverages", "Power"],
            "description": "High demand for electricity, cooling systems, and renewable energy."
        },
        "MONSOON": {
            "months": [7, 8, 9],
            "sectors": ["Agriculture", "Fertilizers", "Logistics", "Consumer Goods"],
            "description": "Critical for rural demand and agricultural output."
        },
        "AUTUMN/FESTIVAL": {
            "months": [10, 11],
            "sectors": ["E-commerce", "Retail", "Automobiles", "Paints", "Jewelry"],
            "description": "Peak consumption period due to major Indian festivals."
        },
        "WINTER": {
            "months": [12, 1, 2],
            "sectors": ["Thermal Wear", "Power/Heating", "Tourism", "Construction"],
            "description": "Shift towards winter apparel and travel."
        }
    }

    def get_current_seasonal_context(self) -> Dict[str, Any]:
        month = datetime.now().month
        
        current_season = "UNKNOWN"
        for season, data in self.SEASONS.items():
            if month in data["months"]:
                current_season = season
                break
        
        return {
            "season": current_season,
            "month": datetime.now().strftime("%B"),
            "target_sectors": self.SEASONS.get(current_season, {}).get("sectors", []),
            "reasoning_hint": self.SEASONS.get(current_season, {}).get("description", "")
        }

    def get_weather_weightage(self, temperature: float, is_transitioning: bool = False) -> Dict[str, float]:
        """
        Adjusts weightage based on specific temperature trends.
        If transitioning from Summer to Winter (e.g., October/November), 
        weight for 'Cool' products like woolens increases.
        """
        weights = {}
        
        if temperature > 35:
            weights["Solar Energy"] = 0.4
            weights["Cooling/Appliances"] = 0.5
        elif temperature < 15:
            weights["Thermal Wear"] = 0.4
            weights["Power"] = 0.3
            
        return weights

if __name__ == "__main__":
    engine = SeasonalEngine()
    print(f"Current Context: {engine.get_current_seasonal_context()}")
