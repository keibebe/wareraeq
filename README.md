Equipment Production Cost Calculator

Calculate equipment production costs from warera.io considering current market prices for scrap and steel.

Features

- Real-time material price fetching (scrap, steel, copper, etc.)
- Equipment material composition tracking
- Detailed cost breakdown by material
- Comprehensive cost reporting
- Easy extensibility for additional equipment and materials

Installation

```bash
git clone https://github.com/keibebe/wareraeq.git
cd wareraeq
pip install -r requirements.txt
```

Usage

Basic Example

```python
from equipment_cost_calculator import Equipment, EquipmentCatalog

# Create catalog
catalog = EquipmentCatalog()

# Define equipment with material composition (in kg)
excavator = Equipment(
    "Excavator CAT 320",
    {
        'steel': 25000,
        'scrap': 2000,
        'copper': 150
    }
)

# Add to catalog
catalog.add_equipment(excavator)

# Fetch current prices
catalog.update_prices()

# Calculate costs
catalog.calculate_all_costs()

# Generate report
print(catalog.get_equipment_report())
```

Material Price Sources

The calculator integrates with:
- **metals.live API** - Real-time commodity prices
- **Custom integrations** - Can be extended for warera.io API

To use warera.io API, update the `PriceFetcher` class with appropriate API endpoints and authentication.

Equipment Data Format

Define equipment with material compositions:

```python
equipment = Equipment(
    "Equipment Name",
    {
        'steel': 25000,    # Weight in kg
        'scrap': 2000,
        'copper': 150,
        'aluminum': 500
    }
)
```

Project Structure

```
wareraeq/
├── equipment_cost_calculator.py  # Main calculator logic
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

Future Enhancements

- [ ] Integration with warera.io API for real-time pricing
- [ ] Database storage for historical price data
- [ ] Web interface for equipment management
- [ ] Export to PDF/Excel reports
- [ ] Equipment category management
- [ ] Price prediction models
- [ ] API endpoint for external integrations

License

MIT

Author

keibebe
