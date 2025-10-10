"""
Check countries in the disaster data and identify non-Sub-Saharan African countries
"""

import pandas as pd

# Define Sub-Saharan African countries (excluding North African countries)
SUB_SAHARAN_COUNTRIES = {
    'AGO': 'Angola', 'BEN': 'Benin', 'BWA': 'Botswana', 'BFA': 'Burkina Faso',
    'BDI': 'Burundi', 'CMR': 'Cameroon', 'CPV': 'Cape Verde', 'CAF': 'Central African Republic',
    'TCD': 'Chad', 'COM': 'Comoros', 'COG': 'Congo', 'COD': 'Democratic Republic of Congo',
    'DJI': 'Djibouti', 'GNQ': 'Equatorial Guinea', 'ERI': 'Eritrea', 'SWZ': 'Eswatini',
    'ETH': 'Ethiopia', 'GAB': 'Gabon', 'GMB': 'Gambia', 'GHA': 'Ghana', 'GIN': 'Guinea',
    'GNB': 'Guinea-Bissau', 'CIV': 'Ivory Coast', 'KEN': 'Kenya', 'LSO': 'Lesotho', 
    'LBR': 'Liberia', 'MDG': 'Madagascar', 'MWI': 'Malawi', 'MLI': 'Mali', 'MRT': 'Mauritania',
    'MUS': 'Mauritius', 'MOZ': 'Mozambique', 'NAM': 'Namibia', 'NER': 'Niger',
    'NGA': 'Nigeria', 'RWA': 'Rwanda', 'STP': 'São Tomé and Príncipe', 'SEN': 'Senegal',
    'SYC': 'Seychelles', 'SLE': 'Sierra Leone', 'SOM': 'Somalia', 'ZAF': 'South Africa',
    'SSD': 'South Sudan', 'SDN': 'Sudan', 'TZA': 'Tanzania', 'TGO': 'Togo',
    'UGA': 'Uganda', 'ZMB': 'Zambia', 'ZWE': 'Zimbabwe'
}

# Countries that are in Africa but NOT Sub-Saharan (North Africa)
NORTH_AFRICAN_COUNTRIES = {
    'DZA': 'Algeria',
    'EGY': 'Egypt', 
    'LBY': 'Libya',
    'MAR': 'Morocco',
    'TUN': 'Tunisia'
}

def check_countries():
    """Check which countries are in the data and identify non-Sub-Saharan ones"""
    
    try:
        # Load the data
        df = pd.read_csv('data/processed/african_disasters_emdat.csv')
        
        # Get unique countries
        countries_in_data = df[['country', 'country_code']].drop_duplicates().sort_values('country')
        
        print("=== COUNTRIES CURRENTLY IN DISASTER DATA ===\n")
        print(f"Total countries: {len(countries_in_data)}")
        print("\nAll countries:")
        for _, row in countries_in_data.iterrows():
            print(f"  {row['country_code']}: {row['country']}")
        
        print("\n" + "="*60)
        
        # Identify Sub-Saharan vs North African countries
        sub_saharan_in_data = []
        north_african_in_data = []
        other_countries_in_data = []
        
        for _, row in countries_in_data.iterrows():
            code = row['country_code']
            name = row['country']
            
            if code in SUB_SAHARAN_COUNTRIES:
                sub_saharan_in_data.append((code, name))
            elif code in NORTH_AFRICAN_COUNTRIES:
                north_african_in_data.append((code, name))
            else:
                other_countries_in_data.append((code, name))
        
        print(f"\n✅ SUB-SAHARAN AFRICAN COUNTRIES IN DATA ({len(sub_saharan_in_data)}):")
        for code, name in sub_saharan_in_data:
            disaster_count = len(df[df['country_code'] == code])
            print(f"  {code}: {name} ({disaster_count} disasters)")
        
        print(f"\n❌ NORTH AFRICAN COUNTRIES TO REMOVE ({len(north_african_in_data)}):")
        for code, name in north_african_in_data:
            disaster_count = len(df[df['country_code'] == code])
            print(f"  {code}: {name} ({disaster_count} disasters)")
        
        if other_countries_in_data:
            print(f"\n❓ OTHER COUNTRIES (NOT IN EXPECTED LISTS) ({len(other_countries_in_data)}):")
            for code, name in other_countries_in_data:
                disaster_count = len(df[df['country_code'] == code])
                print(f"  {code}: {name} ({disaster_count} disasters)")
        
        # Summary statistics
        total_disasters = len(df)
        sub_saharan_disasters = len(df[df['country_code'].isin(SUB_SAHARAN_COUNTRIES.keys())])
        north_african_disasters = len(df[df['country_code'].isin(NORTH_AFRICAN_COUNTRIES.keys())])
        
        print(f"\n📊 DISASTER STATISTICS:")
        print(f"  Total disasters in data: {total_disasters:,}")
        print(f"  Sub-Saharan disasters: {sub_saharan_disasters:,} ({sub_saharan_disasters/total_disasters*100:.1f}%)")
        print(f"  North African disasters: {north_african_disasters:,} ({north_african_disasters/total_disasters*100:.1f}%)")
        print(f"  Other disasters: {total_disasters - sub_saharan_disasters - north_african_disasters:,}")
        
        return north_african_in_data, other_countries_in_data
        
    except Exception as e:
        print(f"Error: {e}")
        return [], []

if __name__ == "__main__":
    check_countries()