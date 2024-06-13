#Prob3-1
import pandas as pd
import re


class Country:
    def __init__(self, name, population, total_area, who_region, population_data):
        self.name = name
        self.population = population
        self.total_area = total_area
        self.who_region = who_region
        self.population_data = population_data

    def info(self):
        return {
            "name": self.name,
            "population": self.population,
            "total_area": self.total_area,
            "who_region": self.who_region
        }

    def population_density(self):
        density = self.population / self.total_area
        return f"{density:.2f}"

    def update_population(self):
        # 연간 인구 성장률 계산
        growth_rates = []
        years = sorted(self.population_data.keys())
        for i in range(len(years) - 1):
            year = years[i]
            next_year = years[i + 1]
            if self.population_data[next_year] > 0 and self.population_data[year]:
                growth_rate = (self.population_data[next_year] - self.population_data[year]) / self.population_data[year]
                growth_rates.append(growth_rate)
        if growth_rates:
            avg_growth_rate = sum(growth_rates) / len(growth_rates)
        else:
            avg_growth_rate = 0

        # 2024년 인구 예측
        years_to_project = 2024 - max(years)

        projected_population = self.population.item()
        for _ in range(years_to_project):
            projected_population += projected_population * avg_growth_rate

        self.population = projected_population

    def compare(countries, target_region):
        same_region_countries = [country for country in countries if country.who_region == target_region]
        same_region_countries.sort(key=lambda x: float(x.population_density()), reverse=True)
        return same_region_countries[:10]

def clean_area_data(value):
    match = re.search(r'\d+[\d,]*', value)
    if match:
        return float(match.group(0).replace(',', ''))
    return None

# 데이터 로드
WHO_COVID_19_global_data = pd.read_csv("WHO-COVID-19-global-data.csv")
country_population_df = pd.read_csv("country-population.csv")
list_of_countries_by_area = pd.read_csv("list_of_countries_by_area.CSV")

# EURO 지역 국가 필터링
euro_countries = WHO_COVID_19_global_data[WHO_COVID_19_global_data['WHO_region'] == 'EURO']['Country'].unique()

# 국가별 면적 정보 딕셔너리 생성
list_of_countries_by_area['Total in km (mi)'] = list_of_countries_by_area['Total in km (mi)'].apply(clean_area_data)
area_data = dict(zip(list_of_countries_by_area['Country / Dependency'], list_of_countries_by_area['Total in km (mi)']))

# EURO 지역 국가 인스턴스 생성
countries = []
for country in euro_countries:
    if country in area_data:
        country_population = country_population_df[country_population_df["Country Name"] == country]
        if not country_population.empty:
            population_data = {int(year): pop for year, pop in country_population.iloc[0].items() if year.isdigit()}
            total_area = area_data[country]
            population = population_data.get(2022)
            if population and total_area:
                countries.append(Country(name=country, population=population, total_area=total_area, who_region='EURO', population_data=population_data))

# 국가 인스턴스 확인
print(f"Total countries in EURO region: {len(countries)}")
for country in countries[:5]:  # 상위 5개 국가만 출력
    print(country.info())

# 인구 밀도를 기준으로 EURO 지역 국가들 비교 및 순위 매기기
top_10_density_countries = Country.compare(countries, "EURO")

# 순위 출력
print("Top 10 countries by population density in EURO region (before update):")
for i, country in enumerate(top_10_density_countries, start=1):
    print(f"{i}. {country.name} - Density: {country.population_density()}")

# 각 국가의 인구를 2024년으로 업데이트
for country in countries:
    country.update_population()

# 인구 업데이트 후 정보 확인
print("Updated population information:")
for country in countries[:5]:  # 상위 5개 국가만 출력
    print(country.info())

# 인구 밀도를 기준으로 EURO 지역 국가들 다시 비교 및 순위 매기기
top_10_density_countries_updated = Country.compare(countries, "EURO")

# 순위 출력
print("Top 10 countries by population density in EURO region (after update):")
for i, country in enumerate(top_10_density_countries_updated, start=1):
    print(f"{i}. {country.name} - Density: {country.population_density()}")