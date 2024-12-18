import unittest
import pandas as pd
from io import StringIO
from taxonomic_stats import read_data, calculate_summary_statistics

class TestTaxonomicDataAnalysis(unittest.TestCase):
    """
    Unit test class for taxonomic data analysis script.
    """

    def setUp(self):
        """
        Set up sample data for tests.
        """
        self.valid_data = """species,phylum,count
        SpeciesA,Firmicutes,120
        SpeciesB,Firmicutes,80
        SpeciesC,Bacteroidetes,200 
        SpeciesD,Bacteroidetes,50
        SpeciesE,Proteobacteria,300
        """
        
        self.invalid_data_missing_columns = """species,count
        SpeciesA,120
        SpeciesB,80
        """
        
        self.invalid_data_missing_values = """species,phylum,count
        SpeciesA,Firmicutes,
        SpeciesB,,80
        SpeciesC,Bacteroidetes,200
        """
        
        self.invalid_data_type_values = """species,phylum,count
        SpeciesA,Firmicutes,not_numeric
        SpeciesB,Proteobacteria,80
        SpeciesC,Bacteroidetes,200
        """

    def test_read_data_valid(self):
        """
        Test read_data function with valid data.
        """
        # Create a mock CSV file
        data = StringIO(self.valid_data)
        df = read_data(data)
        self.assertEqual(df.shape[0], 5)  # Expect 5 valid rows
        self.assertIn("phylum", df.columns)
        self.assertIn("count", df.columns)

    def test_read_data_missing_columns(self):
        """
        Test read_data function with missing columns.
        """
        data = StringIO(self.invalid_data_missing_columns)
        with self.assertRaises(SystemExit):
            read_data(data)

    def test_read_data_missing_values(self):
        """
        Test read_data function with missing values.
        """
        data = StringIO(self.invalid_data_missing_values)
        df = read_data(data)
        self.assertEqual(df.shape[0], 1)  # Only 1 valid row should remain

    def test_read_data_type_values(self):
        """
        Test read_data function with non numeric count values.
        """
        data = StringIO(self.invalid_data_type_values)
        df = read_data(data)
        self.assertEqual(df.shape[0], 2)  # Only 2 valid rows should remain

    def test_calculate_summary_statistics(self):
        """
        Test calculate_summary_statistics function with valid input.
        """
        data = StringIO(self.valid_data)
        df = read_data(data)
        summary = calculate_summary_statistics(df)
        expected_phyla = {"Firmicutes", "Bacteroidetes", "Proteobacteria"}
        self.assertSetEqual(set(summary["phylum"]), expected_phyla)
        self.assertEqual(summary.loc[summary["phylum"] == "Firmicutes", "total_species_count"].values[0], 200)
        self.assertAlmostEqual(summary.loc[summary["phylum"] == "Firmicutes", "average_species_count"].values[0], 100.0)

    def test_empty_dataframe(self):
        """
        Test calculate_summary_statistics with an empty DataFrame.
        """
        empty_df = pd.DataFrame(columns=["species", "phylum", "count"])
        summary = calculate_summary_statistics(empty_df)
        self.assertTrue(summary.empty)

if __name__ == "__main__":
    unittest.main()
