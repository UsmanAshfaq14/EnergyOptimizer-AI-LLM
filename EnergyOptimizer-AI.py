import json
import csv
from typing import Dict, List, Union
from dataclasses import dataclass
from io import StringIO

@dataclass
class MachineData:
    machine_id: str
    power_usage_kw: float
    operational_hours: float

class EnergyOptimizer:
    def __init__(self):
        self.INEFFICIENCY_THRESHOLD = 500  # kWh
        self.ELECTRICITY_COST = 0.10  # USD per kWh

    def validate_data_structure(self, data: List[MachineData]) -> Dict:
        """Validates the basic data structure and returns validation report."""
        return {
            "num_machines": len(data),
            "fields_per_record": 3,
            "required_fields": {
                "machine_id": "present",
                "power_usage_kw": "present",
                "operational_hours": "present"
            }
        }

    def validate_data_types(self, data: List[MachineData]) -> Dict:
        """Validates data types and values."""
        validation = {
            "power_usage_kw": "validated",
            "operational_hours": "validated"
        }
        
        for machine in data:
            if not isinstance(machine.power_usage_kw, (int, float)) or machine.power_usage_kw <= 0:
                validation["power_usage_kw"] = "not valid"
            if not isinstance(machine.operational_hours, (int, float)) or machine.operational_hours <= 0:
                validation["operational_hours"] = "not valid"
        
        return validation

    def calculate_energy_consumption(self, power_usage: float, hours: float) -> float:
        """Calculates total energy consumption in kWh."""
        return round(power_usage * hours, 2)

    def calculate_recommended_hours(self, power_usage: float) -> float:
        """Calculates recommended operational hours if machine is inefficient."""
        return round(self.INEFFICIENCY_THRESHOLD / power_usage, 2)

    def calculate_energy_savings(self, current_consumption: float, power_usage: float, 
                               recommended_hours: float) -> float:
        """Calculates potential energy savings in kWh."""
        return round(current_consumption - (power_usage * recommended_hours), 2)

    def calculate_cost_reduction(self, energy_savings: float) -> float:
        """Calculates cost reduction in USD."""
        return round(energy_savings * self.ELECTRICITY_COST, 2)

    def generate_report(self, data: List[MachineData]) -> str:
        """Generates a detailed analysis report in markdown format."""
        validation_data = self.validate_data_structure(data)
        type_validation = self.validate_data_types(data)
        
        report = [
            "# Data Validation Report",
            "## 1. Data Structure Check:",
            f"- Number of machines: {validation_data['num_machines']}",
            f"- Number of fields per record: {validation_data['fields_per_record']}",
            "",
            "## 2. Required Fields Check:",
            f"- machine_id: {validation_data['required_fields']['machine_id']}",
            f"- power_usage_kw: {validation_data['required_fields']['power_usage_kw']}",
            f"- operational_hours: {validation_data['required_fields']['operational_hours']}",
            "",
            "## 3. Data Type and Value Validation:",
            f"- power_usage_kw (positive number): {type_validation['power_usage_kw']}",
            f"- operational_hours (number > 0): {type_validation['operational_hours']}",
            "",
            "## Validation Summary:",
            "Data validation is successful! Proceeding with analysis...",
            "",
            "# Formulas Used:",
            "1. Energy Consumption:",
            "   $$",
            "   \\text{Energy Consumption (kWh)} = \\text{power_usage_kw} \\times \\text{operational_hours}",
            "   $$",
            "2. Recommended Operational Hours (if inefficient):",
            "   $$",
            "   \\text{Recommended Operational Hours} = \\frac{500}{\\text{power_usage_kw}}",
            "   $$",
            "3. Energy Savings:",
            "   $$",
            "   \\text{Energy Savings (kWh)} = \\text{Energy Consumption} - (\\text{power_usage_kw} \\times \\text{Recommended Operational Hours})",
            "   $$",
            "4. Electricity Cost Reduction:",
            "   $$",
            "   \\text{Cost Reduction (\\$)} = \\text{Energy Savings (kWh)} \\times 0.10",
            "   $$",
            "",
            f"# Machine Efficiency Summary",
            f"Total Machines Evaluated: {len(data)}",
            "",
            "# Detailed Analysis"
        ]

        for machine in data:
            energy_consumption = self.calculate_energy_consumption(
                machine.power_usage_kw, machine.operational_hours
            )
            
            machine_report = [
                f"## Machine {machine.machine_id}",
                "### Input Data:",
                f"- Power Usage: {machine.power_usage_kw} kW",
                f"- Operational Hours: {machine.operational_hours} hours",
                "",
                "### Detailed Calculations:",
                "1. **Energy Consumption Calculation:**",
                f"   - Formula: $ \\text{{Energy Consumption}} = \\text{{power_usage_kw}} \\times \\text{{operational_hours}} $",
                f"   - Calculation: ${machine.power_usage_kw} \\times {machine.operational_hours} = {energy_consumption}$ kWh",
                "",
                "2. **Efficiency Check:**"
            ]

            if energy_consumption > self.INEFFICIENCY_THRESHOLD:
                recommended_hours = self.calculate_recommended_hours(machine.power_usage_kw)
                energy_savings = self.calculate_energy_savings(
                    energy_consumption, machine.power_usage_kw, recommended_hours
                )
                cost_reduction = self.calculate_cost_reduction(energy_savings)
                
                machine_report.extend([
                    f"   - Machine is flagged as inefficient ({energy_consumption} kWh > 500 kWh)",
                    "   - Compute Recommended Operational Hours:",
                    f"     $ \\text{{Recommended Operational Hours}} = \\frac{{500}}{{{machine.power_usage_kw}}} = {recommended_hours} $ hours",
                    "   - Compute Energy Savings:",
                    f"     $ \\text{{Energy Savings}} = {energy_consumption} - ({machine.power_usage_kw} \\times {recommended_hours}) = {energy_savings} $ kWh",
                    "   - Compute Cost Reduction:",
                    f"     $ \\text{{Cost Reduction}} = {energy_savings} \\times 0.10 = \\${cost_reduction} $",
                    "",
                    "### Final Recommendation:",
                    f"Reduce operational hours to {recommended_hours} hours for an expected cost reduction of ${cost_reduction}.",
                    "",
                    "### Application Summary:",
                    f"- Energy Consumption: {energy_consumption} kWh",
                    "- Status: Inefficient"
                ])
            else:
                machine_report.extend([
                    f"   - Machine is operating efficiently ({energy_consumption} kWh ≤ 500 kWh)",
                    "",
                    "### Final Recommendation:",
                    "Machine is operating efficiently. No changes recommended.",
                    "",
                    "### Application Summary:",
                    f"- Energy Consumption: {energy_consumption} kWh",
                    "- Status: Efficient"
                ])

            report.extend(machine_report)
            report.append("")

        report.append("# Feedback Request")
        report.append("Would you like detailed calculations for any specific machine? Please rate this analysis on a scale of 1-5.")

        return "\n".join(report)

    def parse_csv_data(self, csv_data: str) -> List[MachineData]:
        """Parses CSV data and returns list of MachineData objects."""
        machines = []
        csv_file = StringIO(csv_data)
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            machines.append(MachineData(
                machine_id=row['machine_id'],
                power_usage_kw=float(row['power_usage_kw']),
                operational_hours=float(row['operational_hours'])
            ))
        
        return machines

    def parse_json_data(self, json_data: str) -> List[MachineData]:
        """Parses JSON data and returns list of MachineData objects."""
        data = json.loads(json_data)
        machines = []
        
        for machine in data['machines']:
            machines.append(MachineData(
                machine_id=machine['machine_id'],
                power_usage_kw=float(machine['power_usage_kw']),
                operational_hours=float(machine['operational_hours'])
            ))
        
        return machines

# Example usage
if __name__ == "__main__":
#     # Example CSV data
#     csv_data = """machine_id,power_usage_kw,operational_hours
# M007,75,8
# M008,110,3
# M009,45,12
# M010,90,7
# M011,55,9
# M012,40,15
# """

    # Example JSON data
    json_data = """
            {
    "machines": [
        {"machine_id": "M401", "power_usage_kw": 95, "operational_hours": 8},
        {"machine_id": "M402", "power_usage_kw": 70, "operational_hours": 10},
        {"machine_id": "M403", "power_usage_kw": 85, "operational_hours": 7},
        {"machine_id": "M404", "power_usage_kw": 60, "operational_hours": 9},
        {"machine_id": "M405", "power_usage_kw": 50, "operational_hours": 12},
        {"machine_id": "M406", "power_usage_kw": 100, "operational_hours": 6},
        {"machine_id": "M407", "power_usage_kw": 55, "operational_hours": 11},
        {"machine_id": "M408", "power_usage_kw": 80, "operational_hours": 5},
        {"machine_id": "M409", "power_usage_kw": 65, "operational_hours": 10},
        {"machine_id": "M410", "power_usage_kw": 90, "operational_hours": 7},
        {"machine_id": "M411", "power_usage_kw": 75, "operational_hours": 8},
        {"machine_id": "M412", "power_usage_kw": 105, "operational_hours": 4},
        {"machine_id": "M413", "power_usage_kw": 45, "operational_hours": 13},
        {"machine_id": "M414", "power_usage_kw": 85, "operational_hours": 9},
        {"machine_id": "M415", "power_usage_kw": 95, "operational_hours": 6}
    ]
    }


    """

    optimizer = EnergyOptimizer()
    
    # # Process CSV data
    # print("Processing CSV data:")
    # machines_csv = optimizer.parse_csv_data(csv_data)
    # report_csv = optimizer.generate_report(machines_csv)
    # print(report_csv)
    
    print("\nProcessing JSON data:")
    machines_json = optimizer.parse_json_data(json_data)
    report_json = optimizer.generate_report(machines_json)
    print(report_json)