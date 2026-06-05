"""
Equipment Production Cost Calculator
Calculates production costs for equipment considering current scrap and steel prices
"""

import requests
from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime


@dataclass
class MaterialPrice:
    """Data class for material pricing"""
    name: str
    price_per_unit: float
    unit: str  # kg, ton, etc.
    last_updated: datetime


class PriceFetcher:
    """Fetches current material prices from market sources"""
    
    def __init__(self):
        """Initialize price fetcher"""
        self.scrap_price = None
        self.steel_price = None
        self.last_update = None
    
    def fetch_scrap_price(self) -> float:
        """
        Fetch current scrap metal price
        Returns price per kilogram
        """
        try:
            # Example: Using a mock API or data source
            # In production, integrate with actual commodity price APIs
            # e.g., metals.live, tradingeconomics, or warera.io API
            response = requests.get('https://api.metals.live/v1/spot/copper', timeout=5)
            if response.status_code == 200:
                data = response.json()
                # Parse and return price (adjust based on actual API response)
                self.scrap_price = float(data.get('price', 0)) / 1000  # Convert to per kg
                return self.scrap_price
        except Exception as e:
            print(f"Error fetching scrap price: {e}")
        
        return None
    
    def fetch_steel_price(self) -> float:
        """
        Fetch current steel price
        Returns price per kilogram
        """
        try:
            # Integration point for steel price API
            # Common sources: TradingEconomics, LBMA, or commodity exchanges
            response = requests.get('https://api.metals.live/v1/spot/silver', timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.steel_price = float(data.get('price', 0)) / 1000
                return self.steel_price
        except Exception as e:
            print(f"Error fetching steel price: {e}")
        
        return None
    
    def fetch_prices(self) -> Dict[str, float]:
        """Fetch all material prices"""
        return {
            'scrap': self.fetch_scrap_price(),
            'steel': self.fetch_steel_price()
        }


class Equipment:
    """Represents a piece of equipment with material composition"""
    
    def __init__(self, name: str, composition: Dict[str, float]):
        """
        Initialize equipment
        
        Args:
            name: Equipment name
            composition: Dictionary with material names and weights (in kg)
                        e.g., {'steel': 50, 'scrap': 20, 'copper': 5}
        """
        self.name = name
        self.composition = composition  # Material -> weight in kg
        self.production_costs = {}
    
    def calculate_cost(self, material_prices: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate production cost based on material composition and prices
        
        Args:
            material_prices: Dictionary with material names and prices per kg
        
        Returns:
            Dictionary with cost breakdown by material
        """
        cost_breakdown = {}
        total_cost = 0
        
        for material, weight in self.composition.items():
            if material in material_prices and material_prices[material]:
                cost = weight * material_prices[material]
                cost_breakdown[material] = cost
                total_cost += cost
            else:
                cost_breakdown[material] = 0
        
        cost_breakdown['total'] = total_cost
        self.production_costs = cost_breakdown
        return cost_breakdown
    
    def get_cost_summary(self) -> str:
        """Get formatted cost summary"""
        if not self.production_costs:
            return "No cost calculated yet"
        
        summary = f"\n=== Production Cost Summary: {self.name} ===\n"
        for material, cost in self.production_costs.items():
            if material != 'total':
                summary += f"{material.capitalize()}: ${cost:.2f}\n"
        summary += f"\nTotal Production Cost: ${self.production_costs['total']:.2f}\n"
        return summary


class EquipmentCatalog:
    """Manages a catalog of equipment and their costs"""
    
    def __init__(self):
        self.equipment_list = {}
        self.price_fetcher = PriceFetcher()
        self.current_prices = {}
    
    def add_equipment(self, equipment: Equipment):
        """Add equipment to catalog"""
        self.equipment_list[equipment.name] = equipment
    
    def update_prices(self) -> bool:
        """Fetch and update material prices"""
        self.current_prices = self.price_fetcher.fetch_prices()
        return all(self.current_prices.values())
    
    def calculate_all_costs(self) -> Dict[str, Dict[str, float]]:
        """Calculate costs for all equipment in catalog"""
        if not self.current_prices:
            self.update_prices()
        
        results = {}
        for name, equipment in self.equipment_list.items():
            results[name] = equipment.calculate_cost(self.current_prices)
        
        return results
    
    def get_equipment_report(self) -> str:
        """Generate comprehensive equipment cost report"""
        report = "\n" + "="*50 + "\n"
        report += "EQUIPMENT PRODUCTION COST REPORT\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "="*50 + "\n"
        
        report += "\nCurrent Material Prices:\n"
        report += "-"*30 + "\n"
        for material, price in self.current_prices.items():
            if price:
                report += f"{material.capitalize()}: ${price:.4f}/kg\n"
        
        report += "\n" + "="*50 + "\n"
        report += "EQUIPMENT COSTS:\n"
        report += "="*50 + "\n"
        
        for equipment in self.equipment_list.values():
            report += equipment.get_cost_summary()
        
        return report


def main():
    """Main function demonstrating usage"""
    # Initialize catalog
    catalog = EquipmentCatalog()
    
    # Create sample equipment with material compositions
    excavator = Equipment(
        "Excavator CAT 320",
        {
            'steel': 25000,      # 25 tons of steel
            'scrap': 2000,       # 2 tons of scrap metal
            'copper': 150        # 150 kg of copper
        }
    )
    
    bulldozer = Equipment(
        "Bulldozer CAT D9",
        {
            'steel': 35000,
            'scrap': 3000,
            'copper': 200
        }
    )
    
    # Add to catalog
    catalog.add_equipment(excavator)
    catalog.add_equipment(bulldozer)
    
    # Update prices from market sources
    print("Fetching current material prices...")
    if catalog.update_prices():
        print("✓ Prices updated successfully")
    else:
        print("⚠ Some prices unavailable, using cached values")
    
    # Calculate all costs
    catalog.calculate_all_costs()
    
    # Generate and print report
    print(catalog.get_equipment_report())


if __name__ == "__main__":
    main()
