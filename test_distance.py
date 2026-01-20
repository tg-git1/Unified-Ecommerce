from modules.carbon_emissions import CarbonEmissionsCalculator

carbon_calc = CarbonEmissionsCalculator()
eco_ratings = carbon_calc.get_all_platform_ratings('560001', platforms=['Amazon', 'Flipkart', 'Croma'])

print("Eco-Friendliness with Distance:")
print("=" * 50)
for platform, rating in eco_ratings.items():
    print(f"\n{platform}:")
    print(f"  Distance: {rating['distance']:.0f} km")
    print(f"  Emissions: {rating['emissions']:.3f} kg CO2")
    print(f"  Rating: {rating['rating']}")
